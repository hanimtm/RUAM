from odoo import fields,models, api, _
from datetime import date
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    dummy_move_line = fields.One2many('stock.dummy.move','picking_id','Receipts')
    product_imported = fields.Boolean('Product Imported')

    @api.onchange('dummy_move_line')
    def onchange_dummy_move_line(self):
        total = sum(self.dummy_move_line.mapped('qty'))
        for line in self.move_lines:
            move_line = self.env['stock.move.line'].search([(
                'move_id', '=', line._origin.id
            )])
            if not move_line:
                print('Line id :: ',line.id)
                move_line = self.env['stock.move.line'].create({
                                'move_id': line._origin.id,
                                'product_id': line.product_id.id,
                                'qty_done': total,
                                'product_uom_id': line.product_uom.id,
                                'location_id': line.location_id.id,
                                'location_dest_id': line.location_dest_id.id,
                                'company_id':line.company_id.id
                            })
                print(move_line)
            line.quantity_done = total
            move_line.qty_done = total

    # def _action_done(self):
    #     if self.scheduled_date:
    #         self.env.context = dict(self.env.context)
    #         scheduled_date = self.scheduled_date
    #         accounting_date = scheduled_date.date()
    #         self.env.context.update({
    #             'manual_validate_date_time': scheduled_date,
    #             'picking_type_code': self.picking_type_id.code,
    #             'force_period_date': accounting_date
    #         })
    #         res = super(StockPicking, self)._action_done()
    #
    #         manual_validate_date_time = self._context.get('manual_validate_date_time', False)
    #         if manual_validate_date_time:
    #             self.filtered(lambda x: x.state == 'done').write({'date_done': manual_validate_date_time})
    #         return False