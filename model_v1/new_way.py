from function import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler

X_train_combined, Y_train_combined, X_test_combined, Y_test_combined = load_date_def(42,1)

# section_list = return_section_list
# useful_section_getway = f_e_mean_std(X_train_combined, Y_train_combined, 2)
# lists = list_getways(useful_section_getway, 2)
# l1 = lists['list_1']
# X_train_combined, X_test_combined = list_to_data(l1, X_train_combined, X_test_combined)
#
# X_train_combined = clean_divest(X_train_combined)
# X_test_combined = clean_divest(X_test_combined)

X_train_combined = pathloss_preprose(X_train_combined, Y_train_combined)
X_test_combined = pathloss_preprose(X_test_combined, Y_test_combined)
#
# scaler = StandardScaler()
# X_train_combined = scaler.fit_transform(X_train_combined)
# X_test_combined = scaler.transform(X_test_combined)


Model = RandomForestRegressor()
Model.fit(X_train_combined, Y_train_combined)
Preds = Model.predict(X_test_combined)
a = evaluation(Y_test_combined, Preds, 42, 0)
print(a)