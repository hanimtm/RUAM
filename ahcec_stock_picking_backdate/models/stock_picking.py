from odoo import fields,models, api, _
from datetime import date
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    forced_date = fields.Datetime('Forced Date')
    forced_clicked = fields.Boolean('Forced Clicked')

    def _set_scheduled_date(self):
        for picking in self:
            if picking.state == 'cancel':
                raise UserError(_("You cannot change the Scheduled Date on a done or cancelled transfer."))
            picking.move_lines.write({'date': picking.scheduled_date})

    def action_force_date(self):
        if self.forced_date:
            self.write({'scheduled_date':self.forced_date,'forced_clicked':True})
            accounting_date = self.forced_date.date()
            for move in self.move_ids_without_package:
                move.write({'date':self.forced_date})
                for move_line in self.env['stock.move.line'].search([('move_id','=',move.id)]):
                    move_line.write({'date':self.forced_date})
                for account_move in self.env['account.move'].search([('stock_move_id','=',move.id)]):
                    account_move.write({'date':self.forced_date.date()})

    def _action_done(self):
        if self.scheduled_date:
            self.env.context = dict(self.env.context)
            scheduled_date = self.scheduled_date
            accounting_date = scheduled_date.date()
            self.env.context.update({
                'manual_validate_date_time': scheduled_date,
                'picking_type_code': self.picking_type_id.code,
                'force_period_date': accounting_date
            })
            res = super(StockPicking, self)._action_done()

            manual_validate_date_time = self._context.get('manual_validate_date_time', False)
            if manual_validate_date_time:
                self.filtered(lambda x: x.state == 'done').write({'date_done': manual_validate_date_time})
            return False