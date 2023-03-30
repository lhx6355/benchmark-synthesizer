# -*- coding: utf-8 -*-

from string import Template
import random

#code structure template
structFuncName = Template(u'${tab}void ${suffx}(){\n')
structInitial = Template(u'${tab}int ${suffx} = ${suffx1};\n')
structFor = Template(u'${tab}for(${suffx}; ${suffx} < ${suffx1}; ${suffx}++){\n')
structIf = Template(u'${tab}if(i % ${suffx} ${suffx1}= 0){\n')
structElse = Template(u'${tab}else{\n')
structRightBrace = Template(u'${tab}}\n')
structMain = Template(u'${tab}int main(){\n')
structWhile = Template(u'${tab}while(1)\n${tab}\t;\n')
structFuncCall = Template(u'${tab}${suffx}();\n')
#structTab = Template(u'\t')
structReturn = Template(u'${tab}return 0;\n')

structMaps = Template(u'${tab}int temp[5000000][200] = {0};\n')       # lhx
# structMaps = Template(u'${tab}void *ptr = temp + 5000000 / 2;\n')       # lhx
structPoint = Template(u'${tab}    asm volatile ("mov x12, #0x800000;\\n\\t" ::: "x12"); //[point];\n')       # lhx




#asm code template
asmMov    = Template(u'${tab}asm volatile (\n${tab}\t"mov ${suffx}, ${suffx1};\\n\\t"\n${tab}\t:::"${suffx}"\n${tab}); //[AsmMov]')
asmMov2    = Template(u'${tab}asm volatile (\n${tab}\t"mov ${suffx}, ${suffx1};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}"\n${tab}); //[AsmMov]')
asmSIMD   = Template(u'${tab}asm volatile (\n${tab}\t"dup ${suffx}.2d,${suffx1};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}"\n${tab}); //[AsmSIMDDup]')
asmLogic  = Template(u'${tab}asm volatile (\n${tab}\t"and ${suffx}, ${suffx1}, #0x04;\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}"\n${tab}); //[AsmLogic]')
asmIntAdd = Template(u'${tab}asm volatile (\n${tab}\t"add ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}"\n${tab}); //[AsmIntAdd]')
asmIntAdd2 = Template(u'${tab}asm volatile (\n${tab}\t"add ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}"\n${tab}); //[AsmIntAdd2]')
#asmIntAdd2 = Template(u'${tab}asm volatile (\n${tab}\t"add ${suffx}, ${suffx1}, ${suffx2}, LSL ${suffx3};\\n\\t"\n${tab}\t:::"${suffx}"\n${tab}); //[AsmIntAdd2]')
asmIntAdd3 = Template(u'${tab}asm volatile (\n${tab}\t"add ${suffx}, ${suffx1}, ${suffx2}, LSL ${suffx3};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx2}"\n${tab}); //[AsmIntAdd3]')
asmIntSub = Template(u'${tab}asm volatile (\n${tab}\t"sub ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}"\n${tab}); //[AsmIntSub]')
asmIntSub2 = Template(u'${tab}asm volatile (\n${tab}\t"sub ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}"\n${tab}); //[AsmIntSub2]')
asmIntSub3 = Template(u'${tab}asm volatile (\n${tab}\t"sub ${suffx}, ${suffx1}, ${suffx2}, LSL ${suffx3};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx2}"\n${tab}); //[AsmIntSub3]')
asmIntMul = Template(u'${tab}asm volatile (\n${tab}\t"smulh ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}", "${suffx2}"\n${tab}); //[AsmIntMul]')
asmIntDiv = Template(u'${tab}asm volatile (\n${tab}\t"sdiv ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}", "${suffx2}"\n${tab}); //[AsmIntDiv]')
asmFloatAdd = Template(u'${tab}asm volatile (\n${tab}\t"fadd ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}", "${suffx2}"\n${tab}); //[AsmFloatAdd]')
asmFloatSub = Template(u'${tab}asm volatile (\n${tab}\t"fsub ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}", "${suffx2}"\n${tab}); //[AsmFloatSub]')
asmFloatMul = Template(u'${tab}asm volatile (\n${tab}\t"fmul ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}", "${suffx2}"\n${tab}); //[AsmFloatMul]')
#asmFloatDiv = Template(u'${tab}asm volatile (\n${tab}\t"fdiv ${suffx}.4,${suffx1}.4,${suffx2}.4;\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}", "${suffx2}"\n${tab}); //[AsmFloatDiv]')
asmFloatDiv = Template(u'${tab}asm volatile (\n${tab}\t"fdiv ${suffx},${suffx1},${suffx2};\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}", "${suffx2}"\n${tab}); //[AsmFloatDiv]')


