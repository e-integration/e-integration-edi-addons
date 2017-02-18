# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import api

class edi_document_partner(models.Model):
    _name = 'edi.document.partner'
    _description = 'EDI partner with a GLN connected to a res.patner'
    _inherit = 'mail.thread'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner', required=True)
    gln = fields.Char()

    @api.model
    def create(self, values):
        res_id = super(edi_document_partner, self).create(values)
        res_id.name = '%s - %s' % (res_id.partner_id.name, res_id.gln)
        return res_id

class res_partner_extension(models.Model):
    _inherit = 'res.partner'

    edi_document_partner_ids = fields.One2many('edi.document.partner', inverse_name='partner_id')