import logging
from odoo import models, fields, api

from datetime import timedelta, datetime, date

from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)
class Offer(models.Model):
    _name = "estate.offer"
    _description = "estate.offer"
    _order = "price desc"
    
    price = fields.Float(string="Price")
    status = fields.Selection([('0','Accepted'), ('1','Refuse')], string="Status")
    
    """One2many fields"""
    
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    
    """Computed/Inverse Fields"""
    
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline", default=date.today())
    validity = fields.Integer(string="Validity(days)", default=7)
    
    """Related Fields"""
    
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    
    @api.depends("date_deadline", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline -record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - date.today()).days
                
    """button actions"""
    
    def action_accept_offer(self):
        for record in self:
            if record.status != '0':
                record.status = '0'
                
                record.property_id.write({
                    'selling_price': record.price,
                    'buyer': record.partner_id.id,
                    'state': '2',
                })
            
        return True    
            
    def action_refuse_offer(self):
        for record in self:
            record.status = '1'
            record.property_id.write({
                'selling_price': 0.0,
                'buyer': False,
            })
        return True
    
    @api.model_create_multi
    def create(self, vals):
        
        property_obj = self.env['estate.property'].browse(vals[0]['property_id'])

        existing_offer = self.search([
            ('property_id', '=', vals[0]['property_id']),
            ('price', '>=', vals[0]['price'])
        ])
        if existing_offer:
            raise UserError("Cant create an offer with a lower amount than an existing offer.")

        property_obj.write({'state': '1'})

        return super().create(vals)