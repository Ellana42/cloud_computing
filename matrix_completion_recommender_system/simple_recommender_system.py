import numpy as np
import pickle

class recommender_system:
  '''Simple recommender system class based on matrix factorization'''

  def __init__(self, k, lr, lambda_reg):
    '''Instantiates recommendation_system class.
    k : rank dimension of factorized matrix
    lr : learning rate
    lambda_reg : regularization parameter
    max_value : maximum value possible for the generated matrices to avoid overflow'''
    self.k = k
    self.lr = lr
    self.lambda_reg = lambda_reg


  def set_k(self, k):
    '''Set rank of the two factorized matrices'''
    self.k = k

  def set_lr(self, lr):
    '''set learning rate '''
    self.lr = lr

  def set_lambda_reg(self,lambda_reg):
    '''set regularization parameter'''
    self.lambda_reg=lambda_reg

  def instantiate_matrices(self):
    '''Instantiate factorized matrixes'''
    self.first_mat = np.random.randn(self.nb_rows, self.k)
    self.second_mat = np.random.randn(self.nb_cols, self.k)

  def instantiate_initially_pressent_items(self):
    '''Creates a 2d list from Ratings. Each row i of this list contains the items that the user i has already rated'''
    self.tested_items = [[] for i in range(self.nb_rows)]
    for row, col, _ in self.Ratings:
      self.tested_items[row].append(col)

  def load_sparse_data(self,file_, delimiter = ",", nb_rows_to_keep = -1, nb_cols_to_keep =-1, shuffle_matrix = True, correct_shape = False):
    '''Load data and shape it correctly for recommendation. Output format is a 2d numpy array. Each element of this output
      is in the format [row of the rating, column of the rating, Rating]
    file : either path to txt or csv file containing the dataset, or matrix to be used for recommendation. If file is a path
    shuffle_matrix : Boolean. if set to True
    nb_rows_to_keep : Number of rows to keep (if negative, keep all rows)
    nb_cols_to_keep : Number of columns to keep (if negative, keep all rows)
    correct_shape : set to True if input matrix is already in correct shape'''

    if isinstance(file_,str):
      grade_matrix = np.genfromtxt(file_, delimiter=delimiter, dtype = "int32")

    else:
      grade_matrix = file_

    if not correct_shape :

      self.nb_rows = len(grade_matrix)
      self.nb_cols = len(grade_matrix[0])

      if nb_rows_to_keep >0 and nb_rows_to_keep < len(grade_matrix):
        grade_matrix = grade_matrix[:nb_rows_to_keep]
        self.nb_rows = len(grade_matrix)

      if nb_cols_to_keep >0 and nb_cols_to_keep < len(grade_matrix[0]):
        grade_matrix = grade_matrix[:,:nb_cols_to_keep]
        self.nb_cols = len(grade_matrix[0])

      self.instantiate_matrices()

      non_zero_indexes = np.nonzero(grade_matrix)

      n = len(non_zero_indexes[0])
      put_in_shape_matrix = np.array([[non_zero_indexes[0][i], non_zero_indexes[1][i], grade_matrix[non_zero_indexes[0][i], non_zero_indexes[1][i]]] for i in range(n)])
      put_in_shape_matrix = put_in_shape_matrix.astype(int)

      if shuffle_matrix:
        np.random.shuffle(put_in_shape_matrix)

      self.Ratings = put_in_shape_matrix

      self.instantiate_initially_pressent_items()

    else:

      if nb_rows_to_keep >0 :
        grade_matrix = grade_matrix[grade_matrix[:,0]<nb_rows_to_keep]

      if nb_cols_to_keep >0:
        grade_matrix = grade_matrix[grade_matrix[:,1]<nb_cols_to_keep]

      self.Ratings = grade_matrix

      self.nb_rows = np.max(grade_matrix[:,0])+1
      self.nb_cols = np.max(grade_matrix[:,1])+1

      self.instantiate_matrices()
      self.instantiate_initially_pressent_items()
    return None


  def root_mean_square_error(self, first_mat, second_mat):
    '''Compute avera root mean square error'''
    error = 0
    Ratings = self.Ratings
    for row,col,rating in Ratings:
      predicted_ratings = first_mat[row].dot(second_mat[col].T)
      error += (rating-predicted_ratings)**2

    error = error / len(Ratings)
    return np.sqrt(error)

  def sgd_gradient_step(self):
    '''Stochastic gradient descent of factorized matrixes over a batch of indexex
    batch_indexes : array containing [row,col,rating] elements
    '''
    for row,col,rating in self.Ratings:

      predicted_rating = self.first_mat[row].dot(self.second_mat[col].T)
      error = rating - predicted_rating

      self.first_mat += self.lr*(error*self.second_mat[col] - self.lambda_reg*self.first_mat[row])
      self.second_mat += self.lr*(error*self.first_mat[row] - self.lambda_reg*self.second_mat[col])

  def matrix_factorization(self, number_iterations):
    losses = []
    for i in range(number_iterations):
      self.sgd_gradient_step()
      loss = self.root_mean_square_error(self.first_mat, self.second_mat)
      losses.append(loss)
      print("RMSE after epoch is :",loss)
    return losses

  def get_recommendation(self, user_id, nb_recom = 2):
    curr_ratings = np.array(np.matmul(self.first_mat, self.second_mat.T)[user_id])

    ordered_item_indexes = np.argsort(curr_ratings)
    ordered_item_indexes = [index for index in ordered_item_indexes if index not in self.tested_items[user_id]]
    nb_recom = nb_recom if nb_recom< len(ordered_item_indexes) else len(ordered_item_indexes)
    recommendations = ordered_item_indexes[-nb_recom:]

    return recommendations

  def save_model(self, path):
    '''Save a pickled version of the model's parameters
    path : path under which to save pickled parameters'''
    to_save = [self.first_mat.tolist(), self.second_mat.tolist(), self.k]
    with open(path,"wb") as f:
      pickle.dump(to_save, f)
    print("Done")
    return None

  def load_model(self,path):
    '''Load model from pickled parameters
    path : path to pickled parameters'''
    with open(path,'rb') as f:
      parameters = pickle.load(f)
    self.first_mat = np.array(parameters[0]).astype(int)
    self.second_mat = np.array(parameters[1]).astype(int)
    self.k = parameters[2]


  def get_nearest_neighbors(self, user_rating, nb_neighbors):
    '''Given a user which is not present in our dataset, find nearest neighbors
    user_rating : 1D vector containing user rating
    nb_neighbors : number of neighbors indexes that we want to retrieve'''
    ratings = np.matmul(self.first_mat, self.second_mat.T)

    squared_dist = (ratings-user_rating)**2

    distances = np.sum(squared_dist, axis = 1)

    sorted_distances_idx = np.argsort(distances)

    closest = sorted_distances_idx[-nb_neighbors:]

    return(closest)


  def get_recommendation_new_user(self, user_rating, nb_recom, nb_neighbors=10):

    rated_items = np.nonzero(user_rating)[0]

    neighbors_indexes = self.get_nearest_neighbors(user_rating, nb_neighbors)
    ratings = np.matmul(self.first_mat, self.second_mat.T)
    for i in range(nb_neighbors) :

      if i == 0:
        res = ratings[neighbors_indexes[i]]
      else :
        res += ratings[neighbors_indexes[i]]

    res = res / nb_neighbors

    ordered_item_indexes = np.argsort(res)

    ordered_item_indexes = [index for index in ordered_item_indexes if index not in rated_items]

    recommendations = ordered_item_indexes[-nb_recom:]

    return(recommendations)
