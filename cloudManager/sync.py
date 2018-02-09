
"""
reference: https://docs.openstack.org/python-novaclient/pike/reference/api/index.html
"""
VERSION = "2.0"
USERNAME = "facebook10154155422496882"
PASSWORD = "FJBRk7OofgnES5xt"
PROJECT_ID = "facebook10154155422496882"
AUTH_URL = "http://8.43.86.2:5000/v2.0"


with client.Client("2.0", USERNAME, PASSWORD,PROJECT_ID, AUTH_URL) as nova:
    print (nova.servers.list())
    print (nova.flavors.list())

