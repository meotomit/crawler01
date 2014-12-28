import numpy as np
from sklearn.naive_bayes import MultinomialNB
x = np.array([[42, 25, 7, 56],
              [10, 28, 45, 2],
              [11, 25, 22, 4],
              [33, 40, 8, 48],
              [28, 32, 9, 60],
              [8, 22, 30, 1]])
y = np.array(['Math', 'Comp', 'Comp', 'Math', 'Math', 'Comp'])

nb = MultinomialNB(alpha=0)

nb.fit(x, y)

print np.exp(nb.feature_log_prob_)
