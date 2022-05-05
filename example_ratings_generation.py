def generate_ratings(nb_rows, nb_cols, min_nb_recomm=1, max_nb_recomm=2, min_rating =1, max_rating=5, seed = 0):
  '''Function to generate test rating matrices
  nb_rows : nb of users
  nb_cols : nb of items
  min_nb_recomm : minimum number of recommendation for each user
  max_nb_recomm : max number of recommendation for each user
  min_rating : minimum rating possible
  max_rating : maximum rating possible
  seed : np random seed for reproducibility '''
  np.random.seed(seed)
  ratings = np.zeros((nb_rows,nb_cols))

  for i in range(nb_rows):

    nb_recomm = np.random.randint(min_nb_recomm, max_nb_recomm+1)

    indexes = np.random.choice(np.arange(nb_cols), nb_recomm, replace = False)

    for index in indexes :
      ratings[i,index] = np.random.randint(min_rating, max_rating)
  return ratings.astype(int)
