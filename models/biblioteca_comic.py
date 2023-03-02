# -*- coding: utf-8 -*-
from datetime import timedelta
from operator import index

from odoo import models, fields, api
from odoo.exceptions import ValidationError


# Modelo base, creado como modelo abstracto 
# Este modelo lo heredarara el modelo BibliotecaComic
# Y se ha creado puramente con fin didáctico para ver herencia entre modelos
class BaseArchive(models.AbstractModel):
    #Nombre y descripcion del modelo
    _name = 'base.archive'
    _description = 'Fichero abstracto'

    #Introduce el atributo "Activo"
    activo = fields.Boolean(default=True)

    #Introducice metodo "archivar" que invierte el estado de "activo"
    #Recordamos se recive "self" como el modelo entero y no como un registro,
    #por ese motivo debemos iterar
    def archivar(self):
        #Por cada registro del modelo
        for record in self:
            #Cambiamos el valor de activo a su version negada
            record.activo = not record.activo


#Definimos modelo Biblioteca comic
class BibliotecaComic(models.Model):

    _name = 'biblioteca.comic'
    _inherit = ['base.archive']

    _description = 'Comic de biblioteca'

    _order = 'fecha_publicacion desc, nombre'

    _rec_name = 'nombre'
    nombre = fields.Char('Titulo', required=True, index=True)
    isbn = fields.Char('ISBN', required=True)
    estado = fields.Selection(
        [('borrador', 'No disponible'),
         ('disponible', 'Disponible'),
         ('perdido', 'Perdido')],
        'Estado', default="borrador")
    descripcion = fields.Html('Descripción', sanitize=True, strip_style=False)
    portada = fields.Binary('Portada Comic')

    fecha_publicacion = fields.Date('Fecha publicación')

    precio = fields.Float('Precio')
    paginas = fields.Integer('Numero de páginas',
        #Hace que este atributo este disponible para este grupo de seguridad 
        #Que en este caso son todos los usuarios
        groups='base.group_user',
        #Establece que si el estado es perdido, el numero de paginas no se puede cambiar
        estados={'perdido': [('readonly', True)]},
        #Texto a mostrar en la ayuda de la interfaza al dejar el ratón encima
        help='Total numero de paginas',
        #Si se pone a true, indica que si este atributo se aplica a distintas empreas en Odoo
        #para cada empresa ponga un valor distintos
        #Esta colocado con fin didactico a false 
        company_dependent=False)
 
    #Valoración lector, indicando como son los datos
    valoracion_lector = fields.Float(
        'Valoración media lectores',
        digits=(14, 4),  # Precision opcional (total, decimales),
    )
    autor_ids = fields.Many2many('res.partner', string='Autores')

    #Constraints de SQL del modelo
    #Util cuando la constraint se puede definir con sintaxis SQL
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El titulo Comic debe ser único.'),
        ('positive_page', 'CHECK(paginas>0)', 'El comic debe tener al menos una página')
    ]

    @api.constrains('fecha_publicacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_publicacion and record.fecha_publicacion > fields.Date.today():
                raise models.ValidationError('La fecha de lanzamiento debe ser anterior a la actual')
