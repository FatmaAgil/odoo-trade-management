from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # -------------------------
    # Customer Segmentation
    # -------------------------

    customer_type = fields.Selection(
        [
            ('regular', 'Regular'),
            ('vip', 'VIP'),
            ('blacklisted', 'Blacklisted')
        ],
        string="Customer Type",
        default='regular'
    )

    # -------------------------
    # Credit Control
    # -------------------------

    credit_limit = fields.Float(
        string="Credit Limit"
    )

    is_blocked = fields.Boolean(
        string="Blocked"
    )