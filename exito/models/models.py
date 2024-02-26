# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions  
from datetime import datetime
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging
import random

# cada jugador puede tener objetos como casa coche o ropas cara que te ayudan a ligar o tener mas carisma entre otros
class public_place(models.Model):
    _name = 'exito.public_place'
    _description = 'Public places on the map where you can take actions such as dating or fulfilling your characters\' needs'

    name = fields.Char(string='Unknown public place')
    price = fields.Float()
    characteristic_boost_amount = fields.Float(string='Characteristic Boost',
                                               help='Amount by which the characteristic is enhanced')
    characteristic_boost = fields.Many2one("exito.characteristic", string='Caracteristica', ondelete='restrict')
    dating_succes_rate_percentage = fields.Float(string='Ligating Percentage', help='Percentage of success in dating')


class local(models.Model):
    _name = 'exito.local'
    _description = 'Locals on the map where you can take actions such as dating or fulfilling your characters\' needs'

    name = fields.Char(string='Local name')
    price = fields.Float()
    characteristic_boost_amount = fields.Float(string='Characteristic Boost',
                                               help='Amount by which the characteristic is enhanced')
    characteristic_boost = fields.Many2one("exito.characteristic", string='Caracteristica', ondelete='restrict')
    dating_succes_rate_percentage = fields.Float(string='Probabilidad de ligar', help='Percentage of success in dating')


class country(models.Model):
    _name = 'exito.country'
    _description = 'Character field'

    name = fields.Char(string='Name')
    multiplier_PIB = fields.Float(default=1.0)
    multiplier_taxes = fields.Float(default=0.79)
    cities = fields.One2many("exito.city", 'country', string='Ciudades')
    # a espera de castillo characters = fields.Many2many
    # characters = fields.One2many('exito.character', 'country', string='Characters')


class city(models.Model):
    _name = 'exito.city'
    _description = 'Character field'

    name = fields.Char(string='Name')
    country = fields.Many2one("exito.country", string='Pais', ondelete='restrict')
    default_parcel_price = fields.Float()
    number_parcels = fields.Integer()
    parcel_ids = fields.One2many("exito.parcel", "city", string="Parcels")

    @api.model
    def create(self, vals):
        # Create the city record
        new_city = super(city, self).create(vals)

        # Create parcel records based on number_parcels and default_parcel_price
        for i in range(new_city.number_parcels):
            parcel_vals = {
                'name': f'{new_city.name} {i + 1}',
                'city': new_city.id,
                'monthly_price': new_city.default_parcel_price,
            }
            self.env['exito.parcel'].create(parcel_vals)

        return new_city


class parcel(models.Model):
    _name = 'exito.parcel'
    _description = 'Character field'

    name = fields.Char(string='Nombre')
    city = fields.Many2one("exito.city", string='Ciudad', ondelete='restrict')
    monthly_price = fields.Float(string="Coste mensual")
    business = fields.Many2one('exito.character_business', string='Negocio que la ocupa',  ondelete='restrict' )
    owner = fields.Many2one('exito.character', string='Propietario',  ondelete='restrict')

    @api.depends('business')
    def _compute_occupation_status(self):
        for parcel in self:
            if parcel.business:
                parcel.occupation_status = "Ocupado: Sí"
            else:
                parcel.occupation_status = "Ocupado: No"

    occupation_status = fields.Char(string="Estado de ocupación", compute="_compute_occupation_status", store=True)



