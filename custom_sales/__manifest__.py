# -*- coding: utf-8 -*-
{
    # Nom del mòdul (apareixerà en Odoo)
    'name': 'Mòdul Personalitzat de Vendes',
    # Versió del mòdul (útil per gestionar actualitzacions)
    'version': '1.1',
    # Categoria dins d'Odoo per organitzar el mòdul
    'category': 'Vendes',
    # Breu descripció del mòdul i la seva funcionalitat
    'summary': "Funcionalitats personalitzades per a comandes de venda",
    # Autor del mòdul (qui el desenvolupa)
    'author': 'Harvey John Glover',
    # Dependències (altres mòduls que han d'estar instal·lats per funcionar)
    'depends': ['sale_management'],

    # Llista d'arxius XML i QWeb inclosos en el mòdul
    'data': [
        # Fitxer de seguretat per definir permisos d'accés als models
        'security/ir.model.access.csv',
        # Informe comercial en format PDF
        'reports/informe_comercial.xml',
        # Vista personalitzada de comandes de venda
        'views/vista_comanda.xml',
        # Vista de llistat comercial i la seva acció associada
        'views/llistat_comercial.xml',
        # Personalització de l'informe de comandes de venda
        'reports/informe_comanda.xml',
        # Plantilla per generar l'informe comercial
        'reports/plantilla_informe_comercial.xml',
    ],

    # Indica si el mòdul es pot instal·lar
    'installable': True,
    # Defineix si és una aplicació independent o un complement
    'application': False,
}
