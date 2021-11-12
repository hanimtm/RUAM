# -*- coding: utf-8 -*-

import base64
import csv
from datetime import datetime

import xlrd
from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools import ustr
import datetime as dt


class ImportdummyWizard(models.TransientModel):
    _name = 'import.dummy.wizard'

    import_type = fields.Selection([
        # ('csv', 'CSV File'),
        ('excel', 'Excel File')
    ], default="excel", string="Import File Type", required=True)
    file = fields.Binary(string="File", required=True)
    product_by = fields.Selection([
        ('name', 'Name'),
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode')
    ], default="name", string="Product By", required=True)

    def show_success_msg(self, counter, skipped_line_no):

        # open the new success message box
        view = self.env.ref('ahcec_stock_picking_import.ahcec_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        dic_msg = str(counter) + " Records imported successfully \n"
        if skipped_line_no:
            dic_msg = dic_msg + "\nNote:"
        for k, v in skipped_line_no.items():
            dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        context['message'] = dic_msg

        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def import_po_apply(self):
        picking = self.env['stock.picking'].browse(self.env.context['picking_id'])
        dummy_move = self.env['stock.dummy.move']
        if self and self.file:
            # For Excel
            if self.import_type == 'excel':
                counter = 1
                data = 0
                skipped_line_no = {}
                try:
                    wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
                    sheet = wb.sheet_by_index(0)
                    skip_header = True
                    created_po_list = []

                    for row in range(sheet.nrows):
                        try:
                            if skip_header:
                                skip_header = False
                                counter = counter + 1
                                continue

                            if picking:
                                if sheet.cell(row, 0).value in (None, ""):
                                    skipped_line_no[str(counter)] = " - No AWB Number. "
                                    counter = counter + 1
                                    continue

                                date = False
                                if sheet.cell(row, 1).value not in (None, "", 0, 0.0):
                                    print(sheet.cell(row, 1).value)
                                    date = datetime.fromordinal(
                                        datetime(1900, 1, 1).toordinal() + int(sheet.cell(row, 1).value) - 2)
                                    print(date)

                                if sheet.cell(row, 2).value in (None, ""):
                                    skipped_line_no[str(counter)] = " - No Quantity. "
                                    counter = counter + 1
                                    continue
                                dummy_move.create({
                                    'picking_id': picking.id,
                                    'name': sheet.cell(row, 0).value,
                                    'date': date,
                                    'qty': sheet.cell(row, 2).value,
                                })
                                data = data + 1
                                counter = counter + 1
                            else:
                                skipped_line_no[str(counter)] = " - Move not created. "
                                counter = counter + 1
                                continue

                        except Exception as e:
                            skipped_line_no[str(counter)] = " - Value is not valid " + ustr(e)
                            counter = counter + 1
                            continue

                except Exception as e:
                    raise UserError(_("Sorry, Your excel file does not match with our format " + ustr(e)))

                if counter > 1:
                    completed_records = data
                    res = self.show_success_msg(completed_records, skipped_line_no)
                    picking.onchange_dummy_move_line()
                    picking.write({'product_imported': True})
                    return res
