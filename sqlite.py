#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION='''
module: sqlite
author: zatav
description: Module for manipulate sqlite databases
 
options:
  path:
    description: list of database locations
    required: yes
  state:
    description: action type (present;absent;request;dump)
    required: yes
  request:
    description: execute a list of sqlite requests (create the db if not exists)
    required: no
  dumpDir:
    description: create dumps using list of directory locations
    required: no	
'''

EXAMPLES='''
- name: "SQLITE create database file"
  sqlite:
    state: present
    path: ["/opt/test.db", "/home/user/test2.db"]	

- name: "SQLITE request"
  sqlite:
    state: request
    path: "/opt/test.db"	
    request: ["CREATE TABLE test (name TEXT, age INTEGER)", "INSERT INTO test VALUES('bob', 30)"]

- name: "SQLITE request 2"
  sqlite:
    state: request
    path: "/opt/test.db"	
    request: ["SELECT * FROM test"]
  register: result
- debug: var=result

- name: "SQLITE dump database"
  sqlite:
    state: dump
    path: "/opt/test.db"	
    dumpDir: "/home/user/"

- name: "SQLITE delete database"
  sqlite:
    state: absent
    path: ["/opt/test.db", "/home/user/test2.db"]	
'''

RETURN = '''
results:
    description: indicates if there was a change in the node in 'changed'
				 results of operations in 'result' 
				 optionnal error in 'failed'
'''

from ansible.module_utils.basic import AnsibleModule
import sqlite3 as sqlite
import os
from shutil import copy2


def run_module():
	# try to execute instructions and catch all exceptions
	# for formatting them and return them in "failed" inside the "result" list.
	# if all goes well, return results of the actions 
	# in "result" inside the "result" list.
	try:
		
		moduleArgs = dict(
				state = dict(required=True, type='str'),
				path = dict(required=True, type='list'),
				request	= dict(required=False, type='list'),
				dumpDir = dict(required=False, type='list'),
		)

		result = dict(
		    changed=False,
		    result=[]
		)

		module = AnsibleModule(
		    argument_spec=moduleArgs,
		    supports_check_mode=True
		)

		if module.check_mode:
		    module.exit_json(**result)

		dbPaths  = module.params.get('path')
		state  = module.params.get('state')

		for i in dbPaths:

			if state == "present":
				if not os.path.exists(i):
					sqlite.connect(i)	# create an empty file
					result['changed'] = True
					result['result'].append(i) # returns a list of created files

			elif state == "absent":
				if os.path.exists(i):
					os.remove(i)
					result['changed'] = True
					result['result'].append(i)  # returns a list of deleted files

			elif state == "request":	
				requests  = module.params.get('request')
				conn = sqlite.connect(i)	# also create the db
				c = conn.cursor()
				result['result'].append({i: []})	# returns a list of dict of paths and result of every request on each db (may be empty)
				for j in requests:
					c.execute(j)
					response = c.fetchall()
					result['result'][-1][i].append(response)	# form: [{pathdb : [result1, result2, ...]}, {pathdb2: [...]}]
				conn.commit() 
				conn.close()
				result['changed'] = True

			elif state == "dump":
				dumpDirs  = module.params.get('dumpDir')
				result['result'].append({i: []})	# returns a list of dict of paths and locations of dumps
				if os.path.exists(i):
					dumpName = "dump." + os.path.basename(i)
					for j in dumpDirs:
						if os.path.exists(j):
							dumpPath = os.path.join(j, dumpName)	# concatenate path and name of the dump (adapted for os)
							copy2(i, dumpPath)
							result['changed'] = True
							result['result'][-1][i].append(dumpPath)	# form: [{pathdb : [dump1, dump2, ...]}, {pathdb2: [...]}]

			else:
				raise ValueError("This state value is not supported: " + state)
		
	except Exception as e:
		module.fail_json(msg='Error - ' + str(e), **result)
	else:
		module.exit_json(**result)
 
def main():
    run_module()

if __name__ == "__main__":
	main()
