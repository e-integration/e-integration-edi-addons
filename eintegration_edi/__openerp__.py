# -*- coding: utf-8 -*-
##############################################################################
#    eintegration_edi
#    Copyright (c) 2016 e-integration GmbH (<http://www.e-integration.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    This program based on Odoo, formerly OpenERP
#    Copyright (C) Odoo S.A. (<http://www.odoo.com>).
##############################################################################

{
    'name': "e-integration EDI Basics",

    'summary': """
        Basic entities and views for EDI master data
        """,

    'description': """
        - edi.message with corresponding views for management
        - edi.communication entities with corresponding views
    """,

    'author': "e-integration",
    'website': "http://www.e-integration.de",

    'category': 'Service Management',
    'version': '1.0',

    'depends': [
                'eintegration',
                ],

    # always loaded
    'data': [
             'views/edi_message_views.xml',
             'views/edi_communication_views.xml',
             'security/security.xml',
             'security/ir.model.access.csv',
             'data/edi_communication_data.xml',
    ],
    # demo data
    'demo': [
             'data/edi_message_demo_data.xml',
             ],
    'installable': True,
    'auto_install': False,
    'application': False,
}