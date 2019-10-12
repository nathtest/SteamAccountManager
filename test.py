import subprocess
import os

FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
login = 'RaptorJesusIII'
password = 'WzpaeU4}A.>%~ruk'
args = r"C:\Program Files (x86)\Steam\Steam.exe -login" + " " + login + " " + password + ""
subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

