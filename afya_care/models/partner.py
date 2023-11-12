from odoo import fields, models,api,_
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    supervisor = fields.Many2one("res.users",string="Supervisor")