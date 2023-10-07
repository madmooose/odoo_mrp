# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Manufacturing One Time Components',
    'version': '16.0.1.0.1',
    'category': 'Manufacturing/Manufacturing',
    'sequence': 55,
    'summary': 'Add the possibillity to add a component in the quantity of the bom and not bom multiplied MO amount.',
    'depends': ['mrp'],
    'data': [
        'views/mrp_bom_views.xml',
    ],
    'license': 'LGPL-3',
}
