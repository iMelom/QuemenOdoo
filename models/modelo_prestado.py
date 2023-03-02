# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Prestado(models.Model):
    _name = 'biblioteca.prestado'
    _description = "Libros prestados"
    _rec_name = 'id'

    comic = fields.Many2one('biblioteca.comic',string='Comic',)
    inicio = fields.Date(string="Inicio", default=lambda self: fields.Date.today())
    socio = fields.Many2one('biblioteca.socio', string="Socio",)
    fin = fields.Date("Fin")

    @api.constrains('inicio')
    def _check_start (self):
        for record in self:
            if record.inicio > fields.Date.today():
                raise ValidationError("No puede ser mayor al dia de inicio")
            
    @api.constrains('fin', 'inicio')
    def _check_finish (self):
        for record in self:
            if record.fin < record.inicio:
                raise ValidationError("No puede ser inferior al dia de inicio")