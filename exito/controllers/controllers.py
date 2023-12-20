# -*- coding: utf-8 -*-
# from odoo import http


# class Exito(http.Controller):
#     @http.route('/exito/exito', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exito/exito/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exito.listing', {
#             'root': '/exito/exito',
#             'objects': http.request.env['exito.exito'].search([]),
#         })

#     @http.route('/exito/exito/objects/<model("exito.exito"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exito.object', {
#             'object': obj
#         })
