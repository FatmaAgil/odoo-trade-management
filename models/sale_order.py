from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trade_notes = fields.Text(
        string='Trade Notes',
        help='Internal notes for trade management'
    )

    priority = fields.Selection(
        [
            ('0', 'Low'),
            ('1', 'Medium'),
            ('2', 'High')
        ],
        string="Priority",
        default='1'
    )

    internal_note = fields.Text(
        string="Internal Note"
    )

    def action_confirm(self):
        for order in self:
            partner = order.partner_id

            # 🚫 Rule 1: Blocked customer
            if partner.is_blocked:
                raise ValidationError(
                    f"Customer {partner.name} is blocked. Cannot confirm this order."
                )

            # 🚫 Rule 2: Credit limit check
            if partner.credit_limit and order.amount_total > partner.credit_limit:
                raise ValidationError(
                    f"Customer {partner.name} exceeded credit limit.\n"
                    f"Limit: {partner.credit_limit}, Order: {order.amount_total}"
                )

        # ✅ If all checks pass → proceed normally
        return super(SaleOrder, self).action_confirm()