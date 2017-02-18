# -*- coding: utf-8 -*-

from openerp import models
from openerp import api
from openerp import _
from openerp import fields

class edi_document_temporary(models.TransientModel):
    _name = 'edi.document.temporary'

    invoice_id = fields.Many2one('account.invoice', readonly=True)
    recipient_ids = fields.Many2one('edi.document.partner')

class edi_document_invoice_create(models.TransientModel):
    """
    This wizard creates edi documents from invoices.
    """

    _name = 'edi.document.invoice.create'
    _description = "Create edi documents from the selected invoices"

    def _default_edi_document_temporary_ids(self):
        edi_document_temporary_obj = self.env['edi.document.temporary']
        account_invoice_ids = self.env['account.invoice'].browse(self._context.get('active_ids'))
        edi_document_temporary_ids = []
        for account_invoice_id in account_invoice_ids:
            recipient_id = account_invoice_id.edi_recipient_id if account_invoice_id.edi_recipient_id else self._get_document_partner(account_invoice_id.partner_id)
            edi_document_temporary_new = edi_document_temporary_obj.create({
                                                                           'invoice_id': account_invoice_id.id,
                                                                           'recipient_ids': recipient_id.id,
                                                                          })
            edi_document_temporary_ids.append(edi_document_temporary_new.id)
        return edi_document_temporary_obj.browse(edi_document_temporary_ids)

#     recipient_ids = fields.Many2many('edi.document.partner', relation="edi_doc_inv_create_edi_doc_partner_rel", default=_default_recipient_ids)
#     invoice_ids = fields.Many2many('account.invoice', default=_default_invoice_ids)
    edi_document_temporary_ids = fields.Many2many('edi.document.temporary', relation="edi_doc_inv_create_edi_doc_temp_rel", default=_default_edi_document_temporary_ids)

    @api.multi
    def create_edi_document(self):
        edi_document_obj = self.env['edi.document']
        account_invoice_obj = self.env['account.invoice']
        edi_template_obj = self.env['edi.template']
        edi_template = edi_template_obj.search([('model_name', '=', 'account.invoice')])
        account_invoice_ids = account_invoice_obj.browse(self._context.get('active_ids'))
        to_be_sent_stage = self.env.ref('eintegration_edi_manager.edi_document_stage_tt_to_be_sent')
        for account_invoice_id in account_invoice_ids:
            if account_invoice_id.state == 'open':
                recipient = account_invoice_id.edi_recipient_id if account_invoice_id.edi_recipient_id else self._get_document_partner(account_invoice_id.partner_id)
                sender = self._get_document_partner(account_invoice_id.company_id.partner_id)

                edi_document_obj.create({
                                         'res_id': account_invoice_id.id,
                                         'model': account_invoice_id._model,
                                         'stage_id': to_be_sent_stage.id,
                                         'sender': sender.id,
                                         'recipient': recipient.id,
                                         'message_type': edi_template.message_type.id or False,
                                         })
                account_invoice_id.message_post(_('EDI Document created'))
        return {'type': 'ir.actions.act_window_close'}

    def _get_document_partner(self, partner_id):
        edi_document_partner_obj = self.env['edi.document.partner']
        document_partner = False
        gln = False
        if not partner_id.edi_document_partner_ids:
            if partner_id.is_company:
                gln = partner_id.iln
            else:
                gln = partner_id.parent_id.iln
            document_partner = edi_document_partner_obj.create({
                                                         'name': partner_id.name,
                                                         'partner_id': partner_id.id,
                                                         'gln': gln,
                                                         })
        else:
            document_partner = partner_id.edi_document_partner_ids[0]
        return document_partner
