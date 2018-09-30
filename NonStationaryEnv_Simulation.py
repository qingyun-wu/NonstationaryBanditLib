import copy
import numpy as np
import random
from random import sample, shuffle, choice
from scipy.sparse import csgraph
import datetime
import os.path
import matplotlib.pyplot as plt
import argparse
from sklearn.decomposition import TruncatedSVD
from sklearn import cluster
from sklearn.decomposition import PCA
# local address to save simulated users, simulated articles, and results
from conf import sim_files_folder, save_address
from util_functions import featureUniform, gaussianFeature
from Articles import ArticleManager
from Users import UserManager
#Stationary Bandit algorithms
from lib.LinUCB import LinUCB, LinUCB_Restart
from lib.AdaptiveThompson import AdaptiveThompson
from lib.dLinUCB import dLinUCB

class simulateOnlineData(object):
	def __init__(self, namelabel, context_dimension,testing_iterations, change_schedule, testing_method, plot, articles, users, 
					batchSize = 1000,
					noise = lambda : 0,
					type_ = 'UniformTheta', 
					signature = '', 
					poolArticleSize = 10, 
					NoiseScale = 0,
					Plot = True,
					Write_to_File = False):

		self.simulation_signature = signature
		self.type = type_
		self.context_dimension = context_dimension
		self.testing_iterations = testing_iterations
		self.change_schedule = change_schedule
		self.testing_method = testing_method
		self.noise = noise
		self.NoiseScale = NoiseScale
		self.articles = articles 
		self.users = users
		self.poolArticleSize = poolArticleSize
		self.batchSize = batchSize

		self.Plot = Plot
		self.Write_to_File = Write_to_File

	def getTheta(self):
		Theta = np.zeros(shape = (self.dimension, len(self.users)))
		for i in range(len(self.users)):
			Theta.T[i] = self.users[i].theta
		return Theta
	def batchRecord(self, iter_):
		print "Iteration %d"%iter_, "Pool", len(self.articlePool)," Elapsed time", datetime.datetime.now() - self.startTime

	def regulateArticlePool(self):
		# Randomly generate articles
		self.articlePool = sample(self.articles, self.poolArticleSize)   

	def getReward(self, user, pickedArticle):
		return np.dot(user.theta, pickedArticle.featureVector)

	def GetOptimalReward(self, user, articlePool):		
		maxReward = float('-inf')
		maxx = None
		for x in articlePool:	 
			reward = self.getReward(user, x)
			if reward > maxReward:
				maxReward = reward
				maxx = x
		return maxReward, x
	
	def getL2Diff(self, x, y):
		return np.linalg.norm(x-y) # L2 norm

	def runAlgorithms(self, algorithms):
		self.startTime = datetime.datetime.now()
		timeRun = self.startTime.strftime('_%m_%d_%H_%M') 
		filenameWriteRegret = os.path.join(save_address, 'AccRegret' + timeRun + '.csv')
		filenameWritePara = os.path.join(save_address, 'ParameterEstimation' + timeRun + '.csv')

		tim_ = []
		BatchCumlateRegret = {}
		AlgRegret = {}
		ThetaDiffList = {}
		ThetaDiff = {}
		Var = {}
		
		# Initialization
		userSize = len(self.users)
		for alg_name, alg in algorithms.items():
			AlgRegret[alg_name] = []
			BatchCumlateRegret[alg_name] = []
			if alg.CanEstimateUserPreference:
				ThetaDiffList[alg_name] = []
			Var[alg_name] = []

		if self.Write_to_File:
			with open(filenameWriteRegret, 'w') as f:
				f.write('Time(Iteration)')
				f.write(',' + ','.join( [str(alg_name) for alg_name in algorithms.iterkeys()]))
				f.write('\n')
			
			with open(filenameWritePara, 'w') as f:
				f.write('Time(Iteration)')
				f.write(','+ ','.join([str(alg_name)+'Theta' for alg_name in ThetaDiffList.iterkeys()]))
				f.write('\n')
			

		# Shuffle the candidate arm pool
		shuffle(self.articles)
		actual_changes = [0]
		actual_changes_value = {}
		ThetaList = {}
		arm_trueReward = {}
		for u in self.users:
			actual_changes_value[u.id] = [1]
			ThetaList[u.id] = [u.theta]
		for iter_ in range(self.testing_iterations):
			noise = self.noise()
			# prepare to record theta estimation error
			for a in self.articles:
				if a.id not in arm_trueReward:
					arm_trueReward[a.id] = []
				arm_trueReward[a.id].append(np.dot(a.featureVector, self.users[0].theta)+ noise)

			for alg_name, alg in algorithms.items():
				if alg.CanEstimateUserPreference:
					ThetaDiff[alg_name] = 0
				
			#Simulate the changes
			if iter_ > (actual_changes[-1] + self.change_schedule):
				roll = random.random()
				if (roll > 0.5):
					actual_changes.append(iter_)
					for u in self.users:
						new_theta_vector = featureUniform(10, argv = {'l2_limit':1}) #hardcoded 5 in for now
						l2_norm = np.linalg.norm(new_theta_vector, ord =2)
						new_theta = new_theta_vector / l2_norm
						while (np.linalg.norm(new_theta - u.theta) < 0.9):
							new_theta_vector = featureUniform(10, argv = {'l2_limit':1}) #hardcoded 5 in for now
							l2_norm = np.linalg.norm(new_theta_vector, ord =2)
							new_theta = new_theta_vector / l2_norm

						old_theta = u.theta
						u.theta = new_theta
						actual_changes_value[u.id].append(1)


			for u in self.users:
				self.regulateArticlePool() # select random articles
				noise = self.noise()
				OptimalReward, OptimalArticle = self.GetOptimalReward(u, self.articlePool) 
				OptimalReward += noise
							
				for alg_name, alg in algorithms.items():
					#Observe the candiate arm pool and algoirhtm makes a decision
					pickedArticle = alg.decide(self.articlePool, u.id)
					#Get the feedback from the environment
					reward = self.getReward(u, pickedArticle) + noise
					#The feedback/observation will be fed to the algorithm to further update the algorithm's model estimation
					alg.updateParameters(pickedArticle, reward, u.id)

					#Calculate and record the regret
					regret = OptimalReward - reward	
					AlgRegret[alg_name].append(regret)

					#Update parameter estimation record
					if alg.CanEstimateUserPreference:
						ThetaDiff[alg_name] += self.getL2Diff(u.theta, alg.getTheta(u.id))
					
			for alg_name, alg in algorithms.items():
				if alg.CanEstimateUserPreference:
					ThetaDiffList[alg_name] += [ThetaDiff[alg_name]/userSize]
							
			if iter_%self.batchSize == 0:
				self.batchRecord(iter_)
				tim_.append(iter_)
				for alg_name in algorithms.iterkeys():
					BatchCumlateRegret[alg_name].append(sum(AlgRegret[alg_name]))

				if self.Write_to_File:
					with open(filenameWriteRegret, 'a+') as f:
						f.write(str(iter_))
						f.write(',' + ','.join([str(BatchCumlateRegret[alg_name][-1]) for alg_name in algorithms.iterkeys()]))
						f.write('\n')
					with open(filenameWritePara, 'a+') as f:
						f.write(str(iter_))
						f.write(','+ ','.join([str(ThetaDiffList[alg_name][-1]) for alg_name in ThetaDiffList.iterkeys()]))
			
						f.write('\n')

		print("Actual change points: " + str(actual_changes))
		for alg_name in algorithms.iterkeys():
			if 'dLinUCB' in alg_name:
				print alg_name,'Switch Points:', str(algorithms[alg_name].users[0].SwitchPoints)
				print( str(alg_name)+ "New UCBS: " + str(algorithms[alg_name].users[0].newUCBs))
				print(str(alg_name) + "Discarded UCBS: " + str(algorithms[alg_name].users[0].discardUCBs))

		#Plot Switch Points
		for alg_name, alg in algorithms.items():
			if 'dLinUCB' in alg_name:
				total = len(alg.users[0].ModelSelection)
				break
		ActualChanges_List = []

		for j in range(total):
			if j in actual_changes:
				index = actual_changes.index(j)
				print index, actual_changes_value[0][index]
				ActualChanges_List.append(actual_changes_value[0][index] )

		Alg_Changes_List = {}
		Alg_newUCBs_List = {}
		Alg_discardUCBs_List = {}

		if self.Plot: # only plot
		 	linestyles = ['o-', 's-', '*-','>-','<-','g-', '.-', 'o-', 's-', '*-']
			markerlist = ['*', 's', 'o', '*', 's']

			f, axa = plt.subplots(2, sharex=True)
			# plot the results	
			#f, axa = plt.subplots(1, sharex=True)
			count = 0
			linestyles = ['o-', 's-', '*-','>-','<-','g-', '.-', 'o-', 's-', '*-']
			markerslist = ['o','s','*','g','>','<']
			for alg_name, alg in algorithms.items():
				labelName = alg_name
				axa[0].plot(tim_, BatchCumlateRegret[alg_name], linewidth = 2, marker = markerlist[count], markevery = 400,  label = labelName)
				if alg.CanEstimateUserPreference:
					axa[1].plot(tim_, ThetaDiffList[alg_name], linewidth = 2, marker = markerlist[count], markevery = 400,  label = labelName)
				count +=1
			axa[0].axvline(actual_changes[0], color='r', linestyle='-', linewidth=1.5 , label = 'Actual Changes')
			for k in actual_changes:
				axa[0].axvline(k, color='r', linestyle='-', linewidth=1.5 )

			for alg_name, alg in algorithms.items():	
				if 'dLinUCB' in alg_name:
					alg = algorithms[alg_name]
					axa[0].axvline(alg.users[0].newUCBs[0], color='b', linestyle='-', linewidth=1.5 , label = 'dLinUCB Detected Changes')
					for j in alg.users[0].newUCBs:
						axa[0].axvline(j, color='b', linestyle='-', linewidth=1.5 )
				
			axa[0].legend(loc='upper left',prop={'size':10}, ncol = 2)
			#axa[2].set_xlabel("Iteration", fontsize = 20, fontweight='bold')
			axa[0].set_ylabel("Regret", fontsize = 22, fontweight='bold')
			axa[0].set_title("Accumulated Regret")
	
			axa[1].legend(loc='upper left',prop={'size':10}, ncol = 1)
			axa[1].set_xlabel("Iteration")
			axa[1].set_ylabel("L2 Diff")
			#axa[1].set_yscale('log')
			axa[1].set_title("Parameter estimation error")

			plt.xlabel("Iteration", fontsize = 22, fontweight='bold')
			#plt.savefig('./results/'  + str(namelabel) + str(timeRun) + '.pdf')
			plt.show()
		finalRegret = {}
		for alg_name in algorithms.iterkeys():
			print '%s: %.2f' % (alg_name, BatchCumlateRegret[alg_name][-1])

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = '')
	parser.add_argument('--alg', dest='alg', help='Select a specific algorithm, could be CoLin, hLinUCB, factorUCB, LinUCB, etc.')
	parser.add_argument('--namelabel', dest='namelabel', help='Name')
	parser.add_argument('--tau', type=int, help='Set the obsevation window of dLinUCB (should be smaller than the length of longest stationary period).')
	parser.add_argument('--delta_1', type=float, help='Set delta_1 in dLinUCB (should be a quite small float number).')
	parser.add_argument('--delta_2', type=float, help='Set delta_1 in dLinUCB (should be a quite small float number).')
	
	args = parser.parse_args()
	algName = str(args.alg)
	namelabel = str(args.namelabel)
	
	#Configuration about the environmention
	testing_iterations = 2000   # Total iteration num
	change_schedule = 500       # Change schedule
	NoiseScale = 0.01			# Noise in the feedback
	context_dimension = 10      #Feature dimension
	n_articles = 1000         	# Total number of arms/articles
	ArticleGroups = 0           # 
	n_users = 1                 # Number of users
	UserGroups = 50 
	poolSize = 10               # The number of arms in the armpool in each itereation
	batchSize = 1               # The batchsize when calculating and plotting the regret
	Write_to_File = False

	#Parameters of LinUCB
	lambda_ = 0.1   # Regularization in slave model (since we are using linear model as slave model, it is the regularization in ridge regression)   
	alpha = 0.6     # The coefficient for exploration in LinUCB
	# Additional paraters for dLinUCB
	# tau is the observation window in dLinUCB (should be larger than 0 and smaller than the change schedule)
	if args.tau:
		tau = int(args.tau)
	else:
		tau = 100    
	# delta_1 and delta_2 should be very small numbers
	if args.delta_1:
		delta_1 = float(args.delta_1)
	else:
		delta_1 = 1e-2 
	if args.delta_1:
		delta_1 = float(args.delta_1)
	else:
		delta_1 = 1e-1 
	# tilde_delta_1 should be a number between 0 and self.delta_1
	tilde_delta_1 = delta_1/5.0


	userFilename = os.path.join(sim_files_folder, "users_"+str(n_users)+"context_"+str(context_dimension)+ "Ugroups" + str(UserGroups)+".json")
	
	#"Run if there is no such file with these settings; if file already exist then comment out the below funciton"
	# we can choose to simulate users every time we run the program or simulate users once, save it to 'sim_files_folder', and keep using it.
	UM = UserManager(context_dimension, n_users, UserGroups = UserGroups, thetaFunc=gaussianFeature, argv={'l2_limit':1})
	users = UM.simulateThetafromUsers()
	# UM.saveUsers(users, userFilename, force = False)
	# users = UM.loadUsers(userFilename)

	articlesFilename = os.path.join(sim_files_folder, "articles_"+str(n_articles)+"context_"+str(context_dimension)+ "Agroups" + str(ArticleGroups)+".json")
	# Similarly, we can choose to simulate articles every time we run the program or simulate articles once, save it to 'sim_files_folder', and keep using it.
	AM = ArticleManager(context_dimension, n_articles=n_articles, ArticleGroups = ArticleGroups,
			FeatureFunc=gaussianFeature,  argv={'l2_limit':1})
	articles = AM.simulateArticlePool()
	AM.saveArticles(articles, articlesFilename, force=False)
	articles = AM.loadArticles(articlesFilename)
	

	
	for i in range(len(articles)):
		articles[i].contextFeatureVector = articles[i].featureVector[:context_dimension]

	simExperiment = simulateOnlineData(namelabel = namelabel, context_dimension = context_dimension,
						testing_iterations = testing_iterations,
						change_schedule = change_schedule,
						testing_method = "online", # batch or online
						plot = True,
						articles=articles,
						users = users,		
						noise = lambda : np.random.normal(scale = NoiseScale),
						batchSize = batchSize,
						type_ = "UniformTheta", 
						signature = AM.signature,
						poolArticleSize = poolSize, NoiseScale = NoiseScale, Write_to_File = False)

	print "Starting for ", simExperiment.simulation_signature

	algorithms = {}
	if not args.alg:
		algorithms['LinUCB'] = LinUCB(dimension = context_dimension, alpha = alpha, lambda_ = lambda_, NoiseScale =NoiseScale)
		#algorithms['adTS'] = AdaptiveThompson(dimension = context_dimension, AdTS_Window = 200, AdTS_CheckInter = 50, sample_num = 1000, v = 0.1)
		algorithms['dLinUCB'] = dLinUCB(dimension = context_dimension, alpha = alpha, lambda_ = lambda_, NoiseScale =NoiseScale, tau = tau)
	

	elif algName == 'LinUCB':
		algorithms['LinUCB'] = LinUCB(dimension = context_dimension, alpha = alpha, lambda_ = lambda_, NoiseScale =NoiseScale)
	#elif algName == 'adTS':
		#algorithms['adTS'] = AdaptiveThompson(dimension = context_dimension, AdTS_Window = 200, AdTS_CheckInter = 50, sample_num = 1000, v = 0.1)
	else:
		algorithms['dLinUCB'] = dLinUCB(dimension = context_dimension, alpha = alpha, lambda_ = lambda_, NoiseScale =NoiseScale, tau = tau)
		

	simExperiment.runAlgorithms(algorithms)