class player(models.Model):
    #_name = 'exito.player'
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Character field'

    name = fields.Char(string='Name')
    age = fields.Integer(default=18)
    characters = fields.One2many("exito.character", 'player', string='Personajes',readonly=True)
    default_character_name = fields.Char(string="Nombre para su personaje")
    sex = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino')], string='Sexo')
    photo = fields.Image(max_width=200, max_height=200)
    is_player = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        new_player = super(player, self).create(vals)

        character_vals = {
            'name': new_player.default_character_name,
            'player': new_player.id,
            'main_character': True,
            'sex': new_player.sex,
        }
        self.env['exito.character'].create(character_vals)

        return new_player

    def crear_personaje_aleatorio(self):
        random_character_names = ['Juan', 'Maria', 'Carlos', 'Laura', 'Andres', 'Sofia', 'Diego', 'Ana','Luis', 'Elena', 'Pedro', 'Isabella', 'Javier', 'Valentina', 'Miguel', 'Lucia','Fernando', 'Camila', 'David', 'Julia', 'Raul', 'Carolina', 'Roberto', 'Mariana','Manuel', 'Alicia', 'Ricardo', 'Paula', 'Gustavo', 'Natalia', 'Jorge', 'Catalina','Gabriel', 'Daniela', 'Eduardo', 'Monica', 'Alejandro', 'Gabriela', 'Antonio', 'María José', 'Francisco','Isabel', 'José Luis', 'Carmen', 'Daniel', 'Patricia','Manuela', 'Joaquín', 'Raquel', 'José Manuel', 'Victoria', 'Alberto', 'Teresa','Rosa María', 'Fernando José', 'Pilar', 'Ángel', 'Inés', 'Santiago', 'Beatriz', 'Enrique', 'Adriana', 'Rafael', 'Cristina', 'Roberto Carlos', 'Martha', 'Diego José', 'Lorena', 'Alfonso','Sara', 'Guillermo', 'Valeria', 'Hugo', 'Verónica', 'Pedro José', 'Carla']

        random_name = random.choice(random_character_names)
        random_sex = random.choice(['masculino', 'femenino'])

        character_vals = {
            'name': random_name,
            'player': self.id,
            'main_character': False,
            'sex': random_sex,
        }

        # self.env['exito.character'].create(character_vals)
        created_character = self.env['exito.character'].create(character_vals)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Personaje Creado',
            'view_mode': 'form',
            'res_model': 'exito.character',
            'res_id': created_character.id,
            'target': 'current',
        }

    def crear_personaje(self):

        return {
            'type': 'ir.actions.act_window',
            'name': ' ',
            'view_mode': 'form',
            'res_model': 'exito.player_wizard',
            'target': 'new',
            'context': {'default_player_id': self.id},
        }



class player_wizard(models.TransientModel):
    _name = 'exito.player_wizard'
    _description = 'Asistente de Creación de Personaje'

    player_id = fields.Many2one('res.partner', string='Jugador')

    name = fields.Char(string='Nombre', required=True)
    age = fields.Integer(default=18, string='Edad', required=True)
    sex = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino')], string='Sexo', required=True)

    money = fields.Float(default=750.00, string='Dinero')
    main_character = fields.Boolean(default=False, string='Personaje principal?')


    state = fields.Selection([
        ('step1', 'Paso 1'),
        ('step2', 'Paso 2'),
        ('step3', 'Paso 3'),
    ], default='step1')


    # def action_next(self):
    #     self.ensure_one()
    #     if self.state == 'step1':
    #         return self.write({'state': 'step2'})
    #     elif self.state == 'step2':
    #         return self.write({'state': 'step3'})
    def action_next(self):
        self.ensure_one()
        new_state = 'step1'
        if self.state == 'step1':
            self.env.ref('exito.action_check_age').with_context(active_id=self.id, active_model=self._name).sudo().run()
            new_state = 'step2'
        elif self.state == 'step2':
            new_state = 'step3'
        self.write({'state': new_state})

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'name': ' ',
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
        }


    def action_prev(self):
        self.ensure_one()
        new_state = 'step1'
        if self.state == 'step3':
            new_state = 'step2'
        elif self.state == 'step2':
            new_state = 'step1'
        self.write({'state': new_state})
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'name': ' ',
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
        }

    def action_save(self):
        self.ensure_one()
        created_character = self.env['exito.character'].create({
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'money': self.money,
            'main_character': self.main_character,
            'player': self.player_id.id,
        })
        # return {'type': 'ir.actions.act_window_close'}
        return {
            'type': 'ir.actions.act_window',
            'name': 'Personaje Creado',
            'view_mode': 'form',
            'res_model': 'exito.character',
            'res_id': created_character.id,  # ID del personaje creado
            'target': 'current',
        }



