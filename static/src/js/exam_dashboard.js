odoo.define('exam_management.dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');

    var ExamDashboard = AbstractAction.extend({
        template: 'ExamDashboardMain',
        events: {
            'click .refresh-dashboard': '_onRefreshDashboard',
            'click .exam-stat-box': '_onExamStatClick',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboardData = {};
        },

        willStart: function() {
            var self = this;
            return this._super().then(function() {
                return self._fetchDashboardData();
            });
        },

        start: function() {
            var self = this;
            return this._super().then(function() {
                self._renderDashboard();
            });
        },

        _fetchDashboardData: function() {
            var self = this;
            return rpc.query({
                model: 'exam.exam',
                method: 'get_dashboard_data',
                args: [],
            }).then(function(result) {
                self.dashboardData = result;
            });
        },

        _renderDashboard: function() {
            var $content = $(QWeb.render('ExamDashboardContent', {
                widget: this,
                data: this.dashboardData
            }));
            this.$('.o_exam_dashboard_content').empty();
            this.$('.o_exam_dashboard_content').append($content);
        },

        _onRefreshDashboard: function(ev) {
            ev.preventDefault();
            this._fetchDashboardData().then(this._renderDashboard.bind(this));
        },

        _onExamStatClick: function(ev) {
            ev.preventDefault();
            var actionName = $(ev.currentTarget).data('action');
            this.do_action(actionName);
        },
    });

    core.action_registry.add('exam_dashboard', ExamDashboard);
    return ExamDashboard;
});
