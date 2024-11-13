from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Exam(models.Model):
    _name = 'exam.exam'
    _description = 'Examination'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Exam Name', required=True, tracking=True)
    code = fields.Char(string='Exam Code', readonly=True, copy=False)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)

    section_ids = fields.One2many('exam.section', 'exam_id', string='Exam Sections')
    total_marks = fields.Float(compute='_compute_total_marks', store=True)
    passing_marks = fields.Float(string='Passing Marks')
    duration = fields.Float(string='Duration (hours)')
    is_published = fields.Boolean('Published', copy=False)
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')
    allowed_attempts = fields.Integer('Allowed Attempts', default=1)
    instruction_ids = fields.One2many('exam.instruction', 'exam_id', string='Instructions')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('exam.exam')
        return super().create(vals_list)

    @api.depends('section_ids.total_marks')
    def _compute_total_marks(self):
        for exam in self:
            exam.total_marks = sum(exam.section_ids.mapped('max_marks'))

    def action_confirm(self):
        for exam in self:
            if not exam.section_ids:
                raise ValidationError('Please add at least one section before confirming.')
            exam.state = 'confirmed'

    def action_start(self):
        for exam in self:
            exam.state = 'in_progress'

    def action_complete(self):
        for exam in self:
            exam.state = 'completed'

    def action_cancel(self):
        for exam in self:
            exam.state = 'cancelled'

    def action_publish(self):
        self.write({'is_published': True})

    def action_unpublish(self):
        self.write({'is_published': False})

    def toggle_published(self):
        self.is_published = not self.is_published
        return True


class ExamInstruction(models.Model):
    _name = 'exam.instruction'
    _description = 'Exam Instructions'
    _order = 'sequence'

    sequence = fields.Integer(default=10)
    name = fields.Text('Instruction', required=True)
    exam_id = fields.Many2one('exam.exam', string='Exam')


class ExamSection(models.Model):
    _name = 'exam.section'
    _description = 'Exam Section'
    _order = 'sequence'

    name = fields.Char(string='Section Name', required=True)
    sequence = fields.Integer(string='Sequence')
    exam_id = fields.Many2one('exam.exam', string='Exam')
    section_type = fields.Selection([
        ('reading_comp', 'Reading Comprehension (E1)'),
        ('written_expr', 'Written Expression (E2)'),
        ('thematic_mcq', 'Thematic MCQ (E3)'),
        ('oral_comp', 'Oral Comprehension (E4)'),
        ('oral_expr', 'Oral Expression (E5)')
    ], string='Section Type', required=True)

    # Section-specific configuration
    total_marks = fields.Integer('Total Marks', required=True)  # Added this field

    total_questions = fields.Integer('Total Questions')
    correct_answers_required = fields.Integer('Required Correct Answers')

    # Written Expression fields
    has_subsections = fields.Boolean('Has Subsections')
    subsection_ids = fields.One2many('exam.subsection', 'section_id', 'Subsections')

    # Audio fields for Oral Comprehension
    audio_file = fields.Binary('Audio File')
    audio_filename = fields.Char('Audio Filename')

    # Oral Expression fields
    evaluation_criteria_ids = fields.One2many('exam.evaluation.criteria', 'section_id', 'Evaluation Criteria')
    recording_duration = fields.Integer('Recording Duration (seconds)')

    @api.onchange('section_type')
    def _onchange_section_type(self):
        if self.section_type == 'reading_comp':
            self.total_questions = 60
            self.correct_answers_required = 48
            self.total_marks = 60
        elif self.section_type == 'thematic_mcq':
            self.total_questions = 40
            self.correct_answers_required = 32
            self.total_marks = 40
        elif self.section_type == 'oral_comp':
            self.total_questions = 50
            self.correct_answers_required = 40
            self.total_marks = 50



class ExamSubsection(models.Model):
    _name = 'exam.subsection'
    _description = 'Written Expression Subsection'

    name = fields.Char('Subsection Name', required=True)
    section_id = fields.Many2one('exam.section', 'Section')
    subsection_type = fields.Selection([
        ('vocabulary_context', 'Vocabulary Usage'),
        ('social_context', 'Social Context')
    ], required=True)
    word_threshold = fields.Integer('Word Threshold')
    autosave_interval = fields.Integer('Autosave Interval (seconds)', default=30)


class ExamEvaluationCriteria(models.Model):
    _name = 'exam.evaluation.criteria'
    _description = 'Oral Expression Evaluation Criteria'

    name = fields.Char('Criterion Name', required=True)
    section_id = fields.Many2one('exam.section', 'Section')
    description = fields.Text('Description')
    weight = fields.Float('Weight', default=1.0)