class character(models.Model):
    _name = 'exito.character'
    _description = 'Character field'

    name = fields.Char( string='Nombre')
    age = fields.Integer(default=18, string='Edad')
    money = fields.Float(default='750.00', string='Dinero')
    alive = fields.Boolean(default=True, string='Está vivo?')
    main_character = fields.Boolean( string='Personaje principal?')
    loans = fields.One2many("exito.loan", 'client', string='Prestamos')
    player = fields.Many2one("res.partner", string='Jugador', ondelete='restrict')
    sex = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino')], string='Sexo')
    business = fields.One2many('exito.character_business', 'owner', string='Negocios')
    prisoner = fields.Boolean(default=False, string='Preso?')
    # se tiene que asignar random
    city = fields.Many2one("exito.city",  ondelete='restrict', string='Ciudad')
    # se tiene que calcular de la city
    country = fields.Many2one("exito.country", ondelete='restrict', related='city.country', string='Pais')
    dairy_spend = fields.Float(default='15', string='Gasto diario')
    characteristics = fields.One2many('exito.character_characteristic', 'character_id', string='Caracteristicas')
    parcels = fields.One2many('exito.parcel', 'owner', string='Parcelas')

    @api.model
    def create(self, vals):
        # Crear un personaje
        new_character = super(character, self).create(vals)

        # Obtener todas las características
        characteristics = self.env['exito.characteristic'].search([])

        # Crear registros en la tabla intermedia para las características únicas del personaje
        for characteristic in characteristics:
            self.env['exito.character_characteristic'].create({
                'character_id': new_character.id,
                'characteristic_name': characteristic.name,
                'characteristic_level': 0,
            })

        return new_character
    def participar_en_subasta(self):

        return {
            'type': 'ir.actions.act_window',
            'name': ' ',
            'view_mode': 'form',
            'res_model': 'exito.character_wizard',
            'target': 'new',
            'context': {'default_character_id': self.id},
        }

class character_wizard(models.TransientModel):
    _name = 'exito.character_wizard'
    _description = 'Asistente de Creación de subasta'


    character_id = fields.Many2one('exito.character', string='Personaje', default=lambda self: self.env.context.get('default_character_id'))
    auction_id = fields.Many2one('exito.auction', string='Subasta', required=True)
    bid_amount = fields.Float(string='Cantidad Apostada', required=True)
    state = fields.Selection([
        ('step1', 'Paso 1'),
        ('step2', 'Paso 2'),
        ('step3', 'Paso 3'),
    ], default='step1')


    def action_next(self):
        self.ensure_one()
        new_state = 'step1'
        if self.state == 'step1':
            new_state = 'step2'
        elif self.state == 'step2':
            new_state = 'step3'
        self.write({'state': new_state})

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'name': ' ',
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
        }


    def action_prev(self):
        self.ensure_one()
        new_state = 'step1'
        if self.state == 'step3':
            new_state = 'step2'
        elif self.state == 'step2':
            new_state = 'step1'
        self.write({'state': new_state})
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'name': ' ',
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
        }

    def action_save(self):
        self.ensure_one()
        if self.character_id.money < self.bid_amount:
            return {
                'warning': {
                    'title': "No suficiente dinero",
                    'message': "El personaje no tiene suficiente dinero para realizar esta apuesta."
                }
            }
        self.env['exito.auction_character_bid'].create({
            'auction_id': self.auction_id.id,
            'character_id': self.character_id.id,
            'amount': self.bid_amount,
        })
        self.character_id.money -= self.bid_amount
        return {
            'type': 'ir.actions.act_window_close',
            'info': 'La apuesta ha sido realizada con éxito.'
        }
        # created_character = self.env['exito.character'].create({
        #     'name': self.name,
        #     'age': self.age,
        #     'sex': self.sex,
        #     'money': self.money,
        #     'main_character': self.main_character,
        #     'player': self.player_id.id,
        # })
        # # return {'type': 'ir.actions.act_window_close'}
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Personaje Creado',
        #     'view_mode': 'form',
        #     'res_model': 'exito.character',
        #     'res_id': created_character.id,
        #     'target': 'current',
        # }


