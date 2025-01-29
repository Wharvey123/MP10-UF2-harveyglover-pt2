# estate_property_offer.py
from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'  # Nom del model
    _description = 'Ofertes de propietat'  # Descripció del model

    price = fields.Float('Preu Oferit', required=True)  # Preu de l'oferta
    state = fields.Selection(  # Estat de l'oferta
        [
            ('accepted', 'Acceptada'),  # Estat "Acceptada"
            ('rejected', 'Rebutjada'),  # Estat "Rebutjada"
            ('pending', 'En tractament')  # Estat "En tractament"
        ], 
        default='pending', string="Estat"  # Valor per defecte 'pending'
    )
    property_id = fields.Many2one('estate.property', string="Propietat", required=True)  # Propietat relacionada
    partner_id = fields.Many2one('res.partner', string="Comprador")  # Comprador de la propietat
    comments = fields.Text('Comentaris')  # Comentaris relacionats amb l'oferta

    # Actualitzem propietat quan s'accepta una oferta
    def action_accept(self):
        self.ensure_one()  # Assegura que només s'operi sobre una oferta
        self.state = 'accepted'  # Actualitza l'estat a 'acceptada'
        self.property_id.final_price = self.price  # Assigna el preu de l'oferta com a preu final
        self.property_id.buyer_id = self.partner_id  # Assigna el comprador a la propietat

    # Funció per rebutjar l'oferta
    def action_reject(self):
        self.ensure_one()  # Assegura que només s'operi sobre una oferta
        self.state = 'rejected'  # Actualitza l'estat a 'rebutjada'