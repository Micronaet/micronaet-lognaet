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


{
    'name': 'Lognaet',
    'category': 'Log',
    'description':"""
        Log accounting program for control and statistics.
        Collage: 21 > movement
        Collage: 90 > orders
        """,
    'version': '0.1',
    'depends': [],
    'js': [],
    'css': [],
    'data': [
        'security/lognaet_group.xml',
        'security/ir.model.access.csv',
        'lognaet_view.xml',
        ],
    'auto_install': False,
    'web_preload': False,
    'application': True,
    }
