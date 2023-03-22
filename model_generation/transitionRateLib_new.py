# -*- coding: utf-8 -*-
# generate and store diverse transition rates with specific loop time, branch instruction numbers, if/else pair and modulos;
# the format of the TRLib element is {
#								       [
#                                          code structure type,
#                                          branch instruction number,
#                                          transiton rate,
#                                          loop time,
#                                          if/else pair,
#                                          embedded loop time
#                                      ]: 
#                                           [
#                                               modulos list,
#                                               ismoduled list,
#												branch taken backward ratio,
#												branch not taken ratio
#												 ]
#     						         }
# this file can satisfy up to 1K if/else pairs

import os
import pickle
import random
import math

TRLib = {}
#TRlib = {[]:[[],[]]}

# generate transition rate data with specific loop time, branch instruction numbers and if/else pair
def transitionrate(loop_time, ifelse_pair, embedded_loop_time):
# code structure: a loop with if else pair inside; type: 6    12/27 lining
    if loop_time != 0 and ifelse_pair != 0 and embedded_loop_time == 0:
        transitionRate = 0
        #loop_time = 0
        branchInstNum = 0
        #ifelse_pair = 0
        modulos = []
        ismoduled = []
        branchTakenForward = 0
        branchTakenBackward = 0
        branchNotTaken = 0
        #embedded_loop_time = 0
        code_struct_type = 6

        #generate the modulos and ismoduled randomly
        modulo_max_power = math.floor(math.log(loop_time, 2))
        for i in range(0, ifelse_pair):
            modulo = 2 ** random.randint(1, modulo_max_power)
            modulos.append(modulo)
            #modulos.append(random.randint(1, modulo))
            ismoduled.append(random.random() < 0.5)
        numberofBB = 3 * ifelse_pair + 1

        #store each basic block in the format: B0001, B0002,...
        BBNames = []
        for i in range(0, numberofBB):
            BBNames.append("B" + (4 - len(str(i))) * "0" + str(i))

        #store the branch information(taken or not-taken) between 2 basic blocks
        relations = {}
        for i in range(0, ifelse_pair):
            relations[BBNames[i * 3] + BBNames[i * 3 + 1]] = "0"
            relations[BBNames[i * 3] + BBNames[i * 3 + 2]] = "1"
            relations[BBNames[i * 3 + 1] + BBNames[i * 3 + 3]] = "1"
            relations[BBNames[i * 3 + 2] + BBNames[i * 3 + 3]] = "x"
        relations[BBNames[numberofBB - 1] + BBNames[0]] = "1"

        #generate the control flow in the format:B0001B0003B0004... we use 4 bits to implement at most 10000/3 pairs of if/else
        #the if block is not-taken branch, the else block is taken-branch
        controlFlow = BBNames[numberofBB - 1]
        for i in range(0, loop_time):
            for j in range(0, ifelse_pair):
                controlFlow  = controlFlow + BBNames[j * 3]
                if ((i % modulos[j] == 0) and (ismoduled[j])) or ((i % modulos[j] != 0) and (not ismoduled[j])):
                    controlFlow = controlFlow + BBNames[j * 3 + 1]
                else:
                    controlFlow = controlFlow + BBNames[j * 3 + 2]
            controlFlow = controlFlow + BBNames[numberofBB - 1]

        #generate the transition flow in the format:110111...
        branchNotTaken = 0
        transitionRateSequence = "1"
        for i in range(0, len(controlFlow) - 9, 5):
            isBranched = relations[controlFlow[i: i + 9] + controlFlow[i + 9]]
            if isBranched == "1" or isBranched == "0":
                transitionRateSequence += isBranched
                if isBranched == 0:
                    branchNotTaken += 1

        transitionRateSequence += "0"
        branchNotTaken += 1
        #calculate the branch instruction number
        branchInstNum = len(transitionRateSequence)

        #calculate the taken-forward and taken-backward and not-taken ratio
        branchTakenBackward = loop_time
        branchTakenForward = branchInstNum - branchNotTaken - branchTakenBackward

        #calculate the transition rate
        transitionCount = 0
        for i in range(0, len(transitionRateSequence) - 1):
            if transitionRateSequence[i] != transitionRateSequence[i + 1]:
                transitionCount += 1
        transitionRate = float(transitionCount) / float(branchInstNum)
        code_struct_type = 6
        return transitionRate, loop_time, branchInstNum, ifelse_pair, modulos, ismoduled, \
               branchTakenForward, branchTakenBackward, branchNotTaken, embedded_loop_time, code_struct_type