class character_characteristic(models.Model):
    _name = 'exito.character_characteristic'
    _description = 'Character Characteristics'

    characteristic_name = fields.Char()
    character_id = fields.Integer()
    characteristic_level = fields.Float()

    @api.constrains('characteristic_level')
    def _check_characteristic_level(self):
        for record in self:
            if record.characteristic_level < 0 or record.characteristic_level > 100:
                raise ValidationError("El nivel de la característica debe estar entre 0 y 100 (incluidos).")
class characteristic(models.Model):
    _name = 'exito.characteristic'
    _description = 'character characteristics'

    name = fields.Char(default="Unknown characteristic")
    level = fields.Float(default=0.0)

class business(models.Model):
    _name = 'exito.business'
    _description = 'business field'

    name = fields.Char()
    startDate = fields.Datetime(default=lambda self: datetime.now())
    #level = fields.Integer()
    #max_level = fields.Integer()
    investment = fields.Float()
    worker_salary = fields.Float()
    succes_rate_min=fields.Float()
    succes_rate_max=fields.Float()
    #min_workers = fields.Integer()
    amount_workers = fields.Integer()
    min_inteligence_level = fields.Integer()
    min_creativity_level = fields.Integer()
    min_ambition_level = fields.Integer()
    min_conscience_level = fields.Integer()
    min_monthly_return = fields.Float()
    max_monthly_return = fields.Float()
    min_parcels = fields.Integer(default=1)




class character_business(models.Model):
    _name = 'exito.character_business'
    _description = 'Character business field'

    name = fields.Char()
    startDate = fields.Datetime(default=lambda self: datetime.now())
    level = fields.Integer()
    investment = fields.Float()
    worker_salary = fields.Float()
    succes_rate_min=fields.Float()
    succes_rate_max=fields.Float()
    amount_workers = fields.Integer()
    min_inteligence_level = fields.Integer()
    min_creativity_level = fields.Integer()
    min_ambition_level = fields.Integer()
    min_conscience_level = fields.Integer()
    monthly_return = fields.Float()
    parcels = fields.One2many('exito.parcel', 'business', string='Parcels')
    owner = fields.Many2one('exito.character', string='Propietario')

class bank(models.Model):
    _name = 'exito.bank'
    _description = 'bank field'

    name = fields.Char(default="Exito bank")
    loans = fields.One2many("exito.loan", 'bank', string='Prestamos')

    @api.model
    def create(self, vals):
        # Check if a bank record already exists
        existing_bank = self.search([], limit=1)
        if existing_bank:
            raise exceptions.ValidationError("Ya existe un banco, por lo que no es posible crear mas.")

        return super(bank, self).create(vals)


class jail(models.Model):
    _name = 'exito.jail'
    _description = 'Character field'

    name = fields.Char(string='Name')
    age = fields.Integer(default=18)
    # characters = fields.One2many('exito.character', 'jail', string='Characters')


class loan(models.Model):
    _name = 'exito.loan'
    _description = 'bank field'

    name = fields.Char(compute='_compute_loan_name', store=True)
    bank = fields.Many2one("exito.bank", string='Banco', ondelete='restrict')
    client = fields.Many2one("exito.character", string='Cliente', ondelete='restrict')

    @api.depends('client')
    def _compute_loan_name(self):
        for loan in self:
            if loan.client:
                loan.name = f'loan {loan.client.name} {loan.id}'
            else:
                loan.name = 'loan'

    def create_loan_with_default_bank(self, loan_data):
        default_bank = self.env['exito.bank'].search([], limit=1)
        if default_bank:
            loan_data['bank'] = default_bank.id
        return self.create(loan_data)



