# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    location_prod_id = fields.Many2one(
        'stock.location', 'Production Location',
        store=True, check_company=True,
        readonly=False,
        help="Location where the system will put things during production.")
