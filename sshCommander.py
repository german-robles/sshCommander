#!/usr/bin/python
# -*- coding: utf-8 *-*

import sys
import time
import select
import paramiko
import yaml
import getpass


class SshConnector:

	def __init__(self):
		greeting = '''
		                   ____                  
		                _.' :  `._               
		            .-.'`.  ;   .'`.-.           
		   __      / : ___\ ;  /___ ; \      __  
		 ,'_ ""--.:__;".-.";: :".-.":__;.--"" _`,
		 :' `.t""--.. '<@.`;_  ',@>` ..--""j.' `;
		      `:-.._J '-.-'L__ `-- ' L_..-;'     
		        "-.__ ;  .-"  "-.  : __.-"       
		            L ' /.------.\ ' J           
		             "-.   "--"   .-"            
		            __.l"-:_JL_;-";.__           
		         .-j/'.;  ;""""  / .'\"-.        
		       .' /:`. "-.:     .-" .';  `.      
		    .-"  / ;  "-. "-..-" .-"  :    "-.   
		 .+"-.  : :      "-.__.-"      ;-._   \  
		 ; \  `.; ;                    : : "+. ; 
		 :  ;   ; ;                    : ;  : \: 
		 ;  :   ; :                    ;:   ;  : 
		: \  ;  :  ;    Welcome to    : ;  /  :: 
		;  ; :   ; :    ssh runner    ;   :   ;: 
		:  :  ;  :  ;                : :  ;  : ; 
		;\    :   ; :                ; ;     ; ; 
		: `."-;   :  ;              :  ;    /  ; 
		 ;    -:   ; :              ;  : .-"   : 
		 :\     \  :  ;            : \.-"      : 
		  ;`.    \  ; :            ;.'_..--  / ; 
		  :  "-.  "-:  ;          :/."      .'  :
		   \         \ :          ;/  __        :
		    \       .-`.\        /t-""  ":-+.   :
		     `.  .-"    `l    __/ /`. :  ; ; \  ;
		       \   .-" .-"-.-"  .' .'j \  /   ;/ 
		        \ / .-"   /.     .'.' ;_:'    ;  
		         :-""-.`./-.'     /    `.___.'   
		               \ `t  ._  /            
		                "-.t-._:'             
		'''
		print greeting
		with open("sshConfig.yaml", 'r') as ymlfile:
			cfg = yaml.load(ymlfile)
		username = (cfg['sshUser'])
		port = (cfg['sshPort'])
		host = (cfg['sshHost'])
		
		for h in host:
			host = h
			usingKeys = (cfg['usingKeys'])
			if 	usingKeys == 'yes':
				password = None
			else: 
				print '\nPlease enter password to connect with %s' % host
				password = getpass.getpass()
			self.ssh_command_runner(host, username, port, password)	



	def ssh_command_runner(self, host, username, port, password):
		with open("sshConfig.yaml", 'r') as ymlfile:
			cfg = yaml.load(ymlfile)
		command = (cfg['sshCommand'])			
		i = 1
		while True:
			print "Trying to connect to %s, user: %s, port: %s (%i/3)" % (host, username, port, i)

			try:
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(host, port, username, password)
				print "Connected to %s" % host
				break
			except paramiko.AuthenticationException:
				print "Authentication failed when connecting to %s" % host
				sys.exit(1)
			except:
				print "Could not SSH to %s, waiting for it to start" % host
				i += 1
				time.sleep(2)

			# If we could not connect within time limit
			if i == 3:
				print "Could not connect to %s. Giving up" % host
				sys.exit(1)
		for cmd in command:
			command = cmd
			# Send the command (non-blocking)
			print '\nExecuting the following command: ',command
			print '--------------------------------------------'
			stdin, stdout, stderr = ssh.exec_command(command)

			# Wait for the command to terminate
			while not stdout.channel.exit_status_ready():
			    # Only print data if there is data to read in the channel
			    if stdout.channel.recv_ready():
			        rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
			        if len(rl) > 0:
			            # Print data from stdout
			            print stdout.channel.recv(1024),

			#
			# Disconnect from the host
			#
			print "\nCommand %s execution successfuly	" % command
			print "###################### END OF COMMAND ######################"
		print "\n***______ Commands exec done, closing SSH connection______***"	
		ssh.close()	        
init = SshConnector()		