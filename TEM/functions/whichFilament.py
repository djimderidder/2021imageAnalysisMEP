# -*- coding: utf-8 -*-
"""
@author: djimderidder
"""
def WhichFilament(lineCoord):
    """
    Plot
    inputs
        lineCoord: arrays of x-y coordinates of linear splines
            lineCoord
    returns
        K
            int
        kplus
            int
        kmin
            int
        
    """
    print('Which filament do you want to measure?')
    while True:
        try:
            K = int(input('K='))
            break
        except:
            print("That's not a valid option!")

    if K<int(lineCoord.shape[1]/2)-1:
        print('How many filaments below filament',K,'?')
    elif K <= 0:
        print('That\'s not an option!')
    else:
        print('That\'s not an option!')

    while True:
        try:
            kmin= int(input(' kmin='))
            break
        except:
            print("That's not a valid option!")

    if K-kmin>0:
        print('How many filaments above filament_',K,';')
    elif K <= 0:
        print('That\'s not an option!')
    else:
        print('That\'s not an option!')

    while True:
        try:
            kplus= int(input(' kplus='))
            break
        except:
            print("That's not a valid option!")

    if K+kplus<int(lineCoord.shape[1]/2):
        print('Please wait...')
    elif K <= 0:
        print('That\'s not an option!')
    else:
        print('That\'s not an option!')
    
    return K,kmin,kplus
