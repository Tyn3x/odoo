# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

from odoo.fields import float_is_zero, float_compare
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class estate_property(models.Model):
    _name = 'estate.property'
    _description = 'estate.property'
    _order = "id desc"
    
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.add(fields.Date.today(), days=90))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection([('0', 'North'),('1', 'South'),('2', 'East'),('3', 'West')], string="Garden orientation")
    state = fields.Selection([('0','New'),('1','Offer Received'),('2','Offer Accepted'),('3','Sold'),('4','Cancelled')], string="Status", required=True, default='0')
    active = fields.Boolean(string="Active", default=True)
    
    """Many2one fields"""
    
    property_type_id = fields.Many2one("estate.type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    
    """Many2many"""
    
    tag_ids = fields.Many2many("estate.tags", string="Property Tag")
    
    """One2many"""
    
    offer_ids = fields.One2many("estate.offer", "property_id", string="Offer")
    
    """Computed Fields"""
    
    total_area = fields.Float(compute="_compute_total_area", string="Total Area(sqm)", readonly=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer", readonly=True)
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0
                
    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = '0'               
        else:
            self.garden_area = False
            self.garden_orientation = False 
            
    """Button actions"""
    def action_sold_property(self):
        for record in self:
            if record.state  != "4":
                record.state = "3"
            else:
                raise UserError("Cancelled properties cannot be Sold")
        return True
            
            
    def action_cancel_property(self):
        for record in self:
            if record.state  != "3":
                record.state = "4"
            else:
                raise UserError("Sold properties cannot be Cancelled")
        return True
    
    """Constrains"""
    
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be stricly positive"
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The Selling Price must be positive"
        ),
    ]
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            
            min_price = record.expected_price * 0.9
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_new_or_cancelled(self):
        for record in self:
            if record.state not in['0', '4']:
                raise UserError("Only New and Cancelled properties can be deleted")        