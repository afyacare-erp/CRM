# -*- coding: utf-8 -*-
{
    'name': "afya_care",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Afya Care",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','contacts','account','account_asset'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking.xml',
        'views/res_partner.xml',
        'views/account_move.xml',
        'views/location.xml',
        'views/asset_user.xml',
        'views/asset_tag.xml',
        'views/asset_condition.xml',
        'views/serial_number.xml',
        'views/account_asset_view.xml',
        'data/ApprovalTemplates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
