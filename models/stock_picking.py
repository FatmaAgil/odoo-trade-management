from odoo import models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:

            if picking.picking_type_code == 'outgoing':

                # ❌ No moves at all
                if not picking.move_ids:
                    raise ValidationError(
                        "You cannot validate a delivery with no products."
                    )

                # ✅ Always go through moves → move lines (SAFE)
                move_lines = picking.move_ids.mapped('move_line_ids')

                has_done_qty = any(
                    line.qty_done > 0 for line in move_lines
                )

                if not has_done_qty:
                    raise ValidationError(
                        "You cannot validate a delivery with zero done quantities."
                    )

        return super().button_validate()