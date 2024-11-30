from odoo import models, fields


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    location_id = fields.Many2one('afyacare.location', string="Location")
    asset_tag_id = fields.Many2one('afyacare.asset.tag', string="Asset Tag")
    asset_condition_id = fields.Many2one('afyacare.asset.condition', string="Asset Condition")
    asset_user_id = fields.Many2one('afyacare.asset.user', string="Asset User")
    serial_number_id = fields.Many2one('afyacare.serial.number', string="Serial Number")
    afy_salvage_value = fields.Float(string="Salvage Value")
    afy_remaining_active_life = fields.Float(string="Remaining Active Life (Year)")



