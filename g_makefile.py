
def g_makefile(TARGET='main', LANG='c'):
    CC='/usr/bin/gcc'
    CC_VERILOG=''
    SIM=''
    if LANG in ['v']:
        CC_VERILOG = 'iverilog'
        SIM = 'vvp'

    with open('makefile', "w") as f:
        f.write(f'TARGET={TARGET}\n')
        f.write('BUILDDIR=build\n')
        f.write('SRCDIR=src\n')
        f.write('\n')
        f.write('MAKE=make\n')
        f.write('RM=rm\n')
        f.write('MV=mv\n')
        f.write(f'CC={CC}\n')
        f.write(f'CC_VERILOG={CC_VERILOG}\n')
        f.write(f'SIM={SIM}\n')
        f.write('\n')
        if LANG in ['c', 'cpp']:
            f.write(f'SOURCES=$(wildcard $(SRCDIR)/*.{LANG})\n')
            f.write('HEADERS=$(wildcard $(SRCDIR)/*.h)\n')
            f.write(f'OBJFILES=$(addprefix $(BUILDDIR)/, $(patsubst %.{LANG}, %.o, $(notdir $(SOURCES))))\n')
            f.write('\n')
            f.write(f'{TARGET}: $(BUILDDIR)/{TARGET}\n')
            f.write('\n')
            f.write(f'$(BUILDDIR)/{TARGET}: $(OBJFILES)\n')
            f.write('\t$(CC) -o $@ $^\n')
            f.write('\n')
            f.write(f'$(BUILDDIR)/%.o: $(SRCDIR)/%.{LANG} $(SRCDIR)/%.h\n')
            f.write(f'\t$(CC) -c -o $@ $(SRCDIR)/$*.{LANG}\n')
            f.write('\n')
            f.write('clean:\n')
            f.write('\t$(RM) -f $(BUILDDIR)/*\n')
        elif LANG in 'v':
            f.write('$(TARGET): $(BUILDDIR)/$(TARGET).out $(BUILDDIR)/top.out $(BUILDDIR)/$(TARGET).vpi\n')
            f.write('\t$(SIM) -M$(BUILDDIR) -m$(TARGET) $(BUILDDIR)/$(TARGET).out\n')
            f.write('\t$(MV) out.vcd $(BUILDDIR)/$(TARGET).vcd\n')
            f.write('\n')
            f.write('$(BUILDDIR)/top.out: $(SRCDIR)/top.v\n')
            f.write('\t$(CC_VERILOG) $(CFLAGS) -o $(BUILDDIR)/top.out $(SRCDIR)/top.v\n')
            f.write('\n')
            f.write('$(BUILDDIR)/$(TARGET).out: $(SRCDIR)/$(TARGET).v\n')
            f.write('\t$(CC_VERILOG) $(CFLAGS) -o $(BUILDDIR)/$(TARGET).out $(SRCDIR)/$(TARGET).v\n')
            f.write('\n')
            f.write('$(BUILDDIR)/$(TARGET).vpi: $(SRCDIR)/$(TARGET).c\n')
            f.write('\t$(CC) -c -fpic -I/usr/include/iverilog -o $(BUILDDIR)/$(TARGET).o $(SRCDIR)/$(TARGET).c\n')
            f.write('\t$(CC) -shared -lvpi -o $(BUILDDIR)/$(TARGET).vpi $(BUILDDIR)/$(TARGET).o\n')
            f.write('\n')
            f.write('clean:\n')
            f.write('\t$(RM) -f $(BUILDDIR)/*\n')
