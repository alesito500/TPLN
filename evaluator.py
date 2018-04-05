from sklearn import metrics
import pandas as pd
import numpy as np
def get_metrics(true_labels, predicted_labels):
    print ( 'Accuracy:', np.round( metrics.accuracy_score(true_labels, predicted_labels), 2))
    print ( 'Precision:', np.round( metrics.precision_score(true_labels, predicted_labels, pos_label=1),2))
    print ( 'Recall:', np.round( metrics.recall_score(true_labels, predicted_labels, pos_label=1), 2))
    print ( 'F1 Score:', np.round( metrics.f1_score(true_labels, predicted_labels, pos_label=1), 2))
    get_matrix(true_labels, predicted_labels)

def get_matrix(true_labels, predicted_labels):
    cm = metrics.confusion_matrix(y_true=true_labels, y_pred=predicted_labels, labels=[1,0])
    print(pd.DataFrame(data=cm, columns=pd.MultiIndex(levels=[['Predicted:'],['Positive', 'Negative']],labels=[[0,0],[0,1]]),index=pd.MultiIndex(levels=[['Actual:'],['Positive','Negative']],labels=[[0,0],[0,1]])))

def display_features(features, feature_names):
    df = pd.DataFrame(data=features,
                      columns=feature_names)
    return df
