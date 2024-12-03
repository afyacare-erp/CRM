from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    location_id = fields.Many2one('afyacare.location', string="Location")
    asset_tag_id = fields.Many2one('afyacare.asset.tag', string="Asset Tag")
    asset_condition_id = fields.Many2one('afyacare.asset.condition', string="Asset Condition")
    asset_user_id = fields.Many2one('afyacare.asset.user', string="Asset User")
    serial_number_id = fields.Many2one('afyacare.serial.number', string="Serial Number")
    afy_salvage_value = fields.Float(string="Salvage Value")
    afy_remaining_active_life = fields.Float(string="Remaining Active Life (Year)")
    depreciation_end_date = fields.Date(
        string="Depreciation End Date",
        compute="_compute_depreciation_end_date",
        store=True,
        help="The date on which the asset's depreciation will end.",
    )

    @api.depends('method_number', 'prorata_date', 'method_period')
    def _compute_depreciation_end_date(self):
        for asset in self:
            if asset.prorata_date and asset.method_number:
                duration_months = asset.method_number * int(asset.method_period)
                asset.depreciation_end_date = asset.prorata_date + relativedelta(months=duration_months)
            else:
                asset.depreciation_end_date = False
