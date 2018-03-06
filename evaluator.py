from sklearn import metrics
import numpy as np
def get_metrics(true_labels, predicted_labels):
    print ( 'Accuracy:', np.round( metrics.accuracy_score(true_labels, predicted_labels), 2))
    print ( 'Precision:', np.round( metrics.precision_score(true_labels, predicted_labels, average='weighted'),2))
    print ( 'Recall:', np.round( metrics.recall_score(true_labels, predicted_labels, average='weighted'), 2))
    print ( 'F1 Score:', np.round( metrics.f1_score(true_labels, predicted_labels, average='weighted'), 2))
