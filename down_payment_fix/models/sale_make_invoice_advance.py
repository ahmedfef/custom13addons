# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_invoice_values(self, order, name, amount, so_line):
        if len(so_line) == 1:
            res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
            res['invoice_line_ids'] = [(0, 0, {
                        'name': so_line.name,
                        'price_unit': so_line.price_unit,
                        'quantity': so_line.rel_sale_order_line_id.product_uom_qty,
                        'product_id': self.product_id.id,
                        'product_uom_id': so_line.product_uom.id,
                        'tax_ids': [(6, 0, so_line.tax_id.ids)],
                        'sale_line_ids': [(6, 0, [so_line.id])],
                        'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
                        'analytic_account_id': order.analytic_account_id.id or False,
                    })]
        else:
            invoice_line_ids = []
            for line in so_line:
                invoice_line_ids.append(
                    (0, 0, {
                        'name': line.name,
                        'price_unit': line.price_unit,
                        'quantity': line.rel_sale_order_line_id.product_uom_qty,
                        'product_id': self.product_id.id,
                        'product_uom_id': line.product_uom.id,
                        'tax_ids': [(6, 0, line.tax_id.ids)],
                        'sale_line_ids': [(6, 0, [line.id])],
                        'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                        'analytic_account_id': order.analytic_account_id.id or False,
                    })
                )
            res = {
                'ref': order.client_order_ref,
                'type': 'out_invoice',
                'invoice_origin': order.name,
                'invoice_user_id': order.user_id.id,
                'narration': order.note,
                'partner_id': order.partner_invoice_id.id,
                'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
                'partner_shipping_id': order.partner_shipping_id.id,
                'currency_id': order.pricelist_id.currency_id.id,
                'invoice_payment_ref': order.reference,
                'invoice_payment_term_id': order.payment_term_id.id,
                'invoice_partner_bank_id': order.company_id.partner_id.bank_ids[:1].id,
                'team_id': order.team_id.id,
                'campaign_id': order.campaign_id.id,
                'medium_id': order.medium_id.id,
                'source_id': order.source_id.id,
                'invoice_line_ids': invoice_line_ids,
            }
        return res

    def _prepare_so_line(self, order, analytic_tag_ids, tax_ids, amount):
        res = super(SaleAdvancePaymentInv, self)._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
        if self.advance_payment_method == 'percentage':
            context = {'lang': order.partner_id.lang}
            res = []
            for sale_order_line in order.order_line:
                if not sale_order_line.is_downpayment:
                    price_unit = (sale_order_line.price_total * self.amount / 100) / sale_order_line.product_uom_qty
                    res.append({
                        'name': sale_order_line.name,
                        'price_unit': price_unit,
                        'product_uom_qty': 0,
                        'order_id': order.id,
                        'discount': 0.0,
                        'product_uom': self.product_id.uom_id.id,
                        'product_id': self.product_id.id,
                        'analytic_tag_ids': analytic_tag_ids,
                        'tax_id': [(6, 0, tax_ids)],
                        'is_downpayment': True,
                        'rel_sale_order_line_id': sale_order_line.id,
                    })
            del context
        return res

