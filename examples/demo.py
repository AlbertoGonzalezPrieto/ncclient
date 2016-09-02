from ncclient.operations.rpc import *
from ncclient.xml_ import *
from ncclient import manager
from ncclient.operations.subscribe import *
from datetime import *
import time
import re
from lxml import objectify, etree

# import to subscribe.py
from dateutil import parser

# CREATE = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
# <aaa xmlns="http://tail-f.com/ns/aaa/1.1">
# <authentication> <users> <user xc:operation="create">
# <name>bob</name> <uid>42</uid> <gid>42</gid>
# <password>*</password> <ssh_keydir/> <homedir/>
# </user></users></authentication></aaa></config>"""
# DELETE = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
# <aaa xmlns="http://tail-f.com/ns/aaa/1.1">
# <authentication> <users> <user xc:operation="delete">
# <name>bob</name> </user></users></authentication></aaa></config>"""

CREATE = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
<devices xmlns="http://tail-f.com/ns/ncs">
<device xc:operation="create"><name>ToR2</name><address>1.3.3.7</address>
<port>10023</port><ssh><host-key><algorithm>ssh-dss</algorithm><key-data>AAAAB3NzaC1kc3MAAACBAN79ur5pT8cJ6N+XOJsIr/qpUnSBNoQqUVNwx3KgAmkmxLYJb/cB
w18grvzQmAFrJoAJx2gRU1ujDf0aboS+GKQsGyqT8SLPutMc5XX5cJDBs8cSlae2v6FuHL0e
YEuv+fce+MbkOTz0oBxPqDGazFVm9WHutroJ5VcMO84HHnpbAAAAFQC3m8RQvYDAFWIClV96
NM1WcZz4JQAAAIA9OM4gy7UCeUbkDFqbzN3nDbxtlRhycY8CYKkd0B1AsnOVOFRjE78dCckQ
08cDYgZ9FTRLXN3Agvr0GepnMkrUY2C49qoJsv0vTBLCdYMNrxPDapCzDEbxgxRrzbLBOFe1
aPq7uxRVy0vMD9BGcs/dPGCrtEi5QtPFu+OAcG9i9wAAAIAaaB8UtHmYqUx/dSQFnEGNPiha
rUTPqywUd583MeqkkVh/eldmlTBD9bFxVe+aa7WtxtrJNFxDNR6QXkPy7JHcIRkWLh1Skm4n
KQlmLRtWx0lLs7igKL28ZiN+Pg/TQc/6WXzz+5QlR/c0TSXx1b/lcE8VBDE2sHAriIvsW/bl
cw==</key-data></host-key></ssh><authgroup>default</authgroup><device-type>
<cli><ned-id xmlns:cisco-nx-id="http://tail-f.com/ned/cisco-nx-id">cisco-nx-id:cisco-nx</ned-id></cli></device-type><state><admin-state>unlocked</admin-state></state>
</device></devices></config>"""

DELETE = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
<devices xmlns="http://tail-f.com/ns/ncs">
<device xc:operation="delete"><name>ToR2</name><address>1.3.3.7</address>
</device></devices></config>"""

def callback(notification):
	# root = to_ele(notification)
	# print type(parser.parse(root[0].text)), root[0].text
	# print "notificationComplete" in root[1].tag, root[1].tag
	print notification

def errback(ex):
	pass

update_manager = manager.connect(host="127.0.0.1", port=2022,
	username="admin", password="admin",
	hostkey_verify=False, look_for_keys=False,
	allow_agent=False)

subscribed_manager = manager.connect(host="127.0.0.1", port=2022,
	username="admin", password="admin",
	hostkey_verify=False, look_for_keys=False,
	allow_agent=False)

try:
	update_manager.edit_config(target='running', config=DELETE)
except:
	pass
print subscribed_manager.create_subscription(callback, errback,
	manager=subscribed_manager)

update_manager.edit_config(target='running', config=CREATE)
time.sleep(40)
update_manager = manager.connect(host="127.0.0.1", port=2022,
	username="admin", password="admin",
	hostkey_verify=False, look_for_keys=False,
	allow_agent=False)
update_manager.edit_config(target='running', config=DELETE)

# print manager.connect(host="127.0.0.1", port=2022,
# 	username="admin", password="admin",
# 	hostkey_verify=False, look_for_keys=False,
# 	allow_agent=False).create_subscription(
# 	callback, errback)

# start_time = datetime.now() - timedelta(seconds=1)
# stop_time = datetime.now() + timedelta(seconds=1)

# root_filter = etree.Element('filter')
# devices_filter = etree.Element(qualify('devices', "http://tail-f.com/ns/ncs"))
# device_filter = etree.Element('device')
# root_filter.append(devices_filter)
# devices_filter.append(device_filter)
# device_filter.append(etree.Element('name'))
# print subscribed_manager.get_config("running", root_filter)
# print subscribed_manager.get_config("running",
# 	filter=('subtree', "<devices><device><name></name></device></devices>"))
# print subscribed_manager.get_config("running",
# 	filter="<filter><devices><device><name></name></device></devices></filter>")
# print subscribed_manager.get_config("running", filter=('xpath', '/devices/device/name'))

# # print subscribed_manager.create_subscription(callback, errback,
# # 	stream='ncs-events', start_time=start_time, stop_time=stop_time)
# # time.sleep(3)

# subscribed_manager.close_manager()
# update_manager.close_manager()