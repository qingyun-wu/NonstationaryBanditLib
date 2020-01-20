#Command Line
#python DeliciousLastFM_ResultPlot.py ./ Delicious 3  200   10_Master_Uniform 10_Uniform_LinUCB 10_UniformAdTS
#python DeliciousLastFM_ResultPlot.py ./ Delicious 5  200 48_13 avg   10_Master_Uniform 10_UniformAdTS 10_Uniform_LinUCB
import numpy as np
import os
#from conf import *
from matplotlib.pylab import *
from operator import itemgetter
import sys
import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy

if __name__ == '__main__':
    save_address = str(sys.argv[1])
    
    filenames = [x for x in os.listdir(save_address) if '.csv' in x]

    #lastFM_ChangeList_Dense10 = pickle.load(open('./Delicious_Dense10.Change', 'rb'))
    #lastFM_ChangeList_Dense50 = pickle.load(open('./LastFM_Dense50.Change', 'rb'))
    #lastFM_ChangeList_Dense100 = pickle.load(open('./LastFM_Dense100.Change', 'rb'))

    #NewUCBList_10 = pickle.load(open('./Dense10_Delicious_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_14_11_43_47.NewUCBs', 'rb'))
    #SWPointsList_10 = pickle.load(open('./Dense10_Delicious_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_14_11_43_47.SwitchPoints', 'rb'))

    #NewUCBList_50 = pickle.load(open('./Dense50_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_15_50_06.NewUCBs', 'rb'))
    #SWPointsList_50 = pickle.load(open('./Dense50_LastFM_200_shuffled_Clustering_Master_UniformLCB_Diagnol_Opt__07_13_15_50_06.SwitchPoints', 'rb'))


    algName = {}
    dataset = str(sys.argv[2])
    fileSig = str(sys.argv[3])

    user_user_dic = {}
    user_id_list = []
    
    #linestyles = ['o-', '*-', '^-', '-', 'D-', 's-', '>-','--']
    linestyles = ['o-', 's-', '*-','>-','<-','g-', '.-', 'o-', 's-', '*-']
    #linestyles = ['o-', '*-', '^-', '-', 'D-', 's-', '>-','--']
    RandomCTR = {}
    tim = {}
    filenames.sort()
    i = -1
    CLUB_i = -1
    AlgCTR = {}
    for x in filenames:    
        filename = os.path.join(save_address, x)    
        if str(fileSig) in x:     
            with open(filename, 'r') as f:            
                print str(filename)      
                for line in f:           
                    words = line.split(',')
                    if words[0].strip() != 'data':
                        continue
                    CLUB_i = CLUB_i + 1
                    if (CLUB_i)%1==0:
                        i+=1
                        data_2= [float(x) for x in words[2].split(';')]
                        data_3 = [x for x in words[3].split(';')]
                        
                        temp, AlgCTR[i] = data_2[0],data_2[2]
                        userID, ClusterID = int(data_3[1]), int(data_3[2])
                        if userID not in user_user_dic:
                            user_user_dic[userID] = {}
                        if userID not in user_id_list:
                            user_id_list.append(userID)
                        selected_model = data_3[-1]
                        selected_model_user = int(str(selected_model).split('_')[0])
                        if selected_model_user not in user_user_dic[userID]:
                            user_user_dic[userID][selected_model_user] = 0.0
                        user_user_dic[userID][selected_model_user] +=1.0

    orginal_dic = {}
    orginal_dic = copy.copy(user_user_dic)
    print user_user_dic
    print len(user_user_dic)  
    print user_user_dic 
    print len(user_user_dic), len(user_id_list)
    sorted_user = []  
    u_matrix = []
    for u in user_user_dic.keys():
        for j in user_id_list:
            if j not in user_user_dic[u].keys():
                user_user_dic[u][j] = 0.0

    for u in user_user_dic.keys():
        u_list = []
        sorted_user.append(u)
        sorted_user_2 = []
        for i in user_user_dic[u].keys():
            sorted_user_2.append(i)
            #if user_user_dic[u][i] >0.0:
            u_list.append(user_user_dic[u][i])
            #print 'user:', u, 'user:' ,i, 'Connection:', user_user_dic[u][i]
        u_matrix.append(u_list)
    u_matrix = np.array(u_matrix)
    #print u_matrix   
    # print u_list  
    # print sorted_user , len(sorted_user)
    # print sorted_user_2 , len(sorted_user_2)
    # print len(u_matrix), len(u_matrix[0])



    vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
              "potato", "wheat", "barley"]
    farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
               "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]

    harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                        [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                        [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                        [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                        [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                        [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                        [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])

    fig, ax = plt.subplots()
    im = ax.imshow(u_matrix)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(sorted_user)))
    ax.set_yticks(np.arange(len(sorted_user)))
    # ... and label them with the respective list entries
    #ax.set_xticklabels(sorted_user)
    #ax.set_yticklabels(sorted_user_2)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    # for i in range(len(sorted_user)):
    #     for j in range(len(sorted_user_2)):
    #         text = ax.text(j, i, u_matrix[i, j],
    #                        ha="center", va="center", color="w")

    #ax.set_title("Harvest of local farmers (in tons/year)")
    #fig.tight_layout()
    #plt.show()
    for u in range(len(sorted_user)):
        print 'user', sorted_user[u], u_matrix[u]

    #Make the matrix symmetric
    u_matrix_symmetirc = u_matrix
    for i in range(len(sorted_user)):
        for j in range(len(sorted_user)):
            u_i = sorted_user[i]
            u_j = sorted_user[j]
            i_j = max(u_matrix[i][j], u_matrix[j][i])
            if i_j >1:
                result = i_j
            else:
                i_j = 0.0
            #result = i_j
            u_matrix_symmetirc[i][j] = i_j
            u_matrix_symmetirc[j][i] = i_j
    print u_matrix_symmetirc
    for i in range(len(sorted_user)):
        SUM = sum(u_matrix_symmetirc[i]) - u_matrix_symmetirc[i][i]
        if SUM ==0:
            print 'ZEROOOOOO'


    fig, ax = plt.subplots()
    im = ax.imshow(u_matrix_symmetirc)

    # We want to show all ticks...
    #ax.set_xticks(np.arange(len(sorted_user)))
    #ax.set_yticks(np.arange(len(sorted_user)))
    # ... and label them with the respective list entries
    #ax.set_xticklabels(sorted_user)
    #ax.set_yticklabels(sorted_user_2)

    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             #rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    # for i in range(len(sorted_user)):
    #     for j in range(len(sorted_user_2)):
    #         text = ax.text(j, i, u_matrix[i, j],
    #                        ha="center", va="center", color="w")

    #ax.set_title("Harvest of local farmers (in tons/year)")
    #fig.tight_layout()
    plt.show()

    ratio_matrix = u_matrix_symmetirc
    for i in range(len(sorted_user)):
        SUM_i = sum(u_matrix_symmetirc[i])
        for j in range(len(sorted_user)):
            ratio = u_matrix_symmetirc[i][j]/float(SUM_i)
            ratio_matrix[i][j] = ratio
            print ratio


    fig, ax = plt.subplots()
    im = ax.imshow(ratio_matrix)

    # We want to show all ticks...
    #ax.set_xticks(np.arange(len(sorted_user)))
    #ax.set_yticks(np.arange(len(sorted_user)))
    # ... and label them with the respective list entries
    #ax.set_xticklabels(sorted_user)
    #ax.set_yticklabels(sorted_user_2)

    # Rotate the tick labels and set their alignment.
    #plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             #rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    # for i in range(len(sorted_user)):
    #     for j in range(len(sorted_user_2)):
    #         text = ax.text(j, i, u_matrix[i, j],
    #                        ha="center", va="center", color="w")

    #ax.set_title("Harvest of local farmers (in tons/year)")
    #fig.tight_layout()
    plt.show()
    print orginal_dic
    



    

   
