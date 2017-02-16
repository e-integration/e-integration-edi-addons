from openerp import models
from openerp import fields

class edi_communication(models.Model):
    _name = 'edi.communication'
    
    name = fields.Char()
    description = fields.Char()