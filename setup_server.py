from plugin_jm_server import *

# https
server = JmServer(
    'B:\\manga\\JMComic',
    'password',
)
server.run(
    host='0.0.0.0',
    port=443,
    ssl_context='adhoc',
)