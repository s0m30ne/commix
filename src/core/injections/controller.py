#!/usr/bin/env python
# encoding: UTF-8

"""
 This file is part of commix (@commixproject) tool.
 Copyright (c) 2015 Anastasios Stasinopoulos (@ancst).
 https://github.com/stasinopoulos/commix

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 For more see the file 'readme/COPYING' for copying permission.
"""

import os
import sys
import time
import datetime

from src.utils import menu
from src.utils import colors
from src.utils import settings

from src.core.requests import authentication

from src.core.injections.results_based.techniques.classic import cb_handler
from src.core.injections.results_based.techniques.eval_based import eb_handler
from src.core.injections.blind_based.techniques.time_based import tb_handler
from src.core.injections.semiblind_based.techniques.file_based import fb_handler 

"""
 Command Injection and exploitation controler.
 Checks if the testable parameter is exploitable.
"""

def do_check(url):

  # Print the findings to log file.
  parts = url.split('//', 1)
  host = parts[1].split('/', 1)[0]
  try:
      os.stat(settings.OUTPUT_DIR + host + "/")
  except:
      os.mkdir(settings.OUTPUT_DIR + host + "/") 
  
  filename = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')
  filename = settings.OUTPUT_DIR + host + "/" + filename
  output_file = open(filename + ".txt", "a")
  output_file.write("\n(+) Host : " + host)
  output_file.write("\n(+) Date : " + datetime.datetime.fromtimestamp(time.time()).strftime('%m/%d/%Y'))
  output_file.write("\n(+) Time : " + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S'))
  output_file.close()

  # Check if defined "--delay" option.
  if menu.options.delay:
    delay = menu.options.delay
  else:
    delay = settings.DELAY
      
  # Do authentication if needed.
  if menu.options.auth_url and menu.options.auth_data:
    authentication.auth_process()
	    
  elif menu.options.auth_url or menu.options.auth_data: 
    print colors.BGRED + "(x) Error: You must specify both login panel URL and login parameters.\n" + colors.RESET
    sys.exit(0)
    
  else:
    pass
  
  # Check if HTTP Method is POST.
  if not menu.options.data:
    http_request_method = "GET"
  else:
    http_request_method = "POST"
    parameter = menu.options.data

  # Check if it is vulnerable to classic command injection technique.
  if menu.options.tech == "classic":
    if cb_handler.exploitation(url,delay,filename,http_request_method) == False:
      if http_request_method == "GET":
	print colors.BGRED + "(x) The '"+ url +"' appear to be not injectable." + colors.RESET
      else:
	print colors.BGRED + "(x) The '"+ parameter +"' appear to be not injectable." + colors.RESET
    print "(*) The scan has finished successfully!"
    print "(*) Results can be found at : '" + os.getcwd() + "/" + filename +".txt' \n"
    sys.exit(0)
    
  # Check if it is vulnerable to eval-based command injection technique.
  elif menu.options.tech == "eval-based":
    if eb_handler.exploitation(url,delay,filename,http_request_method) == False:
      if http_request_method == "GET":
	print colors.BGRED + "(x) The '"+ url +"' appear to be not injectable." + colors.RESET
      else:
	print colors.BGRED + "(x) The '"+ parameter +"' appear to be not injectable." + colors.RESET
    print "(*) The scan has finished successfully!"
    print "(*) Results can be found at : '" + os.getcwd() + "/" + filename +".txt' \n"
    sys.exit(0)
    
  # Check if it is vulnerable to time-based blind command injection technique.
  elif menu.options.tech == "time-based":
    if tb_handler.exploitation(url,delay,filename,http_request_method) == False:
      if http_request_method == "GET":
	print colors.BGRED + "(x) The '"+ url +"' appear to be not injectable." + colors.RESET
      else:
	print colors.BGRED + "(x) The '"+ parameter +"' appear to be not injectable." + colors.RESET
    print "(*) The scan has finished successfully!"
    print "(*) Results can be found at : '" + os.getcwd() + "/" + filename +".txt' \n"
    sys.exit(0)
    
  # Check if it is vulnerable to file-based semiblind command injection technique.
  elif menu.options.tech == "file-based":
    if fb_handler.exploitation(url,delay,filename,http_request_method) == False:
      if http_request_method == "GET":
	print colors.BGRED + "(x) The '"+ url +"' appear to be not injectable." + colors.RESET
      else:
	print colors.BGRED + "(x) The '"+ parameter +"' appear to be not injectable." + colors.RESET
    print "(*) The scan has finished successfully!"
    print "(*) Results can be found at : '" + os.getcwd() + "/" + filename +".txt' \n"
    sys.exit(0)
  
  else:
    # Automated command injection and exploitation.
    if cb_handler.exploitation(url,delay,filename,http_request_method) == False:
	classic_state = False
    else:
      classic_state = True
      
    if eb_handler.exploitation(url,delay,filename,http_request_method) == False:
      eval_based_state = False
    else:
      eval_based_state = True
      
    if tb_handler.exploitation(url,delay,filename,http_request_method) == False:
      time_based_state = False
    else:
      time_based_state = True
      
    if fb_handler.exploitation(url,delay,filename,http_request_method) == False:
      file_based_state = False
    else:
      file_based_state = True

    if classic_state == False and eval_based_state == False and time_based_state == False and file_based_state == False :
      if http_request_method == "GET":
	print colors.BGRED + "(x) The '"+ url +"' appear to be not injectable." + colors.RESET
      else:
	print colors.BGRED + "(x) The '"+ parameter +"' appear to be not injectable." + colors.RESET
	    
  print "\n(*) The scan has finished successfully!"
  print "(*) Results can be found at : '" + os.getcwd() + "/" + filename +".txt' \n"
  sys.exit(0)
  
#eof