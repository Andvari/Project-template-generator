
def g_settings(LANG='c'):
    with open(".vscode/settings.json", "w") as f:
        f.write('{\n')
        f.write('\t"files.exclude": {\n')
        f.write('\t\t"**/.git*": true,\n')
        if LANG in ['c', 'cpp', 'v']:
            f.write('\t\t"**/build": true,\n')
        f.write('\t}\n')
        f.write('}\n')
