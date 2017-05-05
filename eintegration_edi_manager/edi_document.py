# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import api
from openerp import _
from lxml import etree
from lxml.etree import CDATA
from openerp.exceptions import ValidationError

class edi_document(models.Model):
    _name = 'edi.document'
    _description = 'General EDI document'
    _inherit = 'mail.thread'

    body = fields.Text()
    sender = fields.Many2one('edi.document.partner')
    recipient = fields.Many2one('edi.document.partner')
    message_type = fields.Many2one('edi.message')
    model = fields.Char('Related Document Model', size=128, select=1)
    res_id = fields.Integer('Related Document ID', select=1)
    name = fields.Char()
    stage_id = fields.Many2one('edi.document.stage')

    @api.one
    def send_now(self):
        self.send_document()

    @api.one
    def send_document(self):
        ir_attachment_obj = self.env['ir.attachment']
        mail_template_obj = self.env['email.template']
        mail_mail_obj = self.env['mail.mail']
        ir_model_data_obj = self.env['ir.model.data']
        sent_stage = self.env.ref('eintegration_edi_manager.edi_document_stage_tt_sent')
        ir_attachment = ir_attachment_obj.create({
                                                 'datas': self.body.encode('base64'),
                                                 'name': 'invoic.xml',
                                                 'datas_fname': 'invoic.xml',
                                                 'res_model': 'edi.document',
                                                 'res_id': self.id,
                                                 'type': 'binary',
                                                })
        edi_document_template_id = ir_model_data_obj.xmlid_to_res_id('eintegration_edi_manager.edi_document_email_template')
        edi_document_template = mail_template_obj.browse(edi_document_template_id)
        overview_mail_id = edi_document_template.send_mail(self.id)
        overview_mail = mail_mail_obj.browse(overview_mail_id)
        overview_mail.attachment_ids = [(4, ir_attachment.id)]
        overview_mail.send()
        self.stage_id = sent_stage.id

    @api.model
    def cron_send_edi_documents(self):
        edi_document_obj = self.env['edi.document']
        to_be_sent_stage = self.env.ref('eintegration_edi_manager.edi_document_stage_tt_to_be_sent')
        edi_document_ids = edi_document_obj.search([('stage_id', '=', to_be_sent_stage.id)])
        for edi_document_id in edi_document_ids:
            edi_document_id.send_document()

    def create(self, vals):
        res = super(edi_document, self).create(vals)
        res.name = res.res_id

        #fill the 'body' field with the xml content based on an EDI template
        res._set_body_content()
        return res

    def _set_body_content(self):
        """
        Fills the 'body' field of the 'self' with an xml content based on an EDI template connected to a business object.
        """
        edi_template_obj = self.env['edi.template']
        if self.model:
            source_object_obj = self.env[self.model]
            edi_template = edi_template_obj.search([('model_name', '=', self.model)])
            source_object_id = source_object_obj.browse(self.res_id)
            export_data = self._get_export_data(edi_template, source_object_id)
            self._create_xml_content(export_data)

    def _get_export_data(self, edi_template, source_object):
        """
        Returns the data from the source object based on the EDI template.
        The structure of the data follows the element hierarchy of the selected fields in the template.
        For example if an invoice has two lines then there will be two <invoice_line> elements inside the 'MESSAGEBODY' element.

        :param edi_template: EDI template which contains the set of field names which should be exported
        :return: list of dictionaries which contain the field names and values; top elements are the keys and the value is a dictionary that contains two lists - one for field names and one for the data)
        """
        #create a dictionary which will contain the names of the top elements as its keys
        #all the keys of names_dict will be direct child elements of the 'MESSAGEBODY' element
        exported_field_names = []
        names_dict = {}
        export_data = []
        for exported_field in edi_template.export_field_ids:
            element_names = exported_field.name.split('/')
            top_element_name = element_names[0]
            if top_element_name not in names_dict:
                names_dict[top_element_name] = []
            related_object = source_object
            for element_name in element_names:
                related_object = self._get_attr_value(related_object, element_name)[0]
            related_fields = related_object.fields_get(False)
            for k, v in related_fields.iteritems():
                if self._is_basic_and_exportable(v):
                    exported_field_names.append(exported_field.name + '/' + k)
                    names_dict[top_element_name].append(exported_field.name + '/' + k)

        #add the basic field from the source object into the list
        basic_fields = source_object.fields_get(False)
        for k, v in basic_fields.iteritems():
            if self._is_basic_and_exportable(v):
                exported_field_names.append(k)
                names_dict[k] = [k]

        #add the data of the exported fields
        for k, v in names_dict.iteritems():
            temp_data = self.export_db_data(source_object, v).get('datas',[])
            for temp_data_item in temp_data:
                export_data.append({'names': v, 'data': temp_data_item})

        return export_data

    def _is_basic_and_exportable(self, field_attributes):
        """
        Check if the field is non relation (basic) and exportable.

        :param field_attributes: a dictionary containing the field attributes
        """
        # If the 'exportable' attribute is missing then the field is exportable. The attribute is always present for fields which are not exportable.
        is_basic_and_exportable = not 'relation' in field_attributes and field_attributes.get('exportable',True)
        return is_basic_and_exportable

    def _create_xml_content(self, export_data):
        """
        Creates an xml content based on the input data and the EDI report template and puts it into the 'body' field of the 'self'.

        :param export_data: a list of dictionaries with element names and values

        This method is called explicitly when the EDI document is created.
        """
        report_obj = self.env['report']
        self.body = report_obj.get_html(self, 'eintegration_edi_manager.edi_document_report_template')
        root = etree.fromstring(self.body.lstrip())
        message_body = root.find('.//MESSAGEBODY')
        element_list = []
        for export_data_item in export_data:
            top = None
            for exported_field in export_data_item['names']:
                element_names = exported_field.split('/')
                field_element = None
                parent_element = top
                for element_name in element_names:
                    if top is None:
                        field_element = etree.Element(element_name)
                        top = field_element
                    else:
                        field_element = parent_element.find(element_name)
                        if field_element is None:
                            field_element = parent_element if parent_element.tag == element_name else etree.SubElement(parent_element, element_name)
                    parent_element = field_element
                data_value = export_data_item['data'].pop(0)
                if isinstance(data_value, (int, float)):
                    field_element.text = CDATA(str(data_value))
                else:
                    field_element.text = CDATA(data_value)
            element_list.append(top)
        for element in element_list:
            message_body.append(element)
        self.body = "<?xml version='1.0' encoding='ISO-8859-1'?>\n" + etree.tostring(root, pretty_print=True)

    def _get_attr_value(self, source_object, attr_name):
        """
        Returns the attribute value of the source object.

        :param source_object: the input object with attributes
        :param attr_name: the name of the desired attribute
        :return: the value of the source object's attribute
        """
        res_object = source_object
        res_value = []
        for res_id in res_object.ids:
            res_value.append(getattr(res_object.browse(res_id), attr_name))
        return res_value

    def export_records(self, source_object, fields):
        """
        Exports fields of the source_obect.

        :param source_object: the object which contains the source data
        :param fields: list of lists of fields which should be exported
        :return: list of lists of corresponding values
        """
        lines = []
        for record in source_object:
            # main line of record, initially empty
            current = [''] * len(fields)
            lines.append(current)

            # list of primary fields followed by secondary field(s)
            primary_done = []

            # process column by column
            for i, path in enumerate(fields):
                if not path:
                    continue

                name = path[0]
                if name in primary_done:
                    continue

                field = record._fields[name]
                value = record[name]

                # binary fields should be skipped
                if field.type == 'binary':
                    continue

                # this part could be simpler, but it has to be done this way
                # in order to reproduce the former behavior
                if not isinstance(value, models.BaseModel):
                    current[i] = field.convert_to_export(value, source_object.env)
                else:
                    primary_done.append(name)

                    # This is a special case, its strange behavior is intended!
                    if field.type == 'many2many' and len(path) > 1 and path[1] == 'id':
                        xml_ids = [r.id for r in value]
                        current[i] = ','.join(xml_ids) or False
                        continue

                    # recursively export the fields that follow name
                    fields2 = [(p[1:] if p and p[0] == name else []) for p in fields]
                    lines2 = self.export_records(value, fields2)
                    if lines2:
                        # merge first line with record's main line
                        for j, val in enumerate(lines2[0]):
                            if val or isinstance(val, bool):
                                current[j] = val
                        # check value of current field
                        if not current[i] and not isinstance(current[i], bool) and not current[i] == '':
                            # assign xml_ids, and forget about remaining lines
                            xml_ids = [item[1] for item in value.name_get()]
                            current[i] = ','.join(xml_ids)
                        else:
                            # append the other lines at the end
                            lines += lines2[1:]
                    else:
                        current[i] = False

        return lines

    def export_db_data(self, source_object, fields_to_export):
        """
        Export fields for the source object

        :param source_object: the object which contains the data for the export
        :param fields_to_export: list of fields
        :rtype: dictionary with a *datas* matrix
        """
        fields_to_export = map(models.fix_import_export_id_paths, fields_to_export)
        return {'datas': self.export_records(source_object, fields_to_export)}

    def create_edi_document(self, res_object, partner_id):
        edi_document_obj = self.env['edi.document']
        edi_template_obj = self.env['edi.template']
        to_be_sent_stage = self.env.ref('eintegration_edi_manager.edi_document_stage_tt_to_be_sent')
        model_name = res_object._model._name
        recipient = res_object.edi_recipient_id
        sender = self.get_document_partner(partner_id)
        if not sender:
            raise ValidationError(_('No GLN found for invoice issuer: %s')%(partner_id.name, ))
        edi_template = edi_template_obj.search([('model_name', '=', model_name)])
        if not edi_template:
            raise ValidationError(_('No EDI template for %s found.')%(model_name))
        edi_document_obj.create({
                                'res_id': res_object.id,
                                'model': model_name,
                                'stage_id': to_be_sent_stage.id,
                                'sender': sender.id,
                                'recipient': recipient.id,
                                'message_type': edi_template.message_type.id or False,
                                })
        res_object.message_post(_('EDI Document created'))

    @api.model
    def get_document_partner(self, partner_id):
        edi_document_partner_obj = self.env['edi.document.partner']
        edi_document_partner_ids = partner_id.edi_document_partner_ids or partner_id.parent_id.edi_document_partner_ids
        edi_document_partner_id = False
        company_id = False
        if not edi_document_partner_ids:
            if partner_id.is_company:
                company_id = partner_id
            elif partner_id.parent_id:
                company_id = partner_id.parent_id
            else:
                raise ValidationError(_('No company contact found for %s.')%partner_id.name)
            if not company_id.iln:
                raise ValidationError(_('No GLN found for %s.')%(company_id.name))
            edi_document_partner_id = edi_document_partner_obj.create({
                                                         'name': company_id.name,
                                                         'partner_id': company_id.id,
                                                         'gln': company_id.iln,
                                                         })
        else:
            edi_document_partner_id = edi_document_partner_ids[0]
        return edi_document_partner_id
