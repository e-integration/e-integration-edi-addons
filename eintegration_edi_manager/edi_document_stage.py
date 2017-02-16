# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields

class edi_document_stage(models.Model):
    _name = 'edi.document.stage'
    _description = 'EDI Document Stage'

    name = fields.Char('Stage Name')
    description = fields.Text('Description')
    is_default = fields.Boolean('Default for New EDI Documents')
    sequence = fields.Integer('Sequence')
    edi_document_ids = fields.One2many('edi.document', inverse_name='stage_id', help='EDI Documents')