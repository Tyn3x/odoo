from odoo import models, fields, api

class InheretedUsers(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many("estate.property", inverse_name="salesperson", domain=['|',('state','=','0'), ('state','=','1')], string="Properties")