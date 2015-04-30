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
cfg_file = os.path.join(os.path.expanduser(
    os.path.join(os.path.curdir, "openerp.cfg"))
config = ConfigParser.ConfigParser()
config.read([cfg_file])

# Read parameters:
server = config.get('openerp', 'server')
port = config.get('openerp', 'port')
dbname = config.get('openerp', 'dbname')
user = config.get('openerp', 'user')
pwd = config.get('openerp', 'pwd')

# -----------------------------------------------------------------------------
# XMLRPC connection for autentication (UID) and proxy 
# -----------------------------------------------------------------------------
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/common' % (server, port), allow_none=True)
uid = sock.login(dbname, user, pwd)
sock = xmlrpclib.ServerProxy(
    'http://%s:%s/xmlrpc/object' % (server, port), allow_none=True)

if len(sys.argv) == 6:    
    pass # TODO Error wrong list of argument:    

sock.execute(
    dbname, uid, pwd, 'lognaet.movement', 'create', {
        'name': "Data %s: %s, dalle %s alle %s, Righe: %s" % (
            sys.argv[1], # type
            sys.argv[2], # account date
            sys.argv[4], # start time
            sys.argv[5], # stop time
            sys.argv[3], # number of row
            ),
        'hostname': platform.node(), # computer name
        'username': getpass.getuser(), # user name
        
        #'user': # TODO ???
        'type': sys.argv[1], # type
        'start': sys.argv[4], # start time
        'end': sys.argv[5], # end time
        #'date': sys.argv[2], # account date  TODO format
        'total': int(sys.argv[3]), # number of row
        })
