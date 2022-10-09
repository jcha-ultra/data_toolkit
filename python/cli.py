# run cli command
import os
os.system('some cli command')

# get list of files tracked by git in current project
import subprocess
tracked_files = list(map(lambda b: b.decode('utf-8'), subprocess.check_output('git ls-files', shell=True).splitlines()))
