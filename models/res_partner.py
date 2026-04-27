from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Selection(
        [
            ('regular', 'Regular'),
            ('vip', 'VIP'),
            ('blacklisted', 'Blacklisted')
        ],
        string="Customer Type",
        default='regular'
    )

    credit_limit = fields.Float(
        string="Credit Limit"
    )

    is_blocked = fields.Boolean(
        string="Blocked"
    )