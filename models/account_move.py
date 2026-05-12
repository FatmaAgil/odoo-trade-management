from odoo import models, fields
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


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

    # -------------------------
    # Day 20 Integration
    # -------------------------

    integration_status = fields.Selection(
        [
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('failed', 'Failed')
        ],
        string="Integration Status",
        default='pending'
    )

    # -------------------------
    # Compute Sales Reference
    # -------------------------

    def _compute_sale_reference(self):
        for move in self:

            sale_orders = move.invoice_line_ids.mapped(
                'sale_line_ids.order_id'
            )

            move.sale_order_reference = ", ".join(
                sale_orders.mapped('name')
            )

    # -------------------------
    # Day 20 API Simulation
    # -------------------------

    def simulate_external_api(self):

        for move in self:

            try:

                payload = {
                    'invoice': move.name,
                    'customer': move.partner_id.name,
                    'amount': move.amount_total,
                    'date': str(move.invoice_date),
                }

                # Simulated API log
                _logger.warning(
                    "SIMULATED API CALL -> %s",
                    payload
                )

                move.integration_status = 'sent'

                move.message_post(
                    body=(
                        f"✅ Invoice sent to external system.\n"
                        f"Customer: {move.partner_id.name}\n"
                        f"Amount: {move.amount_total}"
                    )
                )

            except Exception as e:

                move.integration_status = 'failed'

                _logger.error(
                    "API INTEGRATION FAILED -> %s",
                    str(e)
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

        result = super().action_post()

        # -------------------------
        # Day 20 Trigger Integration
        # -------------------------

        self.simulate_external_api()

        return result