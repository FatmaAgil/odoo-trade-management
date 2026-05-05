from odoo import models, fields
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # -------------------------
    # Day 11: Delivery Validation
    # -------------------------

    def button_validate(self):
        for picking in self:

            _logger.info(f"🔍 Validating picking: {picking.name}")

            if picking.picking_type_code == 'outgoing':

                # ❌ No products
                if not picking.move_ids:
                    raise ValidationError(
                        "You cannot validate a delivery with no products."
                    )

                # ✅ Check done quantities safely
                move_lines = picking.move_ids.mapped('move_line_ids')

                has_done_qty = any(
                    line.qty_done > 0 for line in move_lines
                )

                if not has_done_qty:
                    raise ValidationError(
                        "You cannot validate a delivery with zero done quantities."
                    )

        return super().button_validate()

    # -------------------------
    # Day 12: Automation (Late Delivery Notification)
    # -------------------------

    def write(self, vals):
        _logger.info("🔥 WRITE TRIGGERED ON STOCK PICKING")

        res = super().write(vals)

        for picking in self:
            _logger.info(f"➡️ Checking picking: {picking.name}")

            # 🔗 Try direct link first
            sale_order = picking.sale_id

            # 🔁 Fallback using origin (more reliable)
            if not sale_order and picking.origin:
                sale_order = self.env['sale.order'].search([
                    ('name', '=', picking.origin)
                ], limit=1)

            if not sale_order:
                _logger.info("❌ No related sale order found")
                continue

            _logger.info(f"✅ Linked Sale Order: {sale_order.name}")

            # 🚨 Late delivery condition
            if (
                picking.scheduled_date
                and picking.scheduled_date < fields.Datetime.now()
                and picking.state != 'done'
            ):
                _logger.info("🚨 LATE DELIVERY DETECTED")

                # 🚫 Prevent duplicate messages
                already_posted = any(
                    picking.name in (msg.body or '')
                    for msg in sale_order.message_ids
                )

                if not already_posted:
                    sale_order.message_post(
                        body=f"⚠️ Delivery {picking.name} is late."
                    )

        return res