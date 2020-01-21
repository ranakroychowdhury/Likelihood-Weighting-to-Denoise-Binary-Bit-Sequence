# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 13:06:25 2019

@author: Ranak Roy Chowdhury
"""    
import itertools
import numpy as np
from matplotlib import pyplot
from matplotlib.pyplot import figure


#compute P(Z|all B)
def prob_Z_B(Z, f_B, alpha):

    a = (1 - alpha)/(1 + alpha)
    b = pow(alpha, abs(Z - f_B))
    return a * b


#generate all the samples and their weights
def generateSamplesandWeights(num_samples, n, B, alpha):
    
    s = np.random.uniform(0, 1, num_samples * n) #generate samples*n random numbers
    s = np.reshape(s, (num_samples, n)) #reshape them to a samples*n matrix
    condlist = [s<0.5, s>=0.5] #check if every random no.<0.5 or >=0.5
    choicelist = [0, 1] #if random no.<0.5, B_i = 0, else 1
    s = np.select(condlist, choicelist) #convert to a matrix of 0 and 1 based on the condition
    t = tuple(map(tuple, s))
    W = [] #weights for all the samples
    
    for j in range(num_samples):
        W.append(prob_Z_B(Z, B.index(t[j]), alpha)) #f_B = position of tuple in B
    
    return s, W

    
#compute P(B_i/Z)
def prob_Bi_Z(samples, weights, i):
    
    boolArr = samples[ : , -i] == 1 #choose sample with B_i = 1
    total = sum(np.array(weights)[boolArr]) #for the chosen samples, sm up their weights
    return total /sum(weights)   #weight(samples with B_i=1)/total weight
    
    
def plotResult(result, num_samples_list, list_i):
    x_axis = [pow(10,i) for i in range(1, len(num_samples_list) + 1)]
    
    fig = pyplot.gcf()
    fig.set_size_inches(20, 15)
    ax1 = fig.add_subplot(211)
    ax1.set_ylabel('P(B_i=1|Z=128)')
    ax1.set_xlabel('Number of samples')
    
    for i in range(len(list_i)):
        pyplot.subplot(2,1,1)
        pyplot.plot(x_axis, result[i], label = str(list_i[i]))
        pyplot.xscale('log')
        
    pyplot.legend(loc='upper right')
    pyplot.show()
    
    
if __name__ == "__main__":
    n = 10
    B = list(itertools.product([0, 1], repeat = n)) #generates all binary strings of n bits
    Z = 128
    alpha = 0.1
    result = []
    num_samples_list = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    list_i = [2, 5, 8, 10]
    
    for num_samples in num_samples_list:
        #generate all the samples and their weights
        print(num_samples)
        samples, weights = generateSamplesandWeights(num_samples, n, B, alpha)

        answer = []
        for i in list_i:
            #compute P(B_i/Z)
            answer.append(prob_Bi_Z(samples, weights, i))
        result.append(answer)
    result = list(map(list, zip(*result)))

    plotResult(result, num_samples_list, list_i)
    
    