#Command Line
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
    save_address = './'
    
    filenames = [x for x in os.listdir(save_address) if '.csv' in x]

    u_id_list = [41, 87, 181, 212, 223, 362, 411, 509, 510, 511, 566, 645, 652, 698, 851, 923, 945, 1088, 1098, 1140, 1196, 1250, 1399, 1465, 1516, 1535, 1656, 1682, 1741, 1830]

    u_id = 87

    all_user_list = [1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 15, 19, 21, 23, 24, 25, 26, 29, 31, 33, 35, 37, 38, 39, 41, 43, 44, 45, 46, 47, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 70, 71, 75, 80, 81, 82, 84, 87, 88, 92, 93, 95, 97, 98, 100, 105, 106, 107, 113, 115, 119, 120, 123, 125, 129, 131, 132, 133, 135, 137, 138, 139, 142, 144, 145, 147, 148, 150, 154, 155, 157, 158, 160, 161, 162, 163, 164, 165, 166, 168, 169, 173, 175, 178, 180, 181, 183, 187, 188, 191, 192, 194, 197, 198, 199, 200, 203, 204, 206, 207, 209, 211, 212, 214, 215, 216, 219, 221, 222, 223, 225, 226, 227, 229, 232, 233, 234, 236, 237, 239, 240, 245, 246, 247, 248, 250, 251, 256, 257, 260, 262, 264, 265, 266, 270, 271, 276, 278, 279, 280, 283, 288, 289, 292, 293, 296, 297, 298, 300, 301, 303, 304, 305, 307, 308, 315, 319, 328, 330, 331, 333, 334, 336, 337, 338, 340, 343, 345, 349, 351, 355, 356, 357, 362, 363, 364, 365, 366, 367, 369, 370, 373, 377, 379, 380, 382, 383, 387, 391, 392, 395, 396, 399, 402, 403, 405, 407, 408, 411, 412, 418, 420, 422, 424, 425, 428, 429, 430, 431, 432, 435, 440, 443, 444, 450, 453, 457, 459, 460, 461, 462, 463, 465, 468, 472, 475, 476, 479, 481, 483, 484, 485, 488, 494, 495, 498, 501, 504, 506, 508, 509, 510, 511, 513, 516, 521, 522, 526, 527, 528, 530, 532, 534, 537, 541, 542, 543, 544, 545, 546, 549, 556, 557, 559, 562, 563, 564, 566, 567, 569, 570, 571, 573, 575, 581, 582, 583, 586, 588, 592, 593, 596, 598, 599, 600, 601, 602, 603, 604, 607, 609, 610, 611, 612, 613, 614, 615, 623, 624, 626, 628, 629, 630, 632, 634, 636, 638, 639, 642, 643, 644, 645, 647, 650, 651, 652, 657, 658, 659, 660, 662, 663, 665, 667, 668, 673, 677, 679, 680, 686, 688, 689, 694, 695, 698, 700, 701, 702, 703, 705, 706, 707, 708, 710, 712, 713, 714, 717, 719, 720, 722, 724, 725, 729, 730, 735, 736, 737, 739, 741, 742, 744, 750, 752, 754, 755, 756, 763, 764, 765, 766, 767, 770, 775, 777, 778, 780, 784, 786, 787, 788, 789, 790, 798, 799, 800, 802, 809, 813, 814, 819, 821, 822, 828, 830, 831, 832, 834, 835, 836, 838, 839, 842, 844, 845, 846, 847, 848, 849, 850, 851, 852, 854, 855, 859, 861, 863, 864, 865, 866, 867, 868, 869, 870, 874, 875, 876, 877, 878, 879, 883, 885, 887, 889, 891, 892, 894, 896, 897, 898, 899, 901, 904, 910, 911, 913, 914, 916, 919, 920, 922, 923, 924, 925, 926, 928, 931, 932, 936, 937, 939, 940, 941, 942, 945, 946, 947, 950, 951, 953, 955, 958, 961, 962, 963, 964, 966, 967, 971, 972, 973, 975, 983, 984, 985, 988, 989, 990, 991, 993, 995, 997, 998, 1000, 1001, 1002, 1003, 1004, 1005, 1007, 1008, 1010, 1011, 1014, 1016, 1018, 1023, 1026, 1029, 1032, 1033, 1040, 1041, 1049, 1050, 1051, 1052, 1053, 1057, 1061, 1062, 1064, 1065, 1067, 1069, 1070, 1072, 1073, 1074, 1079, 1080, 1082, 1083, 1084, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1095, 1098, 1101, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1111, 1115, 1116, 1117, 1120, 1122, 1123, 1124, 1125, 1126, 1127, 1129, 1131, 1134, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1145, 1146, 1147, 1153, 1155, 1157, 1159, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1173, 1177, 1180, 1186, 1189, 1190, 1196, 1198, 1201, 1202, 1203, 1204, 1205, 1207, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1228, 1230, 1231, 1233, 1234, 1235, 1237, 1242, 1243, 1244, 1250, 1251, 1257, 1258, 1259, 1261, 1262, 1264, 1269, 1270, 1271, 1272, 1275, 1277, 1280, 1284, 1286, 1287, 1289, 1290, 1291, 1294, 1295, 1296, 1299, 1300, 1302, 1304, 1306, 1307, 1310, 1311, 1313, 1314, 1315, 1316, 1319, 1321, 1322, 1323, 1324, 1325, 1326, 1329, 1331, 1332, 1337, 1338, 1340, 1343, 1344, 1346, 1347, 1348, 1349, 1350, 1353, 1354, 1355, 1356, 1360, 1363, 1365, 1366, 1369, 1371, 1372, 1375, 1377, 1379, 1380, 1383, 1386, 1387, 1393, 1395, 1397, 1399, 1402, 1403, 1407, 1410, 1411, 1412, 1417, 1418, 1419, 1420, 1426, 1427, 1428, 1429, 1431, 1432, 1436, 1439, 1441, 1443, 1447, 1449, 1450, 1458, 1459, 1460, 1463, 1464, 1465, 1466, 1467, 1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1480, 1483, 1484, 1485, 1487, 1490, 1491, 1492, 1494, 1496, 1500, 1501, 1503, 1505, 1506, 1507, 1508, 1510, 1511, 1514, 1515, 1516, 1518, 1519, 1520, 1522, 1524, 1525, 1526, 1530, 1534, 1535, 1536, 1537, 1539, 1540, 1541, 1542, 1543, 1544, 1545, 1546, 1547, 1549, 1550, 1551, 1555, 1556, 1558, 1559, 1560, 1562, 1563, 1566, 1567, 1570, 1572, 1574, 1575, 1577, 1580, 1582, 1583, 1584, 1585, 1586, 1587, 1591, 1596, 1598, 1599, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1614, 1617, 1618, 1619, 1620, 1622, 1624, 1625, 1626, 1627, 1628, 1630, 1634, 1637, 1638, 1640, 1642, 1646, 1647, 1648, 1649, 1651, 1656, 1659, 1661, 1666, 1667, 1668, 1670, 1671, 1672, 1673, 1674, 1675, 1676, 1677, 1680, 1681, 1682, 1686, 1690, 1691, 1694, 1695, 1696, 1697, 1699, 1700, 1701, 1702, 1703, 1705, 1706, 1710, 1711, 1714, 1715, 1716, 1719, 1722, 1723, 1724, 1726, 1728, 1730, 1731, 1732, 1733, 1735, 1738, 1739, 1740, 1741, 1742, 1743, 1745, 1746, 1749, 1751, 1752, 1754, 1755, 1758, 1759, 1761, 1764, 1765, 1768, 1769, 1770, 1771, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1781, 1782, 1785, 1788, 1792, 1793, 1795, 1796, 1797, 1798, 1799, 1805, 1808, 1809, 1811, 1812, 1815, 1817, 1818, 1819, 1820, 1822, 1823, 1827, 1829, 1830, 1831, 1832, 1836, 1838, 1839, 1842, 1843, 1846, 1847, 1848, 1849, 1851, 1853, 1858, 1859, 1860, 1863, 1864, 1865, 1866, 1868, 1872, 1874, 1876, 1882, 1883, 1884, 1887, 1888, 1889, 1891, 1892]
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
    #dataset = str(sys.argv[2])
    #algNum = int(sys.argv[3])
    #UserNum = int(sys.argv[4])
    #for a in range(algNum):
    #    algName[a] = sys.argv[5+a]
    #linestyles = ['o-', '*-', '^-', '-', 'D-', 's-', '>-','--']
    linestyles = ['o-', 's-', '*-','>-','<-','g-', '.-', 'o-', 's-', '*-']
    RandomCTR = {}
    tim = {}
    all_time = {}
    better_ratio = {}
    worse_ratio = {}

    better_count = 0
    worse_count = 0
    #filenames.sort()
    i = -1


    fig, ax = plt.subplots()
    #name_1 = 'Dense10_N_LinUCB_LastFM_user_relation_adjacency_list.dat.part.200_0.3_20_0.0_07_14_15_34_37.csv'
    name_1 = 'Dense10_N_Master_LCBInterval_LastFM_user_relation_adjacency_list.dat.part.200_0.3_50.0_0.3_08_10_21_07_38.csv'
    name_2 = 'Dense10_dLinUCB_Likelihood_N_Log_LastFM_user_relation_adjacency_list.dat.part.200_0.3_Likeli_100_5.0_0.25__08_31_20_45_39.csv'
    #name_2 = 'Dense10_CoDBand_N__LastFM_user_relation_adjacency_list.dat.part.200_0.3_Likeli_100_0.1_0.2_Sample_Stored_Sample200__01_15_22_08_49.csv'
    filename_1 = os.path.join(save_address, name_1)  
    filename_2 = os.path.join(save_address, name_2)    
    user_cluster_dic = {} 
    all_reward_list1= []
    all_reward_list2 = []   
    user_reward_list1 = []
    user_reward_list2 = []
    random_reward_list = []

    user_rewardRatio_list1 = []
    user_rewardRatio_list2 = []


    user_reward_dic_1 = {}
    user_reward_dic_2 = {}

    user_reward_acc_dic_1 = {}
    user_reward_acc_dic_2 = {}


 
    with open(filename_1, 'r') as f:            
        #print str(filename)      
        for line in f:
            words = line.split(',')
            if words[0].strip() != 'data':
                continue
            i +=1 
            
            data= [float(x) for x in words[2].split(';')]
            cluster_id = int(words[3].split(';')[1])
            if cluster_id not in user_cluster_dic:
                user_cluster_dic[cluster_id] = 0
                user_reward_dic_1[cluster_id] = []
                user_reward_acc_dic_1[cluster_id] = []

            user_cluster_dic[cluster_id] +=1
            all_reward_list1.append(data[2])
            if len(all_reward_list1) >1:
                user_reward_dic_1[cluster_id].append(all_reward_list1[-1] - all_reward_list1[-2])
            else:
                user_reward_dic_1[cluster_id].append(all_reward_list1[-1] )

            user_reward_acc_dic_1[cluster_id].append(sum(user_reward_dic_1[cluster_id]))


    i = -1
    user_cluster_dic = {}
    with open(filename_2, 'r') as f_2:            
        #print str(filename)      
        for line in f_2:
            words = line.split(',')
            if words[0].strip() != 'data':
                continue
            i +=1 
            data= [float(x) for x in words[2].split(';')]
            cluster_id = int(words[3].split(';')[1])
            if cluster_id not in user_cluster_dic:
                user_cluster_dic[cluster_id] = 0
                user_reward_dic_2[cluster_id] = []
                user_reward_acc_dic_2[cluster_id] = []

            user_cluster_dic[cluster_id] +=1
            all_reward_list2.append(data[2])
            if len(all_reward_list2) >1:
                user_reward_dic_2[cluster_id].append(all_reward_list2[-1] - all_reward_list2[-2])
            else:
                user_reward_dic_2[cluster_id].append(all_reward_list2[-1])

            user_reward_acc_dic_2[cluster_id].append(sum(user_reward_dic_2[cluster_id]))

    print "Yes"
    current_user_list = []
    i = -1
    with open(filename_2, 'r') as f_3:            
        #print str(filename)  

        for line in f_3:
            words = line.split(',')
            if words[0].strip() != 'data':
                continue
            i +=1 
            all_time[i] = i
            data= [float(x) for x in words[2].split(';')]
            cluster_id = int(words[3].split(';')[1])
            current_user_list.append(cluster_id)
            uu = cluster_id
            l = len(current_user_list)
            #for uu in current_user_list:
            diff_buffer = 0.01
            if user_reward_acc_dic_2[uu][-1] > (1.0 + diff_buffer)*user_reward_acc_dic_1[uu][-1]:
                better_count +=1
                #print 'better', better_count
            elif user_reward_acc_dic_2[uu][-1] < (1.0 - diff_buffer)*user_reward_acc_dic_1[uu][-1]:
                worse_count +=1
                #print 'worse', worse_count
            better_ratio[i] = better_count/float(l)
            worse_ratio[i] = worse_count/float(l)

    # print better_ratio
    plt.plot(all_time.values(), better_ratio.values(), linestyles[0], markevery=1000, linewidth=1.0,label = 'CoDBand better ratio')
    plt.plot(all_time.values(), worse_ratio.values(), linestyles[0], markevery=1000, linewidth=1.0,label = 'CoDBand wrose ratio')
    #plt.plot(tim.values(), user_reward_list1_acc, linestyles[0], markevery=1000, linewidth=1.0,label = 'dLinUCB' + ':u_id ' + str(u_id))
    #plt.plot(tim.values(), user_reward_list2_acc, linestyles[1], markevery=1000, linewidth=1.0,label = 'CoDBand' + ':u_id ' + str(u_id))
    # plt.ylim([5,9])
    # plt.xlim([0.0, 95000])
    plt.xlabel('time', fontsize = 32, fontweight='bold')
    plt.ylabel('Accumulated reward', fontsize = 32, fontweight='bold')
    # #plt.legend( ncol = 1,prop={'size':32}, loc = 'upper right')
    plt.legend( ncol = 1,prop={'size':15}, loc = 'lower right')
    # matplotlib.rcParams.update({'font.size': 28})
    # #plt.title(str(dataset)+' UserNum =' + str(UserNum))
    plt.show()


   