class criminal_activity(models.Model):
    _name = 'exito.criminal_activity'
    _description = 'criminal activity'

    name = fields.Char(default="Unknown criminal activity")
    risk = fields.Float(required=True)
    profit_min = fields.Float(required=True)
    profit_max = fields.Float(required=True)
    days_in_prison_min = fields.Integer(required=True)
    days_in_prison_max = fields.Integer(required=True)


class criminal_activity(models.Model):
    _name = 'exito.criminal_activity'
    _description = 'criminal activity'

    name = fields.Char(default="Unknown criminal activity")
    risk = fields.Float(required=True)
    profit_min = fields.Float(required=True)
    profit_max = fields.Float(required=True)
    days_in_prison_min = fields.Integer(required=True)
    days_in_prison_max = fields.Integer(required=True)

class auction(models.Model):
    _name = 'exito.auction'
    _description = 'Subasta'

    name = fields.Char(string="Nombre subasta", compute="_compute_name", store=True, help='Nombre por el cual es identificada dicha subasta',readonly=True)
    #name = fields.Char(default="Subasta desconocida", string="nombre subasta",help='Nombre por el cual es identificada dicha subasta')
    startDate = fields.Datetime(default=lambda self: datetime.now(), string="Hora de inicio")
    finishDate = fields.Datetime()
    durationHours = fields.Integer(default=2, help='La cantidad de horas que va a permanecer activa esta subasta', string="Duración subasta")
    parcel_id = fields.Many2one('exito.parcel', string='Parcela')
    character_bids = fields.One2many('exito.auction_character_bid', 'auction_id', string='Apuestas de personajes')
    parcel_name = fields.Char(related='parcel_id.name', string='Nombre de Parcela', store=True, readonly=True)
    sorted_character_bids = fields.One2many('exito.auction_character_bid', compute='_compute_sorted_character_bids')
    status = fields.Selection([
        ('iniciado', 'Iniciado'),
        ('terminado', 'Terminado'),
        ('finalizado', 'Finalizado')
    ], string='Estado de la subasta', default='iniciado', readonly=True)

    @api.depends('parcel_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.parcel_name} {record.id}"

    def example_cron_method(self):
        _logger = logging.getLogger(__name__)
        _logger.info("¡El cron se ha ejecutado con éxito! Este es un mensaje de ejemplo por consola.")
        current_time = datetime.now()
        auctions_to_update = self.search([
            ('status', '=', 'iniciado'),
            ('startDate', '<=', current_time - timedelta(hours=1) * self.durationHours)
        ])

        for auction in auctions_to_update:
            auction.status = 'terminado'
            highest_bid = max(auction.character_bids, key=lambda bid: bid.amount)

            if highest_bid:
                character_id = highest_bid.character_id.id
                auction.status = 'terminado'
                character = self.env['exito.character'].browse(character_id)
                # character.write({'city': auction.parcel_id.city.id})
                character.parcels += auction.parcel_id

    def get_unprocessed_finished_auctions(self):
        finished_auctions = self.filtered(lambda a: a.status == 'terminado')
        return finished_auctions

    @api.depends('character_bids.amount')
    def _compute_sorted_character_bids(self):
        for auction in self:
            sorted_bids = auction.character_bids.sorted(key=lambda bid: bid.amount, reverse=True)
            auction.sorted_character_bids = [(6, 0, sorted_bids.ids)]


    def action_view_sorted_bids(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apuestas Ordenadas',
            'res_model': 'exito.auction_character_bid',
            'view_mode': 'tree',
            'domain': [('auction_id', '=', self.id)],
            'context': {'default_auction_id': self.id},
            'target': 'new',
        }

class auction_character_bid(models.Model):
    _name = 'exito.auction_character_bid'
    _description = 'Apuesta de Personaje en Subasta'

    auction_id = fields.Many2one('exito.auction', string='Subasta')
    character_id = fields.Many2one('exito.character', string='Personaje')
    amount = fields.Float(string='Cantidad apostada')
