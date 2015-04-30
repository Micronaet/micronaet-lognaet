# -*- coding: utf-8 -*-
###############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2001-2015 Micronaet S.r.l. (<http://www.micronaet.it>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import os
import sys
import logging
import openerp
import openerp.netsvc as netsvc
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, expression, orm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT, 
    DEFAULT_SERVER_DATETIME_FORMAT, 
    DATETIME_FORMATS_MAP, 
    float_compare)


_logger = logging.getLogger(__name__)

class LognaetMovement(orm.Model):
    ''' Default object for manage movement modifications
    '''    
    _name = 'lognaet.movement'
    _description = 'Log movement'
    
    _columns = {
        'name': fields.char('Reference', size=50),
        'cause': fields.selection([
            ('01', 'Delete'),
            ('02', 'Variation (Q)'),
            ('03', 'Variation (Price)'),
            ('04', 'Variation (Discount)'),
            ('05', 'Add'),
            ], 'Cause'),
        'lot': fields.char('Lot', size=18),
        'hostname': fields.char('Hostname', size=30),
        'username': fields.char('Username', size=30),
        'document': fields.char('Document', size=15),
        'series': fields.char('Series', size=2),
        'code': fields.char('Code', size=20),
        'number': fields.char('Number', size=15),
        'fiscalcode': fields.char('Fiscalcode', size=21),
        'date': fields.date('Date'),
        'year': fields.char('Lot', size=4),
        'timestamp': fields.char('Timestamp', size=15),
        'previous': fields.char('Previous', size=15),
        'current': fields.char('Current', size=15),
        }
        
    _defaults = {
        'timestamp': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
        }    
    
class LognaetOrder(orm.Model):
    ''' Default object for manage order statistics
    '''
    
    
