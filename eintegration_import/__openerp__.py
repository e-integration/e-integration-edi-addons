# -*- coding: utf-8 -*-

##############################################################################
#    eintegration_import
#
#    Copyright (c) 2017 e-integration GmbH (<http://www.e-integration.de>).
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
    'name': "e-integration Import API",

    'summary': """
        Small utility to enable uploading Data files directly into Odoo
        """,

    'description': """
        Data File Import
         
        Allow direct upload of Odoo data files into a running Odoo instance.
    """,

    'author': "e-integration",
    'website': "http://www.e-integration.de",

    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'eintegration'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
#        'demo.xml',
    ],
}