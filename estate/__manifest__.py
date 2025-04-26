{
    "name": "Estate",  # Nom que apareixerà a la llista d'Apps
    "version": "1.0",  # Versió del mòdul
    "summary": "Manage estate properties",  # Descripció breu (opcional però recomanada)
    "category": "Real Estate",  # Categoria del mòdul
    "application": True,  # Indica que és una aplicació
    "depends": ["base"],  # Dependències (per exemple, 'base' per al nucli d'Odoo)
    "data": [
        'security/ir.model.access.csv', # Arxiu CSV amb els permisos d'accés
        'views/estate_menus.xml', # Menús
        'views/estate_property_views.xml', # Vistes
        'views/estate_property_reports_views.xml', # Vistes dels informes
        'report/estate_property_templates.xml', # Plantilles dels informes
        'report/estate_property_reports.xml', # Informes
    ],
    "installable": True,  # Indica que es pot instal·lar
    "license": "LGPL-3",  # Llicència
}