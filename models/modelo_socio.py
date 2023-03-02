# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BibliotecaSoci(models.Model):
    _name = 'biblioteca.socio'
    _description = "Socios de la biblioteca"
    _rec_name = 'nombre'

    nombre = fields.Char("Nomvre", required=True)
    apellidos = fields.Char("Apellidos")
    identificador = fields.Char("Id")