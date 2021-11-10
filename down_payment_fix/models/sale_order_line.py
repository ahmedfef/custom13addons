# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    rel_sale_order_line_id = fields.Many2one('sale.order.line', ondelete='restrict')
