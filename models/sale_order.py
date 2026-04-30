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
    # Warehouse (DAY 12 NEW)
    # -------------------------

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string="Warehouse",
        default=lambda self: self.env['stock.warehouse'].search([], limit=1),
        help="Warehouse responsible for fulfilling this order"
    )

    # -------------------------
    # Smart Button (Invoices - Day 5)
    # -------------------------

    invoice_count = fields.Integer(
        string="Invoices",
        compute="_compute_invoice_count"
    )

    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)

    # -------------------------
    # Delivery Insights (Day 9)
    # -------------------------

    delivery_status = fields.Selection(
        [
            ('no', 'Nothing to Deliver'),
            ('pending', 'Waiting'),
            ('partial', 'Partially Delivered'),
            ('done', 'Fully Delivered')
        ],
        string="Delivery Status",
        compute="_compute_delivery_status"
    )

    is_late_delivery = fields.Boolean(
        string="Late Delivery",
        compute="_compute_delivery_status"
    )

    def _compute_delivery_status(self):
        for order in self:
            pickings = order.picking_ids.filtered(lambda p: p.state != 'cancel')

            if not pickings:
                order.delivery_status = 'no'
                order.is_late_delivery = False
                continue

            if all(p.state == 'done' for p in pickings):
                order.delivery_status = 'done'
            elif any(p.state == 'done' for p in pickings):
                order.delivery_status = 'partial'
            else:
                order.delivery_status = 'pending'

            order.is_late_delivery = any(
                p.scheduled_date and p.scheduled_date < fields.Datetime.now()
                and p.state != 'done'
                for p in pickings
            )

    # -------------------------
    # Business Logic (Day 4)
    # -------------------------

    def action_confirm(self):
        for order in self:
            partner = order.partner_id

            if partner.is_blocked:
                raise ValidationError(
                    f"Customer '{partner.name}' is blocked. Cannot confirm this order."
                )

            if partner.credit_limit and order.amount_total > partner.credit_limit:
                raise ValidationError(
                    f"Customer '{partner.name}' exceeded credit limit.\n"
                    f"Limit: {partner.credit_limit}, Order: {order.amount_total}"
                )

        return super().action_confirm()