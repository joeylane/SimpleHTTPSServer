# ################################################################################################################
#
# Title: SimpleHTTPSServer
# Author: Joey Lane
# Description: A simple Python 2.7 HTTPS server module, which mimics the standard SimpleHTTPServer module.
# Tested on Kali Linux
#
# Save this script anywhere, then add the folder containing it to your PYTHONPATH:
#       export PYTHONPATH=$PYTHONPATH:/path/to/folder/with/this/script
#
# You can also add it to ~/.profile for reboot persistence using the following command:
#       echo 'export PYTHONPATH=$PYTHONPATH:/path/to/folder/with/this/script' >> ~/.profile
#
# You can execute the module with the following syntax, if no port number is specified it will assume port 8443:
#       python -m SimpleHTTPSServer <PORT NUMBER>
#
# ################################################################################################################

import BaseHTTPServer
import SimpleHTTPServer
import ssl
import subprocess
import signal
import sys
import os
import tempfile

# Signal handler to catch CTRL-C so that we can clean up properly when quitting.
def signal_handler(signal, frame):
    sys.exit(0)

# File path for our temporary SSL certificate.
pemfile = os.path.join(tempfile.gettempdir(),'SimpleHTTPSServer.pem')

# Use try/except/finally to handle any errors and cleanup after execution.
try:
    # Start listening for CTRL-C.
    signal.signal(signal.SIGINT, signal_handler)

    # If we didn't specify a port, assume port 8443.
    port = 8443
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
        
        # If a port was specified, make sure it is within the valid port range.
        if port == 0 or port > 65535:
            raise ValueError

    # Use OpenSSL to generate a temporary SSL certificate.
    print '\n[*] Generating temporary SSL certificate ...'
    with open(os.devnull, 'w') as f:
        subprocess.call(['openssl','req','-new','-x509','-keyout',pemfile,'-out',pemfile,'-days','365','-nodes','-subj','/C=US/ST=Illinois/O=test'], stdout=f, stderr=f)

    # Start the web server and wait for incoming connections.
    httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', int(port)), SimpleHTTPServer.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket (httpd.socket, server_side=True, certfile=pemfile)
    print '[*] Serving HTTPS on 0.0.0.0 port ' + str(port) + ' ...\n'
    httpd.serve_forever()

# Catch the ValueError exception which occurrs when an invalid port is specified, and notify the user.
except ValueError:
    print '\n[!] ERROR: You must specify a valid port!\n'
    sys.exit(0)

# Catch the SystemExit exception which occurs when we hit CTRL-C, and suppress the exception output.
except SystemExit:
    pass

# Catch all other exceptions and report them, then abort.
except:
    print sys.exc_info()[0]
    sys.exit(0)

# Cleanup when the program terminates, remove the SSL certificate from the /tmp directory if it was successfully created.
finally:
    if os.path.isfile(pemfile):
        print '\n\n[*] Removing temporary SSL certificate ...\n[*] Done!\n'
        os.remove(pemfile)