asmSerial = Template(u'${tab}asm volatile (\n${tab}\t"dsb ${suffx};\\n\\t"\n${tab}); //[AsmSerial]')
asmSerial2 = Template(u'${tab}asm volatile (\n${tab}\t"dmb ${suffx};\\n\\t"\n${tab}); //[AsmSerial]')
asmLoad = Template(u'${tab}asm volatile (\n${tab}\t"ldr ${suffx}, [${suffx1},#${suffx2}];\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}"\n${tab}); //[AsmLoad]')
asmStore = Template(u'${tab}asm volatile (\n${tab}\t"str ${suffx}, [${suffx1},#${suffx2}];\\n\\t"\n${tab}\t:::"${suffx}", "${suffx1}"\n${tab}); //[AsmStore]')
# asmMov    = Template(u'\tasm volatile (\n\t\t"mov ${suffx}, ${suffx1};\\n\\t"\n\t\t:::"${suffx}"\n\t); //[AsmMov]')
# asmSIMD   = Template(u'\tasm volatile (\n\t\t"dup ${suffx}.2d,${suffx1};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}"\n\t); //[AsmSIMDDup]')
# asmLogic  = Template(u'\tasm volatile (\n\t\t"and ${suffx}, ${suffx1}, #0x04;\\n\\t"\n\t\t:::"${suffx}", "${suffx1}"\n\t); //[AsmLogic]')
# asmIntAdd = Template(u'\tasm volatile (\n\t\t"add ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}", "${suffx2}"\n\t); //[AsmIntAdd]')
# asmIntSub = Template(u'\tasm volatile (\n\t\t"sub ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}"\n\t); //[AsmIntSub]')
# asmIntMul = Template(u'\tasm volatile (\n\t\t"smulh ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}", "${suffx2}"\n\t); //[AsmIntMul]')
# asmIntDiv = Template(u'\tasm volatile (\n\t\t"sdiv ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}", "${suffx2}"\n\t); //[AsmIntDiv]')
# asmFloatAdd = Template(u'\tasm volatile (\n\t\t"fadd ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}", "${suffx2}"\n\t); //[AsmFloatAdd]')
# asmFloatSub = Template(u'\tasm volatile (\n\t\t"fsub ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}", "${suffx2}"\n\t); //[AsmFloatSub]')
# asmFloatMul = Template(u'\tasm volatile (\n\t\t"fmul ${suffx}, ${suffx1}, ${suffx2};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}", "${suffx2}"\n\t); //[AsmFloatMul]')
# #asmFloatDiv = Template(u'\tasm volatile (\n\t\t"fdiv ${suffx}.4,${suffx1}.4,${suffx2}.4;\\n\\t"\n\t\t:::"${suffx}", "${suffx1}", "${suffx2}"\n\t); //[AsmFloatDiv]')
# asmFloatDiv = Template(u'\tasm volatile (\n\t\t"fdiv ${suffx},${suffx1},${suffx2};\\n\\t"\n\t\t:::"${suffx}", "${suffx1}", "${suffx2}"\n\t); //[AsmFloatDiv]')


# asmSerial = Template(u'\tasm volatile (\n\t\t"dsb ${suffx};\\n\\t"\n\t); //[AsmSerial]')
# asmLoad = Template(u'\tasm volatile (\n\t\t"ldr ${suffx}, [${suffx1},#${suffx2}];\\n\\t"\n\t\t:::"${suffx}", "${suffx1}"\n\t); //[AsmLoad]')
# asmStore = Template(u'\tasm volatile (\n\t\t"str ${suffx}, [${suffx1},#${suffx2}];\\n\\t"\n\t\t:::"${suffx}", "${suffx1}"\n\t); //[AsmStore]')

