from odoo import models, fields, api, SUPERUSER_ID


class ResUsers(models.Model):
    _inherit = 'res.users'

    user_type = fields.Selection([
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('candidate', 'Candidate')
    ], string='User Type', default='candidate')

    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        uid = super(ResUsers, cls)._login(db, login, password, user_agent_env)
        if uid:
            with cls.pool.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                user = env['res.users'].browse(uid)
                if user.user_type == 'candidate':
                    return uid
        return uid
