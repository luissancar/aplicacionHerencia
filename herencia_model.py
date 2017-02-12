#-*- coding: utf-8 -*-
from openerp import models, fields, api
class HerenciaModel(models.Model):
    _inherit = 'aplicacionejemplo01.task''
    user_id = fields.Many2one('res.users', 'Responsible')
    date_deadline = fields.Date('Deadline')
