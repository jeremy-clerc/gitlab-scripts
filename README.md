Two scripts:
* One script that takes users information from a csv file and creates them 
  in GitLab
* A second script that takes a list of project with a list of branches to 
  protect

Tested with GitLab 6.4.3 API v3, python27

Usage
=====

```
easy_install requests termcolor 
```
Create users
```
usage: create_gitlab_users.py [-h] --token TOKEN --url URL users.csv

Create gitlab users from csv file, with format:
    Name;Username;email;Group1,Group2,Groupn;sshkey,sshkey
SSHKey names are formed with the username and counter ex: bob1, bob2, ...       

positional arguments:
  users.csv             A csv file containing users.

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN, -t TOKEN
                        User api token
  --url URL, -u URL     API Url: http://gitlab.example.com/api/v3
```
Protect branches
```
usage: protect_branches.py [-h] --token TOKEN --url URL repos.csv

Protect repositories branches with format: repo_name;branch0,branch2,..

positional arguments:
  repos.csv             A csv file containing repositories with branches to
                        protect.

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN, -t TOKEN
                        User api token
  --url URL, -u URL     API Url: http://gitlab.example.com/api/v3
```
