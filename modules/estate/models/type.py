from odoo import models, fields, api

class Type(models.Model):
    _name = "estate.type"
    _description = "estate.type"
    _order = "sequence, name"
    
    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.offer", "property_type_id")
    
    offer_count = fields.Integer(compute="_compute_offer_count")
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    _sql_constraints = [
        (
            "unique_type_name",
            "unique(name)",
            "Type name must be unique"
        )
    ]