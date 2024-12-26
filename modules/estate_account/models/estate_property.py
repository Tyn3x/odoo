import logging
from odoo import models, fields, api
from odoo import Command

from odoo.fields import float_is_zero, float_compare
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class InheritedProperty(models.Model):
    _inherit = "estate.property"
    
    def action_sold_property(self):
        _logger.info("Entro")
        
        fees = 100
        
        for prop in self:
            if not prop.buyer:
                raise ValidationError("The property must have a client before selling it")
        extra = prop.selling_price * 0.06
        move_value = {
            'move_type': 'out_invoice',
            'partner_id': prop.buyer.id,
            'invoice_line_ids': [
                Command.create({
                    'name': prop.name,
                    'quantity': 1,
                    'price_unit': extra,
                }),
                Command.create({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': fees,
                }),
            ],
        }
        self.env['account.move'].create(move_value)
        
        return super().action_sold_property()