#turn an instruction parameters into an asm volatile inst string
def inst2asm(inst_para, indention):
    asm_code = ''
    opcode = inst_para[0]
    if opcode == 'dsb':
        asm_code = asmSerial.substitute(tab = '\t' * indention, suffx = inst_para[1])
    elif opcode == 'dmb':
        asm_code = asmSerial2.substitute(tab = '\t' * indention, suffx = inst_para[1])
    elif opcode == 'mov':
        asm_code = asmMov.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2])
    elif opcode == 'mov2':
        asm_code = asmMov2.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2])
    elif opcode == 'dup':
        asm_code = asmSIMD.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2])
    elif opcode == 'and':
        asm_code = asmLogic.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2])
    elif opcode == 'ldr':
        asm_code = asmLoad.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'str':
        asm_code = asmStore.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'add':
        asm_code = asmIntAdd.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'sub':
        asm_code = asmIntSub.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'smul':
        asm_code = asmIntMul.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'sdiv':
        asm_code = asmIntDiv.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'fadd':
        asm_code = asmFloatAdd.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'fsub':
        asm_code = asmFloatSub.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'fmul':
        asm_code = asmFloatMul.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'fdiv':
        asm_code = asmFloatDiv.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'add2': #used for data locality
        asm_code = asmIntAdd2.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'add3': #used for data locality
        asm_code = asmIntAdd3.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3], suffx3 = inst_para[4])
    elif opcode == 'sub2': #used for data locality
        asm_code = asmIntSub2.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3])
    elif opcode == 'sub3': #used for data locality
        asm_code = asmIntSub3.substitute(tab = '\t' * indention, suffx = inst_para[1], suffx1 = inst_para[2], suffx2 = inst_para[3], suffx3 = inst_para[4])

    else:
        asm_code = ''
    return asm_code + '\n'

#convert a list to string
def list2text(code_list):
    code_text = u''
    code_text = ''.join(code_list)
    return code_text

