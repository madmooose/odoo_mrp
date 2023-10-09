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

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    is_tool = fields.Boolean(string="Tool",
        help="This component will be moved to Production Location and back.")

class MrpBomByproduct(models.Model):
    _inherit = 'mrp.bom.byproduct'

    is_tool = fields.Boolean(string="Tool",
        help="This By-Product will be moved from Production Location to Post-Production.")