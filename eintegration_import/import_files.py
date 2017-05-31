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


from openerp import http

from openerp.tools.convert import convert_xml_import

import logging
import werkzeug
LOG = logging.getLogger(__name__)



class ImportFiles(http.Controller):

    

    @http.route('/eintegration_import/api/import', type='http', auth='user', methods=['POST'])
    def import_files(self, module, data_file):

        try:
            convert_xml_import(http.request.cr, module, data_file)
            return "<html><body>Done</body></html>"
        except Exception, e:
            response = werkzeug.exceptions.InternalServerError("Error: %s"%(e,))
            return response