# code structure: a loop with if else pair and embedded loop inside; type: 7    12/27 lining
    elif loop_time != 0 and ifelse_pair != 0 and embedded_loop_time != 0:
        transitionRate = 0
        #loop_time = 0
        branchInstNum = 0
        #ifelse_pair = 0
        modulos = []
        ismoduled = []
        branchTakenForward = 0
        branchTakenBackward = 0
        branchNotTaken = 0
        #embedded_loop_time = 0
        code_struct_type = 7

        #generate the modulos and ismoduled randomly
        modulo_max_power = math.floor(math.log(loop_time, 2))
        for i in range(0, ifelse_pair):
            modulo = 2 ** random.randint(1, modulo_max_power)
            modulos.append(modulo)
            #modulos.append(random.randint(1, modulo))
            ismoduled.append(random.random() < 0.5)
        numberofBB = 3 * ifelse_pair + 5

        #store each basic block in the format: B0001, B0002,...
        BBNames = []
        for i in range(0, numberofBB):
            BBNames.append("B" + (4 - len(str(i))) * "0" + str(i))        

        #store the branch information(taken or not-taken) between 2 basic blocks
        relations = {}
        for i in range(0, ifelse_pair):
            relations[BBNames[i * 3] + BBNames[i * 3 + 1]] = "0"
            relations[BBNames[i * 3] + BBNames[i * 3 + 2]] = "1"
            relations[BBNames[i * 3 + 1] + BBNames[i * 3 + 3]] = "1"
            relations[BBNames[i * 3 + 2] + BBNames[i * 3 + 3]] = "x"
        relations[BBNames[ifelse_pair * 3 - 2] + BBNames[ifelse_pair * 3 + 2]] = "1"
        relations[BBNames[ifelse_pair * 3 - 1] + BBNames[ifelse_pair * 3 + 2]] = "1"
        relations[BBNames[ifelse_pair * 3] + BBNames[ifelse_pair * 3 + 1]] = "x"
        relations[BBNames[ifelse_pair * 3 + 1] + BBNames[ifelse_pair * 3 + 2]] = "x"
        relations[BBNames[ifelse_pair * 3 + 2] + BBNames[ifelse_pair * 3 + 3]] = "0"
        relations[BBNames[ifelse_pair * 3 + 2] + BBNames[ifelse_pair * 3]] = "1"
        relations[BBNames[ifelse_pair * 3 + 3] + BBNames[ifelse_pair * 3 + 4]] = "x"
        relations[BBNames[ifelse_pair * 3 + 4] + BBNames[0]] = "1"

        #generate the control flow in the format:B0001B0003B0004... we use 4 bits to implement at most 10000/3 pairs of if/else
        #the if block is not-taken branch, the else block is taken-branch
        controlFlow = BBNames[numberofBB - 1]
        for i in range(0, loop_time):
            for j in range(0, ifelse_pair):
                controlFlow  = controlFlow + BBNames[j * 3]
                if ((i % modulos[j] == 0) and (ismoduled[j])) or ((i % modulos[j] != 0) and (not ismoduled[j])):
                    controlFlow = controlFlow + BBNames[j * 3 + 1]
                else:
                    controlFlow = controlFlow + BBNames[j * 3 + 2]
            #controlFlow += "B2"
            controlFlow += BBNames[ifelse_pair * 3 + 2]
            for k in range(0, embedded_loop_time):
                #controlFlow += "B0"
                controlFlow += BBNames[ifelse_pair * 3]
                #controlFlow += "B1"
                controlFlow += BBNames[ifelse_pair * 3 + 1]
                #controlFlow += "B2"
                controlFlow += BBNames[ifelse_pair * 3 + 2]
            #controlFlow += "B3"
            controlFlow += BBNames[ifelse_pair * 3 + 3]
            #controlFlow += "B4"
            controlFlow += BBNames[ifelse_pair * 3 + 4]

        #generate the transition flow in the format:110111...
        branchNotTaken = 0
        transitionRateSequence = "1"
        for i in range(0, len(controlFlow) - 9, 5):
            isBranched = relations[controlFlow[i: i + 9] + controlFlow[i + 9]]
            if isBranched == "1" or isBranched == "0":
                transitionRateSequence += isBranched
                if isBranched == 0:
                    branchNotTaken += 1

        transitionRateSequence += "0"
        branchNotTaken += 1
        #calculate the branch instruction number
        branchInstNum = len(transitionRateSequence)

        #calculate the taken-forward and taken-backward and not-taken ratio
        branchTakenBackward = embedded_loop_time * loop_time + loop_time
        branchTakenForward = branchInstNum - branchNotTaken - branchTakenBackward

        #calculate the transition rate
        transitionCount = 0
        for i in range(0, len(transitionRateSequence) - 1):
            if transitionRateSequence[i] != transitionRateSequence[i + 1]:
                transitionCount += 1
        transitionRate = float(transitionCount) / float(branchInstNum)

        return transitionRate, loop_time, branchInstNum, ifelse_pair, modulos, ismoduled, \
               branchTakenForward, branchTakenBackward, branchNotTaken, embedded_loop_time, code_struct_type

