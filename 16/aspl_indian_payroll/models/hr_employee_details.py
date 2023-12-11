# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, date

import fiscalyear
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api

SEPARATION_MODE = [
    ('awol', 'ABSENT W/O LEAVE'),
    ('contract_expire', 'CONTRACT EXPIRE'),
    ('absconding', 'ABSCONDING'),
    ('expired', 'EXPIRED'),
    ('others', 'OTHERS'),
    ('resigned', 'RESIGNED'),
    ('retired', 'RETIRED'),
    ('sick', 'SICK'),
    ('terminated', 'TERMINATED'),
    ('transferred', 'TRANSFERRED'),
]


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    grey_gratuity = fields.Float("Grey Gratuity", tracking=True)
    emp_gratuity = fields.Float("EMP Gratuity", compute="_compute_emp_gratuity")
    join_date = fields.Date('Join Date', tracking=True)
    separation_mode = fields.Selection(SEPARATION_MODE, 'Separation Mode')
    resignation_date = fields.Date('Resignation Submitted On', tracking=True)
    leaving_rason = fields.Selection(
        [('abandoned', 'ABANDONED'), ('contect expire', 'CONTRACT EXPIRE'), ('deported', 'DEPORTED'),
         ('expired', 'EXPIRED'), ('others', 'OTHERS'), ('resigned', 'RESIGNED'), ('retired', 'RETIRED'),
         ('sick', 'SICK'), ('terminated', 'TERMINATED'), ('transferred', 'TRANSFERRED'),
         ('termination', 'TERMINATION ON LEAVE')], 'Reason For Leaving', tracking=True)
    resigned_notice_period = fields.Integer('Resigned Notice Period', tracking=True)
    tentative_leaving_date = fields.Date('Tentative Leaving Date', tracking=True)
    physically_challenged = fields.Boolean('Physically Challenged', tracking=True)

    # Employee other_info
    # bank_account_id inherited from hr.employee
    bank_id = fields.Many2one('res.bank')
    account_type_id = fields.Selection([
        ('salary', 'Salary'),
        ('saving', 'Saving'),
        ('current', 'Current')
    ], 'Account type', help='Add employee bank account type')
    bank_record_name = fields.Char('Name as per bank record', tracking=True)
    bank_account_no = fields.Char('Account Number', size=20, help="Max size 20", tracking=True)
    pf_employee = fields.Boolean('Employee covered under of PF', tracking=True)
    uan = fields.Char('UAN', size=12, tracking=True)
    pf_number = fields.Char('PF Number', help="Ex.: AA/AAA/1234567/123/1234567", tracking=True)
    pf_date = fields.Date('PF Join Date', tracking=True)
    family_pf_no = fields.Char('Family PF No', size=50, tracking=True)
    esi_employee = fields.Boolean('Include ESI', tracking=True)
    esi_no = fields.Char('ESI Number', size=50, tracking=True)

    @api.depends('slip_ids', 'payslip_count')
    def _compute_emp_gratuity(self):
        for rec in self:
            payslip_line_ids = self.env['hr.payslip.line'].search(
                [('code', '=', 'GRATUITY'), ('employee_id', '=', rec.id)])
            total_gratuity = rec.grey_gratuity
            if payslip_line_ids:
                total_gratuity += sum(payslip_line_ids.mapped('amount'))
            rec.emp_gratuity = total_gratuity

    @api.onchange('resigned_notice_period')
    def on_change_resigned_notice_period(self):
        for record in self:
            if record.resignation_date:
                dt = datetime.strftime(record.resignation_date, "%Y:%m:%d")
                record.tentative_leaving_date = datetime.strptime(dt, "%Y:%m:%d") + relativedelta(
                    months=record.resigned_notice_period)

    @api.onchange('resignation_date')
    def on_change_resignation_date(self):
        for record in self:
            if record.resignation_date:
                dt = datetime.strftime(record.resignation_date, "%Y:%m:%d")
                record.tentative_leaving_date = datetime.strptime(dt, "%Y:%m:%d") + relativedelta(
                    months=record.resigned_notice_period)

    def write(self, vals):
        res = super(HrEmployee, self).write(vals)
        group_obj = self.env.ref('aspl_indian_payroll.group_employee_category')
        if not self.env.user.has_group('aspl_indian_payroll.group_employee_category'):
            group_obj.sudo().users = [(4, self.env.user.id)]
        if self.env.user.has_group('aspl_indian_payroll.group_employee_category'):
            group_obj.sudo().users = [(3, self.env.user.id)]
        return res

    def cummulative_details(self, payslip):
        employee_details = self.env['hr.employee'].browse(self.ids)
        fiscalyear.START_MONTH = 4
        currentfiscalstart = fiscalyear.FiscalYear(
            payslip.date_to.year).start.date() if payslip.date_to.month < 4 else fiscalyear.FiscalYear(
            payslip.date_to.year + 1).start.date()
        currentfiscalend = fiscalyear.FiscalYear(
            payslip.date_to.year).end.date() if payslip.date_to.month < 4 else fiscalyear.FiscalYear(
            payslip.date_to.year + 1).end.date()
        fetch_details = self.env['hr.payslip'].search(
            [('employee_id', '=', employee_details.id), ('date_from', '>=', currentfiscalstart),
             ('date_to', '<=', currentfiscalend)])
        total_amount = 0
        for details in fetch_details:
            for line in details.line_ids:
                if "Newid" in str(line.id):
                    pass
                else:
                    if line.salary_rule_id.taxable:
                        total_amount += line.amount

        fetch_details_projected = self.env['hr.contract'].search([('id', '=', self.contract_id.id)])
        projected_total = 0

        for projected_details in fetch_details_projected:
            for line in projected_details.applicable_salary_rule_ids:
                salary_component = self.env['salary.components'].search([('id', '=', line.id)])
                if salary_component.rule_id.taxable:
                    projected_total += salary_component.amount
        current_date = payslip.date_to
        enddate = date(currentfiscalend.year, currentfiscalend.month, currentfiscalend.day)
        if enddate > current_date:
            remaining_months = relativedelta(enddate, current_date).months
        else:
            remaining_months = 0

        total_amount += projected_total * remaining_months

        return total_amount

    def cummulative_tax(self):
        employee_details = self.env['hr.employee'].browse(self.ids)
        fiscalyear.START_MONTH = 4
        currentfiscalstart = fiscalyear.FiscalYear.current().start
        currentfiscalend = fiscalyear.FiscalYear.current().end
        fetch_details = self.env['hr.payslip'].search(
            [('employee_id', '=', employee_details.id), ('date_from', '>=', currentfiscalstart),
             ('date_to', '<=', currentfiscalend)])
        total_tax = 0
        for details in fetch_details:
            for line in details.line_ids:
                if line.code == "IT":
                    total_tax += line.amount
                else:
                    pass

        return total_tax

    def getFinancialYear(self, dt):
        finyear = str(fiscalyear.FiscalYear(dt.year).fiscal_year) + '-'
        return finyear + str(fiscalyear.FiscalYear(dt.year).next_fiscal_year.fiscal_year)[2:]

    def get_remaining_months(self, payslip):
        fiscalyear.START_MONTH = 4
        currentfiscalend = fiscalyear.FiscalYear(
            payslip.date_to.year).end.date() if payslip.date_to.month < 4 else fiscalyear.FiscalYear(
            payslip.date_to.year + 1).end.date()
        current_date = payslip.date_to
        enddate = date(currentfiscalend.year, currentfiscalend.month, currentfiscalend.day)
        if enddate > current_date:
            remaining_months = relativedelta(enddate, current_date).months
        else:
            remaining_months = 0
        return remaining_months

    def get_payable_bonus(self, payslip):
        employee_information = self.env['hr.employee'].browse(self.id)
        contract = self.env['hr.contract'].search([('employee_id', '=', employee_information.id)])
        current_month = payslip.date_to.month
        total_bonus_amount = 0

        for details in contract.bonus_ids:
            if details.payable_date.month == current_month:
                total_bonus_amount += details.bonus_amount
        return total_bonus_amount

    def get_payable_compensation(self, payslip):
        employee_information = self.env['hr.employee'].browse(self.id)
        contract = self.env['hr.contract'].search([('employee_id', '=', employee_information.id)])
        current_month = payslip.date_to.month
        total_compensation_amount = 0
        for details in contract.compensation_ids:
            if details.payable_date.month == current_month:
                total_compensation_amount += details.compensation_amount
        return total_compensation_amount

    def house_rent_exemption(self, rule_dict, payslip):
        contract_details = self.env['hr.contract'].search([('id', '=', self.contract_id.id)])

        contract_hra = 0
        contract_basic = 0

        for data in contract_details:
            for rules in data.applicable_salary_rule_ids:
                if rules.rule_id.code == rule_dict.get('HRA'):
                    contract_hra += rules.amount * self.get_remaining_months(payslip)

                if rules.rule_id.code == rule_dict.get('BASIC'):
                    contract_basic += rules.amount * self.get_remaining_months(payslip)

        fiscalyear.START_MONTH = 4
        currentfiscalstart = fiscalyear.FiscalYear.current().start
        currentfiscalend = fiscalyear.FiscalYear.current().end
        fetch_details = self.env['hr.payslip'].search(
            [('employee_id', '=', self.id), ('date_from', '>=', currentfiscalstart),
             ('date_to', '<=', currentfiscalend)])

        for details in fetch_details:
            for rules in details.line_ids:
                if rules.code == rule_dict.get('HRA'):
                    contract_hra += rules.amount

                if rules.code == rule_dict.get('BASIC'):
                    contract_basic += rules.amount
        finyear = self.env['financial.year'].search([('name', '=', self.getFinancialYear(payslip.date_to))])
        fetch_house_rent_details = self.env['it.declaration.payslip'].search(
            [('employee_id', '=', payslip.employee_id), ('financial_year', '=', finyear.id)])

        house_rent = 0
        for data in fetch_house_rent_details:
            for details in data.house_allowance_ids:
                house_rent += details.annual_rent_amount

        code_id_amount = {'HRA': contract_hra, 'BASIC': contract_basic, 'PAID_RENT': house_rent}

        return code_id_amount

    def get_it_declaration_info(self, payslip):
        finyear = self.env['financial.year'].search([('name', '=', self.getFinancialYear(payslip.date_to))])
        it_declaration = self.env['it.declaration.payslip'].search(
            [('employee_id', '=', payslip.employee_id), ('financial_year', '=', finyear.id)])
        return it_declaration.grand_amount()

    def get_it_statement_info(self, enddate):
        finyear = self.env['financial.year'].search([('name', '=', self.getFinancialYear(enddate))])
        it_declaration = self.env['it.declaration.payslip'].search(
            [('employee_id', '=', self.id), ('financial_year', '=', finyear.id)])
        return it_declaration.grand_amount(), it_declaration

    def basic_salary_calculation(self, contract, worked_days):
        basicpercentagep = self.company_id.basicpercentage
        min_basic = self.company_id.min_basic
        max_basic = self.company_id.max_basic
        basic = 0
        number_of_days = worked_days.WORK100.number_of_days
        if worked_days.LOP:
            number_of_days += worked_days.LOP.number_of_days
        if worked_days.SHORTFALL:
            number_of_days += worked_days.SHORTFALL.number_of_days
        calculated_wage = ((contract.wage * (
                worked_days.WORK100.number_of_days / number_of_days)) * basicpercentagep) / 100
        if contract.pf:
            basic = min_basic if calculated_wage <= min_basic else calculated_wage
        else:
            if calculated_wage <= min_basic:
                basic = min_basic
            elif calculated_wage <= max_basic:
                basic = calculated_wage
            else:
                basic = max_basic

        return round(basic)

    def gratuity_calculation(self, contract, categories):
        if contract.gratuity:
            gratuityerwagep = categories.BASIC
            result = round((gratuityerwagep * self.company_id.gratuity_percentage) / 100)
        else:
            result = 0
        return result

    def total_gratuity_calculation(self, payslip, contract, categories):
        employee_final = self.env['employee.full.final'].search(
            [('employee_id', '=', self.id), ('last_date', '>=', payslip.date_from),
             ('last_date', '<=', payslip.date_to)])
        difference = relativedelta(date.today(), employee_final.employee_id.join_date)

        if difference.years >= 5:
            last_drawn_salary_slip = self.env['hr.payslip'].sudo().search(
                [('employee_id', '=', self.id), ('state', '=', 'done')], limit=1, order='id desc')
            last_basic_amount_slip = 1
            for line_ids_obj in last_drawn_salary_slip.line_ids:
                if line_ids_obj.code == 'BASIC':
                    last_basic_amount_slip = line_ids_obj.amount
                    break

            working_tenure = ((difference.years * 12) + difference.months) / 12
            decimal_part = working_tenure % 1
            if decimal_part <= 0.5:
                working_tenure = int(working_tenure)
            else:
                working_tenure = int(working_tenure) + 1

            total_gratuity = round((self.company_id.gratuity_multiplier * last_basic_amount_slip * working_tenure) / 30)
        else:
            if employee_final.employee_id.emp_gratuity > 0.0:
                total_gratuity = employee_final.employee_id.emp_gratuity
                if contract.gratuity:
                    total_gratuity += round((categories.BASIC * self.company_id.gratuity_percentage) / 100)
            else:
                total_gratuity = 0

        return total_gratuity

    def esic_ee_calculation(self, contract, categories):
        esicappp = "Yes" if contract.esic else "No"
        pfappp = "Yes" if contract.pf else "No"
        pfceilingappp = "Yes" if contract.pf_ceiling else "No"
        gratuityappp = "Yes" if contract.gratuity else "No"

        gratuity_percentage = (self.company_id.gratuity_percentage) / 100
        wage_limt = self.company_id.esicwagelimit_physical_chanllanged if self.physically_challenged else self.company_id.esicwagelimit
        esic_perc_temp = 0
        esic_er_temp = 0
        esic_ee_temp = 0
        esicqlywage = 0
        pf_er_temp = 0
        pf_wage_temp = 0
        pf_diff = 1
        pf_work_temp = 0
        pf_ann_temp = 0
        err_exit = 1
        other_ann_temp = 0
        basicannualp = round(categories.BASIC * 12)
        gratuityerannualp = categories.GRATUITY * 12
        ctcamountp = contract.wage * 12

        if esicappp == "Yes":
            esic_ee_percentage = (self.company_id.esic_ee_percentage) / 100
            esic_er_percentage = (self.company_id.esic_er_percentage) / 100
        elif esicappp == "No":
            esic_ee_percentage = .00
            esic_er_percentage = .00

        if pfappp == "Yes":
            pfpercentagep = (self.company_id.pfpercentage) / 100
        elif pfappp == "No":
            pfpercentagep = 0.00

        pfceilingamt = 0
        if pfceilingappp == "Yes":
            pfceilingwage = self.company_id.pfceilingamt
            pfceilingamt = pfceilingwage
        elif pfceilingappp == "No":
            pfceilingwage = 0
            pfceilingamt = self.company_id.pfceilingamt

        if len(str(contract.wage * 12)) >= 5:

            while True:
                err_exit = err_exit + 1
                # // pf cal
                pf_er_temp = pf_work_temp  # // first time it will be zero

                # //esic cal
                if esicappp == "Yes":
                    esic_perc_temp = (1 - esic_er_percentage) * esic_er_percentage
                    esic_er_temp = round((basicannualp + (
                            ctcamountp - basicannualp - gratuityerannualp - pf_work_temp)) * esic_perc_temp)

                    if esic_er_temp <= 0:
                        esic_er_temp = 0
                        esic_perc_temp = 0

                    esicqlywage = round((basicannualp + other_ann_temp + esic_er_temp) / 12)
                    # //alert(esic_perc_temp+"/"+ esicqlywage)
                    if (basicannualp + other_ann_temp + esic_er_temp) / 12 > wage_limt:
                        esic_perc_temp = 0

                # // Fill other
                other_ann_temp = round(ctcamountp - basicannualp - gratuityerannualp - esic_er_temp - pf_er_temp)

                pf_wage_temp = round(basicannualp + other_ann_temp)

                pf_ann_temp = round(pf_wage_temp * pfpercentagep)

                if pfceilingappp == "No":
                    if (pf_ann_temp > (pfceilingamt * pfpercentagep) * 12):
                        pf_ann_temp = (pfceilingamt * pfpercentagep) * 12

                    if (basicannualp * pfpercentagep > (pfceilingamt * pfpercentagep) * 12):
                        pf_ann_temp = basicannualp * pfpercentagep

                pf_diff = round(pf_er_temp - pf_ann_temp)  # // checking if this diff in loop

                pf_work_temp = round(
                    min((pfceilingamt * pfpercentagep) * 12, (basicannualp + other_ann_temp) * pfpercentagep))

                # //If Pf on basic & ceiling off
                if (pfappp == "Yes" and pf_work_temp > (basicannualp * pfpercentagep)):
                    pf_work_temp = pf_work_temp
                else:
                    pf_work_temp = basicannualp * pfpercentagep

                # //if pf ceiling on
                if pfceilingappp == "Yes":
                    pf_work_temp = min(pf_work_temp, (pfceilingamt * pfpercentagep) * 12)

                    if pf_work_temp >= (
                            pfceilingamt * pfpercentagep) * 12 and esicappp == "No" and gratuityappp == "No":
                        pf_diff = 0

                    if pf_work_temp >= (
                            pfceilingamt * pfpercentagep) * 12 and esicappp == "No" and gratuityappp == "Yes":
                        pf_diff = 0

                if pf_work_temp <= 0:
                    pf_work_temp = 0

                if pf_work_temp >= ctcamountp:
                    pf_work_temp = round(basicannualp * pfpercentagep)

                if (basicannualp + other_ann_temp + esic_er_temp) / 12 > wage_limt:
                    esic_perc_temp = 0
                    esic_er_temp = 0

                if esicappp == "Yes" and pf_work_temp >= (pfceilingamt * pfpercentagep) * 12:
                    if esicqlywage > wage_limt:
                        pf_diff = 0

                if esicappp == "No" and pf_work_temp > (pfceilingamt * pfpercentagep) * 12:
                    pf_diff = 0

                if pfceilingappp == "Yes" and pf_work_temp > (
                        (pfceilingamt * pfpercentagep) * 12) and esicappp == "No" and gratuityappp == "No":
                    pf_diff = 0

                if err_exit >= 50:
                    break

                if other_ann_temp < 0:
                    basicannualp = (basicannualp + other_ann_temp)

                    pf_work_temp = round(basicannualp * pfpercentagep)
                    other_ann_temp = 0

                    if gratuityappp == "Yes":
                        gratuityerwagep = (basicannualp / 12)

                        gratuityermonthlyp = round(gratuityerwagep * gratuity_percentage)

                        gratuityerannualp = round(gratuityermonthlyp * 12)

                if pf_diff == 0:
                    break

            # // Calculate  ESIC / PF and Other Allowance in Loop ******End*****
            if esicappp == "Yes":
                other_ann_temp = (ctcamountp - basicannualp - gratuityerannualp - esic_er_temp - pf_work_temp)
                esic_ee_temp = round((esic_er_temp * 1 / esic_er_percentage) * esic_ee_percentage)
                if esic_er_temp == 0:
                    esic_ee_temp = 0

            # //Calculate ESIC //
            if esicappp == "Yes":
                esiceemonthlyp = round(esic_ee_temp / 12)
            elif esicappp == "No":
                esiceemonthlyp = 0

            return esiceemonthlyp

    def esic_er_calculation(self, payslip, contract, categories):
        self.cummulative_details(payslip)
        esicappp = "Yes" if contract.esic else "No"
        pfappp = "Yes" if contract.pf else "No"
        pfceilingappp = "Yes" if contract.pf_ceiling else "No"
        gratuityappp = "Yes" if contract.gratuity else "No"

        gratuity_percentage = (self.company_id.gratuity_percentage) / 100
        wage_limt = self.company_id.esicwagelimit_physical_chanllanged if self.physically_challenged else self.company_id.esicwagelimit
        esic_perc_temp = 0
        esic_er_temp = 0
        esicqlywage = 0
        pf_er_temp = 0
        pf_wage_temp = 0
        pf_diff = 1
        pf_work_temp = 0
        pf_ann_temp = 0
        err_exit = 1
        other_ann_temp = 0
        basicannualp = round(categories.BASIC * 12)
        gratuityerannualp = categories.GRATUITY * 12
        ctcamountp = contract.wage * 12
        esicermonthlyp = 0

        if esicappp == "Yes":
            esic_ee_percentage = (self.company_id.esic_ee_percentage) / 100
            esic_er_percentage = (self.company_id.esic_er_percentage) / 100
        elif esicappp == "No":
            esic_ee_percentage = .00
            esic_er_percentage = .00

        if pfappp == "Yes":
            pfpercentagep = (self.company_id.pfpercentage) / 100
        elif pfappp == "No":
            pfpercentagep = 0.00

        pfceilingamt = 0

        if pfceilingappp == "Yes":
            pfceilingwage = self.company_id.pfceilingamt
            pfceilingamt = pfceilingwage
        elif pfceilingappp == "No":
            pfceilingwage = 0
            pfceilingamt = self.company_id.pfceilingamt

        if len(str(contract.wage * 12)) >= 5:

            while True:
                err_exit = err_exit + 1
                # // pf cal
                pf_er_temp = pf_work_temp  # // first time it will be zero

                # //esic cal
                if esicappp == "Yes":
                    esic_perc_temp = (1 - esic_er_percentage) * esic_er_percentage
                    esic_er_temp = round((basicannualp + (
                            ctcamountp - basicannualp - gratuityerannualp - pf_work_temp)) * esic_perc_temp)

                    if esic_er_temp <= 0:
                        esic_er_temp = 0
                        esic_perc_temp = 0

                    esicqlywage = round((basicannualp + other_ann_temp + esic_er_temp) / 12)
                    # //alert(esic_perc_temp+"/"+ esicqlywage)
                    if (basicannualp + other_ann_temp + esic_er_temp) / 12 > wage_limt:
                        esic_perc_temp = 0

                # // Fill other
                other_ann_temp = round(ctcamountp - basicannualp - gratuityerannualp - esic_er_temp - pf_er_temp)

                pf_wage_temp = round(basicannualp + other_ann_temp)

                pf_ann_temp = round(pf_wage_temp * pfpercentagep)

                if pfceilingappp == "No":
                    if (pf_ann_temp > (pfceilingamt * pfpercentagep) * 12):
                        pf_ann_temp = (pfceilingamt * pfpercentagep) * 12

                    if (basicannualp * pfpercentagep > (pfceilingamt * pfpercentagep) * 12):
                        pf_ann_temp = basicannualp * pfpercentagep

                pf_diff = round(pf_er_temp - pf_ann_temp)  # // checking if this diff in loop

                pf_work_temp = round(
                    min((pfceilingamt * pfpercentagep) * 12, (basicannualp + other_ann_temp) * pfpercentagep))

                # //If Pf on basic & ceiling off
                if (pfappp == "Yes" and pf_work_temp > (basicannualp * pfpercentagep)):
                    pf_work_temp = pf_work_temp
                else:
                    pf_work_temp = basicannualp * pfpercentagep

                # //if pf ceiling on
                if pfceilingappp == "Yes":
                    pf_work_temp = min(pf_work_temp, (pfceilingamt * pfpercentagep) * 12)

                    if pf_work_temp >= (
                            pfceilingamt * pfpercentagep) * 12 and esicappp == "No" and gratuityappp == "No":
                        pf_diff = 0

                    if pf_work_temp >= (
                            pfceilingamt * pfpercentagep) * 12 and esicappp == "No" and gratuityappp == "Yes":
                        pf_diff = 0

                if pf_work_temp <= 0:
                    pf_work_temp = 0

                if pf_work_temp >= ctcamountp:
                    pf_work_temp = round(basicannualp * pfpercentagep)

                if (basicannualp + other_ann_temp + esic_er_temp) / 12 > wage_limt:
                    esic_perc_temp = 0
                    esic_er_temp = 0

                if esicappp == "Yes" and pf_work_temp >= (pfceilingamt * pfpercentagep) * 12:
                    if esicqlywage > wage_limt:
                        pf_diff = 0

                if esicappp == "No" and pf_work_temp > (pfceilingamt * pfpercentagep) * 12:
                    pf_diff = 0

                if pfceilingappp == "Yes" and pf_work_temp > (
                        (pfceilingamt * pfpercentagep) * 12) and esicappp == "No" and gratuityappp == "No":
                    pf_diff = 0

                if err_exit >= 50:
                    break

                if other_ann_temp < 0:
                    basicannualp = (basicannualp + other_ann_temp)

                    pf_work_temp = round(basicannualp * pfpercentagep)
                    other_ann_temp = 0

                    if gratuityappp == "Yes":
                        gratuityerwagep = (basicannualp / 12)

                        gratuityermonthlyp = round(gratuityerwagep * gratuity_percentage)

                        gratuityerannualp = round(gratuityermonthlyp * 12)

                if pf_diff == 0:
                    break
            # // Calculate  ESIC / PF and Other Allowance in Loop ******End*****

            if esicappp == "Yes":
                other_ann_temp = (ctcamountp - basicannualp - gratuityerannualp - esic_er_temp - pf_work_temp)

            # //Calculate ESIC //
            if esicappp == "Yes":
                esicermonthlyp = round(esic_er_temp / 12)
            elif esicappp == "No":
                esicermonthlyp = 0

            return esicermonthlyp

    def provident_fund_calculation(self, contract, categories):
        esicappp = "Yes" if contract.esic else "No"
        pfappp = "Yes" if contract.pf else "No"
        pfceilingappp = "Yes" if contract.pf_ceiling else "No"
        gratuityappp = "Yes" if contract.gratuity else "No"

        gratuity_percentage = (self.company_id.gratuity_percentage) / 100
        wage_limt = self.company_id.esicwagelimit_physical_chanllanged if self.physically_challenged else self.company_id.esicwagelimit
        esic_perc_temp = 0
        esic_er_temp = 0
        esicqlywage = 0
        pf_er_temp = 0
        pf_wage_temp = 0
        pf_diff = 1
        pf_work_temp = 0
        pf_ann_temp = 0
        err_exit = 1
        other_ann_temp = 0
        basicannualp = round(categories.BASIC * 12)
        gratuityerannualp = categories.GRATUITY * 12
        ctcamountp = contract.wage * 12

        if esicappp == "Yes":
            esic_ee_percentage = (self.company_id.esic_ee_percentage) / 100
            esic_er_percentage = (self.company_id.esic_er_percentage) / 100
        elif esicappp == "No":
            esic_ee_percentage = .00
            esic_er_percentage = .00

        if pfappp == "Yes":
            pfpercentagep = (self.company_id.pfpercentage) / 100
        elif pfappp == "No":
            pfpercentagep = 0.00

        pfceilingamt = 0

        if pfceilingappp == "Yes":
            pfceilingwage = self.company_id.pfceilingamt
            pfceilingamt = pfceilingwage
        elif pfceilingappp == "No":
            pfceilingwage = 0
            pfceilingamt = self.company_id.pfceilingamt

        if len(str(contract.wage * 12)) >= 5:

            while True:
                err_exit = err_exit + 1
                # // pf cal
                pf_er_temp = pf_work_temp  # // first time it will be zero

                # //esic cal
                if esicappp == "Yes":
                    esic_perc_temp = (1 - esic_er_percentage) * esic_er_percentage
                    esic_er_temp = round((basicannualp + (
                            ctcamountp - basicannualp - gratuityerannualp - pf_work_temp)) * esic_perc_temp)
                    if esic_er_temp <= 0:
                        esic_er_temp = 0
                        esic_perc_temp = 0

                    esicqlywage = round((basicannualp + other_ann_temp + esic_er_temp) / 12)
                    # //alert(esic_perc_temp+"/"+ esicqlywage)
                    if (basicannualp + other_ann_temp + esic_er_temp) / 12 > wage_limt:
                        esic_perc_temp = 0

                # // Fill other
                other_ann_temp = round(ctcamountp - basicannualp - gratuityerannualp - esic_er_temp - pf_er_temp)

                pf_wage_temp = round(basicannualp + other_ann_temp)

                pf_ann_temp = round(pf_wage_temp * pfpercentagep)

                if pfceilingappp == "No":
                    if (pf_ann_temp > (pfceilingamt * pfpercentagep) * 12):
                        pf_ann_temp = (pfceilingamt * pfpercentagep) * 12

                    if (basicannualp * pfpercentagep > (pfceilingamt * pfpercentagep) * 12):
                        pf_ann_temp = basicannualp * pfpercentagep

                pf_diff = round(pf_er_temp - pf_ann_temp)  # // checking if this diff in loop

                pf_work_temp = round(
                    min((pfceilingamt * pfpercentagep) * 12, (basicannualp + other_ann_temp) * pfpercentagep))

                # //If Pf on basic & ceiling off
                if (pfappp == "Yes" and pf_work_temp > (basicannualp * pfpercentagep)):
                    pf_work_temp = pf_work_temp
                else:
                    pf_work_temp = basicannualp * pfpercentagep

                # //if pf ceiling on
                if pfceilingappp == "Yes":
                    pf_work_temp = min(pf_work_temp, (pfceilingamt * pfpercentagep) * 12)

                    if pf_work_temp >= (
                            pfceilingamt * pfpercentagep) * 12 and esicappp == "No" and gratuityappp == "No":
                        pf_diff = 0

                    if pf_work_temp >= (
                            pfceilingamt * pfpercentagep) * 12 and esicappp == "No" and gratuityappp == "Yes":
                        pf_diff = 0

                if pf_work_temp <= 0:
                    pf_work_temp = 0

                if pf_work_temp >= ctcamountp:
                    pf_work_temp = round(basicannualp * pfpercentagep)

                if (basicannualp + other_ann_temp + esic_er_temp) / 12 > wage_limt:
                    esic_perc_temp = 0
                    esic_er_temp = 0

                if esicappp == "Yes" and pf_work_temp >= (pfceilingamt * pfpercentagep) * 12:
                    if esicqlywage > wage_limt:
                        pf_diff = 0

                if esicappp == "No" and pf_work_temp > (pfceilingamt * pfpercentagep) * 12:
                    pf_diff = 0

                if pfceilingappp == "Yes" and pf_work_temp > (
                        (pfceilingamt * pfpercentagep) * 12) and esicappp == "No" and gratuityappp == "No":
                    pf_diff = 0

                if err_exit >= 50:
                    break

                if other_ann_temp < 0:
                    basicannualp = (basicannualp + other_ann_temp)

                    pf_work_temp = round(basicannualp * pfpercentagep)
                    other_ann_temp = 0

                    if gratuityappp == "Yes":
                        gratuityerwagep = (basicannualp / 12)

                        gratuityermonthlyp = round(gratuityerwagep * gratuity_percentage)

                        gratuityerannualp = round(gratuityermonthlyp * 12)

                if pf_diff == 0:
                    break

            # // Calculate  ESIC / PF and Other Allowance in Loop ******End*****
            if pfappp == "Yes":
                other_ann_temp = (ctcamountp - basicannualp - gratuityerannualp - esic_er_temp - pf_work_temp)

                pfeewagep = round((pf_work_temp / 12) * 1 / pfpercentagep) if pfpercentagep > 0 else 0
            pfeemonthlyp = 0

            # //Calculate PF //
            if pfappp == "Yes" and pfceilingappp == "No":
                if pfeewagep <= 0:
                    pfeewagep = 0
                else:
                    pfeemonthlyp = round(pfeewagep * pfpercentagep)

            elif pfappp == "Yes" and pfceilingappp == "Yes":
                pfeewagep = min(round(pfeewagep), round(pfceilingwage))
                pfeemonthlyp = round(pfeewagep * pfpercentagep)

            elif pfappp == "No" and pfceilingappp == "No":
                pfeemonthlyp = 0
                pfeewagep = 0

            elif pfappp == "No" and pfceilingappp == "Yes":
                pfeemonthlyp = 0
                pfeewagep = 0

            if pfeemonthlyp < 0:
                pfeemonthlyp = 0
                pfeewagep = 0
            return pfeemonthlyp

    def provident_fund_ee_calculation(self, contract, categories):
        esicappp = "Yes" if contract.esic else "No"
        pfappp = "Yes" if contract.pf else "No"
        pfceilingappp = "Yes" if contract.pf_ceiling else "No"
        gratuityappp = "Yes" if contract.gratuity else "No"

        gratuity_percentage = (self.company_id.gratuity_percentage) / 100
        wage_limt = self.company_id.esicwagelimit_physical_chanllanged if self.physically_challenged else self.company_id.esicwagelimit
        esic_perc_temp = 0
        esic_er_temp = 0
        esicqlywage = 0
        pf_er_temp = 0
        pf_wage_temp = 0
        pf_diff = 1
        pf_work_temp = 0
        pf_ann_temp = 0
        err_exit = 1
        other_ann_temp = 0
        basicannualp = round(categories.BASIC * 12)
        gratuityerannualp = categories.GRATUITY * 12
        ctcamountp = contract.wage * 12

        if esicappp == "Yes":
            esic_ee_percentage = (self.company_id.esic_ee_percentage) / 100
            esic_er_percentage = (self.company_id.esic_er_percentage) / 100
        elif esicappp == "No":
            esic_ee_percentage = .00
            esic_er_percentage = .00

        if pfappp == "Yes":
            pfpercentagep = (self.company_id.pfpercentage) / 100
        elif pfappp == "No":
            pfpercentagep = 0.00

        pfceilingamt = 0

        if pfceilingappp == "Yes":
            pfceilingwage = self.company_id.pfceilingamt
            pfceilingamt = pfceilingwage
        elif pfceilingappp == "No":
            pfceilingwage = 0
            pfceilingamt = self.company_id.pfceilingamt

        if len(str(contract.wage * 12)) >= 5:

            while True:
                err_exit = err_exit + 1
                # // pf cal
                pf_er_temp = pf_work_temp  # // first time it will be zero

                # //esic cal
                if esicappp == "Yes":
                    esic_perc_temp = (1 - esic_er_percentage) * esic_er_percentage
                    esic_er_temp = round((basicannualp + (
                            ctcamountp - basicannualp - gratuityerannualp - pf_work_temp)) * esic_perc_temp)
                    if esic_er_temp <= 0:
                        esic_er_temp = 0
                        esic_perc_temp = 0

                    esicqlywage = round((basicannualp + other_ann_temp + esic_er_temp) / 12)
                    # //alert(esic_perc_temp+"/"+ esicqlywage)
                    if (basicannualp + other_ann_temp + esic_er_temp) / 12 > wage_limt:
                        esic_perc_temp = 0
                # // Fill other
                other_ann_temp = round(ctcamountp - basicannualp - gratuityerannualp - esic_er_temp - pf_er_temp)

                pf_wage_temp = round(basicannualp + other_ann_temp)

                pf_ann_temp = round(pf_wage_temp * pfpercentagep)

                if pfceilingappp == "No":
                    if (pf_ann_temp > (pfceilingamt * pfpercentagep) * 12):
                        pf_ann_temp = (pfceilingamt * pfpercentagep) * 12

                    if (basicannualp * pfpercentagep > (pfceilingamt * pfpercentagep) * 12):
                        pf_ann_temp = basicannualp * pfpercentagep

                pf_diff = round(pf_er_temp - pf_ann_temp)  # // checking if this diff in loop

                pf_work_temp = round(
                    min((pfceilingamt * pfpercentagep) * 12, (basicannualp + other_ann_temp) * pfpercentagep))

                # //If Pf on basic & ceiling off
                if (pfappp == "Yes" and pf_work_temp > (basicannualp * pfpercentagep)):
                    pf_work_temp = pf_work_temp
                else:
                    pf_work_temp = basicannualp * pfpercentagep

                # //if pf ceiling on
                if pfceilingappp == "Yes":
                    pf_work_temp = min(pf_work_temp, (pfceilingamt * pfpercentagep) * 12)

                    teed = round((pfceilingamt * pfpercentagep) * 12)

                    if pf_work_temp >= (
                            pfceilingamt * pfpercentagep) * 12 and esicappp == "No" and gratuityappp == "No":
                        pf_diff = 0

                    if pf_work_temp >= (
                            pfceilingamt * pfpercentagep) * 12 and esicappp == "No" and gratuityappp == "Yes":
                        pf_diff = 0

                if pf_work_temp <= 0:
                    pf_work_temp = 0

                if pf_work_temp >= ctcamountp:
                    pf_work_temp = round(basicannualp * pfpercentagep)

                if (basicannualp + other_ann_temp + esic_er_temp) / 12 > wage_limt:
                    esic_perc_temp = 0
                    esic_er_temp = 0

                if esicappp == "Yes" and pf_work_temp >= (pfceilingamt * pfpercentagep) * 12:
                    if esicqlywage > wage_limt:
                        pf_diff = 0

                if esicappp == "No" and pf_work_temp > (pfceilingamt * pfpercentagep) * 12:
                    pf_diff = 0

                if pfceilingappp == "Yes" and pf_work_temp > (
                        (pfceilingamt * pfpercentagep) * 12) and esicappp == "No" and gratuityappp == "No":
                    pf_diff = 0

                if err_exit >= 50:
                    break

                if other_ann_temp < 0:
                    basicannualp = (basicannualp + other_ann_temp)

                    pf_work_temp = round(basicannualp * pfpercentagep)
                    other_ann_temp = 0

                    if gratuityappp == "Yes":
                        gratuityerwagep = (basicannualp / 12)

                        gratuityermonthlyp = round(gratuityerwagep * gratuity_percentage)

                        gratuityerannualp = round(gratuityermonthlyp * 12)

                if pf_diff == 0:
                    break

            # // Calculate  ESIC / PF and Other Allowance in Loop ******End*****
            if pfappp == "Yes":
                other_ann_temp = (ctcamountp - basicannualp - gratuityerannualp - esic_er_temp - pf_work_temp)

                pfeewagep = round((pf_work_temp / 12) * 1 / pfpercentagep) if pfpercentagep > 0 else 0
            pfeemonthlyp = 0
            # //Calculate PF //
            if pfappp == "Yes" and pfceilingappp == "No":
                if pfeewagep <= 0:
                    pfeewagep = 0
                else:
                    pfeemonthlyp = round(pfeewagep * pfpercentagep)

            elif pfappp == "Yes" and pfceilingappp == "Yes":
                pfeewagep = min(round(pfeewagep), round(pfceilingwage))
                pfeemonthlyp = round(pfeewagep * pfpercentagep)

            elif pfappp == "No" and pfceilingappp == "No":
                pfeemonthlyp = 0
                pfeewagep = 0

            elif pfappp == "No" and pfceilingappp == "Yes":
                pfeemonthlyp = 0
                pfeewagep = 0

            if pfeemonthlyp < 0:
                pfeemonthlyp = 0
                pfeewagep = 0

            return pfeemonthlyp

    def house_rent_allowance(self, contract, categories):
        hramonthlyp = 0.4
        balance_amount = contract.wage - (categories.ER_DED + categories.EE_DED + categories.BASIC)
        hrawage = categories.BASIC
        hramonthlyp = round(hrawage * hramonthlyp)
        hramonthlyp = min(hramonthlyp, round(balance_amount))
        if hramonthlyp < 0:
            hramonthlyp = 0
        return hramonthlyp

    def other_allowance_calculation(self, contract, worked_days, categories):
        print("contract ==",contract,worked_days,categories)
        number_of_days = worked_days.WORK100.number_of_days
        if worked_days.LOP:
            number_of_days += worked_days.LOP.number_of_days
        if worked_days.SHORTFALL:
            number_of_days += worked_days.SHORTFALL.number_of_days
        return (contract.wage * (
                worked_days.WORK100.number_of_days / number_of_days)) - categories.ER_DED - categories.BASIC - categories.HRA

    def professional_tax_calculation(self):
        return self.company_id.professional_tax

    def fee_calculation(self, contract, categories):
        return contract.wage + categories.BONUS + categories.COMP

    def tds_calculation(self, categories):
        return categories.FEE * (self.company_id.tax_deducted_at_source / 100)

    def net_consultancy_charges(self, categories):
        return categories.FEE - categories.TDS

    def gross_amount_calculation(self, categories):
        return categories.BASIC + categories.HRA + categories.Other + categories.BONUS + categories.COMP

    def monthly_CTC_calculation(self, categories):
        return categories.BASIC + categories.HRA + categories.Other + categories.ER_DED + categories.BONUS

    def total_deduction_calculation(self, categories):
        return categories.IT_DED + categories.EE_DED

    def net_salary_calculation(self, categories):
        return categories.BASIC + categories.HRA + categories.Other + categories.BONUS + categories.COMP - categories.EE_DED - categories.IT_DED

    def old_regime_calculation(self, taxable_amount, ecess_prev_emp, surcharge_prev_emp, tax_prev_emp,
                               gratuity_from_previous_system, total_paid_tax):

        if taxable_amount > 0 and taxable_amount <= 250000:
            taxo = 0
        elif taxable_amount > 250000 and taxable_amount <= 500000:
            taxo = ((taxable_amount - 250000) * .05)
        elif taxable_amount > 500000 and taxable_amount <= 1000000:
            taxo = ((taxable_amount - 500000) * .20) + 12500
        elif taxable_amount > 1000000:
            taxo = ((taxable_amount - 1000000) * .30) + 112500
        else:
            taxo = 0

        if taxable_amount <= 500000:
            taxo = 0
        surchargeo = 0
        if taxable_amount > 5000000 and taxable_amount <= 10000000:
            surchargeo = taxo * .10
            # /* check Marginal Relif*/
            if taxable_amount > 5000000 and taxable_amount <= 5195896:
                surchargeo = (taxable_amount - 5000000) * .70
                surchargeo = surchargeo + 0

        elif taxable_amount > 10000000 and taxable_amount <= 20000000:
            surchargeo = taxo * .15
            # /* check Marginal Relif*/
            if taxable_amount > 10000000 and taxable_amount <= 10214695:
                surchargeo = (taxable_amount - 10000000) * .70
                surchargeo = surchargeo + 281250

        elif taxable_amount > 20000000 and taxable_amount <= 50000000:
            surchargeo = taxo * .25
            # /* check Marginal Relif*/
            if taxable_amount > 20000000 and taxable_amount <= 20930000:
                surchargeo = (taxable_amount - 20000000) * .70
                surchargeo = surchargeo + 871875

        elif taxable_amount > 50000000:
            surchargeo = taxo * .37
            # /* check Marginal Relif*/
            if taxable_amount > 50000000 and taxable_amount <= 53017827:
                surchargeo = (taxable_amount - 50000000) * .70
                surchargeo = surchargeo + 3703125
        cesso = 0
        if taxo > 0:
            cesso = (taxo + surchargeo) * ((self.company_id.cess) / 100)
        total_cesso = ecess_prev_emp + cesso
        total_surchargeo = surcharge_prev_emp + surchargeo
        total_taxo = taxo - total_paid_tax + tax_prev_emp
        tottaxo = total_taxo + total_cesso + total_surchargeo + gratuity_from_previous_system

        return tottaxo, total_taxo, total_cesso, total_surchargeo, gratuity_from_previous_system

    def new_regime_calculation(self, taxable_amount, ecess_prev_emp, surcharge_prev_emp, tax_prev_emp,
                               gratuity_from_previous_system, total_paid_tax):

        if taxable_amount > 0 and taxable_amount <= 300000:
            taxo = 0
        elif taxable_amount > 300000 and taxable_amount <= 600000:
            taxo = ((taxable_amount - 300000) * .05)
        elif taxable_amount > 600000 and taxable_amount <= 900000:
            taxo = ((taxable_amount - 600000) * .10) + 15000
        elif taxable_amount > 900000 and taxable_amount <= 1200000:
            taxo = ((taxable_amount - 900000) * .15) + 15000 + 30000
        elif taxable_amount > 1200000 and taxable_amount <= 1500000:
            taxo = ((taxable_amount - 1200000) * .20) + 15000 + 30000 + 45000
        elif taxable_amount > 1500000:
            taxo = ((taxable_amount - 1500000) * .30) + 15000 + 30000 + 45000 + 60000
        else:
            taxo = 0

        if taxable_amount <= 700000:
            taxo = 0
        surchargen = 0
        if taxable_amount > 5000000 and taxable_amount <= 10000000:
            surchargen = taxo * .10
            # /* check Marginal Relif*/
            if taxable_amount > 5000000 and taxable_amount <= 5195896:
                surchargen = (taxable_amount - 5000000) * .70
                surchargen = surchargen + 0
                marginaln = "Yes"

        elif taxable_amount > 10000000 and taxable_amount <= 20000000:
            surchargen = taxo * .15
            # /* check Marginal Relif*/
            if taxable_amount > 10000000 and taxable_amount <= 10214695:
                surchargen = (taxable_amount - 10000000) * .70
                surchargen = surchargen + 273750
                marginaln = "Yes"

        elif taxable_amount > 20000000 and taxable_amount <= 50000000:
            surchargen = taxo * .25
            # /* check Marginal Relif*/
            if taxable_amount > 20000000 and taxable_amount <= 20930000:
                surchargen = (taxable_amount - 20000000) * .70
                surchargen = surchargen + 860625
                marginaln = "Yes"

        elif taxable_amount > 50000000:
            surchargen = taxo * .25
            # /* check Marginal Relif*/
            if taxable_amount > 50000000 and taxable_amount <= 53017827:
                surchargen = (taxable_amount - 50000000) * .70
                surchargen = surchargen + 3684375
                marginaln = "Yes"
        cessn = 0
        tottaxo = 0
        total_taxo = 0
        total_cessn = 0
        total_surchargen = 0
        gratuity_from_previous_system = 0
        if taxo > 0:
            cessn = (taxo + surchargen) * .04
            total_cessn = cessn + ecess_prev_emp
            total_surchargen = surchargen + surcharge_prev_emp
            total_taxo = taxo - total_paid_tax + tax_prev_emp
            tottaxo = total_taxo + total_cessn + total_surchargen + gratuity_from_previous_system

        return tottaxo, total_taxo, total_cessn, total_surchargen, gratuity_from_previous_system

    def it_calculation(self, categories, payslip):
        std_dedc = 50000
        remaining_months = self.get_remaining_months(payslip)
        dic = {'BASIC': 'BASIC', 'HRA': 'HRA'}
        dicti = self.house_rent_exemption(dic, payslip)
        totalbasic = dicti.get('BASIC') + categories.BASIC
        totalhra = dicti.get('HRA') + categories.HRA
        rent_paid = dicti.get('PAID_RENT')
        formula = []
        formula_1 = totalhra
        formula_2 = totalbasic * 0.5
        formula_3 = rent_paid - (0.1 * totalbasic)
        formula_3 = 0 if formula_3 < 0 else formula_3
        formula.append(formula_1)
        formula.append(formula_2)
        formula.append(formula_3)
        hra_exempted_amount = min(formula)

        declaration = self.get_it_declaration_info(payslip)
        regime = declaration.get('regime')
        gratuity_from_previous_system = declaration.get('gratuity_from_previous_system')
        tax_prev_emp = declaration.get('tax_on_income')
        surcharge_prev_emp = declaration.get('surcharge')
        ecess_prev_emp = declaration.get('ecess')
        total_paid_tax = self.cummulative_tax()

        pt = 0
        if declaration.get('previous_employer_professional_tax') != 0:
            pt += declaration.get('previous_employer_professional_tax')
            if self.join_date.month >= 4:
                pt += (16 - self.join_date.month) * 200
            else:
                pt += (4 - self.join_date.month) * 200
        else:
            pt = 2400

        if regime == 'old_regime':
            taxable_amount = (self.cummulative_details(
                payslip) + categories.BASIC + categories.HRA + categories.Other + categories.BONUS + categories.COMP - hra_exempted_amount - std_dedc - declaration.get(
                '80c') - declaration.get('80ccd') - declaration.get('80d') - declaration.get(
                '80other') + declaration.get('income_lose_house_property') + declaration.get(
                'other_income') + declaration.get('income_previous_employer') - pt)
            old_regime_tax = self.old_regime_calculation(taxable_amount, ecess_prev_emp, surcharge_prev_emp,
                                                         tax_prev_emp, gratuity_from_previous_system, total_paid_tax)
            tottaxo = old_regime_tax[0]
        else:
            taxable_amount = self.cummulative_details(
                payslip) + categories.BASIC + categories.HRA + categories.Other + categories.BONUS + categories.COMP - std_dedc - pt
            old_regime_tax = self.new_regime_calculation(taxable_amount, ecess_prev_emp, surcharge_prev_emp,
                                                         tax_prev_emp, gratuity_from_previous_system, total_paid_tax)
            tottaxo = old_regime_tax[0]

        return round(tottaxo / remaining_months)
