# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 13:55:09 2021

@author: Irem
"""
import numpy as np
import itertools

def calculateFromData(query_list,evidence_list): #calculates probability from data
    evidence_data=0
    query_data=0     
    for arr in data.transpose(): 
        flag=True
        for i in range(len(evidence_list)):
            if(evidence_list[i]>9): #if item in evidence_list is greater than 9, it indicates  the value being False  
                if(arr[evidence_list[i]-10]!=False):  
                    flag=False
                    break
            else:
                if(arr[evidence_list[i]]!=True):
                    flag=False
                    break
        flag2=True #if flag is True, evidence is provided in this case
        if(flag==True):
            evidence_data+=1
            flag2=True
            for i in range(len(query_list)):
                if(query_list[i]>9):
                    if(arr[query_list[i]-10]!=False):
                        flag2=False
                        break
                else:
                    if(arr[query_list[i]]!=True):
                        flag2=False
                        break
            if(flag2==True): #if flag2 is True, query is provided is this case
                query_data+=1
    if query_data==0:
        return 0.0;
    else:
        return query_data/evidence_data
    

def sumOfConditions(num_list):
    #adds up all conditions using this calculation: P(A)*P(B)*P(C|A)*P(D|A,B)*P(G|D)*P(F|C)*P(E|C)
    product=1
    if 0 in num_list:
        product*=p_a #if A is negative, P(-A) is used
    else:
        product*=p_na
    if 1 in num_list:  #if B is negative, P(-B) is used
        product*=p_b
    else:
        product*=p_nb
    #conditions changes according to values' positivity
    if (0 in num_list) and (1 in num_list) and (3 in num_list): 
            product*=p_d_ab #if A,B and D is positive, P(D|A,B) is used
    elif (10 in num_list) and (1 in num_list) and (3 in num_list): 
            product*=p_d_nab   #if D and B is positive, A is negative, P(D|-A,B) is used and so on.
    elif (0 in num_list) and (11 in num_list) and (3 in num_list):
            product*=p_d_anb
    elif (10 in num_list) and (11 in num_list) and (3 in num_list):
            product*=p_d_nanb
    elif (10 in num_list) and (11 in num_list) and (13 in num_list):
            product*=p_nd_nanb
    elif (0 in num_list) and (1 in num_list) and (13 in num_list):
            product*=p_nd_ab 
    elif (0 in num_list) and (11 in num_list) and (13 in num_list):
            product*=p_nd_anb
    elif (10 in num_list) and (1 in num_list) and (13 in num_list):
            product*=p_nd_nab

    if (0 in num_list) and (2 in num_list):
            product*=p_c_a 
    elif (0 in num_list) and (12 in num_list):
            product*=p_nc_a
    elif (10 in num_list) and (2 in num_list):
            product*=p_c_na
    elif (10 in num_list) and (12 in num_list):
            product*=p_na_nc

    if (3 in num_list) and (6 in num_list):
            product*=p_g_d
    elif (3 in num_list) and (16 in num_list):
            product*=p_ng_d
    elif (13 in num_list) and (6 in num_list):
            product*=p_g_nd
    elif (13 in num_list) and (16 in num_list):
            product*=p_ng_nd

    if (2 in num_list) and (5 in num_list):
            product*=p_f_c  
    elif (2 in num_list) and (15 in num_list):
            product*=p_nf_c
    elif (12 in num_list) and (5 in num_list):
            product*=p_f_nc
    elif (12 in num_list) and (15 in num_list):
            product*=p_nf_nc

    if (2 in num_list) and (4 in num_list):
            product*=p_e_c
    elif (2 in num_list) and (14 in num_list):
            product*=p_ne_c
    elif (12 in num_list) and (4 in num_list):
            product*=p_e_nc
    elif (12 in num_list) and (14 in num_list):
            product*=p_ne_nc
    return product #after all conditions are calculated, product is returned and all products are added up
    

    
def calculateProbability(joint_prob_array):
    remainingList=[0,1,2,3,4,5,6] #it contains values of variables as positive
    for item in joint_prob_array: #to determine changeable varibles(can be positive and negative ), values are removed from remaining list
        if item<10:
            if item in remainingList:
                remainingList.remove(item)
        else:
            if item-10 in remainingList:
                remainingList.remove(item-10)
    all_list=[]
    for i in remainingList:
        current_list= []
        current_list.append(i)
        current_list.append(i+10)
        all_list.append(current_list)
    #all_list contains  indexes of values that can be positive and negative  
    result_array=[]
    for element in itertools.product(*all_list):
        result_array.append(list(element))
    #result_array contains all conditions can occur
    result_probability=0
    for array in result_array:
        #complete enumeration
        result_probability+=sumOfConditions(array+joint_prob_array)
    return result_probability
    
def calculateByInference(joint_prob_array,evidence_array):
    numerator=calculateProbability(joint_prob_array) #it calculates probability for P(X,Y)
    denominator=calculateProbability(evidence_array) #it calculates probablity for P(Y)
    if numerator==0.0:
        return 0.0
    else:
        return (numerator/denominator) #it return P(X|Y)
def createJointDistribution(query_list,evidence_list): #both of X and Y values are inserted to joint_prob_array to figure out P(X,Y)
    for item in query_list:
        joint_prob_array.append(item)
    for item in evidence_list:
        joint_prob_array.append(item)
def calculateProbabilities():
    a,b,c,d,e,f,g=0,0,0,0,0,0,0 #indicates numbers of cases that x is True {x:a,b,c,d,e,f,g}
    na,nc,nd=0,0,0 #indicates numbers of cases that x is False {x:a,b,c,d,e,f,g}
    c_a,c_na,=0,0 #c_a indicates numbers of cases that A and C is True, c_na indicates numbers of cases that A is False and C is True and so on...
    g_d  , g_nd =0,0
    f_c ,f_nc =0,0
    e_c  , e_nc =0,0
    d_a,d_na=0,0
    b_a=0
    d_ab,d_nab,d_nanb,d_anb=0,0,0,0
    na_nb,na_b,nb_a=0,0,0
    
    data_len=len(data.transpose())
    for arr in data.transpose():
        if(arr[0]==True):
            a+=1
            if(arr[1]==True):
                b_a+=1
                if(arr[3]==True):
                    d_ab+=1
            else:
                nb_a+=1
                if(arr[3]==True):
                    d_anb+=1
            if(arr[2]==True):
                c_a+=1
            if(arr[3]==True):
                d_a+=1
        else:
            na+=1
            if(arr[1]==False):
                na_nb+=1
                if(arr[3]==True):
                    d_nanb+=1
            else:
                na_b+=1
                if(arr[3]==True):
                    d_nab+=1
            if(arr[2]==True):
                c_na+=1
            if(arr[3]==True):
                d_na+=1
        if(arr[1]==True):
            b+=1
        if(arr[2]==True):
            c+=1
            if(arr[5]==True):
                f_c+=1
            if(arr[4]==True):
                e_c+=1
        else:
            nc+=1
            if(arr[5]==True):
                f_nc+=1
            if(arr[4]==True):
                e_nc+=1
        if(arr[3]==True):
            d+=1
            if(arr[6]==True):
                g_d+=1
        else:
            nd+=1
            if(arr[6]==True):
                g_nd+=1
        if(arr[4]==True):
            e+=1
        if(arr[5]==True):
            f+=1
        if(arr[6]==True):
            g+=1
      
    global p_a,p_na,p_b,p_nb,p_c_a,p_nc_a,p_c_na,p_na_nc
    p_a=a/data_len 
    p_na=1-p_a 
    
    p_b=b/data_len
    p_nb=1-p_b
    
    p_c_a=c_a/a
    p_nc_a=1-p_c_a
    p_c_na=c_na/na
    p_na_nc=1-p_c_na
    

    global p_g_d,p_ng_d,p_g_nd,p_ng_nd,p_f_c,p_nf_c,p_f_nc,p_nf_nc
    p_g_d=g_d/d
    p_ng_d=1-p_g_d
    p_g_nd=g_nd/nd
    p_ng_nd=1-p_g_nd
    
    p_f_c=f_c/c
    
    p_nf_c=1-p_f_c
    p_f_nc=f_nc/nc
    p_nf_nc=1-p_f_nc
    
    global p_e_c,p_ne_c,p_e_nc,p_ne_nc
    p_e_c=e_c/c
    p_ne_c=1-p_e_c
    p_e_nc=e_nc/nc
    p_ne_nc=1-p_e_nc
    
    global p_d_ab,p_nd_ab,p_d_nab,p_d_nanb,p_d_anb,p_nd_nab,p_nd_nanb,p_nd_anb
    p_d_ab=d_ab/b_a
    p_nd_ab=1-p_d_ab
    p_d_nab=d_nab/na_b
    p_d_nanb=d_nanb/na_nb
    p_d_anb=d_anb/nb_a
    
    p_nd_nab=1-p_d_nab
    p_nd_nanb=1-p_d_nanb
    p_nd_anb=1-p_d_anb
    
data=np.load('data.npy')

probs={}
alphabet="ABCDEFG" #nodes in network structure

#the following indicates the possibilities that can be used for network structure
# P(A) , P(-A) , P(B) , P(-B)
p_a,p_na,p_b,p_nb=0,0,0,0
#P(C|A) , P(-C|A) , P(C|-A) , P(-C|-A) 
p_c_a,p_nc_a,p_c_na,p_na_nc=0,0,0,0

#P(G|D), P(-G|D), P(G|-D), P(-G|-D)
p_g_d,p_ng_d,p_g_nd,p_ng_nd=0,0,0,0

#P(F|C), P(F|C), P(F|-C), P(-F|-C)
p_f_c,p_nf_c,p_f_nc,p_nf_nc=0,0,0,0

#P(E|C), P(-E|C), P(E|-C), P(-E|-C)
p_e_c,p_ne_c,p_e_nc,p_ne_nc=0,0,0,0

#P(D|A,B), P(-D|A,B), P(D|-A,B), P(D|-A,-B), 
p_d_ab,p_nd_ab,p_d_nab,p_d_nanb=0,0,0,0

#P(D|A,-B), P(-D|-A,B), P(-D|-A,-B), P(-D|A,-B), 
p_d_anb,p_nd_nab,p_nd_nanb,p_nd_anb=0,0,0,0
        
query_input=input("Please give query variables:").upper().strip()
evidence_input=input("Please give evidence variables:").upper().strip()


query_array=query_input.split(" "); #query_array contains indexes of  query variables. For example A-> 0, B->1 , C->2 etc.
evidence_array=evidence_input.split(" ") #evidence_array contains indexes of evidence variables.  For example A-> 0, B->1 , C->2 etc.

error=False #checks whether input is correct or not
joint_prob_array=[]
for letter in query_array: 
    index=query_array.index(letter)
    if(letter[0]!="N"):
        if letter in alphabet:
            query_array[index]=alphabet.index(letter)
        else:
            error=True
    else: #if input variable is negative - for exmaple nG- , this value is held like index+10.
        if letter[1] in alphabet:
            query_array[index]=10+alphabet.index(letter[1]) #For example nA->10,nB->11 etc.
        else:
            error=False
for letter in evidence_array: #values in evidence array are also held as in the query_array 
        index=evidence_array.index(letter)
        if(letter[0]!="N"):
            if letter in alphabet:
                evidence_array[index]=alphabet.index(letter)
            else:
                error=True
        else:
            if letter[1] in alphabet:
                evidence_array[index]=10+alphabet.index(letter[1])
            else:
                error=True
if error==True:
    print("Enter variables correctly !")
else:
    dependencies={}
    createJointDistribution(query_array,evidence_array)
    calculateProbabilities() #calculates the probabilities that can be used for network structure

    # Conditional probability: P(X,Y)=P(X|Y)*P(Y) 
    #because of finding P(X|Y) using conditional prob, we divides P(X,Y) by P(Y)
    # joint_prob_array holds values for P(X,Y)
    print("\nThe probability calculated by inference is ", calculateByInference(joint_prob_array,evidence_array))
    print("The probability calculated from data is ", calculateFromData(query_array, evidence_array))





