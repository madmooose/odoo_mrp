from odoo import api, fields, models, _


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    is_onetime_component = fields.Boolean(string="Helper",
        help="This components quantity is not multiplied with to production amount.")