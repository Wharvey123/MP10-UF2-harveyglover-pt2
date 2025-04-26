# -*- coding: utf-8 -*-
from odoo import api, models  # Importem les classes necessàries d'Odoo

class ReportCommercialSummary(models.AbstractModel):
    """Definició d'un model abstracte per generar l'informe comercial"""
    
    _name = 'report.custom_sales.plantilla_informe_comercial'  # Identificador únic del model del report
    _description = 'Informe Comercial resum per comercial i estat'  # Descripció del model

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Funció que retorna els valors necessaris per generar l'informe comercial.
        
        - `docids`: Identificadors dels registres de `sale.order.commercial.summary`
        - `data`: Paràmetres addicionals (pot ser None)
        """
        
        # Obtenim els registres de 'sale.order.commercial.summary' segons els identificadors passats
        summaries = self.env['sale.order.commercial.summary'].browse(docids)

        # Recuperem la informació de l'empresa actual
        company = self.env.company

        # Retornem un diccionari amb les dades que s'utilitzaran a l'informe
        return {
            'doc_ids': docids,  # Identificadors dels documents a incloure en l'informe
            'doc_model': 'sale.order.commercial.summary',  # Model Odoo al qual fa referència l'informe
            'docs': summaries,  # Llista de registres associats a l'informe
            'company': company,  # Informació de l'empresa que genera l'informe
        }