# code structure: a loop with embedded loop inside; type: 5    12/27 lining
    elif loop_time != 0 and ifelse_pair == 0 and embedded_loop_time != 0:
        transitionRate = 0
        #loop_time = 0
        branchInstNum = 0
        #ifelse_pair = 0
        modulos = []
        ismoduled = []
        branchTakenForward = 0
        branchTakenBackward = 0
        branchNotTaken = 0
        #embedded_loop_time = 0
        code_struct_type = 5

        #store each basic block in the format: B1, B2,...
        numberofBB = 5
        BBNames = ["B0", "B1", "B2", "B3", "B4"]

        #store the branch information(taken or not-taken) between 2 basic blocks
        relations = {}
        relations["B0B1"] = "x"
        relations["B1B2"] = "x"
        relations["B2B3"] = "0"
        relations["B2B0"] = "1"
        relations["B3B4"] = "x"
        relations["B4B2"] = "1"

        #generate the control flow in the format:B1B2...
        controlFlow = "B4"
        for i in range(0, loop_time):
            controlFlow += "B2"
            for j in range(0, embedded_loop_time):
                controlFlow += "B0B1B2"
                # controlFlow += "B0"
                # controlFlow += "B1"
                # controlFlow += "B2"
            controlFlow += "B3B4"
            # controlFlow += "B3"
            # controlFlow += "B4"

        #generate the transition flow in the format:110111...
        branchNotTaken = 0
        transitionRateSequence = "1"
        for i in range(0, len(controlFlow) - 3, 2):
            isBranched = relations[controlFlow[i: i + 3] + controlFlow[i + 3]]
            if isBranched == "1" or isBranched == "0":
                transitionRateSequence += isBranched
                if isBranched == 0:
                    branchNotTaken += 1

        transitionRateSequence += "0"
        branchNotTaken += 1
        #calculate the branch instruction number
        branchInstNum = len(transitionRateSequence)

        #calculate the taken-forward and taken-backward and not-taken ratio
        branchTakenBackward = embedded_loop_time * loop_time + loop_time
        branchTakenForward = branchInstNum - branchNotTaken - branchTakenBackward

        #calculate the transition rate
        transitionCount = 0
        for i in range(0, len(transitionRateSequence) - 1):
            if transitionRateSequence[i] != transitionRateSequence[i + 1]:
                transitionCount += 1
        transitionRate = float(transitionCount) / float(branchInstNum)

        return transitionRate, loop_time, branchInstNum, ifelse_pair, modulos, ismoduled, \
               branchTakenForward, branchTakenBackward, branchNotTaken, embedded_loop_time, code_struct_type

    # elif loop_time != 0 and ifelse_pair == 0 and embedded_loop_time == 0:  meaningless

