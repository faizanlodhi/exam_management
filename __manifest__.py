{
    'name': 'Examination Management',
    'version': '16.0.1.0.0',
    'category': 'Education',
    'summary': 'Advanced Examination Management System with AI Integration',
    'description': """
        Comprehensive examination management system featuring:
        - Exam creation and management
        - AI-driven question generation
        - Multiple question types support
        - Automated evaluation
        - Certificate management
        - Advanced reporting
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'mail','website', 'web', 'report_xlsx'],
    'data': [
        'security/exam_security.xml',
        'security/ir.model.access.csv',
        'views/exam_menus.xml',
        'views/res_users_views.xml',
        'views/exam_views.xml',
        'views/question_bank_views.xml',
        'views/candidate_views.xml',
        'views/exam_session_views.xml',
        'views/portal_templates.xml',
        'reports/exam_report_views.xml',
        'reports/exam_reports.xml',
        'data/ir_cron_data.xml',
        'data/exam_sequence.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # 'exam_management/static/src/js/exam_dashboard.js',
            # '/exam_management/static/src/css/exam_style.css',
            # 'exam_management/static/src/xml/exam_dashboard.xml',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}