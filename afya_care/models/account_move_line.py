from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    payment_reference = fields.Char(string='Payment Reference', related='move_id.payment_reference', store=True)
