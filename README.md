This is a simple script that takes users information from a csv file and 
creates them in GitLab

Tested with GitLab 6.4.3 API v3

Requires
========
* Python
         easy\_install requests termcolor 

Usage
=====
```
usage: create_gitlab_users.py [-h] --token TOKEN --url URL users.csv

Create gitlab users from csv file, with format:
Name;Username;email;Group1,Group2,Groupn

positional arguments:
  users.csv             A csv file containing users.

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN, -t TOKEN
                        User api token
  --url URL, -u URL     API Url: http://gitlab.example.com/api/v3
```
