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
    afy_monthly_depreciation_value = fields.Float(string="Monthly Depreciation Value")

    @api.depends('method_number', 'prorata_date', 'method_period')
    def _compute_depreciation_end_date(self):
        for asset in self:
            if asset.prorata_date and asset.method_number:
                duration_months = asset.method_number * int(asset.method_period)
                asset.depreciation_end_date = asset.prorata_date + relativedelta(months=duration_months)
            else:
                asset.depreciation_end_date = False

    def compute_depreciation_board(self, date=False):
        self.ensure_one()

        # Need to unlink draft move before adding new one because if we create new move before, it will cause an error
        # in the compute for the depreciable/cumulative value
        self.depreciation_move_ids.filtered(lambda mv: mv.state == 'draft' and (mv.date >= date if date else True)).unlink()
        new_depreciation_moves_data = self._recompute_board(date)
        new_depreciation_moves = self.env['account.move'].create(new_depreciation_moves_data)
        # Added code for Monthly Depreciation Value Calculate
        self.afy_monthly_depreciation_value = (
            new_depreciation_moves[1].amount_total
            if len(new_depreciation_moves) > 1
            else (new_depreciation_moves[0].amount_total if new_depreciation_moves else 0.0)
        )
        if self.state == 'open':
            # In case of the asset is in running mode, we post in the past and set to auto post move in the future
            new_depreciation_moves._post()
        return True
