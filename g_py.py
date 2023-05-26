
from subprocess import run

def g_py(TARGET='main'):
    with open(f"{TARGET}.py", "w") as f:
        f.write(f'#!/usr/bin/python3\n')
        f.write('\n')
        if TARGET == 'main':
            f.write(f'if __name__ == "__{TARGET}__":\n')
            f.write(f'\tprint("Hello, world!\\n")\n')
            f.write('\n')
        else:
            f.write(f'def {TARGET}():\n')
            f.write('\tprint("Hello, world!\\n")\n')
            f.write('\n')
            f.write(f'{TARGET}()\n')

    run(["chmod", "a+x", f"{TARGET}.py"])