#generate the full code list with asm format
def code_list(code_struct_para, block_inst, code_ID):
    code_struct_type = code_struct_para['code_struct_type']
    loop_time = code_struct_para['loop_time']
    ifelse_pair = code_struct_para['ifelse_pair']
    embedded_loop_time = code_struct_para['embedded_loop_time']
    modulos = code_struct_para['modulos']
    ismoduled = code_struct_para['ismoduled']
    for i in range(ifelse_pair):
        ismoduled[i] = '=' if ismoduled[i] else '!'
    basic_block_size = code_struct_para['basic_block_size']

    code_list = []
    code_list.append(structMaps.substitute(tab = ''))                           # lhx
    code_list.append(structFuncName.substitute(tab = '', suffx = str(code_ID)))
    code_list.append(structPoint.substitute(tab = ''))

    if code_struct_type == 0:
        for i in range(len(block_inst)):
            code_list.append(inst2asm(block_inst[i], 1))

    elif code_struct_type == 1:
        code_list.append(structInitial.substitute(tab = '\t', suffx = 'j', suffx1 = 0))
        code_list.append(structFor.substitute(tab = '\t', suffx = 'j', suffx1 = embedded_loop_time))
        for i in range(len(block_inst)):
            code_list.append(inst2asm(block_inst[i], 2))
        code_list.append(structRightBrace.substitute(tab = '\t'))

    elif code_struct_type == 2:
        block_inst_index = 0
        code_list.append(structInitial.substitute(tab = '\t', suffx = 'i', suffx1 = random.randint(0, 100) * 2 + 1))
        for i in range(ifelse_pair):
            code_list.append(structIf.substitute(tab = '\t', suffx = modulos[i], suffx1 = ismoduled[i]))
            for j in range(basic_block_size):
                code_list.append(inst2asm(block_inst[block_inst_index + j], 2))
            code_list.append(structRightBrace.substitute(tab = '\t'))
            code_list.append(structElse.substitute(tab = '\t'))
            for j in range(basic_block_size):
                code_list.append(inst2asm(block_inst[block_inst_index + j], 2))
            code_list.append(structRightBrace.substitute(tab = '\t'))
            block_inst_index += basic_block_size

    elif code_struct_type == 5:
        code_list.append(structInitial.substitute(tab = '\t', suffx = 'i', suffx1 = 0))
        code_list.append(structFor.substitute(tab = '\t', suffx = 'i', suffx1 = loop_time))
        code_list.append(structInitial.substitute(tab = '\t' * 2, suffx = 'j', suffx1 = 0))
        code_list.append(structFor.substitute(tab = '\t' * 2, suffx = 'j', suffx1 = embedded_loop_time))
        for i in range(basic_block_size):
            code_list.append(inst2asm(block_inst[i], 3))
        code_list.append(structRightBrace.substitute(tab = '\t' * 2))
        code_list.append(structRightBrace.substitute(tab = '\t'))

    elif code_struct_type == 6:
        code_list.append(structInitial.substitute(tab = '\t', suffx = 'i', suffx1 = 0))
        code_list.append(structFor.substitute(tab = '\t', suffx = 'i', suffx1 = loop_time))
        block_inst_index = 0
        for i in range(ifelse_pair):
            code_list.append(structIf.substitute(tab = '\t' * 2, suffx = modulos[i], suffx1 = ismoduled[i]))
            for j in range(basic_block_size):
                code_list.append(inst2asm(block_inst[block_inst_index + j], 3))
            code_list.append(structRightBrace.substitute(tab = '\t' * 2))
            code_list.append(structElse.substitute(tab = '\t' * 2))
            for j in range(basic_block_size):
                code_list.append(inst2asm(block_inst[block_inst_index + j], 3))
            code_list.append(structRightBrace.substitute(tab = '\t' * 2))
            block_inst_index += basic_block_size
        code_list.append(structRightBrace.substitute(tab = '\t'))

    elif code_struct_type == 7:
        block_inst_index = 0
        code_list.append(structInitial.substitute(tab = '\t', suffx = 'i', suffx1 = 0))
        code_list.append(structFor.substitute(tab = '\t', suffx = 'i', suffx1 = loop_time))
        for i in range(ifelse_pair):
            code_list.append(structIf.substitute(tab = '\t' * 2, suffx = modulos[i], suffx1 = ismoduled[i]))
            for j in range(basic_block_size):
                code_list.append(inst2asm(block_inst[block_inst_index + j], 3))
            code_list.append(structRightBrace.substitute(tab = '\t' * 2))
            code_list.append(structElse.substitute(tab = '\t' * 2))
            for j in range(basic_block_size):
                code_list.append(inst2asm(block_inst[block_inst_index + j], 3))
            code_list.append(structRightBrace.substitute(tab = '\t' * 2))
            block_inst_index += basic_block_size
        code_list.append(structInitial.substitute(tab = '\t' * 2, suffx = 'j', suffx1 = 0))
        code_list.append(structFor.substitute(tab = '\t' * 2, suffx = 'j', suffx1 = embedded_loop_time))
        for i in range(basic_block_size):
            code_list.append(inst2asm(block_inst[block_inst_index + j], 3))
        code_list.append(structRightBrace.substitute(tab = '\t' * 2))
        code_list.append(structRightBrace.substitute(tab = '\t'))
        block_inst_index += basic_block_size


    code_list.append(structPoint.substitute(tab = ''))
    code_list.append(structRightBrace.substitute(tab = ''))
    code_list.append(structMain.substitute(tab = ''))
    code_list.append(structFuncCall.substitute(tab = '\t', suffx = code_ID))
    # code_list.append(structWhile.substitute(tab = '\t'))      #  删去 while(1)
    code_list.append(structReturn.substitute(tab = '\t'))
    code_list.append(structRightBrace.substitute(tab = ''))

    return code_list

#print code into file
def print_code(code_struct_para, block_inst, code_ID, file_obj):
    asm_code_list = code_list(code_struct_para, block_inst, code_ID)
    # BASE_DIR = os.path.dirname(__file__)
    # dest_dir = os.path.join(BASE_DIR, 'CodeFiles')
    # if not os.path.exists(dest_dir):
    #     os.mkdir(dest_dir)
    # dest_file = os.path.join(dest_dir, filename)
    # file = open(dest_file, 'wb')
    for i in range(0, len(asm_code_list)):
        file_obj.writelines(list2text(asm_code_list[i]))
    #file_obj.close()
