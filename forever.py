from subprocess import Popen
import sys
import time
filename = sys.argv[1]

while True:
    print("\nStarting " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()
    time.sleep(120)

