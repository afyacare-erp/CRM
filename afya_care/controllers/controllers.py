# -*- coding: utf-8 -*-
# from odoo import http


# class AfyaCare(http.Controller):
#     @http.route('/afya_care/afya_care', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/afya_care/afya_care/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('afya_care.listing', {
#             'root': '/afya_care/afya_care',
#             'objects': http.request.env['afya_care.afya_care'].search([]),
#         })

#     @http.route('/afya_care/afya_care/objects/<model("afya_care.afya_care"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('afya_care.object', {
#             'object': obj
#         })
