import numpy as np
from util_functions import vectorize
class LinUCBUserStruct:
	def __init__(self, featureDimension, alpha, lambda_,  NoiseScale, init="zero"):
		self.d = featureDimension
		self.A = lambda_*np.identity(n = self.d)
		self.b = np.zeros(self.d)
		self.AInv = np.linalg.inv(self.A)
		self.NoiseScale = NoiseScale
		if (init=="random"):
			self.UserTheta = np.random.rand(self.d)
		else:
			self.UserTheta = np.zeros(self.d)
		self.time = 0

	def updateParameters(self, articlePicked_FeatureVector, click):
		self.A += np.outer(articlePicked_FeatureVector,articlePicked_FeatureVector)
		self.b += articlePicked_FeatureVector*click
		self.AInv = np.linalg.inv(self.A)
		self.UserTheta = np.dot(self.AInv, self.b)
		self.time += 1

	def getTheta(self):
		return self.UserTheta
	
	def getA(self):
		return self.A

	def getProb(self, alpha, article_FeatureVector):
		if alpha == -1:
			alpha = alpha = 0.1*np.sqrt(np.log(self.time+1))
		mean = np.dot(self.UserTheta,  article_FeatureVector)
		var = np.sqrt(np.dot(np.dot(article_FeatureVector, self.AInv),  article_FeatureVector))
		#self.alpha_t = self.NoiseScale *np.sqrt(np.log(np.linalg.det(self.A)/float(self.sigma * self.lambda_) )) + np.sqrt(self.lambda_)
		pta = mean + alpha * var
		return pta

	def getProbInfo(self, alpha, article_FeatureVector):
		if alpha == -1:
			alpha = alpha = 0.1*np.sqrt(np.log(self.time+1))
		mean = np.dot(self.UserTheta,  article_FeatureVector)
		var = np.sqrt(np.dot(np.dot(article_FeatureVector, self.AInv),  article_FeatureVector))
		self.alpha_t = self.NoiseScale *np.sqrt(np.log(np.linalg.det(self.A)/float(self.sigma * self.lambda_) )) + np.sqrt(self.lambda_)
		#pta = mean + alpha * var
		return {'mean':mean, 'var':var, 'alpha':alpha, 'alpha_t':self.alpha_t}

	def getProb_plot(self, alpha, article_FeatureVector):
		mean = np.dot(self.UserTheta,  article_FeatureVector)
		var = np.sqrt(np.dot(np.dot(article_FeatureVector, self.AInv),  article_FeatureVector))
		pta = mean + alpha * var
		return pta, mean, alpha * var

#---------------LinUCB(fixed user order) algorithm---------------
class LinUCB:
	def __init__(self, dimension, alpha, lambda_, NoiseScale, init="zero"):  # n is number of users
		self.users = {}
		self.dimension = dimension
		self.alpha = alpha
		self.lambda_ = lambda_
		self.NoiseScale = NoiseScale
		self.init = init

		self.CanEstimateUserPreference = True
		self.CanEstimateCoUserPreference = False
		self.CanEstimateW = False
		self.CanEstimateV = False
		self.CanEstimateBeta = False
	def decide(self, pool_articles, userID):
		if userID not in self.users:
			self.users[userID] = LinUCBUserStruct(self.dimension, self.alpha, self.lambda_ , self.NoiseScale, self.init)
		maxPTA = float('-inf')
		articlePicked = None

		for x in pool_articles:
			x_pta = self.users[userID].getProb(self.alpha, x.contextFeatureVector[:self.dimension])
			# pick article with highest Prob
			if maxPTA < x_pta:
				articlePicked = x
				maxPTA = x_pta

		return articlePicked
	def getProb(self, pool_articles, userID):
		means = []
		vars = []
		for x in pool_articles:
			x_pta, mean, var = self.users[userID].getProb_plot(self.alpha, x.contextFeatureVector[:self.dimension])
			means.append(mean)
			vars.append(var)
		return means, vars

	def updateParameters(self, articlePicked, click, userID):
		self.users[userID].updateParameters(articlePicked.contextFeatureVector[:self.dimension], click)
		
	def getCoTheta(self, userID):
		return self.users[userID].UserTheta
	def getTheta(self, userID):
		return self.users[userID].UserTheta

class LinUCB_Restart:
	def __init__(self, dimension, alpha, lambda_, NoiseScale, init="zero"):  # n is number of users
		self.users = []
		#algorithm have n users, each user has a user structure
		for i in range(n):
			self.users.append(LinUCBUserStruct(dimension, lambda_ , NoiseScale, init)) 

		self.dimension = dimension
		self.alpha = alpha
		self.n = n
		self.lambda_ = lambda_
		self.NoiseScale = NoiseScale
		self.init = init

		self.CanEstimateUserPreference = True
		self.CanEstimateCoUserPreference = False
		self.CanEstimateW = False
		self.CanEstimateV = False
		self.CanEstimateBeta = False

		self.changed = False
		self.precision = []
		self.recall = []
	def decide(self, pool_articles, userID, changed):
		if userID not in self.users:
			self.users[userID] = LinUCBUserStruct(self.dimension, self.alpha, self.lambda_ , self.NoiseScale, self.init)

		if changed:
			self.changed = True
			#Restart the user
			self.users[userID] = LinUCBUserStruct(self.dimension, self.alpha, self.lambda_ , self.NoiseScale, self.init)
		maxPTA = float('-inf')
		articlePicked = None
		for x in pool_articles:
			x_pta = self.users[userID].getProb(self.alpha, x.contextFeatureVector[:self.dimension])
			if maxPTA < x_pta:
				articlePicked = x
				maxPTA = x_pta

		return articlePicked
	def getProb(self, pool_articles, userID):
		means = []
		vars = []
		for x in pool_articles:
			x_pta, mean, var = self.users[userID].getProb_plot(self.alpha, x.contextFeatureVector[:self.dimension])
			means.append(mean)
			vars.append(var)
		return means, vars

	def updateParameters(self, articlePicked, click, userID):
		self.users[userID].updateParameters(articlePicked.contextFeatureVector[:self.dimension], click)
		
	def getCoTheta(self, userID):
		return self.users[userID].UserTheta
	def getTheta(self, userID):
		return self.users[userID].UserTheta



