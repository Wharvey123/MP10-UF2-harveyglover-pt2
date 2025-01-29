# estate_property_tag.py
from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'  # Nom del model
    _description = 'Etiquetes de propietat'  # Descripció del model

    name = fields.Char('Nom', required=True)  # Nom de l'etiqueta
    property_ids = fields.Many2many('estate.property', string="Propietats")  # Relació amb les propietats