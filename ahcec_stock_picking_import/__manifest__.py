# -*- coding: utf-8 -*-
{
    'name': "Stock Move dummy Import",
    'summary': """
                Stock Move dummy Import
        """,
    'author': 'Aneesh.AV',
    'category': 'Warehouse',
    'version': '15.0.1',
    'depends': ['stock'],
    'data': [
        'security/import_po_security.xml',
        'security/ir.model.access.csv',
        'wizard/import_message_wizard.xml',
        'wizard/import_inventory_wizard.xml',
        'views/stock_picking_view.xml'
    ],
    'application': False,
    'installable': True,
}
