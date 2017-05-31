# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import api

class edi_document_partner(models.Model):
    _name = 'edi.document.partner'
    _description = 'EDI partner with a GLN connected to a res.patner'
    _inherit = 'mail.thread'

    name = fields.Char(compute="_compute_partner_name", store=True)
    partner_id = fields.Many2one('res.partner', required=True)
    gln = fields.Char(required=True)

    @api.one
    @api.depends('gln','partner_id')
    def _compute_partner_name(self):
        self.name = '%s - %s' % (self.partner_id.name, self.gln) if self.partner_id else ''

class res_partner_extension(models.Model):
    _inherit = 'res.partner'

    edi_document_partner_ids = fields.One2many('edi.document.partner', inverse_name='partner_id')
