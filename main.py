#!/usr/bin/python3

from subprocess import run
from sys import argv
'''
from sys import path
path.append('.')
'''

from g_makefile import g_makefile
from g_tasks import g_tasks
from g_py import g_py
from g_venv import g_venv
from g_settings import g_settings

KNOWN_LANGS = ['py', 'c', 'cpp', 'v']

if __name__ == '__main__':
    TARGET = ''
    LANG = ''
    for arg in argv[1:]:
        a = arg.split('=')
        if a[0] == 'TARGET':
            TARGET = a[1]
            print(f'TARGET: {TARGET}')
        elif a[0] == 'LANG' and a[1] in KNOWN_LANGS:
            LANG = a[1]
            print(f'LANG: {LANG}')
    
    if TARGET == '':
        print('Warning: TARGET not specified. Set default to "main"')
        TARGET = 'main'

    if LANG == '':
        print('Warning: LANG not specified. Set default to "C"')
        LANG = 'c'

    run(["mkdir", "-p", ".vscode"])

    g_makefile(TARGET=TARGET, LANG=LANG)

    g_tasks(TARGET=TARGET, LANG=LANG)

    g_settings(LANG=LANG)

    if LANG in ['c', 'cpp', 'v']:
        run(["mkdir", "-p", "build"])
        run(["mkdir", "-p", "src"])

        if LANG in ['c', 'cpp']:
            with open(".vscode/c_cpp_properties.json", "w") as f:
                f.write('{\n')
                f.write('\t"configurations":\n')
                f.write('\t[\n')
                f.write('\t\t{\n')
                f.write('\t\t"name": "Default",\n')
                f.write('\t\t"includePath": [\n')
                f.write('\t\t\t"/usr/include/**"\n')
                f.write('\t\t],\n')
                f.write('\t\t"defines": [],\n')
                f.write('\t\t"cStandard": "c99",\n')
                f.write('\t\t"cppStandard": "c++98",\n')
                f.write('\t\t}\n')
                f.write('\t],\n')
                f.write('\t"version": 4\n')
                f.write('}\n')

            with open(f"src/{TARGET}.{LANG}", "w") as f:
                f.write('#include<stdio.h>\n\n')
                f.write(f'#include "{TARGET}.h"\n\n')
                f.write('int main(){\n')
                f.write('    printf("Hello, world!\\n");\n')
                f.write('}\n')

            with open(f"src/{TARGET}.h", "w") as f:
                f.write(f'#ifndef _{TARGET.upper()}_H_\n')
                f.write(f'#define _{TARGET.upper()}_H_\n\n')
                f.write(f'#endif /* _{TARGET.upper()}_H_ */\n')
        else:
            with open(f'src/{TARGET}.c', 'w') as f:
                f.write('#include <vpi_user.h>\n')
                f.write('\n')
                f.write('void register_interface(void);\n')
                f.write('\n')
                f.write('void register_interface(){\n')
                f.write('\ts_vpi_systf_data tf_data;\n')
                f.write('\ttf_data.type = vpiSysTask;\n')
                f.write('\ttf_data.sysfunctype = vpiIntFunc;\n')
                f.write('\ttf_data.compiletf = 0;\n')
                f.write('\ttf_data.sizetf = 0;\n')
                f.write('\ttf_data.user_data = 0;\n')
                f.write('\n')
                f.write('\tvpi_register_systf(&tf_data);\n')
                f.write('}\n')
                f.write('\n')
                f.write('void (*vlog_startup_routines[])() = { register_interface, 0 };\n')

            with open(f'src/{TARGET}.v', "w") as f:
                f.write('`timescale 1ns / 1ps\n')
                f.write('\n')
                f.write(f'module {TARGET}();\n')
                f.write('/*\n')
                f.write('initial\n')
                f.write('begin\n')
                f.write('\n')
                f.write('end\n')
                f.write('\n')
                f.write('always@\n')
                f.write('begin\n')
                f.write('\n')
                f.write('end\n')
                f.write('*/\n')
                f.write('endmodule\n')
                
            with open(f'src/top.v', "w") as f:
                f.write('`timescale 1ns / 1ps\n')
                f.write('\n')
                f.write(f'`include "src/{TARGET}.v"\n')
                f.write('\n')
                f.write('module top();\n')
                f.write('logic clk;\n')
                f.write('logic reset;\n')
                f.write('\n')
                f.write(f'{TARGET} {TARGET}_test_1();\n')
                f.write('\n')
                f.write('initial\n')
                f.write('begin\n')
                f.write('\treset = 1\'b0;\n')
                f.write('\t#100 reset = 1\'b1;\n')
                f.write('end\n')
                f.write('\n')
                f.write('initial\n')
                f.write('begin\n')
                f.write('\tclk = 1\'b1;\n')
                f.write('\t#0.5 clk = ~clk;\n')
                f.write('end\n')
                f.write('\n')
                f.write('initial\n')
                f.write('repeat(10)\n')
                f.write('begin\n')
                f.write('\t//$monitor("", );\n')
                f.write('end\n')
                f.write('\n')
                f.write('initial\n')
                f.write('#1000 $finish;\n')
                f.write('\n')
                f.write('initial\n')
                f.write('begin\n')
                f.write('\t$dumpfile("out.vcd");\n')
                f.write('\t$dumpvars(0, top);\n')
                f.write('end\n')
                f.write('endmodule\n')
                
    elif LANG in ['py']:
        g_venv()
        g_py(TARGET=TARGET)
