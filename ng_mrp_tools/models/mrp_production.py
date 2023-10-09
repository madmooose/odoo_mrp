# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.addons.mrp.models.mrp_production import MrpProduction

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    location_prod_id = fields.Many2one(
        'stock.location', 'Production Location',
        store=True, check_company=True,
        readonly=False,
        help="Location where the system will put things during production.")

    
    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        """ Warning, any changes done to this method will need to be repeated for consistency in:
            - Manually added components, i.e. "default_" values in view
            - Moves from a copied MO, i.e. move.create
            - Existing moves during backorder creation """

        data = super()._get_move_raw_values(product_id, product_uom_qty, product_uom, operation_id, bom_line)

        if bom_line and bom_line.is_tool:
            destination_location = self.location_prod_id
        else:
            destination_location = self.product_id.with_company(self.company_id).property_stock_production

        data['location_dest_id'] = destination_location.id
        return data


def _get_move_finished_values(self, product_id, product_uom_qty, product_uom, operation_id=False, byproduct_id=False, cost_share=0,is_tool=False):
    group_orders = self.procurement_group_id.mrp_production_ids
    move_dest_ids = self.move_dest_ids
    if len(group_orders) > 1:
        move_dest_ids |= group_orders[0].move_finished_ids.filtered(lambda m: m.product_id == self.product_id).move_dest_ids
    if is_tool:
        location = self.location_prod_id
    else:
        location = self.product_id.with_company(self.company_id).property_stock_production

    return {
        'product_id': product_id,
        'product_uom_qty': product_uom_qty,
        'product_uom': product_uom,
        'operation_id': operation_id,
        'byproduct_id': byproduct_id,
        'name': _('New'),
        'date': self._get_date_planned_finished(),
        'date_deadline': self.date_deadline,
        'picking_type_id': self.picking_type_id.id,
        'location_id': location.id,
        'location_dest_id': self.location_dest_id.id,
        'company_id': self.company_id.id,
        'production_id': self.id,
        'warehouse_id': self.location_dest_id.warehouse_id.id,
        'origin': self.product_id.partner_ref,
        'group_id': self.procurement_group_id.id,
        'propagate_cancel': self.propagate_cancel,
        'move_dest_ids': [(4, x.id) for x in self.move_dest_ids if not byproduct_id],
        'cost_share': cost_share,
    }

def _get_moves_finished_values(self):
    moves = []
    for production in self:
        if production.product_id in production.bom_id.byproduct_ids.mapped('product_id'):
            raise UserError(_("You cannot have %s  as the finished product and in the Byproducts", self.product_id.name))
        moves.append(production._get_move_finished_values(production.product_id.id, production.product_qty, production.product_uom_id.id))
        for byproduct in production.bom_id.byproduct_ids:
            if byproduct._skip_byproduct_line(production.product_id):
                continue
            product_uom_factor = production.product_uom_id._compute_quantity(production.product_qty, production.bom_id.product_uom_id)
            if byproduct.is_tool:
                qty = byproduct.product_qty
            else:
                qty = byproduct.product_qty * (product_uom_factor / production.bom_id.product_qty)
            moves.append(production._get_move_finished_values(
                byproduct.product_id.id, qty, byproduct.product_uom_id.id,
                byproduct.operation_id.id, byproduct.id, byproduct.cost_share, byproduct.is_tool))
    return moves

MrpProduction._get_move_finished_values = _get_move_finished_values
MrpProduction._get_moves_finished_values = _get_moves_finished_values