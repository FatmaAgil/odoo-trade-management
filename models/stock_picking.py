from odoo import models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):

        for picking in self:

            # Only outgoing deliveries
            if picking.picking_type_code == 'outgoing':

                # No products
                if not picking.move_ids:
                    raise ValidationError(
                        "You cannot validate a delivery with no products."
                    )

                # Get all move lines
                move_lines = picking.move_ids.mapped('move_line_ids')

                # Odoo 18 uses quantity
                has_done_qty = any(
                    line.quantity > 0
                    for line in move_lines
                )

                # Block empty deliveries
                if not has_done_qty:
                    raise ValidationError(
                        "You cannot validate a delivery with zero quantities."
                    )

        return super().button_validate()