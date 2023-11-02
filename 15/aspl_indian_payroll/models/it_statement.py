# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import calendar
import fiscalyear
from odoo import models, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.http import request


class HrEmoloyee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def get_user_employee_details_payslip(self):
        uid = request.session.uid
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', uid)], limit=1)

        if employee:
            # ********************* YTD SUMMARY IT STATEMENT TABLE ********************* #
            ytd_summary_it_statement_data = {}
            fiscalyear.START_MONTH = 4
            currentfiscalstart = fiscalyear.FiscalYear(
                datetime.now().year).start.date() if datetime.now().month < 4 else fiscalyear.FiscalYear(
                datetime.now().year + 1).start.date()
            currentfiscalend = fiscalyear.FiscalYear(
                datetime.now().year).end.date() if datetime.now().month < 4 else fiscalyear.FiscalYear(
                datetime.now().year + 1).end.date()
            fetch_details = self.env['hr.payslip'].search(
                [('employee_id', '=', employee.id), ('date_from', '>=', currentfiscalstart),
                 ('date_to', '<=', currentfiscalend)])
            for details in fetch_details:
                for line in details.line_ids:
                    if "Newid" in str(line.id):
                        pass
                    else:
                        if line.salary_rule_id.taxable or line.salary_rule_id.is_deduction:
                            a = 'Income' if line.salary_rule_id.taxable else 'Deduction'
                            if ytd_summary_it_statement_data.get(a):
                                if ytd_summary_it_statement_data.get(a).get(line.salary_rule_id.name):
                                    if ytd_summary_it_statement_data.get(a).get(line.salary_rule_id.name).get(
                                            details.date_from.month):
                                        pass
                                    else:
                                        ytd_summary_it_statement_data.get(a).get(line.salary_rule_id.name)[
                                            details.date_from.month] = line.amount
                                else:
                                    ytd_summary_it_statement_data.get(a)[line.salary_rule_id.name] = {
                                        details.date_from.month: line.amount}
                            else:
                                ytd_summary_it_statement_data[a] = {
                                    line.salary_rule_id.name: {details.date_from.month: line.amount}}

            last_day = calendar.monthrange(date.today().year, date.today().month)[1]
            last_full_date = date(date.today().year, date.today().month, last_day)
            current_date = last_full_date
            enddate = date(currentfiscalend.year, currentfiscalend.month, currentfiscalend.day)
            if enddate > current_date:
                remaining_months = relativedelta(enddate, current_date).months
            else:
                remaining_months = 0

            fetch_details_projected = self.env['hr.contract'].search(
                [('employee_id', '=', employee.id), ('state', '=', 'open')])
            counter_month = datetime.now().month
            counter_year = datetime.now().year
            if fetch_details_projected:
                if (datetime.strptime(f'{counter_year}-{counter_month}', "%Y-%m") > datetime.strptime(
                        f'{fetch_details_projected.date_end.year}-{fetch_details_projected.date_end.month}', "%Y-%m")):
                    if self.env['hr.contract'].search([('employee_id', '=', employee.id), ('state', '=', 'draft')]):
                        fetch_details_projected = self.env['hr.contract'].search(
                            [('employee_id', '=', employee.id), ('state', '=', 'draft')])
            for i in range(0, remaining_months + 1):
                for projected_details in fetch_details_projected:
                    for line in projected_details.applicable_salary_rule_ids:
                        if line.rule_id.taxable or line.rule_id.is_deduction:
                            a = 'Income' if line.rule_id.taxable else 'Deduction'
                            if ytd_summary_it_statement_data.get(a):
                                if ytd_summary_it_statement_data.get(a).get(line.rule_id.name):
                                    if ytd_summary_it_statement_data.get(a).get(line.rule_id.name).get(counter_month):
                                        pass
                                    else:
                                        ytd_summary_it_statement_data.get(a).get(line.rule_id.name)[
                                            counter_month] = line.amount
                                else:
                                    ytd_summary_it_statement_data.get(a)[line.rule_id.name] = {counter_month: line.amount}
                            else:
                                ytd_summary_it_statement_data[a] = {line.rule_id.name: {counter_month: line.amount}}
                if (datetime.now().month == 12 or counter_month == 12):
                    counter_month = 1
                    counter_year += 1
                else:
                    counter_month += 1

            month_counter = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
            for i in ytd_summary_it_statement_data:
                for j, k in ytd_summary_it_statement_data[i].items():
                    for mc in month_counter:
                        if mc not in k:
                            k[mc] = 0
                    sorted_items = []
                    for key in range(4, 13):
                        if key in k:
                            sorted_items.append((key, k[key]))
                    for key in range(1, 4):
                        if key in k:
                            sorted_items.append((key, k[key]))
                    sorted_dict = dict(sorted_items)
                    ytd_summary_it_statement_data[i][j] = sorted_dict

            total_of_months = 0
            for i in ytd_summary_it_statement_data:
                for j in ytd_summary_it_statement_data[i]:
                    items = list(ytd_summary_it_statement_data[i][j].items())
                    for key, value in ytd_summary_it_statement_data[i][j].items():
                        total_of_months += value
                    items.insert(0, ('Total', total_of_months))
                    total_of_months = 0
                    ytd_summary_it_statement_data[i][j] = dict(items)

            for i in ytd_summary_it_statement_data:
                temp_dict = {}
                for j in ytd_summary_it_statement_data[i]:
                    for key, value in ytd_summary_it_statement_data[i][j].items():
                        if temp_dict.get('Total'):
                            if temp_dict.get('Total').get(key):
                                temp_dict['Total'][key] += value
                            else:
                                temp_dict.get('Total')[key] = value
                        else:
                            temp_dict['Total'] = {key: value}
                ytd_summary_it_statement_data.get(i).update(temp_dict)

            if ytd_summary_it_statement_data:
                # Tax Calculation
                taxable_amount = ytd_summary_it_statement_data['Income']['Total']['Total']
                it_declaration_info = employee.get_it_statement_info(current_date)
                it_components = it_declaration_info[0]

                ytd_summary_it_deduction_component_last_employer = {}
                ytd_summary_it_deduction_component_last_employer['Total Income After Exemptions'] = it_declaration_info[
                    1].income_after_exemptions
                ytd_summary_it_deduction_component_last_employer['Professional Tax'] = it_declaration_info[1].professional_tax
                ytd_summary_it_deduction_component_last_employer['Provident Fund'] = it_declaration_info[1].provident_fund
                ytd_summary_it_deduction_component_last_employer['Total Tax'] = it_declaration_info[
                    1].total_tax_previous_employer

                totalbasic = ytd_summary_it_statement_data['Income']['Basic Salary']['Total']
                totalhra = ytd_summary_it_statement_data['Income']['House Rent Allowance']['Total']
                rent_paid = it_components['house_rent']
                formula = []
                formula_1 = totalhra
                formula_2 = totalbasic * 0.5
                formula_3 = rent_paid - (0.1 * totalbasic)
                formula_3 = 0 if formula_3 < 0 else formula_3
                formula.append(formula_1)
                formula.append(formula_2)
                formula.append(formula_3)
                hra_exempted_amount = min(formula)

                gratuity_from_previous_system = it_components.get('gratuity_from_previous_system')
                tax_prev_emp = it_components.get('tax_on_income')
                surcharge_prev_emp = it_components.get('surcharge')
                ecess_prev_emp = it_components.get('ecess')
                total_paid_tax = employee.cummulative_tax()

                pt = 0
                if it_components.get('previous_employer_professional_tax') != 0:
                    pt += it_components.get('previous_employer_professional_tax')
                    if employee.join_date.month >= 4:
                        pt += (16 - employee.join_date.month) * 200
                    else:
                        pt += (4 - employee.join_date.month) * 200
                else:
                    pt = 2400
                standard_deduction = 50000

                ytd_summary_it_deduction_components = {}
                ytd_summary_it_deduction_components = {'HRA Exempted Amount': hra_exempted_amount, 'Professional Tax': pt, 'Standard Deduction': standard_deduction, '80c': it_components['80c'], '80ccd': it_components['80ccd'], '80d': it_components['80d'], '80other': it_components['80other']}

                ytd_summary_it_income_components = {'Other Income': it_components['other_income'], 'Income Lose House Property': it_components['income_lose_house_property']}

                # ===================================== OLD REGIME =====================================
                for key, values in ytd_summary_it_deduction_components.items():
                    taxable_amount -= values
                for key, values in ytd_summary_it_income_components.items():
                    taxable_amount += values
                taxable_amount += ytd_summary_it_deduction_component_last_employer['Total Income After Exemptions']

                old_regime_tax = employee.old_regime_calculation(taxable_amount, ecess_prev_emp, surcharge_prev_emp, tax_prev_emp, gratuity_from_previous_system, total_paid_tax)
                taxo_old_regime = old_regime_tax[1]
                surchargeo_old_regime = old_regime_tax[3]
                cesso_old_regime = old_regime_tax[2]
                grayhr_old_regime = old_regime_tax[4]
                tottaxo_old_regime = old_regime_tax[0]

                # ===================================== NEW REGIME =====================================
                taxable_amount_new_regime = ytd_summary_it_statement_data['Income']['Total']['Total']
                for key, values in ytd_summary_it_income_components.items():
                    taxable_amount_new_regime += values
                taxable_amount_new_regime += ytd_summary_it_deduction_component_last_employer['Total Income After Exemptions']
                taxable_amount_new_regime -= standard_deduction
                taxable_amount_new_regime -= pt

                new_regime_tax = employee.new_regime_calculation(taxable_amount_new_regime, ecess_prev_emp, surcharge_prev_emp, tax_prev_emp, gratuity_from_previous_system, total_paid_tax)
                taxo_new_regime = new_regime_tax[1]
                surchargen_new_regime = new_regime_tax[3]
                cessn_new_regime = new_regime_tax[2]
                grayhr_new_regime = new_regime_tax[4]
                tottaxo_new_regime = new_regime_tax[0]

                if taxable_amount < 0:
                    taxable_amount = 0
                if taxable_amount_new_regime < 0:
                    taxable_amount_new_regime = 0
                tax_amount_old_regime_dict = {'Raw Tax': "{:.2f}".format(taxo_old_regime), 'Surcharge': "{:.2f}".format(surchargeo_old_regime),
                                              'Health & Edu.Cess': "{:.2f}".format(cesso_old_regime),
                                              'Accumulated Gratuity(From previous system)': "{:.2f}".format(grayhr_old_regime),
                                              'Total Tax Amount': "{:.2f}".format(tottaxo_old_regime)}
                tax_amount_new_regime_dict = {'Raw Tax': "{:.2f}".format(taxo_new_regime),
                                              'Surcharge': "{:.2f}".format(surchargen_new_regime),
                                              'Health & Edu.Cess': "{:.2f}".format(cessn_new_regime),
                                              'Accumulated Gratuity(From previous system)': "{:.2f}".format(grayhr_new_regime),
                                              'Total Tax Amount': "{:.2f}".format(tottaxo_new_regime)}

                data = {
                    'current_financial_year': it_declaration_info[1].financial_year.name,
                    'ytd_summary_it_statement_data': ytd_summary_it_statement_data,
                    'ytd_summary_it_income_components': ytd_summary_it_income_components,
                    'ytd_summary_it_deduction_component_last_employer': ytd_summary_it_deduction_component_last_employer,
                    'ytd_summary_it_deduction_components': ytd_summary_it_deduction_components,
                    'tax_amount_old_regime_dict': tax_amount_old_regime_dict,
                    'tax_amount_new_regime_dict': tax_amount_new_regime_dict,
                }
                return data
            else:
                return "Employee Payslip or It Declaration Not Found..."
        else:
            return "Employee Not Found..."
