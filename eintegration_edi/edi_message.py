# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging
LOG = logging.getLogger(__name__)


from openerp.tools.translate import _
from openerp.exceptions import ValidationError




class edi_message_variant(models.Model):
    _name = 'edi.message.variant'
    name = fields.Char('Name', required=True)


class edi_message_version(models.Model):
    _name = 'edi.message.version'
    name = fields.Char('Name', required=True)


class edi_message_format(models.Model):
    _name = 'edi.message.format'
    name = fields.Char('Name', required=True)


class edi_message_organisation(models.Model):
    _name = 'edi.message.organisation'
    name = fields.Char('Name', required=True)


class edi_message_type(models.Model):
    _name = 'edi.message.type'
    name = fields.Char('Name', required=True)


class edi_message(models.Model):
    _name = 'edi.message'

    @api.one
    def name_get(self):
        if 'sol' in self.env.context and self.env.context.get('sol'):
            name = self.variant_id.name
        else:
            name = "%s/%s/%s/%s/%s/%s" % (self.type_id.name,
                                       self.organisation_id.name,
                                       self.format_id.name,
                                       self.version_id.name,
                                       self.variant_id.name if self.variant_id else '-',
                                       self.direction
            )
        return (self.id, name)

    @api.model
    def name_search(self, name, operator='ilike', args=None, limit=100):
        return self.search(['|',
            ('format_id', 'ilike', name), '|',
            ('variant_id', 'ilike', name), '|',
            ('version_id', 'ilike', name), '|',
            ('organisation_id', 'ilike', name), '|',
            ('type_id', 'ilike', name),
            ('direction', 'ilike', name)
        ]).name_get()
    
    def _search_name(self, operator, value):
        return ['|', ('format_id', operator, value),
                '|', ('variant_id', operator, value),
                '|', ('version_id', operator, value),
                '|', ('organisation_id', operator, value),
                '|', ('type_id', operator, value),
                ('direction', operator, value)]

    def _compute_name(self):
        for rec in self:
            rec.name = rec.name_get()[0][1]

    name = fields.Char(compute='_compute_name', string='Name', search='_search_name')
    type_id = fields.Many2one('edi.message.type', 'Type', required=True)
    organisation_id = fields.Many2one('edi.message.organisation', 'Organisation', required=True)
    format_id       = fields.Many2one('edi.message.format', 'Format', required=True)
    version_id      = fields.Many2one('edi.message.version', 'Version', required=True)
    variant_id      = fields.Many2one('edi.message.variant', 'Variant')
    direction       = fields.Selection([('ecc-in', 'eCC-IN'), ('ecc-out', 'eCC-Out')], 'Direction', required=True)
