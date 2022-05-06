import numpy as np

class nn_recommender :


  '''Nearest neighbors based recommender system'''

  def __init__(self, nb_neighbors, nb_sample):
    '''Instantiates class
    nb_neighbors : number of closest neighbors to consider to make predictions
    nb_sample : To lower computationnal cost, we sample a number nb_sample of rows from initial matrix and look from closest neighbors among these sampled rows'''
    self.nb_neighbors = nb_neighbors
    self.nb_sample = nb_sample

  def get_recommendation(self, ratings, user, nb_recommendations=2):
    '''Get recommended items id for given user
    ratings : rating matrix
    user : user id
    nb_recommendations : number of items to recommend'''

    indexes = np.random.choice(len(ratings), self.nb_sample, replace=False)
    indexes =[index for index in indexes if index != user]

    sampled_mat = ratings[indexes]

    user_vect = ratings[user]

    squared_dist = (sampled_mat-user_vect)**2

    distances = np.sum(squared_dist, axis = 1)

    sorted_distances_idx = np.argsort(distances)

    neighbors_indexes = sorted_distances_idx[-self.nb_neighbors:]

    for i in range(self.nb_neighbors) :

      if i == 0:
        res = ratings[neighbors_indexes[i]]
      else :
        res += ratings[neighbors_indexes[i]]

    res = res / self.nb_neighbors

    ordered_item_indexes = np.argsort(res)

    ordered_item_indexes = [index for index in ordered_item_indexes if user_vect[index]>0]

    recommendations = ordered_item_indexes[-nb_recommendations:]


    return(recommendations)