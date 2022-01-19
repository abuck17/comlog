#!/usr/bin/python3

import sys
import os
import stat
import glob
import subprocess
import argparse

comlog = os.path.expanduser("~") + "/.comlog"
logDir = "/data/comlogs"

def validPort(port):
  try:
      valid = stat.S_ISCHR(os.lstat(port)[stat.ST_MODE])
  except:
      valid = False

  if not valid:
    print("%s is not a valid port!" % port )
  return valid

def add(port):
  if validPort(port):
    comlogData = list(open(comlog, 'r'));
    for entry in comlogData:
      if entry == port:
        return 
    with open(comlog, 'a') as comlogFID:
      comlogFID.write("%s\n" % port )
  
def remove(port):
  if validPort(port):
    comlogData = list(open(comlog, 'r'));
    with open(comlog, "w") as comlogFID:
      for entry in comlogData:
        if not entry[:-1] == port:
          comlogFID.write("%s\n" % port )

def status():
  comlogData = list(open(comlog, 'r'));
  for entry in comlogData:
    deviceFiles = glob.glob("%s/%s_*" % (logDir, os.path.basename(entry)[:-1]) )
    
    latestDeviceFile = None
    if deviceFiles:
      latestDeviceFile = max(deviceFiles, key=os.path.getctime)

    writing = False
    if latestDeviceFile:
      results = subprocess.getstatusoutput("lsof +D %s 2>/dev/null | grep %s" % (logDir, latestDeviceFile))
      if results[1]:
        writing = True

    print("%s\t%s\t%s" %(entry[:-1], latestDeviceFile, str(writing)) )

def main(argv):

  if not os.path.exists(comlog):
    open(comlog, 'a').close()
    os.chmod(comlog, stat.S_IRUSR | stat.S_IWUSR)

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(dest="command")
  addParser = subparsers.add_parser("add", help="Add port to logging")
  removeParser = subparsers.add_parser("remove", help="Remove port from logging")
  statusParser = subparsers.add_parser("status", help="Display current logging")
  for parse in [addParser, removeParser]:
    parse.add_argument("port", help="Path to device port")

  args = parser.parse_args()

  if not args.command:
    parser.print_help()
  elif args.command == "add":
    add(args.port)
  elif args.command == "remove":
    remove(args.port)
  elif args.command == "status":
    status()
  else:
    parser.print_help()

if __name__ == "__main__":
  main(sys.argv[1:])
