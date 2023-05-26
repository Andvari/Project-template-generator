
def g_tasks(TARGET='main', LANG='c'):

    with open(".vscode/tasks.json", "w") as f:
        f.write('{\n')
        f.write('"version": "2.0.0",\n')
        f.write('"tasks":\n')
        f.write('\t[\n')
        f.write('\t\t{\n')
        f.write('\t\t\t"label": "Run",\n')
        if LANG in ['c', 'cpp', 'v']:
            f.write(f'\t\t\t"command": "{TARGET}",\n')
        elif LANG in ['py']:
            f.write(f'\t\t\t"command": "python3 {TARGET}.py",\n')

        f.write('\t\t\t"type": "shell",\n')
        f.write('\t\t\t"group": "build",\n')
        if LANG in ['c', 'cpp', 'v']:
            f.write('\t\t\t"options": {"cwd": "build"}\n')
        else:
            f.write('\t\t\t"options": {"cwd": "."}\n')
        f.write('\t\t},\n')
        if LANG in ['c', 'cpp', 'v']:
            f.write('\t\t{\n')
            f.write(f'\t\t\t"label": "{TARGET}",\n')
            f.write(f'\t\t\t"command": "make {TARGET}",\n')
            f.write('\t\t\t"type": "shell",\n')
            f.write('\t\t\t"group": "build",\n')
            f.write('\t\t\t"options": {"cwd": "."}\n')
            f.write('\t\t},\n')
            f.write('\t\t{\n')
            f.write('\t\t\t"label": "Build",\n')
            f.write('\t\t\t"command": "make",\n')
            f.write('\t\t\t"type": "shell",\n')
            f.write('\t\t\t"group": "build",\n')
            f.write('\t\t\t"options": {"cwd": "."}\n')
            f.write('\t\t},\n')
            f.write('\t\t{\n')
            f.write('\t\t\t"label": "Clean",\n')
            f.write('\t\t\t"command": "make clean",\n')
            f.write('\t\t\t"type": "shell",\n')
            f.write('\t\t\t"group": "build",\n')
            f.write('\t\t\t"options": {"cwd": "."}\n')
            f.write('\t\t},\n')
        f.write('\t]\n')
        f.write('}\n')

