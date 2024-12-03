from odoo import models, fields, api


class Location(models.Model):
    _name = 'afyacare.location'
    _description = 'Location'
    _rec_name = 'name'

    name = fields.Char(string="Location Name", required=True)
    location_no = fields.Char(string="Location No", required=True)
    active = fields.Boolean(string="Active", default=True)


class AssetTag(models.Model):
    _name = 'afyacare.asset.tag'
    _description = 'Asset Tag'
    _rec_name = 'name'

    name = fields.Char(string="Tag Name", required=True)
    active = fields.Boolean(string="Active", default=True)


class AssetCondition(models.Model):
    _name = 'afyacare.asset.condition'
    _description = 'Asset Condition'
    _rec_name = 'name'

    name = fields.Char(string="Condition Name", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)


class AssetUser(models.Model):
    _name = 'afyacare.asset.user'
    _description = 'Asset User'
    _rec_name = 'name'

    name = fields.Char(string="User Name", required=True)
    department = fields.Char(string="Department")
    active = fields.Boolean(string="Active", default=True)


class SerialNumber(models.Model):
    _name = 'afyacare.serial.number'
    _description = 'Serial Number'
    _rec_name = 'number'

    number = fields.Char(string="Serial Number", required=True)
    active = fields.Boolean(string="Active", default=True)


