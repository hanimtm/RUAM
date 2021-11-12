from odoo import models, api, fields, _
from odoo.exceptions import UserError


class StockDummyMove(models.Model):
    _name = 'stock.dummy.move'

    picking_id = fields.Many2one('stock.picking', 'Picking')
    name = fields.Char('WBT No')
    date = fields.Date('Date of Picking')
    qty = fields.Float('Quantity')
