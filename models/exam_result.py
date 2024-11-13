from odoo import models, fields, api


class ExamResult(models.Model):
    _name = 'exam.result'
    _description = 'Exam Result'
    _rec_name = 'candidate_id'

    candidate_id = fields.Many2one('exam.candidate', string='Candidate', required=True)
    exam_id = fields.Many2one('exam.exam', string='Exam', required=True)
    score = fields.Float(string='Score')
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ], compute='_compute_result', store=True)
    exam_date = fields.Datetime(string='Exam Date', default=fields.Datetime.now)
    # section_results = fields.One2many('exam.section.result', 'result_id', string='Section Results')

    @api.depends('score', 'exam_id.passing_marks')
    def _compute_result(self):
        for record in self:
            record.result = 'pass' if record.score >= record.exam_id.passing_marks else 'fail'
