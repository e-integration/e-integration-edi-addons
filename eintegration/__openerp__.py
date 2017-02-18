# -*- coding: utf-8 -*-
##############################################################################
#    eintegration
#    Copyright (c) 2015 e-integration GmbH (<http://www.e-integration.de>).
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
    'name': "e-integration Parent-Package",

    'summary': """
        All-encompassing e-integration parent package
        """,

    'description': """
        This is an empty package to serve as a single point of dependency for all
        e-integration customizing. The main purpose is to enable a central "update" of
        all e-integration modules.
    """,

    'author': "e-integration",
    'website': "http://www.e-integration.de",

    'category': 'Service Management',
    'version': '1.0',

    'depends': [],  # No own dependencies
    'data': [],     # No own data files
    
    'installable':  True,
    'auto_install': True,
    'application':  False,
}