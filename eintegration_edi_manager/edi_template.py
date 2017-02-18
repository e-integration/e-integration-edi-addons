# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import api

class edi_template(models.Model):
    _name = 'edi.template'
    _inherit = 'mail.thread'

    name = fields.Char()
    message_type = fields.Many2one('edi.message', required=True)
    model = fields.Many2one('ir.model', required=True)
    export_field_ids = fields.One2many('edi.export.field', inverse_name='edi_template_id', ondelete='cascade', string="Exported Fields")
    model_name = fields.Char(compute="_compute_model_name", store=True)

    @api.one
    @api.depends('model')
    def _compute_model_name(self):
        self.model_name = self.model.model