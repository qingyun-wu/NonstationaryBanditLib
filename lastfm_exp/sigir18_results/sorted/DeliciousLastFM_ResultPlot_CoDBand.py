#Command Line
#CoDBand: python DeliciousLastFM_ResultPlot.py ./ LastFM 7  200 52_32 47_24   10_N_Master_LCBInterval  10_N_LinUCB 10_M_LinUCB_L 10_M_LinUCB_Ar CoDBand
#python DeliciousLastFM_ResultPlot.py ./ LastFM 3  200   10_Master_Uniform 10_Uniform_LinUCB 10_UniformAdTS
#python DeliciousLastFM_ResultPlot.py ./ LastFM 5  200 52_32  avg   10_Master_Uniform 10_UniformAdTS 10_Uniform_LinUCB
import numpy as np
import os
#from conf import *
from matplotlib.pylab import *
from operator import itemgetter
import sys
import pickle
if __name__ == '__main__':
    save_address = str(sys.argv[1])
    
    filenames = [x for x in os.listdir(save_address) if '.csv' in x]

    #lastFM_ChangeList_Dense10 = pickle.load(open('./LastFM_Dense10.Change', 'rb'))
    #lastFM_ChangeList_Dense50 = pickle.load(open('./LastFM_Dense50.Change', 'rb'))
    #lastFM_ChangeList_Dense100 = pickle.load(open('./LastFM_Dense100.Change', 'rb'))

    # NewUCBList_10 = pickle.load(open('./Dense10_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_20_06_13.NewUCBs', 'rb'))
    # SWPointsList_10 = pickle.load(open('./Dense10_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_20_06_13.SwitchPoints', 'rb'))

    # NewUCBList_50 = pickle.load(open('./Dense50_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_15_50_06.NewUCBs', 'rb'))
    # SWPointsList_50 = pickle.load(open('./Dense50_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_15_50_06.SwitchPoints', 'rb'))

    # NewUCBList_100 = pickle.load(open('./Dense100_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_14_46_07.NewUCBs', 'rb'))
    # SWPointsList_100 = pickle.load(open('./Dense100_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_14_46_07.SwitchPoints', 'rb'))

    algName = {}
    dataset = str(sys.argv[2])
    algNum = int(sys.argv[3])
    UserNum = int(sys.argv[4])
    for a in range(algNum):
        algName[a] = sys.argv[5+a]
    #linestyles = ['o-', '*-', '^-', '-', 'D-', 's-', '>-','--']
    linestyles = ['o-', 's-', '*-','>-','<-','g-', '.-', 'o-', 's-', '*-']
    RandomCTR = {}
    tim = {}
    filenames.sort()
    i = -1
    fig, ax = plt.subplots()
    for x in filenames:    
        filename = os.path.join(save_address, x)    
        #print 'LIST'
        if str(algName[0]) in x and str(UserNum) in x:     
            #print(str(filename)  )
            with open(filename, 'r') as f:            
                    
                for line in f:
                    words = line.split(',')
                    if words[0].strip() != 'data':
                        continue
                    i +=1 
                    data= [float(x) for x in words[2].split(';')]
                    RandomCTR[i] = data[0]

    #print len(RandomCTR)
    #print RandomCTR[0]
    limit = 1500

    for a in range(algNum):
        
        filenames.sort()
        i = -1
        CLUB_i = -1
        '''
        if ( 'CoLin' in str(algName[a])):
            continue
        '''
        for x in filenames:    
            filename = os.path.join(save_address, x)    
            if str(algName[a]) in x and str(UserNum) in x:  
                tim = {} 
                AlgCTR = {}
                AlgCTRRatio = {}
                with open(filename, 'r') as f:            
                    print(str(filename) )  
                    print(RandomCTR[0] )
                    for line in f:           
                        # print (line)
                        words = line.split(',')
                        if words[0].strip() != 'data':
                            continue
                        CLUB_i = CLUB_i + 1
                        if (CLUB_i)%1==0:
                            i+=1
                            data_2= [float(x) for x in words[2].split(';')]
                            # print (data_2)
                            # print i
                            temp, AlgCTR[i] = data_2[0],data_2[2]
                            
                            if i in RandomCTR:
                                if RandomCTR[i] !=0:
                                    #print AlgCTR[i], RandomCTR[i]
                                    AlgCTRRatio[i] = AlgCTR[i]/RandomCTR[i]
                                else:
                                    AlgCTRRatio[i] = 0 
                                #print AlgCTRRatio[i]
                            
                            tim[i] = i        
                            
        #print len(tim), len(AlgCTRRatio)
        if str(algName[a]) == 'M_LinUCB':
            algName[a] = 'M-LinUCB'
        if str(algName[a]) == 'N_LinUCB':
            algName[a] = 'N-LinUCB'
        if str(algName[a]) == 'Uniform_LinUCB':
            algName[a] = 'Uniform-LinUCB'
        if str(algName[a]) == 'GOBLin':
            algName[a] = 'GOB.Lin'
        if str(algName[a]) =='Hybrid_LinUCB':
            algName[a] = 'Hybrid-LinUCB'
        if str(algName[a]) =='CFUCB':
            algName[a] = 'factorUCB w/o W'
        if str(algName[a]) =='CFEgreedy0':
            algName[a] = 'ALS'
        if str(algName[a]) =='factorLinUCB':
            algName[a] = 'factorUCB'
        if 'Master_Uniform' in str(algName[a]):
            algName[a] = 'Uniform-dLinUCB'
        if 'Uniform_LinUCB' in str(algName[a]):
            algName[a] = 'Uniform-LinUCB'
        if 'N_LinUCB' in str(algName[a]):
            algName[a] = 'N-LinUCB'
        if 'M_LinUCB_A' in str(algName[a]):
            algName[a] = 'M-LinUCB-Arbitrary'
        if 'M_LinUCB_L' in str(algName[a]):
            algName[a] = 'M-LinUCB-Friendship'
        if 'Master_LCB' in str(algName[a]):
            algName[a] = 'M_Master'
        if 'UniformAdTS' in str(algName[a]):
            algName[a] = 'Uniform-adTS'
        if '52_32' in str(algName[a]):
            algName[a] = 'DenBand-lcb'
        if 'avg' in str(algName[a]):
            algName[a] = 'DenBand-avg'
        if 'Likeli_40' in str(algName[a]):
            algName[a] = 'CoDBan'
        if 'N_Log' in str(algName[a]):
            algName[a] = 'N-CoDBan'
        if 'M_Log' in str(algName[a]):
            algName[a] = 'M_CoDBand'
        if 'CoDBand_N' in str(algName[a]):
            algName[a] = 'CoDBand'
        if 'CoDBand_Uniform' in str(algName[a]):
            algName[a] = 'Uniform-CoDBand'





        plt.plot(tim.values(), AlgCTRRatio.values(), linestyles[a], markevery=1000, linewidth=1.0,label = str(algName[a]))
        #plt.xlim([0,limit]) # Here is how to control the axis range.
        
    #print len(lastFM_ChangeList_Dense10), type(lastFM_ChangeList_Dense10)
    #print lastFM_ChangeList_Dense100
    # for i in lastFM_ChangeList_Dense100:
    #     pass
    #     #ax.axvline(i, linestyle='-')
    # for j in SWPointsList_100:
    #     pass
        #ax.axvline(j, color = 'red')
    plt.ylim([5.2,9.3])
    #plt.xlim([0.0, 95000])
    plt.xlabel('time', fontsize = 32, fontweight='bold')
    plt.ylabel('Normalized accumulated reward', fontsize = 32, fontweight='bold')
    #plt.legend( ncol = 1,prop={'size':32}, loc = 'upper right')
    plt.legend( ncol = 2,prop={'size':15}, loc = 'upper right')
    matplotlib.rcParams.update({'font.size': 28})
    #plt.title(str(dataset)+' UserNum =' + str(UserNum))
    plt.show()
    
    '''      
    plt.plot(tim.values(), ucbCTRRatio.values(), label = 'Restart_ucbCTR Ratio')
    plt.plot(tim.values(), greedyCTRRatio.values(),  label = 'greedyCTR Ratio')
    plt.legend()
    plt.show()
    '''

   
