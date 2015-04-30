import getpass
import platform
import sys
import ConfigParser
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
mm_file = config.get('openerp', 'mm_file')

# -----------------------------------------------------------------------------
# XMLRPC connection for autentication (UID) and proxy 
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/common' % (server, port), allow_none=True)
uid = sock.login(dbname, user, pwd)
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/object' % (server, port), allow_none=True)

for row in open(mm_file, 'r'): # loop on all rows
    row.replace(chr('0'), " ") # Accounting bug
    sock.execute(
        dbname, uid, pwd, 'lognaet.movement', 'create', {
            'name': row[60:66], # Number
            'lot': row[11:16], # Lot
            'cause': row[16:18], # Cause: 
                # 01 Del, 02 Var(Q), 03 Var(P.), 04 Var(Disc), 05 Add
            'hostname': platform.node(), # computer name
            'username': getpass.getuser(), # user name
            'document': row[58:60], # Type of doc
            'series': row[66:67], # Serial  row[16:18].replace(chr(0), ''), # Document
            'code': row[:16], # ID article
            'number': row[60:66], # Number
            'fiscalcode': row[67:69], # Fiscal code
            'date': "%s-%s-%s" % (# Date
                row[79:83], 
                row[83:85], 
                row[85:87], ,)
            'year': row[75:79].replace(chr(0), ''), # Year
            'previous': row[18:38].replace(chr(0), ''), # Previous
            'current': row[38:58].replace(chr(0), ''), # Current
            })

# Remove file:
os.delete(mm_file)
