from collections import Counter
from math import log
import numpy as np 

#from random import random, shuffle
from custom_errors import FileExists 
#import random
import random

def get_new_theta(dimension, old_theta, gap):
	new_theta_vector = featureUniform(dimension, argv = {'l2_limit':1}) #hardcoded 5 in for now
	l2_norm = np.linalg.norm(new_theta_vector, ord =2)
	new_theta = new_theta_vector / l2_norm

	#print np.linalg.norm(new_theta - u.theta)
	while (np.linalg.norm(new_theta - old_theta) < gap):
		new_theta_vector = featureUniform(dimension, argv = {'l2_limit':1}) #hardcoded 5 in for now
		l2_norm = np.linalg.norm(new_theta_vector, ord =2)
		new_theta = new_theta_vector / l2_norm
	return new_theta
def get_new_theta_perturbation(dimension, old_theta, perturbation):
	Gaussian_argv = {}
	if 'small' in str(perturbation):
		Gaussian_argv['mean'] = 0.0
		Gaussian_argv['std'] = 0.0001
	else:
		Gaussian_argv['mean'] = 0.0
		Gaussian_argv['std'] = 0.1

	perturbation = gaussianFeature(dimension, argv = Gaussian_argv)
	new_theta_vector = old_theta + perturbation
	l2_norm = np.linalg.norm(new_theta_vector, ord =2)
	new_theta = new_theta_vector / l2_norm
	return new_theta
def get_noramlized_vector(dimension):
	feature_vector = featureUniform(dimension, argv = {'l2_limit':1}) #hardcoded 5 in for now
	l2_norm = np.linalg.norm(feature_vector, ord =2)
	normalized_vector = feature_vector / l2_norm
	return normalized_vector
def get_noramlized_vector_perturbation(dimension, old_vector, perturbation):
	print 'old', old_vector
	old_vector = np.array(old_vector)
	#old_vector =  np.around(old_vector, decimals=3)
	Gaussian_argv = {}
	if 'small' in str(perturbation):
		Gaussian_argv['mean'] = 0.0
		Gaussian_argv['std'] = 0.0001
		perturbation = abs(np.array(gaussianFeature(dimension, argv = Gaussian_argv) ))

		new_vector = old_vector + perturbation
		l2_norm = np.linalg.norm(new_vector, ord =2)
		new_normalized_vector = new_vector / l2_norm
		print 'small', new_normalized_vector
	else:
		Gaussian_argv['mean'] = 0.0
		Gaussian_argv['std'] = 0.1
		random.shuffle(old_vector)
		new_normalized_vector = old_vector
		print 'large', old_vector, list(old_vector), new_normalized_vector
	
	print 'generated', new_normalized_vector
	
	return np.array(new_normalized_vector)


def get_new_theta_from_neighbor(dimension, all_users, W, current_user_id):
	old_theta = all_users[current_user_id].theta
	new_theta = np.zeros(dimension)
	for uj in all_users:
		
		if W[uj.id][current_user_id] > 0.4 and uj.id != current_user_id:
			new_theta = uj.theta

		#if uj != current_user_id:
		#	new_theta += W[uj.id][current_user_id] * np.asarray(uj.theta)
	
	return new_theta


def gaussianFeature(dimension, argv):
	mean = argv['mean'] if 'mean' in argv else 0
	std = argv['std'] if 'std' in argv else 1

	mean_vector = np.ones(dimension)*mean
	stdev = np.identity(dimension)*std
	vector = np.random.multivariate_normal(np.zeros(dimension), stdev)

	l2_norm = np.linalg.norm(vector, ord = 2)
	if 'l2_limit' in argv and l2_norm > argv['l2_limit']:
		"This makes it uniform over the circular range"
		vector = (vector / l2_norm)
		vector = vector * (random.random())
		vector = vector * argv['l2_limit']

	if mean is not 0:
		vector = vector + mean_vector

	vectorNormalized = []
	for i in range(len(vector)):
		vectorNormalized.append(vector[i]/sum(vector))
	return vectorNormalized
	#return vector

def featureUniform(dimension, argv = None):
	vector = np.array([random.random() for _ in range(dimension)])

	l2_norm = np.linalg.norm(vector, ord =2)
	
	vector = vector/l2_norm
	return vector

def getBatchStats(arr):
	return np.concatenate((np.array([arr[0]]), np.diff(arr)))

def checkFileExists(filename):
	try:
		with open(filename, 'r'):
			return 1
	except IOError:
		return 0 

def fileOverWriteWarning(filename, force):
	if checkFileExists(filename):
		if force == True:
			print "Warning : fileOverWriteWarning %s"%(filename)
		else:
			raise FileExists(filename)


def vectorize(M):
	# temp = []
	# for i in range(M.shape[0]*M.shape[1]):
	# 	temp.append(M.T.item(i))
	# V = np.asarray(temp)
	# return V
	return np.reshape(M.T, M.shape[0]*M.shape[1])

def matrixize(V, C_dimension):
	# temp = np.zeros(shape = (C_dimension, len(V)/C_dimension))
	# for i in range(len(V)/C_dimension):
	# 	temp.T[i] = V[i*C_dimension : (i+1)*C_dimension]
	# W = temp
	# return W
	#To-do: use numpy built-in function reshape.
	return np.transpose(np.reshape(V, ( int(len(V)/C_dimension), C_dimension)))

class GraphData(object):
        def __init__(self, name):
            self.__name  = name
            self.__links = set()
    
        def name(self):
            return self.__name
    
        def links(self):
            return set(self.__links)
    
        def add_link(self, other):
            self.__links.add(other)
            other.__links.add(self)
    
    # The function to look for connected components.
def connected_components(nodes):
    
    # List of connected components found. The order is random.
    result = []

    # Make a copy of the set, so we can modify it.
    nodes = set(nodes)

    # Iterate while we still have nodes to process.
    while nodes:

        # Get a random node and remove it from the global set.
        n = nodes.pop()

        # This set will contain the next group of nodes connected to each other.
        group = {n}

        # Build a queue with this node in it.
        queue = [n]

        # Iterate the queue.
        # When it's empty, we finished visiting a group of connected nodes.
        while queue:

            # Consume the next item from the queue.
            n = queue.pop(0)

            # Fetch the neighbors.
            neighbors = n.links

            # Remove the neighbors we already visited.
            neighbors.difference_update(group)

            # Remove the remaining nodes from the global set.
            nodes.difference_update(neighbors)

            # Add them to the group of connected nodes.
            group.update(neighbors)

            # Add them to the queue, so we visit them in the next iterations.
            queue.extend(neighbors)

        # Add the group to the list of groups.
        result.append(group)

    # Return the list of groups.
    return result
    
