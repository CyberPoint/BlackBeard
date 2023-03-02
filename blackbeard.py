#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import urllib3

CURRENT_DIRECTORY = os.path.dirname( os.path.abspath(__file__) )
SOURCE_DIRECTORY = os.path.join( CURRENT_DIRECTORY, 'src' )
sys.path.append( SOURCE_DIRECTORY )

# https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pythopyt
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

NAME = 'BLACKBEARD'
logger = logging.getLogger( '{}'.format(NAME) )

from github import Github

def ransom(token, organization, readme):
    g = Github(token)
    repos = g.get_organization(organization).get_repos()
    for repo in repos:
        print(repo.name)

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('action', metavar='ACTION', type=str, help='Specify action for {}'.format(NAME) )

    parser.add_argument('-L', '--loglevel', help="Specify alternate logging level. (Default is NONE)")
    
    parser.add_argument('-t', '--token', help="Github token to use.", required=True)

    parser.add_argument('-o', '--organization', help="Github organization to attack", required=True)

    parser.add_argument('-R', '--readme', help="Filename of README to pass in.  Defaults to badREADME.md as README.md", default="./badREADME.md")

    parser.add_argument('-q', '--quiet', help="Enable quiet mode for logging.")
    
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments( )

    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=arguments.loglevel)
    logger = logging.getLogger( NAME )

    if arguments.quiet:
        logger.propagate = False

    logger.info( '{} startup'.format(NAME) )


