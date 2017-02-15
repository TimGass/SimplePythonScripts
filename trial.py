import subprocess

stream = subprocess.Popen("ls", stdout=subprocess.PIPE)
for stdout_line in iter(stream.stdout.readline, ""):
    print(stdout_line)
stream.stdout.close()
