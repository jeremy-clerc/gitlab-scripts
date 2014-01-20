#!/usr/bin/python
"""
  run --help for informations

  easy_install requests termcolor 

  Tested with GitLab 6.4.3 API v3 
"""

import os
import sys
import json
import requests
import csv
import argparse
from termcolor import colored, cprint


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
Create gitlab users from csv file, with format:
    Name;Username;email;Group1,Group2,Groupn;sshkey,sshkey
SSHKey names are formed with the username and counter ex: bob1, bob2, ...       
""")

parser.add_argument('csv', metavar='users.csv', 
                   help="A csv file containing users.\n")
parser.add_argument('--token', '-t', required=True, 
                   help='User api token')
parser.add_argument('--url', '-u', required=True, 
                   help='API Url: http://gitlab.example.com/api/v3')
args = parser.parse_args()

apiurl = args.url
headers = {'content-type': 'application/json', 'PRIVATE-TOKEN': args.token}
# dummy password, users will need to do password reset
password = "WoalRoocReysIcCa"
groups = {}

def add_user_to_group(userid, groupid):
   # access_level = 30 -> Developer
    payload = {"id": groupid, "user_id": userid, "access_level": 30}
    r = requests.post(apiurl + '/groups/' + str(groupid) + '/members', data=json.dumps(payload), headers=headers)

    if r.status_code == 201:
      return True
    else:
      return False

def add_user_sshkey(userid, title, key):
    payload = {'id': userid, 'title': title, 'key': key}
    r = requests.post(apiurl + '/users/' + str(userid) + '/keys', data=json.dumps(payload), headers=headers)

    if r.status_code == 201:
      return True
    else:
      return False

# getting all groups, so we can convert name to id
r = requests.get(apiurl + '/groups/', headers=headers)
if r.status_code == 200:
  jsobj = json.loads(r.text)
  for group in jsobj:
    if group.has_key('id') and group.has_key('name'):
      groups[group['name']] = group['id']
else:
  sys.stderr.write(colored("Getting groups FAILED.", "red", attrs['bold']))
  sys.exit(1)

with open(args.csv, 'r') as csvfile:
  usersreader = csv.reader(csvfile, delimiter=';')
  for user in usersreader:
    name = user[0]
    username = user[1]
    email = user[2]
    usergroups = user[3].split(",")
    userkeys = user[4].split(",") 
    createusrmsg = colored("Creating user [" + name + "] with username [" + username + "] and email [" + email + "]: ", "cyan")
    payload = {"username": username, "email": email, "name": name,"password": password}
    r = requests.post(apiurl + '/users/', data=json.dumps(payload), headers=headers)

    if r.status_code == 201:
      print createusrmsg + colored("OK", "green")
      jsobj = json.loads(r.text)
      if jsobj.has_key('id'):
        userid = jsobj['id']
        # add user ssh keys
        for (i, key) in enumerate(userkeys, 1):
          createkeymsg = colored("\tAdding key " + str(i) + ": ", "cyan")
          if add_user_sshkey(userid, username + str(i), key):
            print createkeymsg + colored("OK", "green")
          else:
            print createkeymsg + colored("FAILED", "red", attrs=['bold'])
            
        # add user to groups
        for group in usergroups:
          creategrpmsg = colored("\tAdding user [" + name + "] to group [" + group + "]: ", "cyan")
          if add_user_to_group(userid, groups[group]):
            print creategrpmsg + colored("OK", "green")
          else:
            print creategrpmsg + colored("FAILED", "red", attrs=['bold'])
    elif r.status_code == 404:
      print createusrmsg + colored("FAILED", "red", attrs=['bold'])
    else:
      print createusrmsg + colored("UNKNOWN ERROR", "red", attrs=['bold'])
