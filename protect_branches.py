#!/usr/bin/python
"""
  CSV format: RepoName;branches separated by ,
  RepoName is like "Jeremy / gitlab" whitespaces are removed, and case insensitive
  Branches name are urlencoded so it can be mybranch,jeremy/dev, ...

  Even if a branch is already protected, it will say OK, because it always
  return 200 if branch has protected=true

  run --help for more information

  easy_install requests termcolor 

  Tested with GitLab 6.4.3 API v3 
"""

import os
import sys
import json
import requests
import csv
import argparse
import urllib
from termcolor import colored, cprint


parser = argparse.ArgumentParser(description='Protect repositories branches with format: repo_name;branch0,branch2,..')
parser.add_argument('csv', metavar='repos.csv', 
                   help="A csv file containing repositories with branches to protect.\n")
parser.add_argument('--token', '-t', required=True, 
                   help='User api token')
parser.add_argument('--url', '-u', required=True, 
                   help='API Url: http://gitlab.example.com/api/v3')
args = parser.parse_args()

apiurl = args.url
headers = {'content-type': 'application/json', 'PRIVATE-TOKEN': args.token}

def protect_branch(repoid, branch):
    payload = {"id": repoid, "branch": branch}
    r = requests.put(apiurl + '/projects/' + str(repoid) + '/repository/branches/' + urllib.quote_plus(branch) + '/protect', data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
        jsobj = json.loads(r.text)
        if jsobj.has_key('protected') and jsobj['protected']:
            return True
    return False

def get_repo_id(repos, name):
    name = name.lower().replace(' ', '')
    if repos.has_key(name):
        return repos[name]
    return False

def get_repos():
    repos = {}
    r = requests.get(apiurl + '/projects/', headers=headers)
    if r.status_code == 200:
        jsobj = json.loads(r.text)
        for repo in jsobj:
            repos[repo['path_with_namespace']] = repo['id']
    return repos

repos = get_repos()

with open(args.csv, 'r') as csvfile:
  reporeader = csv.reader(csvfile, delimiter=';')
  for repo in reporeader:
    reponame = repo[0]
    branches = repo[1].split(',')
    
    repoid = get_repo_id(repos, reponame)
    if repoid:
        cprint("Working on repo [" + reponame + "] ", "cyan")
        for branch in branches:
            branchmsg = colored("\tProtecting branch [" + branch + "]: ", "cyan")
            if protect_branch(repoid, branch):
                print branchmsg + colored("OK", "green")
            else:
                print branchmsg + colored("FAILED", "red", attrs=['bold'])
    else:
        cprint("Repo [" + reponame + "] not found!", "red", attrs=['bold'])
