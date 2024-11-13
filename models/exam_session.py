from odoo import models, fields, api
from datetime import timedelta


class ExamSession(models.Model):
    _name = 'exam.session'
    _description = 'Exam Session'
    _inherit = ['mail.thread']

    name = fields.Char(compute='_compute_name', store=True)
    exam_id = fields.Many2one('exam.exam', required=True)
    candidate_ids = fields.Many2many('exam.candidate', string='Candidates')
    start_time = fields.Datetime()
    end_time = fields.Datetime(compute='_compute_end_time', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)

    @api.depends('exam_id', 'start_time')
    def _compute_name(self):
        for session in self:
            if session.exam_id and session.start_time:
                session.name = f"{session.exam_id.name} - {session.start_time.strftime('%Y-%m-%d')}"

    @api.depends('start_time', 'exam_id.duration')
    def _compute_end_time(self):
        for session in self:
            if session.start_time and session.exam_id.duration:
                hours = int(session.exam_id.duration)
                minutes = int((session.exam_id.duration - hours) * 60)
                session.end_time = session.start_time + timedelta(hours=hours, minutes=minutes)
