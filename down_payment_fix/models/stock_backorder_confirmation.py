# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def _process(self, cancel_backorder=False):
        super(StockBackorderConfirmation, self)._process(cancel_backorder)
        for confirmation in self:
            for pick_id in confirmation.pick_ids:
                if pick_id.sale_id:
                    if self.env.user.has_group('sales_team.group_sale_salesman'):
                        # Simulate the click and automatically
                        sale_make_invoice_advance_id = self.env['sale.advance.payment.inv'].with_context(active_ids=pick_id.sale_id.ids).create({'advance_payment_method': 'delivered'})
                        sale_make_invoice_advance_id.create_invoices()
