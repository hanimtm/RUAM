# -*- coding: utf-8 -*-
{
    'name': "Stock Move Back Date / Past Date",
    'summary': """
                Change validation date with scheduled date for stock transfers / picking / receipt / delivery order.
        """,
    'author': 'Aneesh.AV',
    'category': 'Warehouse',
    'version': '14.0.1',
    'depends': ['stock_account'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_view.xml'
    ],
    'application': False,
    'installable': True,
}
