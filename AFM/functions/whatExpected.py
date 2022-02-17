# -*- coding: utf-8 -*-
"""
@author: djimderidder
"""
def WhatExpected():
    """
    Ask user to give an estimation of the Gaussians.
    returns
        expected: Mean, standard deviation and height of two gaussians
            tuple: [6 int]
    """
    print('What is the expected height of the membrane?')
    while True:
        try:
            x1 = float(input('x1='))
            break
        except:
            print("That's not a valid option!")

    if x1>0:
        print('What is the max probability density of the membrane distribution?')
    else:
        print('That\'s not an option!')
    


    while True:
        try:
            y1 = float(input('y1='))
            break
        except:
            print("That's not a valid option!")

    if y1<1 and y1>0:
        print('What is the FWHM/2 of the membrane distribution?')
    else:
        print('That\'s not an option!')



    while True:
        try:
            std1 = float(input('std1='))
            break
        except:
            print("That's not a valid option!")

    if std1>0:
        print('What is the expected height of the septin?')
    else:
        print('That\'s not an option!')



    while True:
        try:
            x2 = float(input('x2='))
            break
        except:
            print("That's not a valid option!")

    if x2>x1:
        print('What is the max probability density of the septin distribution?')
    else:
        print('That\'s not an option!')
    


    while True:
        try:
            y2 = float(input('y2='))
            break
        except:
            print("That's not a valid option!")

    if y2<1 and y2>0:
        print('What is the FWHM/2 of the septin distribution?')
    else:
        print('That\'s not an option!')



    while True:
        try:
            std2 = float(input('std2='))
            break
        except:
            print("That's not a valid option!")

    if std2>0:
        print('What is the expected height of the septin?')
    else:
        print('That\'s not an option!')
    
    
    
    expected = (x1,std1,y1,x2,std2,y2)
    
    return expected