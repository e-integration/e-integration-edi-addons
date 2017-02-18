# -*- coding: utf-8 -*-
##############################################################################
#    eintegration_edi_manager
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
    'name': "e-integration EDI Manager",

    'summary': """
        Specific support for EDI Communication
        """,

    'description': """
        - Sending invoices via EDI
    """,

    'author': "e-integration",
    'website': "http://www.e-integration.de",

    'category': 'Service Management',
    'version': '1.0',

    'depends': [
                'eintegration',
                'eintegration_edi',
                'account',
                'sale',
                ],

    # always loaded
    'data': [
             'views/edi_document_views.xml',
             'views/edi_document_create_wizard.xml',
             'views/edi_partner_views.xml',
             'views/edi_document_stage_views.xml',
             'data/edi_document_stage_data.xml',
             'data/ir_config_parameter_data.xml',
             'views/account_invoice_views.xml',
             'views/sale_order_views.xml',
             'views/edi_document_template.xml',
             'views/edi_document_report_template.xml',
             'views/edi_template_views.xml',
             'views/res_partner_views.xml',
             'cron_send_edi_documents.xml',
             'views/resources.xml',
             'security/ir.model.access.csv',
             ],
    'installable': True,
    'auto_install': False,
    'application': False,

    'qweb': [
             'static/src/xml/templates.xml',
             ],
}