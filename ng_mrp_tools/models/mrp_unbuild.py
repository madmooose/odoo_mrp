# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

class MrpUnbuild(models.Model):
    _inherit = 'mrp.unbuild'

    def _generate_move_from_bom_line(self, product, product_uom, quantity, bom_line_id=False, byproduct_id=False):
#        product_prod_location = product.with_company(self.company_id).property_stock_production
        product_prod_location = self.location_prod_id
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