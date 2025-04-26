from odoo import fields, models, tools

class ReportEstateSumaPreusPerEstat(models.Model):
    _name = 'report.estate.suma.preus.per.estat'
    _description = "Report de la suma de preus d'ofertes per estat"
    _auto = False
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', string="Comercial", readonly=True)
    state = fields.Selection([
        ('new', 'Nou'),
        ('offer_received', 'Oferta rebuda'),
        ('offer_accepted', 'Oferta acceptada'),
        ('sold', 'Venut'),
        ('canceled', 'Cancel·lat')
    ], string="Estat", readonly=True)
    total_price = fields.Float(string="Suma de Preus", readonly=True)
    count_offers = fields.Integer(string="Nombre d'Ofertes", readonly=True)

    def _select(self):
        return """
            p.user_id as user_id,
            p.state as state,
            SUM(o.price) as total_price,
            COUNT(o.id) as count_offers
        """

    def _from(self):
        return """
            estate_property_offer o
            JOIN estate_property p ON o.property_id = p.id
        """

    def _group_by(self):
        return """
            p.user_id, p.state
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(f""" 
            CREATE OR REPLACE VIEW {self._table} AS
            SELECT
                ROW_NUMBER() OVER () AS id,
                {self._select()}
            FROM {self._from()}
            WHERE o.state != 'rejected'
            GROUP BY {self._group_by()}
            ORDER BY p.user_id, p.state
        """)