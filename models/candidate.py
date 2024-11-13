from odoo import models, fields, api


class ExamCandidate(models.Model):
    _name = 'exam.candidate'
    _description = 'Exam Candidate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    registration_number = fields.Char(string='Registration Number', readonly=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    exam_ids = fields.Many2many('exam.exam', string='Assigned Exams')
    result_ids = fields.One2many('exam.result', 'candidate_id', string='Results')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['registration_number'] = self.env['ir.sequence'].next_by_code('exam.candidate')
        return super().create(vals_list)

