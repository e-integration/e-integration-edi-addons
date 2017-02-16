# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields

class edi_export_field(models.Model):
    _name = 'edi.export.field'
    _description = 'Fields selected to be sent via EDI.'

    name = fields.Char()
    display_name = fields.Char()
    edi_template_id = fields.Many2one('edi.template')