from odoo import http, fields
from odoo.http import request
from odoo.addons.web.controllers.home import Home


class ExamController(Home):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        response = super().web_login(redirect=redirect, **kw)
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            if user.user_type == 'candidate':
                return request.redirect('/exam/dashboard')
            else:
                return request.redirect('/web')
        return response

    @http.route(['/exam/dashboard'], type='http', auth='user', website=True)
    def exam_dashboard(self, **kw):
        if request.env.user.user_type != 'candidate':
            return request.redirect('/web')
        exams = request.env['exam.exam'].sudo().search([
            ('is_published', '=', True),
            ('state', 'in', ['confirmed', 'in_progress']),
        ])

        values = {
            'exams': exams,
        }
        return request.render('exam_management.portal_exam_dashboard', values)

    @http.route(['/exam/start/<int:exam_id>'], type='http', auth='user', website=True)
    def start_exam(self, exam_id, **kw):
        exam = request.env['exam.exam'].sudo().browse(exam_id)
        sections = exam.section_ids.sorted(lambda s: s.sequence)

        values = {
            'exam': exam,
            'sections': sections,
        }
        return request.render('exam_management.portal_exam_sections', values)

    @http.route(['/exam/section/<int:section_id>'], type='http', auth='user', website=True)
    def exam_section(self, section_id, **kw):
        section = request.env['exam.section'].sudo().browse(section_id)

        values = {
            'section': section,
            'subsections': section.subsection_ids if section.section_type == 'written_expr' else None,
            'criteria': section.evaluation_criteria_ids if section.section_type == 'oral_expr' else None,
        }

        template_map = {
            'reading_comp': 'exam_management.portal_reading_comp',
            'written_expr': 'exam_management.portal_written_expr',
            'thematic_mcq': 'exam_management.portal_thematic_mcq',
            'oral_comp': 'exam_management.portal_oral_comp',
            'oral_expr': 'exam_management.portal_oral_expr',
        }

        return request.render(template_map[section.section_type], values)