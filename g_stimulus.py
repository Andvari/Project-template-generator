#!/usr/bin/python3

from os.path import abspath
from re import compile

def parse_parameters(string_to_search='', title=''):
    parameters = []
    for parameter in compile(f'{title} *(.*?)[=;]').findall(string_to_search):
        if parameter[:4] == 'reg ':
            parameter = parameter[4:]
        elif parameter[:5] == 'wire ':
            parameter = parameter[5:]

        parameters.append(parameter.strip())
    return parameters

target = 'src/' + abspath('.').split('/')[-1] + '.v'
print(target)

with open(target, "r") as f, open('src/stimulus.v', "w") as g:
    text = f.read().replace('\r', '').replace('\n','')

    modules = compile('module *(.*?)endmodule').findall(text)
    module = modules[0]
    module_name = module[:module.find('(')]
    print(module_name)

    parameters = []
    input_parameters = []
    output_parameters = []
    inout_parameters = []

    g.write('`timescale 1ns / 1ps\n\n')
    g.write(f'`include "{target}"\n\n')
    g.write('module stimulus();\n\n')

    for parameter in parse_parameters(module, 'parameter'):
        g.write(f'parameter {parameter}=;\n')
        parameters.append(parameter)
    g.write('\n'*(len(parameters)!=0))

    for parameter in parse_parameters(module, 'input'):
        g.write(f'reg {parameter};\n')
        input_parameters.append(parameter[parameter.rfind(' ')+1:])
    g.write('\n'*(len(input_parameters)!=0))

    for parameter in parse_parameters(module, 'output'):
        g.write(f'wire {parameter};\n')
        output_parameters.append(parameter[parameter.rfind(' ')+1:])
    g.write('\n'*(len(output_parameters)!=0))

    for parameter in parse_parameters(module, 'inout'):
        g.write(f'reg {parameter};\n')
        inout_parameters.append(parameter[parameter.rfind(' ')+1:])
    g.write('\n'*(len(inout_parameters)!=0))
        
    g.write(f'{module_name}\n')
    if(len(parameters)):
        g.write('\t#(\n\t')
        g.write(',\n\t'.join([f'.{p}({p})' for p in parameters]))
        g.write('\n\t)\n')
    g.write(f'\t{module_name}_test\n\t')
    if len(input_parameters) or len(output_parameters) or len(inout_parameters):
        g.write('(\n\t')
        g.write(',\n\t'.join([f'.{p}({p})' for p in input_parameters+output_parameters+inout_parameters]))
        g.write('\n\t);\n')

    g.write('\n')
    if 'clk' in input_parameters:
        g.write('initial\n')
        g.write('begin\n')
        g.write('\tclk = 1\'b1;\n')
        g.write('\t#0.5 clk = ~clk;\n')
        g.write('end\n')
        g.write('\n')

    g.write('initial\n')
    g.write('repeat(10)\n')
    g.write('begin\n')
    g.write('\t$monitor("%4t' + '\\b'*len(input_parameters+output_parameters+inout_parameters) + '", $time, ' + ", ".join(input_parameters+output_parameters+inout_parameters) + ');\n')
    g.write('end\n')
    g.write('\n')
    g.write('initial\n')
    g.write('#1000 $finish;\n')
    g.write('\n')
    g.write('initial\n')
    g.write('begin\n')
    g.write('\t$dumpfile("out.vcd");\n')
    g.write('\t$dumpvars(0, stimulus);\n')
    g.write('end\n')
    g.write('endmodule\n')