# code structure: a loop with a flow of instructions inside; type: 1    12/27 lining
    elif loop_time == 0 and ifelse_pair == 0 and embedded_loop_time != 0:
        transitionRate = float(0)
        #loop_time = 0
        branchInstNum = embedded_loop_time
        #ifelse_pair = 0
        modulos = []
        ismoduled = []
        branchTakenForward = 0
        branchTakenBackward = embedded_loop_time                    # for循环每一次结束要往前跳
        branchNotTaken = 0
        #embedded_loop_time = 
        code_struct_type = 1

        return transitionRate, loop_time, branchInstNum, ifelse_pair, modulos, ismoduled, \
               branchTakenForward, branchTakenBackward, branchNotTaken, embedded_loop_time, code_struct_type

# code structure: a flow of if else pair instructions; type: 2    12/27 lining
    elif loop_time == 0 and ifelse_pair != 0 and embedded_loop_time == 0:
        transitionRate = 0
        #loop_time = 0
        branchInstNum = 0
        #ifelse_pair = 0
        modulos = []
        ismoduled = []
        branchTakenForward = 0
        branchTakenBackward = 0
        branchNotTaken = 0
        #embedded_loop_time = 0
        code_struct_type = 2

        #generate the modulos and ismoduled randomly, we use a fixed number to modulo on 2, the fixed number is set as an odd
        for i in range(0, ifelse_pair):
            modulo = 2
            modulos.append(modulo)
            ismoduled.append(random.random() < 0.5)

        #store each basic block in the format: B0001, B0002,...
        numberofBB = 3 * ifelse_pair
        BBNames = []
        for i in range(0, numberofBB):
            BBNames.append("B" + (4 - len(str(i))) * "0" + str(i))
        BBNames.append("B" + (4 - len(str(numberofBB))) * "0" + str(numberofBB))

        #store the branch information(taken or not-taken) between 2 basic blocks
        relations = {}
        for i in range(0, ifelse_pair):
            relations[BBNames[i * 3] + BBNames[i * 3 + 1]] = "0"
            relations[BBNames[i * 3] + BBNames[i * 3 + 2]] = "1"
            relations[BBNames[i * 3 + 1] + BBNames[i * 3 + 3]] = "1"
            relations[BBNames[i * 3 + 2] + BBNames[i * 3 + 3]] = "x"

        #generate the control flow in the format:B0001B0003B0004... we use 4 bits to implement at most 10000/3 pairs of if/else
        #the if block is not-taken branch, the else block is taken-branch
        controlFlow = ""
        for i in range(0, ifelse_pair):
            controlFlow = controlFlow + BBNames[i * 3]
            if not ismoduled[i]:
                controlFlow = controlFlow + BBNames[i * 3 + 1]
            else:
                controlFlow = controlFlow + BBNames[i * 3 + 2]
        
        #generate the transition flow in the format:110111...
        transitionRateSequence = ""
        for i in range(0, len(controlFlow) - 9, 5):
            isBranched = relations[controlFlow[i: i + 9] + controlFlow[i + 9]]
            if isBranched == "1" or isBranched == "0":
                transitionRateSequence += isBranched
                if isBranched == 0:
                    branchNotTaken += 1

        #calculate the branch instruction number
        branchInstNum = len(transitionRateSequence)

        #calculate the taken-forward and taken-backward and not-taken ratio
        branchTakenBackward = 0
        branchTakenForward = branchInstNum - branchNotTaken - branchTakenBackward

        #calculate the transition rate
        transitionCount = 0
        for i in range(0, len(transitionRateSequence) - 1):
            if transitionRateSequence[i] != transitionRateSequence[i + 1]:
                transitionCount += 1
        transitionRate = float(transitionCount) / float(branchInstNum)

        return transitionRate, loop_time, branchInstNum, ifelse_pair, modulos, ismoduled, \
               branchTakenForward, branchTakenBackward, branchNotTaken, embedded_loop_time, code_struct_type
    #elif loop_time == 0 and ifelse_pair != 0 and embedded_loop_time != 0:  redundant

# code structure: a flow of instructions; type: 0    12/27 lining
    elif loop_time == 0 and ifelse_pair == 0 and embedded_loop_time == 0:  
        transitionRate = float(0)
        #loop_time = 0
        branchInstNum = 0
        #ifelse_pair = 0
        modulos = []
        ismoduled = []
        branchTakenForward = 0
        branchTakenBackward = 0
        branchNotTaken = 0
        #embedded_loop_time = 0
        code_struct_type = 0
        return transitionRate, loop_time, branchInstNum, ifelse_pair, modulos, ismoduled, \
               branchTakenForward, branchTakenBackward, branchNotTaken, embedded_loop_time, code_struct_type

