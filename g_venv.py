
from subprocess import run

def g_venv():
    with open("venv.sh", "w") as f:
        f.write('#!/bin/bash\n\n')
        f.write('virtualenv venv\n')
        f.write('source venv/bin/activate\n')
        f.write('pip freeze >requirements.txt\n')
        f.write('deactivate\n')
        f.write('#pip install -r requirements.txt\n')

    run(["chmod", "a+x", "venv.sh"])
