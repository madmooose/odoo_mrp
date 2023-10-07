# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Manufacturing Tools',
    'version': '16.0.1.0.1',
    'category': 'Manufacturing/Manufacturing',
    'sequence': 55,
    'summary': 'Add possibility to use Tools in Manufacturing Orders',
    'depends': [
        'mrp',
        'ng_mrp_one_time_components'
        ],
    'data': [
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
    ],
    'license': 'LGPL-3',
}
