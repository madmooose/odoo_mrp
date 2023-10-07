from odoo import api, fields, models, _


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    is_tool = fields.Boolean(string="Tool",
        help="This component will be moved to Production Location and back.")