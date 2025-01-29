# Importem les biblioteques necessàries
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

# Definim el model 'EstateProperty'
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Model per estate_property'

    # a. Nom (obligatori, text curt)
    name = fields.Char('Nom', required=True)  # Nom de la propietat

    # b. Descripció (text llarg)
    description = fields.Text('Descripció')  # Descripció llarga

    # c. Codi postal (obligatori, text curt)
    postalcode = fields.Char('Codi Postal', required=True)  # Codi postal

    # d. Data de disponibilitat (data, no copiable). Valor per defecte: data de creació de l'oferta + 1 mes.
    date_availability = fields.Date(  # Data de disponibilitat
        string="Data de Disponibilitat", 
        default=lambda self: fields.Date.today() + relativedelta(months=1), 
        copy=False
    )

    # e. Preu de venda esperat (valor en euros)
    selling_price = fields.Float('Preu de Venda Esperat', required=True)  # Preu esperat

    # f. Preu de venda final (valor en euros, no modificable i no copiable)
    final_price = fields.Float('Preu de Venda Final', readonly=True, copy=False)  # Preu final

    # g. Millor oferta (valor en euros, valor calculat, no modificable i no emmagatzemat en base de dades)
    best_offer = fields.Float('Millor Oferta', compute="_compute_best_offer", store=False)  # Millor oferta

    # h. Estat (possibles valors: Nova, Oferta Rebuda, Oferta Acceptada, Venuda, Cancel·lada). Valor per defecte Nova.
    state = fields.Selection(  # Estat de la propietat
        [
            ('new', 'Nova'),
            ('offer_received', 'Oferta Rebuda'),
            ('offer_accepted', 'Oferta Acceptada'),
            ('sold', 'Venuda'),
            ('canceled', 'Cancel·lada'),
        ], 
        default='new', string="Estat"
    )

    # i. Nombre d’habitacions (obligatori, nombre)
    bedrooms = fields.Integer('Nombre d\'Habitacions', required=True)  # Nombre d'habitacions

    # j. Tipus: els possibles valors s’han de poder definir per l’usuari dins de l’aplicació (per exemple, Casa, Pis...)
    type_id = fields.Many2one('estate.property.type', string="Tipus")  # Tipus de propietat

    # k. Etiquetes: els possibles valors s’han de poder definir per l’usuari dins de l’aplicació (per exemple: platja, muntanya...)
    tag_ids = fields.Many2many('estate.property.tag', string="Etiquetes")  # Etiquetes

    # l. Ascensor (Verdader/Fals). Valor per defecte: Fals
    has_elevator = fields.Boolean('Ascensor', default=False)  # Indicador d'ascensor

    # m. Parking (Verdader/Fals). Valor per defecte: Fals
    has_parking = fields.Boolean('Parking', default=False)  # Indicador de parking

    # n. Renovat (Verdader/Fals). Valor per defecte: Fals
    is_renovated = fields.Boolean('Renovat', default=False)  # Indicador de renovació

    # o. Banys (nombre)
    bathrooms = fields.Integer('Banys')  # Nombre de banys

    # p. Superfície (obligatori, nombre)
    area = fields.Float('Superfície (m2)', required=True)  # Superfície en m2

    # q. Preu per m2(valor en euros, valor calculat, no modificable i no emmagatzemat en base de dades)
    price_per_m2 = fields.Float('Preu per m2', compute="_compute_price_per_m2", store=False)  # Preu per m2

    # r. Any de construcció (nombre)
    construction_year = fields.Integer('Any de Construcció')  # Any de construcció

    # s. Certificat energètic (possibles valors: A,B,C,D,E,F,G)
    energy_certificate = fields.Selection(  # Certificat energètic
        [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G')], 
        string="Certificat Energètic"
    )

    # t. Actiu (atribut predefinit que no es mostra a l’usuari). Valor per defecte: Verdader
    is_active = fields.Boolean('Actiu', default=True)  # Estat actiu

    # u. Llistat d’ofertes: les ofertes han de poder definir-se per l’usuari en l’aplicació.
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Llistat d'Ofertes")  # Ofertes

    # v. Comprador: ha de ser un contacte existent a l’aplicació. Valor calculat, no modificable i no emmagatzemat en base de dades.
    buyer_id = fields.Many2one('res.partner', string="Comprador", readonly=True)  # Comprador

    # w. Comercial: ha de ser un usuari de l’aplicació. Valor per defecte: usuari actual.
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user)  # Comercial

    # Funcions de càlcul
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            offers = record.offer_ids.filtered(lambda o: o.state != 'rejected')
            record.best_offer = max(offers.mapped('price'), default=0)  # Calcula la millor oferta

    @api.depends('selling_price', 'area')
    def _compute_price_per_m2(self):
        for record in self:
            record.price_per_m2 = record.selling_price / record.area if record.area else 0  # Calcula el preu per m2
