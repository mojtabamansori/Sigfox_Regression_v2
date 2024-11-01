from function import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV  # اضافه کردن این خط
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt

X_train_combined, Y_train_combined, X_test_combined, Y_test_combined = load_date_def(42, 1)

x1, x2, y1, y2 = split_data_by_line_from_excel(X_train_combined, Y_train_combined)
print(x1.shape)
print(x2.shape)
x1 = split_data_by_cluster_train(x1, 0)
x2 = split_data_by_cluster_train(x2, 1)
print(x1.shape)
print(y1.shape)
print(x2.shape)
print(y2.shape)

# تعریف پارامترهای جستجو
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# جستجوی بهترین پارامترها برای مدل 1
grid_search_1 = GridSearchCV(RandomForestRegressor(), param_grid, cv=5)
grid_search_1.fit(x1, y1)

# جستجوی بهترین پارامترها برای مدل 2
grid_search_2 = GridSearchCV(RandomForestRegressor(), param_grid, cv=5)
grid_search_2.fit(x2, y2)

print("Best parameters for model 1:", grid_search_1.best_params_)
print("Best parameters for model 2:", grid_search_2.best_params_)

# ساخت مدل‌ها با بهترین پارامترها
model_1 = RandomForestRegressor(**grid_search_1.best_params_)
model_2 = RandomForestRegressor(**grid_search_2.best_params_)

# فیت کردن مدل‌ها
model_1.fit(x1, y1)
model_2.fit(x2, y2)

X_test_d = pathloss_preprose_d(X_test_combined, Y_train_combined)

X_test_cluster_0, X_test_cluster_1, Y_test_cluster_0, Y_test_cluster_1 = split_data_by_cluster_test(X_test_d, Y_test_combined, X_test_combined)
print(np.array(X_test_cluster_0).shape)
print(np.array(X_test_cluster_1).shape)

P1 = model_1.predict(X_test_cluster_0)
P2 = model_2.predict(X_test_cluster_1)
y_hat = np.concatenate((P1, P2), axis=0)
y_test = np.concatenate((Y_test_cluster_0, Y_test_cluster_1), axis=0)

a = evaluation(y_test, y_hat, 42, 0)
print(a)


############################################### final
# section_list = return_section_list
# useful_section_getway = f_e_mean_std(X_train_combined, Y_train_combined, 2)
# lists = list_getways(useful_section_getway, 2)
# l1 = lists['list_1']
# X_train_combined, X_test_combined = list_to_data(l1, X_train_combined, X_test_combined)
#
# X_train_combined = clean_divest(X_train_combined)
# X_test_combined = clean_divest(X_test_combined)

# X_train_combined = pathloss_preprose(X_train_combined, Y_train_combined)
# X_test_combined = pathloss_preprose(X_test_combined, Y_test_combined)
#
# scaler = StandardScaler()
# X_train_combined = scaler.fit_transform(X_train_combined)
# X_test_combined = scaler.transform(X_test_combined)


# Model = RandomForestRegressor()
# Model.fit(X_train_combined, Y_train_combined)
# Preds = Model.predict(X_test_combined)
# a = evaluation(Y_test_combined, Preds, 42, 0)
