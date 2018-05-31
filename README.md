# SimpleHTTPSServer

A python module which serves content over HTTPS using a temporary SSL certificate. This module mimics the functionality of the native python SimpleHTTPServer.

## Installation

Save this script anywhere, then add the folder containing it to your PYTHONPATH:

    export PYTHONPATH=$PYTHONPATH:/path/to/folder/with/this/script

You can also add it to ~/.profile for reboot persistence using the following command:

    echo 'export PYTHONPATH=$PYTHONPATH:/path/to/folder/with/this/script' >> ~/.profile

## How to use

You can execute the module with the following syntax, if no port number is specified it will assume port 8443:

    python -m SimpleHTTPSServer <PORT NUMBER>