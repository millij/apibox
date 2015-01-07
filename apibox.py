#!/usr/bin/python

"""
API Box Launcher.

Sample usage to launch mock API server:

    with a specified port (default - 5000):
      apibox.py -p <port_number>

    with a api config file (default file type - JSON)
      apibox.py -f <path_to_file> -t <file_content_type>

    with user interface enabled:
      apibox.py -ui

"""

import logging as log
import sys
import getopt
import argparse

from apibox.ui.server import UIServer
from apibox.server import *

def verify_virtualenv():
    'Verifies the virtual environment.'

    # TODO verify dependencies
    pass


def process_arguments(args):
    """
    Entry point of the project. Parses args and processes.
    :param argv: commandline arguments.
    """
    port = args.port


    file_path = args.file
    file_type = args.type

    enable_ui = args.ui
    verbose = args.verbosity

    # launch APP server from file
    if file_path:
        launch_app_server_from_file(port, file_path, file_type)

    # Launch the UI server 
    if enable_ui:
        ui_server = UIServer()
        ui_server.start()

    # TODO Handle verbosity


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    #parser.add_argument("cmd")
    #parser.add_argument("-h", "--host", default="0.0.0.0", help="Server hostname")
    parser.add_argument("-p", "--port", action="store", type=int, default=5000, help="Server port")
    parser.add_argument("-ui", "--ui", action="store_true", default=False, help="Initiate the server with UI")
    parser.add_argument("-f", "--file", action="store", required=False, help="RESTful api configuration file")
    parser.add_argument("-t", "--type", action="store", default="JSON", help="Configuration file type")
    parser.add_argument("-v", "--verbosity", action="store_true", default=False, help="Increase output verbosity")

    args = parser.parse_args()

    # Verify vitual environment settings
    verify_virtualenv()

    # Process the arguments and start the necessary services accordingly.
    process_arguments(args)


