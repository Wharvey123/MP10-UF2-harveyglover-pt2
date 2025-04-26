# -*- coding: utf-8 -*-
from odoo import api, fields, models  # Importem les classes necessàries d'Odoo

class ComandaVenda(models.Model):
    """Model heretat de sale.order amb camps personalitzats"""
    _inherit = 'sale.order'  # Estenem el model 'sale.order' per afegir funcionalitats addicionals

    # Camp que emmagatzema el correu preferent associat a la comanda de venda
    correu_preferent = fields.Char(string="Correu preferent")

    # Camp calculat que compta el total d'articles de la comanda
    total_articles = fields.Integer(
        string="Nombre d'articles",  # Nom que es mostrarà a la interfície d'Odoo
        compute="_compute_total_articles",  # Defineix la funció que calcularà el valor
        store=True  # Guarda el resultat a la base de dades per optimitzar consultes
    )

    # Camp per comptabilitzar el nombre de comandes, útil per a agrupacions en informes
    no_of_orders = fields.Integer(
        string='Nombre de comandes',  # Nom que es mostrarà a la interfície
        compute='_compute_no_of_orders',  # Defineix la funció que establirà el valor
        group_operator='count',  # Indica que aquest camp es pot usar per agrupar registres
        store=False,  # No es desa a la base de dades, només s'usa en temps real
    )

    @api.depends('order_line')  # Indica que el valor del camp depèn de les línies de comanda
    def _compute_total_articles(self):
        """Calcula el nombre total d'articles sumant les quantitats de cada línia de comanda"""
        for comanda in self:  # Iterem sobre cada comanda de venda
            # Sumem la quantitat d'unitats de cada producte a les línies de comanda
            comanda.total_articles = sum(line.product_uom_qty for line in comanda.order_line)

    @api.depends()  # Aquest mètode no depèn de cap camp en concret
    def _compute_no_of_orders(self):
        """Cada registre representa una comanda, per això assignem sempre el valor 1"""
        for order in self:  # Iterem sobre cada comanda de venda
            order.no_of_orders = 1  # Assignem el valor "1" perquè cada registre representa una comanda individual
