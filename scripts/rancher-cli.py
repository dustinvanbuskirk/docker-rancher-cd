import sys
import getopt
import os
import subprocess
import time
import json

def main(argv):
  rancher_options = ''
  rancher_command = ''
  rancher_args = ''
  try:
    opts, args = getopt.getopt(argv,"o:c:a:",["help","rancher_options=","rancher_command=","rancher_args="])
  except getopt.GetoptError:
    print('Unrecognized Argument, See Usage Below.')
    print('rancher-cli.py -o "<OPTIONS>" -c "<COMMAND>" -a "<args>"')
    print('to see rancher cli help for a run rancher-cli.py help with no additional command line args')
    print('to see rancher cli help for a COMMAND run rancher-cli.py -c "<COMMAND>" -a "--help" with no additional command line args')
    sys.exit(2)
  for opt, arg in opts:
    if opt == "--help":
      print('rancher-cli.py -o <rancher_options> -c <rancher_command> -a <rancher_args>')
      print('rancher_options - arguments to pass to rancher, --debug --version')
      print('rancher_command - arguments to pass to rancher, inspect')
      print('rancher_args - COMMAND arguments to pass to rancher')
      command = ['rancher --help']
      proc = subprocess.Popen(command, shell=True)
      stdout, stderr = proc.communicate()
      sys.exit()
    elif opt in ("-o", "--rancher_options"):
      rancher_options = arg
    elif opt in ("-c", "--rancher_command"):
      rancher_command = arg
    elif opt in ("-a", "--rancher_args"):
      rancher_args = arg

  command = ['rancher ' + rancher_options + ' ' + rancher_command + ' ' + rancher_args]
  proc = subprocess.Popen(command, shell=True)
  stdout, stderr = proc.communicate()
  

if __name__ == "__main__":
  main(sys.argv[1:])