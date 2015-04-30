import getpass
import platform
import sys
import os
import ConfigParser
import xmlrpclib
from datetime import datetime

# -----------------------------------------------------------------------------
#                                Parameters
# -----------------------------------------------------------------------------
# Config file:
cfg_file = os.path.join(os.path.expanduser("openerp.cfg"))
config = ConfigParser.ConfigParser()
config.read([cfg_file])

# Read parameters:
server = config.get('openerp', 'server')
port = config.get('openerp', 'port')
dbname = config.get('openerp', 'dbname')
user = config.get('openerp', 'user')
pwd = config.get('openerp', 'pwd')
mm_file = config.get('mexal', 'mm_file')

# -----------------------------------------------------------------------------
# XMLRPC connection for autentication (UID) and proxy 
# -----------------------------------------------------------------------------
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/common' % (server, port), allow_none=True)
uid = sock.login(dbname, user, pwd)
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/object' % (server, port), allow_none=True)

for row in open(mm_file, 'r'): # loop on all rows
    row = row.replace(chr(0), ' ') # Accounting bug
    
    document = row[58:60].strip() # Type of doc
    sock.execute(
        dbname, uid, pwd, 'lognaet.movement', 'create', {
            'name': "%s/%s:%s" % (
                document,
                row[66:67].strip(), # Serial
                row[60:66].strip(), # Number
                ),
            'cause': row[16:18].strip(), # Cause: 
                # 01 Del, 02 Var(Q), 03 Var(P.), 04 Var(Disc), 05 Add
            'hostname': platform.node(), # computer name
            'username': getpass.getuser(), # user name
            'document': document,
            #'series': series,
            #'number': number
            'article': row[:16].strip(), # ID article
            'lot': row[11:16].strip(), # Lot
            'code': row[67:65].strip(), # Partner code
            'date': "%s-%s-%s" % (# Date
                row[79:83], 
                row[83:85], 
                row[85:87], ),
            'year': row[75:79].strip(), # Year
            'previous': row[18:38].strip(), # Previous
            'current': row[38:58].strip(), # Current
            })

# Remove file:
os.delete(mm_file)
