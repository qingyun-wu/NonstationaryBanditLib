#Command Line
#python plot.py ./  Delicious 4  200   Master_Uniform  M_LinUCB Uniform_LinUCB UniformAdTS 
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
    plotDetection = True
    if plotDetection:

        for f in os.listdir(save_address):
            if '.Change' in f:
                lastFM_ChangeList_Dense10 = pickle.load(open('./' + str(f), 'rb'))
            if '.NewUCBs' in f:
                 NewUCBList_10 = pickle.load(open('./' + str(f), 'rb'))
                 print(NewUCBList_10)
            if '.SwitchPoints' in f:
                SWPointsList_10 = pickle.load(open('./' + str(f), 'rb'))
                print('SW', SWPointsList_10)

        #lastFM_ChangeList_Dense100 = pickle.load(open('./LastFMClustered_Dense100.Change', 'rb'))
        #lastFM_ChangeList_Dense100 = pickle.load(open('./LastFM_Dense100.Change', 'rb'))
        ''''
        NewUCBList_10 = pickle.load(open('./LastFMClusterOrder_Dense1000_Master_UniformLCB_LastFM_user_relation_adjacency_list.dat.part.200_0.3_25.0_0.0Master_UniformLCB_08_03_14_57_59.NewUCBs', 'rb'))
        SWPointsList_10 = pickle.load(open('./LastFMClusterOrder_Dense1000_Master_UniformLCB_LastFM_user_relation_adjacency_list.dat.part.200_0.3_25.0_0.0Master_UniformLCB_08_03_14_57_59.SwitchPoints', 'rb'))
        
        NewUCBList_50 = pickle.load(open('./Dense50_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_15_50_06.NewUCBs', 'rb'))
        SWPointsList_50 = pickle.load(open('./Dense50_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_15_50_06.SwitchPoints', 'rb'))
        

        NewUCBList_100 = pickle.load(open('./ClusterOrder_Dense100_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__08_03_00_58_27.NewUCBs', 'rb'))
        SWPointsList_100 = pickle.load(open('./ClusterOrder_Dense100_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__08_03_00_58_27.SwitchPoints', 'rb'))
        '''
    algName = {}
    dataset = str(sys.argv[2])
    algNum = int(sys.argv[3])
    UserNum = int(sys.argv[4])
    for a in range(algNum):
        algName[a] = sys.argv[5+a]
    linestyles = ['o-', '*-', '^-', '-', 'D-', 's-', '>-','--']

    RandomCTR = {}
    tim = {}
    filenames.sort()
    i = -1
    fig, ax = plt.subplots()
    for x in filenames:    
        filename = os.path.join(save_address, x)    
        if str(algName[0]) in x and str(UserNum) in x:     
            with open(filename, 'r') as f:            
                print(str(filename))      
                for line in f:
                    words = line.split(',')
                    if words[0].strip() != 'data':
                        continue
                    i +=1 
                    data= [float(x) for x in words[2].split(';')]
                    RandomCTR[i] = data[0]

    print(len(RandomCTR))
    print(RandomCTR[0])
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
            algName[a] = 'dLinUCB'
        if 'Uniform_LinUCB' in str(algName[a]):
            algName[a] = 'LinUCB'
        if 'N_LinUCB' in str(algName[a]):
            algName[a] = 'N_LinUCB'
        if 'M_LinUCB' in str(algName[a]):
            algName[a] = 'OracleLinUCB'
        if 'Master_Active' in str(algName[a]):
            algName[a] = 'M_Master_noDiscard'
        if 'Master_LCB' in str(algName[a]):
            algName[a] = 'M_Master'
        if 'UniformAdTS' in str(algName[a]):
            algName[a] = 'adTS'
        #if 'AdTS' in 



        plt.plot(tim.values(), AlgCTRRatio.values(), linestyles[a], markevery=1000, linewidth=1.8,label = str(algName[a]))
        #plt.xlim([0,limit]) # Here is how to control the axis range.
    
    
    
    if plotDetection:
        print(len(lastFM_ChangeList_Dense10), type(lastFM_ChangeList_Dense10))
        print('changeList', lastFM_ChangeList_Dense10)
        ChangeList = lastFM_ChangeList_Dense10

        ax.axvline(ChangeList[0], color = 'black', linestyle='--', linewidth= 3, label = 'actuall changes')
        for i in ChangeList:
            #pass
            ax.axvline(i, color = 'black', linestyle='--',linewidth= 3)

        ax.axvline(NewUCBList_10[0], color = 'b', linestyle='--',linewidth= 3, label = 'detected changes')
        for j in NewUCBList_10:
            ax.axvline(j, color = 'b',linestyle='--',linewidth= 3)
    
    plt.ylim([2,15])
    plt.xlabel('time', fontsize = 32, fontweight='bold')
    plt.ylabel('Normalized accumulated reward', fontsize = 32, fontweight='bold')
    plt.legend( ncol = 2,prop={'size':25}, loc = 'lower right')
    matplotlib.rcParams.update({'font.size': 28})
    #plt.title(str(dataset)+' UserNum =' + str(UserNum))
    plt.show()
    
    '''      
    plt.plot(tim.values(), ucbCTRRatio.values(), label = 'Restart_ucbCTR Ratio')
    plt.plot(tim.values(), greedyCTRRatio.values(),  label = 'greedyCTR Ratio')
    plt.legend()
    plt.show()
    '''

   