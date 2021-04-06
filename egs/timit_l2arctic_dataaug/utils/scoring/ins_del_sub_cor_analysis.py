#!/usr/bin/env python
# coding: utf-8
# usage: require 1. ref_human_detail 2. human_our_detail 3 ref_our_detail
import re
f = open("ref_human_detail",'r')
dic={}
insert = 0 
delete = 0
sub = 0
cor=0
count=0
##  0： ref  1：human 2：ops --- 3: human  4： our  5: ops 
for line in f:
    line = line.strip()
    if("ref" in line ):
        ref = line.split("ref")
        ref[0] = ref[0].strip(" ")
        ref[1] = ref[1].strip(" ")
        ref[1] = re.sub(" +"," ",ref[1])
        ref_seq = ref[1].split(" ")
        dic[ref[0]] = []
        dic[ref[0]].append(ref[1])
    elif( "hyp" in line ):
        hyp = line.split("hyp")
        hyp[0] = hyp[0].strip(" ")
        hyp[1] = hyp[1].strip(" ")
        hyp[1] = re.sub(" +"," ",hyp[1])
        hyp_seq = hyp[1].split(" ")
        dic[hyp[0]].append(hyp[1])
    elif( " op " in line ):   
        op = line.split(" op ")
        op[0] = op[0].strip(" ")
        op[1] = op[1].strip(" ")
        op[1] = re.sub(" +"," ",op[1])
        op_seq = op[1].split(" ")
        dic[op[0]].append(op[1])
        for i in op_seq:
            if(i == "I"):
                insert+=1
            elif(i == "D"):
                delete+=1
                count+=1
            elif(i == "S"):
                sub +=1
                count+=1
            elif(i=="C"):
                cor+=1
                count+=1
f.close()
## 发音错误统计
print("insert:" ,insert)
print("delete:" ,delete)
print("sub:" ,sub)
print("cor:" ,cor)
print("sum", count)

f = open("human_our_detail",'r')
for line in f:
    line = line.strip()
    fn = line.split(" ")[0]
    if(fn not in dic):
        continue
    if("ref" in line ):
        ref = line.split("ref")
        ref[0] = ref[0].strip(" ")
        ref[1] = ref[1].strip(" ")
        ref[1] = re.sub(" +"," ",ref[1])
        ref_seq = ref[1].split(" ")
        dic[ref[0]].append(ref[1])
    elif( "hyp" in line ):
        hyp = line.split("hyp")
        hyp[0] = hyp[0].strip(" ")
        hyp[1] = hyp[1].strip(" ")
        hyp[1] = re.sub(" +"," ",hyp[1])
        hyp_seq = hyp[1].split(" ")
        dic[hyp[0]].append(hyp[1])
    elif( " op " in line ):
        op = line.split(" op ")
        op[0] = op[0].strip(" ")
        op[1] = op[1].strip(" ")
        op[1] = re.sub(" +"," ",op[1])
        op_seq = op[1].split(" ")
        dic[op[0]].append(op[1])
f.close()


f = open("ref_our_detail",'r')
for line in f:
    line = line.strip()
    fn = line.split(" ")[0]
    if(fn not in dic):
        continue
    if("ref" in line ):
        ref = line.split("ref")
        ref[0] = ref[0].strip(" ")
        ref[1] = ref[1].strip(" ")
        ref[1] = re.sub(" +"," ",ref[1])
        ref_seq = ref[1].split(" ")
        dic[ref[0]].append(ref[1])
    elif( "hyp" in line ):
        hyp = line.split("hyp")
        hyp[0] = hyp[0].strip(" ")
        hyp[1] = hyp[1].strip(" ")
        hyp[1] = re.sub(" +"," ",hyp[1])
        hyp_seq = hyp[1].split(" ")
        dic[hyp[0]].append(hyp[1])
    elif( " op " in line ):
        op = line.split(" op ")
        op[0] = op[0].strip(" ")
        op[1] = op[1].strip(" ")
        op[1] = re.sub(" +"," ",op[1])
        op_seq = op[1].split(" ")
        dic[op[0]].append(op[1])
f.close()


cor_cor = 0
cor_nocor = 0
sub_sub = 0
sub_nosub = 0
ins_ins = 0
ins_noins =0
del_del = 0
del_nodel =0

for i in dic:
    arr = dic[i]
    # del detection 
    ref_seq = arr[0].split(" ")
    ref_seq3 = arr[6].split(" ")
    op =  arr[2].split(" ")
    op3 = arr[8].split(" ")
    flag = 0
    for i in range( len(ref_seq) ):
        if(ref_seq[i] == "<eps>"):
            continue
        while(ref_seq3[flag] == "<eps>"):
            flag+=1  
        if( ref_seq[i]  == ref_seq3[flag] and ref_seq!="<eps>" ):
            if( op[i] == "D"  and op3[flag] == "D" ):
                del_del+=1
            elif( op[i] == "D" and op3[flag] != "D"):
                del_nodel+=1  
            flag+=1  

    ## cor ins sub detection 
    human_seq = arr[1].split(" ")
    op =  arr[2].split(" ")
    human_seq2 = arr[3].split(" ")
    our_seq2 = arr[4].split(" ")
    op2 = arr[5].split(" ")
    flag = 0 
    for i in range( len(human_seq) ):
        if(human_seq[i] == "<eps>"):
            continue
        while(human_seq2[flag] == "<eps>"):
            flag+=1
        if( human_seq[i]  == human_seq2[flag] and human_seq[i]!="<eps>" ):
            if( op[i] == "C"  and op2[flag] == "C" ):
                cor_cor+=1
            elif( op[i] == "C" and op2[flag] != "C"):
                cor_nocor+=1


            if( op[i] == "S" and op2[flag] == "C" ):
                sub_sub+=1
            elif( op[i] == "S"  and op2[flag] !="C"):
                sub_nosub+=1

            if(op[i] == "I" and op2[flag] == "C" ):
                ins_ins+=1
            elif( op[i] == "I" and op2[flag]!="C"):
                ins_noins+=1

            flag+=1
print("cor_cor:" ,cor_cor)
print("cor_nocor:" ,cor_nocor)
print("sub_sub:" ,sub_sub)
print("sub_nosub:" ,sub_nosub)
print("ins_ins", ins_ins)
print("ins_noins", ins_noins)
print("del_del",del_del)
print("del_nodel",del_nodel)
sum1 = cor_cor + cor_nocor + sub_sub + sub_nosub + ins_ins + ins_noins + del_del + del_nodel
print("sum:",sum1)
TP = sub_sub + ins_ins + del_del
FP = cor_nocor
FN = sub_nosub + ins_noins + del_nodel
print("Recall:",TP/(TP+FN))
print("Precision:",TP/(TP+FP))


