from odoo import models, fields
from io import BytesIO
import xlsxwriter
from datetime import date
import base64
from calendar import monthrange

class AssetRegisterReport(models.TransientModel):
    _name = 'report.account.asset.register'
    _description = 'Asset Register Report'

    date_to = fields.Date(string='End Date', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    def action_generate_report(self):
        assets = self.env['account.asset'].search([
            ('company_id', '=', self.company_id.id),
            ('acquisition_date', '<=', self.date_to)
        ])

        headers = [
            'Asset Original Cost Account', 'Depreciation Expense Account', 'Accum Depreciation Account',
            'Label', 'Reporting Date', 'Original cost', 'Accum Depreciation as at end of last financial year',
            'Current depreciation', 'Closing NBV', 'Status', 'Disposal value', 'Dep Start',
            'Dep End', 'Total Months', 'Location'
        ]

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet("Asset Register")
        bold = workbook.add_format({'bold': True})

        for col, header in enumerate(headers):
            sheet.write(0, col, header, bold)

        prev_year = self.date_to.year - 1
        prev_year_end = date(prev_year, 12, 31)
        
        last_day_of_month = monthrange(self.date_to.year, self.date_to.month)[1]
        is_last_date_of_month = self.date_to.day == last_day_of_month

        if is_last_date_of_month:
            curr_year_end = self.date_to
        else:
            prev_month = self.date_to.month - 1
            if prev_month == 0:
                prev_month = 1
            last_day = monthrange(self.date_to.year, prev_month)[1]
            curr_year_end = date(self.date_to.year, prev_month, last_day)

        for row, asset in enumerate(assets, start=1):
            asset_acc = asset.original_move_line_ids[:1].account_id.name if asset.original_move_line_ids else ''
            depr_lines = asset.depreciation_move_ids.filtered(lambda d: d.date)
            depr_prev_year = sum(depr_lines.filtered(lambda d: d.date == prev_year_end).mapped('asset_depreciated_value'))
            closing_nbv = sum(depr_lines.filtered(lambda d: d.date == curr_year_end).mapped('asset_depreciated_value'))
            current_depr = closing_nbv - depr_prev_year
            closing_nbv = sum(depr_lines.filtered(lambda d: d.date == curr_year_end).mapped('asset_depreciated_value'))
            total_months = asset.method_number * (12 if asset.method_period == 'year' else 1)

            values = [
                asset_acc,
                asset.account_depreciation_expense_id.code,
                asset.account_depreciation_id.code,
                asset.name,
                asset.acquisition_date.strftime('%d/%m/%Y') if asset.acquisition_date else '',
                asset.original_value,
                depr_prev_year,
                current_depr,
                closing_nbv,
                asset.state,
                asset.afy_disposal_date.strftime('%d/%m/%Y') if asset.afy_disposal_date else '',
                asset.prorata_date.strftime('%d/%m/%Y') if asset.prorata_date else '',
                asset.depreciation_end_date.strftime('%d/%m/%Y') if asset.depreciation_end_date else '',
                total_months,
                asset.location_id.name or '',
            ]

            for col, val in enumerate(values):
                sheet.write(row, col, val or '')

        workbook.close()
        output.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': 'Asset Register Report.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }