# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        res = super(StockImmediateTransfer, self).process()
        for picking in self.pick_ids:
            if picking.sale_id:
                if self.env.user.has_group('sales_team.group_sale_salesman'):
                    # Simulate the click and automatically
                    sale_make_invoice_advance_id = self.env['sale.advance.payment.inv'].with_context(active_ids=picking.sale_id.ids).create({'advance_payment_method': 'delivered'})
                    sale_make_invoice_advance_id.create_invoices()
        return res


