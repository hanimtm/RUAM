# -*- coding: utf-8 -*-

from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
    )

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
    )


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
