import subprocess
import time

django = subprocess.Popen(['python', 'manage.py', 'runserver'])
api = subprocess.Popen(['gunicorn', '-w 4', '-b', 'localhost:3000', '--chdir', 'search-api', 'web:app' ])

print("Starting django server and api server")
print("Shutdown all servers with CONTROl-C\n")
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        django.kill()
        api.kill()
        break