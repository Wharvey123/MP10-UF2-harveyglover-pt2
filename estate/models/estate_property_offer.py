from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'  # Nom del model dins d'Odoo
    _description = 'Ofertes de propietat'  # Descripció del model

    price = fields.Float('Preu Oferit', required=True)  # Camp per al preu de l'oferta (obligatori)
    state = fields.Selection(  # Estat de l'oferta (pot ser acceptada, rebutjada o en tractament)
        [
            ('accepted', 'Acceptada'),  # Oferta acceptada
            ('rejected', 'Rebutjada'),  # Oferta rebutjada
            ('pending', 'En tractament')  # Oferta encara pendent
        ], 
        default='pending', string="Estat"  # Valor per defecte: 'pending'
    )
    buyer_id = fields.Many2one('res.partner', string="Comprador")  # Relació amb el comprador de la propietat
    comments = fields.Text('Comentaris')  # Camp per afegir comentaris opcionals sobre l'oferta
    property_id = fields.Many2one('estate.property', string="Propietat", readonly=True)  
    # Relació amb la propietat en venda (només lectura)

    # Funció per acceptar una oferta
    def action_accept(self):
        self.ensure_one()  # Garanteix que només es treballi amb un registre
        self.state = 'accepted'  # Canvia l'estat de l'oferta a acceptada
        self.property_id.final_price = self.price  # Assigna el preu final de la propietat
        self.property_id.buyer_id = self.buyer_id  # Assigna el comprador de la propietat
        self.property_id.state = 'offer_accepted'  # Canvia l'estat de la propietat a "oferta acceptada"

    # Funció per rebutjar una oferta
    def action_reject(self):
        self.ensure_one()  # Garanteix que només es treballi amb un registre
        self.state = 'rejected'  # Canvia l'estat de l'oferta a rebutjada
        
        # Busca si hi ha una altra oferta acceptada
        other_accepted_offer = self.property_id.offer_ids.filtered(lambda o: o.state == 'accepted' and o.id != self.id)
        
        if self.property_id.final_price == self.price:
            if other_accepted_offer:
                self.property_id.final_price = other_accepted_offer[0].price  # Assigna el nou preu final
                self.property_id.buyer_id = other_accepted_offer[0].buyer_id  # Assigna el nou comprador
            else:
                self.property_id.final_price = 0  # Reinicia el preu final
                self.property_id.buyer_id = False  # Reinicia el comprador
                self.property_id.state = 'new'  # Restableix l'estat de la propietat a "nova"
