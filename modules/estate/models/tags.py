from odoo import models, fields, api

class Tags(models.Model):
    _name = "estate.tags"
    _description ="estate.tags"
    _order = "name"
    
    name = fields.Char(string="Tags", required=True)
    color = fields.Integer(string="Color Picker")
    
    _sql_constraints = [
        (
            "unique_tag_name",
            "unique(name)",
            "Tag name must be unique"
        )
    ]