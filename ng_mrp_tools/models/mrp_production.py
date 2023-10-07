# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

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

    def _generate_move_from_bom_line(self, product, product_uom, quantity, bom_line_id=False, byproduct_id=False):
        if self.location_prod_id:
            product_prod_location = self.location_prod_id
        else:
            product_prod_location = self.product_id.with_company(self.company_id).property_stock_production
        location_id = bom_line_id and product_prod_location or self.location_id
        location_dest_id = bom_line_id and self.location_dest_id or product_prod_location
        warehouse = location_dest_id.warehouse_id
        return self.env['stock.move'].create({
            'name': self.name,
            'date': self.create_date,
            'bom_line_id': bom_line_id,
            'byproduct_id': byproduct_id,
            'product_id': product.id,
            'product_uom_qty': quantity,
            'product_uom': product_uom.id,
            'procure_method': 'make_to_stock',
            'location_dest_id': location_dest_id.id,
            'location_id': location_id.id,
            'warehouse_id': warehouse.id,
            'unbuild_id': self.id,
            'company_id': self.company_id.id,
        })
