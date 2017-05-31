# -*- coding: utf-8 -*-

from openerp import models
from openerp import api
from openerp import _
from openerp import fields
from openerp.exceptions import ValidationError

class edi_document_temporary(models.TransientModel):
    _name = 'edi.document.temporary'

    invoice_id = fields.Many2one('account.invoice', readonly=True)
    recipient_ids = fields.Many2one('edi.document.partner')

    @api.multi
    def set_recipients_to_invoices(self):
        for record in self:
            record.invoice_id.edi_recipient_id = record.recipient_ids[0]

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
        recipient_id = False
        for account_invoice_id in account_invoice_ids:
            if account_invoice_id.edi_recipient_id:
                recipient_id = account_invoice_id.edi_recipient_id
            else:
                recipient_id = self.env['edi.document'].get_document_partner(account_invoice_id.partner_id)
            edi_document_temporary_new = edi_document_temporary_obj.create({
                                                                           'invoice_id': account_invoice_id.id,
                                                                           'recipient_ids': recipient_id.id,
                                                                          })
            edi_document_temporary_ids.append(edi_document_temporary_new.id)
        return edi_document_temporary_obj.browse(edi_document_temporary_ids)

    edi_document_temporary_ids = fields.Many2many('edi.document.temporary', relation="edi_doc_inv_create_edi_doc_temp_rel", default=_default_edi_document_temporary_ids)

    @api.multi
    def create_edi_document(self):
        account_invoice_obj = self.env['account.invoice']
        account_invoice_ids = account_invoice_obj.browse(self._context.get('active_ids'))
        if any('open' != account_invoice_id.state for account_invoice_id in account_invoice_ids):
                raise ValidationError(_('Please select only open invoices.'))
        else:
            self.edi_document_temporary_ids.set_recipients_to_invoices()
            account_invoice_ids.create_edi_documents()
        return {'type': 'ir.actions.act_window_close'}
