#!/usr/bin/env python3
import argparse
import configparser
import getpass
import logging
import os
import requests
import requests_toolbelt
import sys
import urllib3

CURRENT_DIRECTORY = os.path.dirname( os.path.abspath(__file__) )
SOURCE_DIRECTORY = os.path.join( CURRENT_DIRECTORY, 'src' )
sys.path.append( SOURCE_DIRECTORY )

# https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pythopyt
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

NAME = 'ourstarter'
logger = logging.getLogger( '{}'.format(NAME) )

STARTER_HOME_DIR = '.{}'.format(NAME)
OUR_CONFIGURATION_FILE = "ourstarter.ini"
DEFAULT_CONFIGURATION = """[server]
url = https://127.0.0.1
apipath = /api/v1
verify_ssl = false"""

def make_project_homedir():
    if sys.platform == 'win32':
        user_home_dir = os.getenv( 'HOMEDRIVE', None ) + os.getenv( 'HOMEPATH', None )
    else:
        user_home_dir = os.getenv( 'HOME' )

    if not user_home_dir:
        user_home_dir = os.getcwd()

    full_path_to_project_dir = user_home_dir + os.sep + STARTER_HOME_DIR

    if not os.path.exists( full_path_to_project_dir ):
        os.mkdir( full_path_to_project_dir )
    
    return full_path_to_project_dir

def read_properties( arguments, logger ):
    our_configuration = None
    full_path_to_project_config = arguments.homedir + os.sep + arguments.configfile

    logger.info( "reading properties" )

    arguments.configfile = full_path_to_project_config
    logger.info( "full path to configuration file is {}".format(arguments.configfile) )

    if os.path.exists(full_path_to_project_config):
        our_configuration = configparser.ConfigParser()        
        our_configuration.read( full_path_to_project_config )
        logger.debug( "all read" )
        return our_configuration
    else:
        logger.info( "property file did not exist, save new default" )
        with open( full_path_to_project_config, 'w' ) as writer:
            writer.write( DEFAULT_CONFIGURATION )
            logger.debug("save") 

        our_configuration = configparser.ConfigParser()        
        our_configuration.read( full_path_to_project_config )
        logger.debug( "all read" )
        return our_configuration

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('action', metavar='ACTION', type=str, help='Specify action for {}'.format(NAME) )

    parser.add_argument('-C', '--configfile', help="Specify an alternate project configuration filename. Default is ~/.{}/{}.ini".format(NAME,NAME))

    parser.add_argument('-H', '--homedir', help="Specify an alternate data directory. Default is ~/.{}".format(NAME) )

    parser.add_argument('-L', '--loglevel', help="Specify alternate logging level. (Default is NONE)")
    
    parser.add_argument('-O', '--outputfile', help="Specify output location")

    parser.add_argument('-q', '--quiet', action='store_true', help="Supress logging. Default is FALSE") 

    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments( )

    if not arguments.configfile:
        arguments.configfile = OUR_CONFIGURATION_FILE

    if not arguments.homedir:
        arguments.homedir = make_project_homedir( )

    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=arguments.loglevel)
    logger = logging.getLogger( NAME )

    if arguments.quiet:
        logger.propagate = False

    logger.info( '{} startup'.format(NAME) )
    our_properties = read_properties( arguments, logger )
