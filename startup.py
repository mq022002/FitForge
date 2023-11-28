import subprocess
import time

django = subprocess.Popen(['python', 'manage.py', 'runserver'])
#api = subprocess.Popen(['gunicorn', '-w 1', '-b', 'localhost:3000', '--chdir', 'search-api', 'web:app' ])
api = subprocess.Popen(['python', 'search-api/web.py'])

print("Starting django server and api server")
print("Shutdown all servers with CONTROl-C\n")
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        django.kill()
        api.kill()
        break