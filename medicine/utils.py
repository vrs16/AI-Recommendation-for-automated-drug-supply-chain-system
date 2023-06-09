from types import new_class
from typing import Tuple, Union, List
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


XY = Tuple[np.ndarray, np.ndarray]
Dataset = Tuple[XY, XY]
LogRegParams = Union[XY, Tuple[np.ndarray]]
XYList = List[XY]


def get_model_parameters(model: LogisticRegression) -> LogRegParams:
    """Returns the paramters of a sklearn LogisticRegression model."""
    if model.fit_intercept:
        params = [model.coef_, model.intercept_]
    else:
        params = [model.coef_,]
    return params


def set_model_params(
    model: LogisticRegression, params: LogRegParams
) -> LogisticRegression:
    """Sets the parameters of a sklean LogisticRegression model."""
    model.coef_ = params[0]
    if model.fit_intercept:
        model.intercept_ = params[1]
    return model


def set_initial_params(model: LogisticRegression):
    """Sets initial parameters as zeros Required since model params are
    uninitialized until model.fit is called.

    But server asks for initial parameters from clients at launch. Refer
    to sklearn.linear_model.LogisticRegression documentation for more
    information.
    """
    n_classes = 8  
    n_features = 1 
    model.classes_ = np.array([i for i in range(8)])

    model.coef_ = np.zeros((n_classes, n_features))
    if model.fit_intercept:
        model.intercept_ = np.zeros((n_classes,))

""" Read and split data """

def load_data() -> Dataset:
    """ Dataset download link:
    https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/download?datasetVersionNumber=3
    """
    data = pd.read_csv('trial.csv')
    data.reset_index(drop=True)
    df =np.array(data)
    x = df[:,2]
    y =df[:,-1]
    y=y.astype('int')
    x=x.reshape(-1,1)
    # Standardizing the features
    #x = StandardScaler().fit_transform(X)
    
    """ Select the 80% of the data as Training data and 20% as test data """
    x_train,x_test,y_train,y_test= train_test_split(x,y, test_size=0.2, random_state=42, shuffle=True)
    return (x_train, y_train), (x_test, y_test)
        

""" Read data for the other client """
def load_data_client() -> Dataset:
    """ Dataset download link:
    https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/download?datasetVersionNumber=3
    """
    data = pd.read_csv('trial.csv')
    data.reset_index(drop=True)
    df =np.array(data)
    x = df[:,2]
    y =df[:,-1]
    y=y.astype('int')
    x=x.reshape(-1,1)
    # Standardizing the features
    
    #x = StandardScaler().fit_transform(X)
    
    """ Select the 80% of the data as Training data and 20% as test data """
    x_train,x_test,y_train,y_test= train_test_split(x,y, test_size=0.2, random_state=42, shuffle=True)
    return (x_train, y_train), (x_test, y_test)
def shuffle(X: np.ndarray, y: np.ndarray) -> XY:
    """Shuffle X and y."""
    rng = np.random.default_rng()
    idx = rng.permutation(len(X))
    return X[idx], y[idx]


def partition(X: np.ndarray, y: np.ndarray, num_partitions: int) -> XYList:
    """Split X and y into a number of partitions."""
    return list(
        zip(np.array_split(X, num_partitions), np.array_split(y, num_partitions))
    )