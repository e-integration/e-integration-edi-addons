# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import api

class sale_order_extensions(models.Model):
    _inherit = 'sale.order'

    edi_document_ids = fields.One2many('edi.document', compute='_compute_edi_document_ids')
    edi_recipient_id = fields.Many2one('edi.document.partner', string='EDI Recipient')
    customer_company_id = fields.Integer(compute='_get_customer_company_id')

    @api.one
    @api.depends('partner_id')
    def _get_customer_company_id(self):
        self.customer_company_id = self.partner_id.parent_id.id or self.partner_id.id

    @api.one
    def _compute_edi_document_ids(self):
        edi_document_obj = self.env['edi.document']
        self.edi_document_ids = edi_document_obj.search([
                                                         ('model', '=', self._name),
                                                         ('res_id', '=', self.id)
                                                         ]).ids

    @api.one
    def create_edi_document(self):
        edi_document_obj = self.env['edi.document']
        edi_document_obj.create_edi_document(self, self.company_id.partner_id)
