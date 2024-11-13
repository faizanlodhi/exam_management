from odoo import models, fields, api
import openai


class ExamQuestion(models.Model):
    _name = 'exam.question'
    _description = 'Exam Question'
    _order = 'sequence'

    name = fields.Text('Question Text')
    section_id = fields.Many2one('exam.section', 'Section')
    sequence = fields.Integer('Sequence')
    question_type = fields.Selection([
        ('mcq', 'Multiple Choice'),
        ('audio', 'Audio Question'),
        ('voice_record', 'Voice Recording'),
        ('text_area', 'Text Area')
    ], string='Question Type')

    # option_ids = fields.One2many('exam.question.option', 'question_id', 'Options')
    correct_option_id = fields.Many2one('exam.question.option', 'Correct Answer')
    audio_file = fields.Binary('Audio Question File')
    audio_filename = fields.Char('Audio Filename')
    max_recording_time = fields.Integer('Max Recording Time (seconds)')

    @api.model
    def generate_ai_questions(self):
        # Implementation for AI question generation using OpenAI
        openai.api_key = self.env['ir.config_parameter'].sudo().get_param('openai_api_key')
        # Add implementation here
