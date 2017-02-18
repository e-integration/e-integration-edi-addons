# -*- coding: utf-8 -*-

from openerp import http
from openerp import tools

class Export(http.Controller):

    @http.route('/edi_manager/export_fields', type='json', auth="user")
    def export_fields(self, data, record_id):
        env = http.request.env
        edi_template_obj = env['edi.template']
        edi_export_field_obj = env['edi.export.field']
        if record_id:
            edi_template_id = edi_template_obj.browse(record_id)
            edi_template_id.export_field_ids.unlink()
            for field_item in data:
                edi_export_field_obj.create({
                                            'name': field_item['field_name'],
                                            'display_name': field_item['field_label'],
                                            'edi_template_id': edi_template_id.id,
                                            })

    @http.route('/edi_manager/get_fields', type='json', auth="user")
    def get_fields(self, model, prefix='', parent_name= '',
                   import_compat=True, parent_field_type=None,
                   exclude=None):

        fields = self.fields_get(model)
        fields['.id'] = fields.pop('id', {'string': 'ID'})

        fields_sequence = sorted(fields.iteritems(),
            key=lambda field: tools.ustr(field[1].get('string', '')))

        records = []
        for field_name, field in fields_sequence:
            if not field.get('exportable', True) or not field.get('relation', False):
                continue

            id = prefix + (prefix and '/'or '') + field_name
            name = parent_name + (parent_name and '/' or '') + field['string']
            record = {'id': id, 'string': name,
                      'value': id, 'children': False,
                      'field_type': field.get('type'),
                      'required': field.get('required'),
                      'relation_field': field.get('relation_field')}
            records.append(record)

            if len(name.split('/')) < 3 and 'relation' in field:
                ref = field.pop('relation')
                record['value'] += '/id'
                record['params'] = {'model': ref, 'prefix': id, 'name': name}

                if not import_compat or field['type'] == 'one2many':
                    # m2m field in import_compat is childless
                    record['children'] = True

        return records

    @http.route('/edi_manager/get_stored_fields', type='json', auth="user")
    def get_stored_fields(self, export_field_ids):
        records = []
        env = http.request.env
        edi_export_field_obj = env['edi.export.field']
        edi_export_field_ids = edi_export_field_obj.browse(export_field_ids)
        for edi_export_field_id in edi_export_field_ids:
            records.append({'name': edi_export_field_id.name, 'label': edi_export_field_id.display_name})
        return records

    def fields_get(self, model):
        Model = http.request.session.model(model)
        fields = Model.fields_get(False, http.request.context)
        return fields