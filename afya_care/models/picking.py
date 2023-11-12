from odoo import fields, models,api,_
from odoo.exceptions import UserError
from datetime import datetime

class StockPicking(models.Model):
    _inherit = "stock.picking"

    approval_status = fields.Selection(
        [('draft', 'Draft'),
         ('pending', 'Pending'),
         ('approved', 'Approved'),
         ('rejected', 'Rejected')],
        string='Approval Status',
        default='draft',
    )
    approved_by = fields.Many2one("res.users",string="Approved By")
    is_created_by_user = fields.Boolean('IS Created by User',compute='_compute_is_created_by_user')
    is_user_in_approvedby = fields.Boolean('IS User in approved by',compute='_compute_is_user_in_approvedby')
    approved_time = fields.Datetime(string='Approved On')

    def _compute_is_created_by_user(self):
        for rec in self:
            user = self.env.user
            if user==rec.create_uid:
                rec.is_created_by_user = True
            else:
                rec.is_created_by_user = False

    def _compute_is_user_in_approvedby(self):
        for rec in self:
            user = self.env.user
            if user==rec.approved_by:
                rec.is_user_in_approvedby = True
            else:
                rec.is_user_in_approvedby = False

    def send_for_approval(self):
        for rec in self:
            rec.approval_status = 'pending'
            if rec.partner_id and rec.partner_id.supervisor:
                rec.approved_by = rec.partner_id.supervisor
                mail_template = rec.env.ref('afya_care.afyacare_transfer_approval_template')
                if mail_template:
                    mail_template.write({'email_to': rec.approved_by.partner_id.email})
                    mail_template.send_mail(self.id,force_send = True)
                    rec.message_post(
                        body=f"Approval request has been sent to {rec.approved_by.name}."
                    )
            else:
                raise UserError('Can not find partner or supervisor')
    
    def button_approve(self):
        for rec in self:
            rec.approval_status = 'approved'
            rec.message_post(
                body=f"Transfer has been approved by {rec.approved_by.name}."
            )
            rec.approved_time = datetime.now()
            mail_template = rec.env.ref('afya_care.afyacare_transfer_approve_reject_template')
            if mail_template:
                mail_template.write({'email_to': rec.partner_id.email})
                mail_template.send_mail(self.id,force_send = True)
                

    def button_reject(self):
        for rec in self:
            rec.approval_status = 'rejected'
            rec.message_post(
                body=f"Transfer has been rejected by {rec.approved_by.name}."
            )
            mail_template = rec.env.ref('afya_care.afyacare_transfer_approve_reject_template')
            if mail_template:
                mail_template.write({'email_to': rec.partner_id.email})
                mail_template.send_mail(self.id,force_send = True)
                