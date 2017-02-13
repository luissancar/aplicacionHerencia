#-*- coding: utf-8 -*-
from openerp import models, fields, api
class HerenciaModel(models.Model):
    _inherit = 'aplicacionejemplo01.task'
    user_id = fields.Many2one('res.users', 'Responsible')
    date_deadline = fields.Date('Deadline')
    name = fields.Char(help="Campo modificado")

    @api.multi
    def do_clear_done(self):
        domain = [('is_done', '=', True), '|', ('user_id', '=', self.env.uid), ('user_id', '=', False)]
        done_recs = self.search(domain)
        done_recs.write({'active': False})
        return True

    @api.one
    def do_toggle_done(self):
        if self.user_id != self.env.user:
            raise Exception('Only the responsible can do this!')
        else:
            return super(TodoTask, self).do_toggle_done()    
