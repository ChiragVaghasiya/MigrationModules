odoo.define(
  "aspl_indian_payroll.ItStatementRewrite",
  function (require) {
    "use strict";

    var AbstractAction = require("web.AbstractAction");
    var core = require("web.core");
    var web_client = require("web.web_client");
    var _t = core._t;
    var QWeb = core.qweb;

    var ItStatement = AbstractAction.extend({
      template: "ItStatementMain",

      events: {
      },

      init: function (parent, context) {
        this._super(parent, context);
        this.dashboards_templates = ["ItStatement"];
        this.login_employee = [];
      },

      willStart: function () {
        var self = this;
        this.login_employee = {};
        return this._super().then(function () {
          var def1 = self
            ._rpc({
              model: "hr.employee",
              method: "get_user_employee_details_payslip",
            })
            .then(function (result) {
              self.login_employee = result;
            });
          return $.when(def1);
        });
      },

      start: function () {
        var self = this;
        this.set("title", "ItStatement");
        return this._super().then(function () {
          self.update_cp();
          self.render_dashboards();
          self.$el.parent().addClass("oe_background_grey");
        });
      },

      render_dashboards: function () {
      var self = this;
      var templates = [];
      if (this.login_employee == "Employee Not Found...") {
        self
          .$(".o_hr_dashboard")
          .append(QWeb.render("EmployeeWarningPayroll", { widget: self }));
      }
      else if (this.login_employee == "Employee Payslip or It Declaration Not Found...") {
        self
          .$(".o_hr_dashboard")
          .append(QWeb.render("PayslipWarningPayroll", { widget: self }));
      }
      else {
        templates = ["ItStatement"];
        _.each(templates, function (template) {
          self
            .$(".o_hr_dashboard")
            .append(QWeb.render(template, { widget: self }));
        });
      }
    },

      update_cp: function () {
        var self = this;
      },
    });
    core.action_registry.add("it_statement", ItStatement);

    return ItStatement;
  }
);
