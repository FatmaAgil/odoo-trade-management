from odoo import models, fields
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    # -------------------------
    # Day 15
    # -------------------------

    sale_order_reference = fields.Char(
        string="Sales Order Reference",
        compute="_compute_sale_reference"
    )

    # -------------------------
    # Day 16
    # -------------------------

    approval_note = fields.Text(
        string="Approval Note",
        help="Internal finance or approval remarks"
    )

    def _compute_sale_reference(self):
        for move in self:

            sale_orders = move.invoice_line_ids.mapped(
                'sale_line_ids.order_id'
            )

            move.sale_order_reference = ", ".join(
                sale_orders.mapped('name')
            )

    # -------------------------
    # Day 17 Validation
    # -------------------------

    def action_post(self):

        for move in self:

            if move.move_type == 'out_invoice' and not move.approval_note:

                raise ValidationError(
                    "Approval Note is required before posting the invoice."
                )

        return super().action_post()