import numpy as np

class nn_recommender :

  '''Nearest neighbors based recommender system'''

  def __init__(self, nb_neighbors, nb_sample):
    '''Instantiates class
    nb_neighbors : number of closest neighbors to consider to make predictions
    nb_sample : To lower computationnal cost, we sample a number nb_sample of rows from initial matrix and look from closest neighbors among these sampled rows'''
    self.nb_neighbors = nb_neighbors
    self.nb_sample = nb_sample

  def get_full_matrix_from_sparse(self, sparse, max_col = None):

    '''Function to get full matrix from sparse matrix with rows [user_id, item_id, rating]
    sparse : sparse matrix
    max_col : max item id'''

    max_row = np.max(sparse[:,0])+1
    max_col = max_col if max_col else (np.max(sparse[:,1])+1)

    result = np.zeros((max_row, max_col))

    for user_id, item_id, rating in sparse :

      result[user_id, item_id] = rating

    return result

  def get_ratings_of_user_id(self, sparse, user_id, max_item_id = None):
    '''retrieve user rating vector from sparse format matrix (rows in format [user_id, item_id, rating])
    sparse : sparse user matrix
    user_id : user_id
    max_item_id : len of output rating vector (None to set to the maximum item id in rating matrix )'''

    max_mat_item_id = max_item_id if max_item_id else (np.max(sparse[:,1]) +1) #Keep max id item ..
    ratings = sparse[sparse[:,0] == user_id]

    rating_vect = np.zeros(max_mat_item_id)

    for _, item_id, rating in ratings:
      if item_id <max_mat_item_id:
        rating_vect[item_id] = rating

    return rating_vect

  def get_recommendation(self, ratings, user_vect = None, user = None, nb_recommendations=2, sparse_shape = False, max_col = None):
    '''Get recommended items id for given user
    ratings : rating matrix
    user_vect : user ratings vector, if user is in rating matrix can be left as None
    user : user id if id is in ratings matrix, else None
    nb_recommendations : number of items to recommend
    sparse_shape : set to True if matrix is with rows of format [user_id, item_id, rating]'''

    if not sparse_shape :

      indexes = np.random.choice(len(ratings), self.nb_sample, replace=False)

      if user :

        indexes =[index for index in indexes if index != user]#Do not count user as one of their neighbors

        user_vect = ratings[user]

      sampled_mat = ratings[indexes]

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

      ordered_item_indexes = [index for index in ordered_item_indexes if user_vect[index]==0]

      recommendations = ordered_item_indexes[-nb_recommendations:]

    else:

      user_indexes = np.unique(ratings[:,0])

      indexes = np.random.choice(user_indexes, self.nb_sample, replace=False)

      if user:

        indexes =[index for index in indexes if index != user]

        user_vect = self.get_ratings_of_user_id(ratings, user, max_col)

      mask = np.isin(ratings[:,0], indexes)

      filtered_sparse_ratings = ratings[mask]

      full_matrix = self.get_full_matrix_from_sparse(filtered_sparse_ratings, max_col)

      squared_dist = (full_matrix-user_vect)**2

      distances = np.sum(squared_dist, axis = 1)

      sorted_distances_idx = np.argsort(distances)

      neighbors_indexes = sorted_distances_idx[-self.nb_neighbors:]

      for i in range(self.nb_neighbors) :

        if i == 0:
          res = full_matrix[neighbors_indexes[i]]
        else :
          res += full_matrix[neighbors_indexes[i]]

      res = res / self.nb_neighbors

      ordered_item_indexes = np.argsort(res)

      ordered_item_indexes = [index for index in ordered_item_indexes if user_vect[index]==0]
      recommendations = ordered_item_indexes[-nb_recommendations:]


    return(recommendations)