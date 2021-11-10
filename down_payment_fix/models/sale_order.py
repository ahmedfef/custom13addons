# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_due = fields.Monetary(string='Amount Due', compute='_compute_amount_due', readonly=True)

    @api.depends('invoice_ids')
    def _compute_amount_due(self):
        for record in self:
            if record.state == "sale":
                if record.invoice_count > 0:
                    record.amount_due = sum([l.amount_residual_signed for l in record.invoice_ids if l.state == "posted"])
                else:
                    record.amount_due = 0
            else:
                record.amount_due = 0

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        # After completing the process of confirming a sale order, do the following
        if res:
            # Automatically simulate the click on "Create Invoice" by creating the required actions.
            # Check invoice_status before creating an invoice. (Otherwise, it will create an empty invoice when the user cancels the quotation and re-confirm it)
            if self.invoice_status == "no":
                # Check if the user have the following access 'sales_team.group_sale_salesman'
                if self.env.user.has_group('sales_team.group_sale_salesman'):
                    # Simulate the click and automatically
                    sale_make_invoice_advance_id = self.env['sale.advance.payment.inv'].with_context(active_ids=self.ids).create({
                        'advance_payment_method': 'percentage',
                        'amount': 100,  # Always full amount (According to the test question ...)
                    })
                    sale_make_invoice_advance_id.create_invoices()
        return True