# function for generating each type of code structure
def generate_code(code_struct):
    [loop_time, ifelse_pair, embedded_loop_time] = code_struct
    transitionRate, loopTime, branchInstNum, ifElsePair, modulos, ismoduled, branchTakenForward, branchTakenBackward, \
            branchNotTaken, embeddedLoopTime, codeStructType = transitionrate(loop_time, ifelse_pair, embedded_loop_time)
    branchTakenBackwardRatio = 0
    branchNotTakenRatio = 0
    if branchInstNum != 0:
        branchTakenBackwardRatio = float(branchTakenBackward) / float(branchInstNum)
        branchNotTakenRatio = float(branchNotTaken) / float(branchInstNum)
    # codeStructType, branchInstNum, transitionRate, loopTime, ifElsePair, embeddedLoopTime 合并为元组
    TRLib[codeStructType, branchInstNum, transitionRate, loopTime, ifElsePair, embeddedLoopTime] = [modulos, ismoduled, branchTakenBackwardRatio, branchNotTakenRatio]

# main()
def main():
    # generate the code structure library
    print ("generatin the branch instruction library...\n")
    TRLib = {}

    # code_struct_type: 000/0       ( e )                                                   # 0 指 该参数一直为 0 
    print ("start generating sub lib for code structure type 0")
    sub_lib_size = 1
    for i in range(sub_lib_size):
        [loop_time, ifelse_pair, embedded_loop_time] = [0, 0, 0]                            # embedded_loop_time ： 内部循环  loop_time  ： 外循环
        generate_code([loop_time, ifelse_pair, embedded_loop_time])
    print (len(TRLib))

    # code_struct_type: 001/1       ( a )
    print ("start generating sub lib for code structure type 1")
    sub_lib_size = 100000
    for i in range(2, sub_lib_size):
        [loop_time, ifelse_pair, embedded_loop_time] = [0, 0, i]
        generate_code([loop_time, ifelse_pair, embedded_loop_time])
    print (len(TRLib))

    # code_struct_type: 010/2        ( d )
    print ("start generating sub lib for code structure type 2")
    sub_lib_size = 100000
    for i in range(sub_lib_size):
        [loop_time, ifelse_pair, embedded_loop_time] = [0, 2 ** random.randint(1, 6), 0]    # ** 乘方
        generate_code([loop_time, ifelse_pair, embedded_loop_time])
        print (i)
    print (len(TRLib))

    # code_struct_type: 101/5        ( c )
    print ("start generating sub lib for code structure type 5")
    sub_lib_size = 1000
    for i in range(5, 500):
        for j in range(5, 500):     
            [loop_time, ifelse_pair, embedded_loop_time] = [i, 0, j]
            generate_code([loop_time, ifelse_pair, embedded_loop_time])
        print ('outer loop: ' + str(i))
    print (len(TRLib))
        
    # code_struct_type: 110/6        ( b )
    print ("start generating sub lib for code structure type 6")
    sub_lib_size = 100000
    for i in range(sub_lib_size):
        [loop_time, ifelse_pair, embedded_loop_time] = [random.randint(5, 100), random.randint(1, 50), 0]
        generate_code([loop_time, ifelse_pair, embedded_loop_time])
        print (i)
    print (len(TRLib))

    # code_struct_type: 111/7        ( e )
    print ("start generating sub lib for code structure type 7")
    sub_lib_size = 100000
    for i in range(sub_lib_size):
        [loop_time, ifelse_pair, embedded_loop_time] = [random.randint(5, 100), random.randint(1, 50), random.randint(5, 100)]
        generate_code([loop_time, ifelse_pair, embedded_loop_time])
        print (i)
    print (len(TRLib))

    # store the transition rate
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR,"TRLib_new.pkl")
    file = open(file_path,"wb")
    pickle.dump(TRLib, file)
    file.close()

    #for i in TRLib:
    #    print (i)

    print (len(TRLib))


if __name__ == '__main__' :
    main()