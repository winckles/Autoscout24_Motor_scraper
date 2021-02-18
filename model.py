import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
import pandas as pd


def train_model():
    """ Pipeline to train and dump a model """

    df = pd.read_csv('data.csv')
    df = df.reset_index()
    features = ['brand', 'new', 'mileage', 'power',
                'year', 'fuel', 'cc']
    x = df[features]
    x = pd.get_dummies(data=x, drop_first=True)
    y = df[['price']]

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # step-1: create a cross-validation scheme
    folds = KFold(n_splits=4, shuffle=True, random_state=100)

    # step-2: specify range of hyper parameters to tune
    hyper_params = [{'n_features_to_select': list(range(1, 9))}]

    # step-3: perform grid search
    # 3.1 specify model
    lm = LinearRegression()
    lm.fit(X_train, y_train)
    rfe = RFE(lm)

    # 3.2 call GridSearchCV()
    model_cv = GridSearchCV(estimator=rfe,
                            param_grid=hyper_params,
                            scoring='r2',
                            cv=folds,
                            verbose=1,
                            return_train_score=True)

    # fit the model
    model_cv.fit(X_train, y_train)
    pickle.dump(model_cv, open("predict.pkl", "wb"))
