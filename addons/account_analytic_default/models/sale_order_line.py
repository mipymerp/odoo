# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_invoice_line(self, qty):
        vals = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if not vals.get('account_analytic_id'):
            analytic_default_model = self.env['account.analytic.default']
            default_analytic_account = analytic_default_model.account_get(self.product_id.id, 
                self.order_id.partner_id.id, self.order_id.user_id.id, fields.Date.context_today(self))
            if default_analytic_account:
                vals.update({
                    'account_analytic_id': default_analytic_account.analytic_id.id,
                    'analytic_tag_ids' : [(6, 0, default_analytic_account.analytic_tag_ids.ids)],
                })
        return vals