from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # -------------------------
    # Custom Fields (Day 1 & 3)
    # -------------------------

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

    # -------------------------
    # Smart Button (Day 5)
    # -------------------------

    invoice_count = fields.Integer(
        string="Invoices",
        compute="_compute_invoice_count"
    )

    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)

    # -------------------------
    # Business Logic (Day 4)
    # -------------------------

    def action_confirm(self):
        for order in self:
            partner = order.partner_id

            # 🚫 Blocked Customer
            if partner.is_blocked:
                raise ValidationError(
                    f"Customer '{partner.name}' is blocked. Cannot confirm this order."
                )

            # 🚫 Credit Limit Check
            if partner.credit_limit and order.amount_total > partner.credit_limit:
                raise ValidationError(
                    f"Customer '{partner.name}' exceeded credit limit.\n"
                    f"Limit: {partner.credit_limit}, Order: {order.amount_total}"
                )

        return super(SaleOrder, self).action_confirm()