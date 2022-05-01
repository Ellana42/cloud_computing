def generate_ratings(nb_rows, nb_cols, min_nb_recomm=1, max_nb_recomm=2, max_rating=5, seed = 0):
  np.random.seed(seed)
  ratings = np.zeros((nb_rows,nb_cols))

  for i in range(nb_rows):

    nb_recomm = np.random.randint(min_nb_recomm, max_nb_recomm+1)

    indexes = np.random.choice(np.arange(nb_cols), nb_recomm, replace = False)

    for index in indexes :
      ratings[i,index] = np.random.randint(max_rating)
  return ratings.astype(int)

ratings = generate_ratings(100,30,2,5)