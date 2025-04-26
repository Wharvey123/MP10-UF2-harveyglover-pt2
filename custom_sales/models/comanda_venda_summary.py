# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class SaleOrderCommercialSummary(models.Model):
    _name = 'sale.order.commercial.summary'
    _description = 'Resum Comercial per Estat de Comanda'
    _auto = False
    _order = 'user_id, state'

    user_id = fields.Many2one(
        'res.users', string='Comercial', readonly=True,
    )
    state = fields.Char(
        string='Estat', readonly=True,
    )
    no_of_orders = fields.Integer(
        string='Nombre de comandes', readonly=True,
    )
    amount_total = fields.Monetary(
        string='Import Total', readonly=True,
        currency_field='company_currency_id'
    )
    company_currency_id = fields.Many2one(
        'res.currency', string='Currency', readonly=True,
    )

    def init(self):
        tools.drop_view_if_exists(self._cr, 'sale_order_commercial_summary')
        self._cr.execute("""
            CREATE OR REPLACE VIEW sale_order_commercial_summary AS (
                SELECT
                    MIN(so.id)            AS id,
                    so.user_id            AS user_id,
                    CASE so.state
                        WHEN 'draft'  THEN 'Esborrany'
                        WHEN 'sent'   THEN 'Enviat'
                        WHEN 'sale'   THEN 'Confirmada'
                        WHEN 'done'   THEN 'Realitzada'
                        WHEN 'cancel' THEN 'Cancel·lat'
                        ELSE so.state
                    END AS state,
                    COUNT(*)             AS no_of_orders,
                    SUM(so.amount_total) AS amount_total,
                    comp.currency_id     AS company_currency_id
                FROM sale_order so
                JOIN res_company comp ON so.company_id = comp.id
                GROUP BY
                    so.user_id,
                    CASE so.state
                        WHEN 'draft'  THEN 'Esborrany'
                        WHEN 'sent'   THEN 'Enviat'
                        WHEN 'sale'   THEN 'Confirmada'
                        WHEN 'done'   THEN 'Realitzada'
                        WHEN 'cancel' THEN 'Cancel·lat'
                        ELSE so.state
                    END,
                    comp.currency_id
            )
        """)
