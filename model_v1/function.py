import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from vincenty import vincenty
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import math

def section_true(section_list, Y_true, list_mearge):
    a = list_mearge[1]-1
    b = list_mearge[2]-1
    index_a = (((np.array(section_list[a])[0]) < (Y_true[:, 1])) & ((Y_true[:, 1]) < (np.array(section_list[a])[1])))
    index_b = (((np.array(section_list[b])[0]) < (Y_true[:, 1])) & ((Y_true[:, 1]) < (np.array(section_list[b])[1])))
    return (index_a | index_b)

def section_true_not_mearge(section_list, Y_true, i_model):
    if (i_model != 0) and (i_model != 8):
        a = i_model
        index_a = (((np.array(section_list[a])[0]) < (Y_true[:,1])) & ((Y_true[:,1]) < (np.array(section_list[a])[1])))

        return index_a

def load_date_def(list_random_seed, n_s):
    dataset = np.array(pd.read_csv(f'..\Dataset\Original.csv'))
    X, Y = dataset[:, :137], dataset[:, 138:]
    n_s = n_s
    X_train_combined = None
    Y_train_combined = None
    X_test_combined = None
    Y_test_combined = None
    flag = 1
    for section in range(n_s):
        index_Y = Y[:, 1]
        Max_getway = np.max(np.max(index_Y))
        min_getway = np.min(np.min(index_Y))
        step = (Max_getway - min_getway) / n_s

        index = (((min_getway + (step * section)) < index_Y) & ((min_getway + (step * (section + 1))) > index_Y))

        X_current = X[index, :]
        Y_current = Y[index, :]

        # X_current = X
        # Y_current = Y

        X_train_temp, X_test_temp, \
            Y_train_temp, Y_test_temp = train_test_split(X_current, Y_current,
                                                         test_size=0.3,
                                                         random_state=list_random_seed)

        imputer = SimpleImputer(strategy='mean')
        X_train_temp_imputed = imputer.fit_transform(X_train_temp)
        X_test_temp_imputed = imputer.transform(X_test_temp)

        # X_train_temp_imputed = X_train_temp
        # X_test_temp_imputed = X_test_temp


        if flag == 1:
            if X_train_combined == None:
                X_train_combined = X_train_temp_imputed
                Y_train_combined = Y_train_temp
                X_test_combined = X_test_temp_imputed
                Y_test_combined = Y_test_temp
                flag = 0
        if flag == 0:
            X_train_combined = np.concatenate((X_train_temp_imputed, X_train_combined), axis=0)
            Y_train_combined = np.concatenate((Y_train_temp, Y_train_combined), axis=0)
            X_test_combined = np.concatenate((X_test_temp_imputed, X_test_combined), axis=0)
            Y_test_combined = np.concatenate((Y_test_temp, Y_test_combined), axis=0)

    return X_train_combined, Y_train_combined, X_test_combined, Y_test_combined


def index_section(numebers_section, Y_train_combined, i_model, index, section_list):
    index_Y = Y_train_combined[:, 1]
    index['model_0'] = ((3.0 < index_Y) & (5.0 > index_Y))
    for i_model in range(0, numebers_section):
        index['model_' + str(i_model+1)] = (((section_list[i_model, 0]) < index_Y) & ((section_list[i_model, 1]) > index_Y))
    return index

def return_section_list(numebers_section,Max_getway,min_getway):
    section_list = np.zeros((numebers_section - 1, 2))
    for li, section in enumerate(range(numebers_section - 1)):
        step = (Max_getway - min_getway) / numebers_section


        if li == 0:
            section_list[li, 0] = (min_getway + (step * section))
            ###########################################################################
            # section_list[li, 0] = 3.95
        else:
            section_list[li - 1, 1] = (min_getway + (step * section))
            ###########################################################################
            # section_list[li - 1, 1] = 3.95

            section_list[li, 0] = (min_getway + (step * section))
        section_list[(numebers_section - 2), 1] = Max_getway
        section_list[0,1] = 3.95
        section_list[1,0] = 3.95

    return section_list


def list_change_section_r1(lists_old, number_section_old, i_1, k, section_list_old):
    res = np.zeros((number_section_old, number_section_old))
    for i in range(1, number_section_old):
        for j in range(i + 1, number_section_old):
            number_multiply = np.intersect1d(lists_old[f"list_{i}"], lists_old[f"list_{j}"])
            res[i, j] = len(number_multiply)
    if 1 < np.max(res):
        return 0
    else:
        return 5


def rename_list(list_with_name_old):
    list_with_name_new = {}
    list_0 = list_with_name_old.pop('list_0')

    for i, key in enumerate(list_with_name_old.keys(), start=1):
        list_with_name_new[f'list_{i}'] = list_with_name_old[key]

    list_with_name_new['list_0'] = list_0
    return list_with_name_new


def list_change_section(lists_old, number_section_old, i_1, k, section_list_old):
    res = np.zeros((number_section_old, number_section_old))
    for i in range(1, number_section_old):
        for j in range(i + 1, number_section_old):
            number_multiply = np.intersect1d(lists_old[f"list_{i}"], lists_old[f"list_{j}"])
            res[i, j] = len(number_multiply)

    a = np.unravel_index(np.argmax(res), res.shape)
    common_elements = np.intersect1d(lists_old[f"list_{a[0]}"], lists_old[f"list_{a[1]}"])
    lists_old.pop(f"list_{a[0]}")
    lists_old.pop(f"list_{a[1]}")

    section_list_new = np.copy(section_list_old)
    temp = len(section_list_new) - 1
    a_index_new = section_list_new[a[0], 0]
    b_index_new = section_list_new[a[1], 1]
    section_list_new = np.delete(section_list_new, a[0], 0)
    section_list_new = np.delete(section_list_new, (a[1] - 1), 0)
    kss = np.zeros((temp, 2))
    lists_old[f"list_{a[0]}_{a[1]}"] = common_elements
    lists_old = rename_list(lists_old)
    kss[0:(temp - 1), :] = section_list_new
    kss[temp - 1, 0] = min(a_index_new, b_index_new)
    kss[temp - 1, 1] = max(a_index_new, b_index_new)
    k.append(i_1)
    k.append(a[0])
    k.append(a[1])

    return lists_old, (number_section_old - 1), k

def f_e_mean_std(input_model, output_model, n_s):
    data_plot_mean = np.zeros((n_s, 137))
    data_plot_std = np.zeros((n_s, 137))
    for section in range(n_s):
        index_Y = output_model[:, 1]
        Max_getway = np.max(np.max(index_Y))
        min_getway = np.min(np.min(index_Y))
        step = (Max_getway - min_getway) / n_s
        step = 3.95
        print(step)
        data_getway = input_model[(((min_getway + (step * section)) < index_Y) & ((min_getway + (step * (section + 1))) > index_Y))]
        mean_getway = np.mean(data_getway, axis=0)
        std_getway = np.std(np.float32(data_getway), axis=0)
        data_plot_mean[section, :] = mean_getway
        data_plot_std[section, :] = std_getway


    getway_useful = []
    for number_getway in range(137):
        for number_sections in range(n_s):
            if data_plot_mean[number_sections, number_getway] == -200:
                if data_plot_std[number_sections, number_getway] != 0:
                    getway_useful.append(number_sections)
                    getway_useful.append(number_getway)

            if data_plot_mean[number_sections, number_getway] != -200:
                getway_useful.append(number_sections)
                getway_useful.append(number_getway)
    return getway_useful


def list_getways(useful_section_getway, n_s):
    lists = {}
    for i in range(n_s):
        lists['list_' + str(i+1)] = []
    for name_section, gateway in zip(useful_section_getway[0::2], useful_section_getway[1::2]):
        lists[f"list_{name_section+1}"].append(gateway)

    lists["list_0"] = [9, 10, 11, 12, 17,
                  19, 20, 22, 26, 30,
                  58, 61, 66, 70, 71,
                  72, 75, 82, 83, 84,
                  85, 86, 88, 89, 90, 91,
                  92, 94, 96, 97, 99, 100,
                  101, 103, 104, 105, 107,
                  110, 118, 119, 28, 24, 18,
                  62, 102, 126, 0, 1, 2, 4,
                  6, 7, 8, 13, 14, 15, 16,
                  21, 29, 31, 32, 33,
                  36, 37, 38, 39, 40, 43,
                  44, 59, 60, 64, 68, 73, 109]
    for i in range(n_s+1):
        lists[f"list_{i}"] = np.unique(np.array(lists[f"list_{i}"]))
    return lists

def preproces(x, number):
    X_current = None
    if number == 0:
        X_current = (x - np.min(x)) / np.min(x) * -1
    elif number == 1:
        X_current = np.exp((x - np.min(x)) / 24) / np.exp(np.min(x) * -1 / 24)
    elif number == 2:
        X_current = (x - np.min(x)) / np.min(x) * -1
        X_current = X_current ** np.e
    return X_current, number


def Label_area(pre, n_s, Y_train_combined):
    index = {}
    P = {}
    for section in range(n_s):
        index_Y = pre[:, 1]
        Max_getway = np.max(np.max(index_Y))
        min_getway = np.min(np.min(index_Y))
        step = (Max_getway - min_getway) / n_s
        step = 3.95
        index['model_' + str(section)] = (
                    ((min_getway + (step * section)) < index_Y) & ((min_getway + (step * (section + 1))) > index_Y))
        P['model_' + str(section)] = index['model_' + str(section)].copy()
        P['model_' + str(section)][P['model_' + str(section)]] = section
        P['model_' + str(section)] = np.where(P['model_' + str(section)], section, 0)
    return P

def index_section(numebers_section, Y_train_combined, i_model, index, section_list):
    index_Y = Y_train_combined[:, 1]
    # print("numebers_section",numebers_section)
    # print("section_list",section_list)

    index['model_0'] = ((3.0 < index_Y) & (5.0 > index_Y))

    for i_model in range(0, numebers_section):
        index['model_' + str(i_model + 1)] = []
        for i in range(len(section_list['start_section'][i_model])):
            index['model_' + str(i_model + 1)].append(((section_list['start_section'][i_model])[i] < index_Y) & (
                        (section_list['final_section'][i_model])[i] > index_Y))
        # index['model_' + str(i_model+1)] = (((section_list[i_model, 0]) < index_Y) & ((section_list[i_model, 1]) > index_Y))

    return index

def Label_area_new_way(pre, n_s, section_list):
    index = {}
    P = {}

    for section in range(0, n_s):
        index_Y = pre[:, 1]
        index['model_' + str(section)] = []
        for i in range(len(section_list['start_section'][section])):
            index['model_' + str(section)].append(((section_list['start_section'][section])[i] < index_Y) & (
                        (section_list['final_section'][section])[i] > index_Y))
        P['model_' + str(section)] = index['model_' + str(section)].copy()
        # P['model_' + str(section)][P['model_' + str(section)]] = section
        P['model_' + str(section)] = np.where(P['model_' + str(section)], 1, 0)
    return P

    # for section in range(n_s):
    #     index_Y = pre[:, 1]
    #     index['model_' + str(section)] = (((section_list[section, 0]) < index_Y) & ((section_list[section, 1]) > index_Y))
    #     P['model_' + str(section)] = index['model_' + str(section)].copy()
    #     # P['model_' + str(section)][P['model_' + str(section)]] = section
    #     P['model_' + str(section)] = np.where(P['model_' + str(section)], 1, 0)
    # return P

def list_to_data(list, X_train_combined, X_test_combined):
    X_Train_1 = None
    X_test_1 = None
    for iii, number_col in enumerate(list):
        if iii == 0:
            X_Train_1 = X_train_combined[:, number_col].reshape(-1, 1)
            X_test_1 = X_test_combined[:, number_col].reshape(-1, 1)
        else:
            X_Train_1 = np.concatenate((X_Train_1, X_train_combined[:, number_col].reshape(-1, 1)), axis=1)
            X_test_1 = np.concatenate((X_test_1, X_test_combined[:, number_col].reshape(-1, 1)), axis=1)
    return X_Train_1, X_test_1

def evaluation(Y_test_combined, pred, i2, number):
    errors = []
    for range_longitude in range(len(pred)):
        centroids = pred[range_longitude]
        error = vincenty(centroids, Y_test_combined[range_longitude])
        errors.append(error)

    mean_error = np.mean(errors) * 1000
    median_error = np.median(errors) * 1000
    # R2_score = r2_score(Y_test_combined, pred)

    # print(f"i_pre {i_pre}:randomseed_{i2}_Mean Error: {mean_error} meters")
    # print(f"i_pre {i_pre}_randomseed_{i2}_Median Error: {median_error} meters")
    # print(f"i_pre {i_pre}_randomseed_{i2}_R2 Score: {R2_score}\n")

    # results_df = pd.DataFrame({
    #     'Random': i2,
    #     'Mean Error (meters)': [mean_error],
    #     'Median Error (meters)': [median_error],
    #     # 'R2 Score': [R2_score],
    #     'Pre process': number
    # })
    # results_df.to_csv(f'../result/evaluation_results_{number}_{i2}.csv', index=False)
    return mean_error

def evaluation1(Y_test_combined, pred, i2, number,i_pre):
    errors = []
    for range_longitude in range(len(pred)):
        centroids = pred[range_longitude]
        error = vincenty(centroids, Y_test_combined[range_longitude])
        errors.append(error)

    mean_error = np.mean(errors) * 1000
    median_error = np.median(errors) * 1000
    # R2_score = r2_score(Y_test_combined, pred)

    print(f"i_pre {i_pre}:randomseed_{i2}_Mean Error: {mean_error} meters")

    results_df = pd.DataFrame({
        'Random': i2,
        'Mean Error (meters)': [mean_error],
        'Median Error (meters)': [median_error],
        # 'R2 Score': [R2_score],
        'Pre process': number
    })
    results_df.to_csv(f'../result/evaluation_results_{number}_{i2}.csv', index=False)


def clean_divest(matrix):
    matrix = np.array(matrix)
    for col in range(matrix.shape[1]):
        unique_values = np.unique(matrix[:, col])

        if len(unique_values) >= 2:
            smallest, second_smallest = unique_values[0], unique_values[1]
            matrix[:, col] = np.where(matrix[:, col] == smallest, second_smallest, matrix[:, col])

    return matrix.tolist()

def pathloss_preprose(x,y):
    P = 0.0145
    f = 868
    distances = []

    x = np.array(x)
    y = np.array(y)

    for i2 in range(x.shape[1]):

        x_1 = x[:, i2]
        y_1 = y[:, 0]
        y_2 = y[:, 1]


        x_1_filtered = x_1
        y_1_filtered = y_1
        y_2_filtered = y_2

        P_loss = P - x_1_filtered
        list_of_d = 10 ** ((P_loss - 20 * np.log10(f) - 32.45) / 20)

        len_x = np.max(y_1) - np.min(y_1)
        len_y = np.max(y_2) - np.min(y_2)
        diameter = math.sqrt((len_x ** 2) + (len_y ** 2))
        list_new_d = (diameter * list_of_d) / 1068

        distances.append(list_new_d)

    distances = np.array(distances).T
    combined_data = np.hstack((x, distances))
    return combined_data


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def split_data_by_line_from_excel(data, coords):
    # مسیر فایل اکسل
    file_path = '../Dataset/GATEWAY_POINT_UPDATED.xlsx'

    # خواندن داده‌ها از فایل اکسل
    df = pd.read_excel(file_path)

    # محاسبه مراکز کلاسترها (برای کلاستر 0 و کلاستر 1)
    cluster_0 = df[df['cluster'] == 0]
    center_0 = (cluster_0['centroid_x'].mean(), cluster_0['centroid_y'].mean())

    cluster_1 = df[df['cluster'] == 1]
    center_1 = (cluster_1['centroid_x'].mean(), cluster_1['centroid_y'].mean())

    # استخراج مختصات مراکز کلاسترها
    center_0_x, center_0_y = center_0
    center_1_x, center_1_y = center_1

    # محاسبه شیب و شیب عمود
    slope = (center_1_y - center_0_y) / (center_1_x - center_0_x)
    perpendicular_slope = -1 / slope

    # محاسبه نقطه میانی
    mid_x = (center_0_x + center_1_x) / 2
    mid_y = (center_0_y + center_1_y) / 2

    above_line, below_line = [], []
    above_line_coords, below_line_coords = [], []

    # مقدار بایاس برای خط
    bias = (mid_x * perpendicular_slope) + mid_y

    for i, (y, x) in enumerate(coords):  # جابجایی y و x
        line_y_value = perpendicular_slope * (x - mid_x) + mid_y  # استفاده از x برای محاسبه

        if y > line_y_value:
            above_line.append(data[i])  # فقط استفاده از مقادیر data
            above_line_coords.append((y, x))  # ذخیره مختصات
        else:
            below_line.append(data[i])  # فقط استفاده از مقادیر data
            below_line_coords.append((y, x))  # ذخیره مختصات

    # تبدیل لیست‌ها به آرایه‌های numpy
    above_line = np.array(above_line)
    below_line = np.array(below_line)
    above_line_coords = np.array(above_line_coords)
    below_line_coords = np.array(below_line_coords)

    # ترسیم نقاط و خط
    plt.figure(figsize=(10, 6))

    # ترسیم همه نقاط
    plt.scatter(coords[:, 1], coords[:, 0], color='lightgray', label='All Coordinates', alpha=0.5)

    # رسم خط عمود
    line_x = np.linspace(center_0_x, center_1_x, 100)
    line_y = perpendicular_slope * (line_x - mid_x) + mid_y
    plt.plot(line_x, line_y, color='green', label='Perpendicular Line', linestyle='--')



    # تنظیمات نمودار
    plt.xlabel('X Coordinates')
    plt.ylabel('Y Coordinates')
    plt.title('Data Split by Perpendicular Line')
    plt.axhline(50.75, color='black', linewidth=0.5, ls='--')
    plt.axvline(3.6, color='black', linewidth=0.5, ls='--')
    plt.grid()
    plt.legend()
    plt.show()

    return above_line, below_line, above_line_coords, below_line_coords

import numpy as np
import math

aaaa = np.array([9, 10, 11, 12, 17,
                  19, 20, 22, 26, 30,
                  58, 61, 66, 70, 71,
                  72, 75, 82, 83, 84,
                  85, 86, 88, 89, 90, 91,
                  92, 94, 96, 97, 99, 100,
                  101, 103, 104, 105, 107,
                  110, 118, 119, 28, 24, 18,
                  62, 102, 126, 0, 1, 2, 4,
                  6, 7, 8, 13, 14, 15, 16,
                  21, 29, 31, 32, 33,
                  36, 37, 38, 39, 40, 43,
                  44, 59, 60, 64, 68, 73, 109])

def pathloss_preprose_d(x, y):
    P = 0.0145
    f = 868
    distances = []

    x = np.array(x)
    y = np.array(y)

    # پردازش هر ستون از x
    for i2 in range(x.shape[1]):
        x_1 = x[:, i2]
        y_1 = y[:, 0]
        y_2 = y[:, 1]

        # محاسبه افت توان
        P_loss = P - x_1
        list_of_d = 10 ** ((P_loss - 20 * np.log10(f) - 32.45) / 20)

        # محاسبه قطر
        len_x = np.max(y_1) - np.min(y_1)
        len_y = np.max(y_2) - np.min(y_2)
        diameter = math.sqrt((len_x ** 2) + (len_y ** 2))
        list_new_d = (diameter * list_of_d) / 1068

        distances.append(list_new_d)

    # تبدیل لیست به آرایه numpy
    distances = np.array(distances).T

    # ترکیب داده‌ها
    combined_data = np.hstack((x, distances))

    # بازگشت فقط 137 ستون آخر
    return combined_data[:, -137:]  # بازگشت 137 ستون آخر

def split_data_by_cluster_train(X_test_d,id):
    # مسیر فایل اکسل
    file_path = '../Dataset/GATEWAY_POINT_UPDATED.xlsx'

    # خواندن داده‌ها از فایل اکسل
    df = pd.read_excel(file_path)

    # فیلتر کردن داده‌ها بر اساس کلاستر
    cluster_0 = df[df['cluster'] == 0]['NAMGE']
    cluster_1 = df[df['cluster'] == 1]['NAMGE']
    cluster_0 = np.array(cluster_0)
    cluster_1 = np.array(cluster_1)

    x1 = X_test_d[:, cluster_0]

    x1_test = []

    for i in range(len(x1)):
        if id == 0:
            x1_test.append(X_test_d[i, aaaa])
        if id == 1:
            x1_test.append(X_test_d[i, cluster_1])

    return np.array(x1_test)

def split_data_by_cluster_test(X_test_d, Y_test, X_test_combined):
    # مسیر فایل اکسل
    file_path = '../Dataset/GATEWAY_POINT_UPDATED.xlsx'

    # خواندن داده‌ها از فایل اکسل
    df = pd.read_excel(file_path)

    # فیلتر کردن داده‌ها بر اساس کلاستر
    cluster_0 = df[df['cluster'] == 0]['NAMGE']
    cluster_1 = df[df['cluster'] == 1]['NAMGE']
    cluster_0 = np.array(cluster_0)
    cluster_1 = np.array(cluster_1)

    x1 = X_test_d[:,cluster_0]
    x2 = X_test_d[:,cluster_1]

    x1_test = []
    x2_test = []
    y1_test = []
    y2_test = []
    for i in range(len(x1)):
        sum_1 = np.sum(x1[i,:])
        sum_2 = np.sum(x2[i,:])
        if sum_1 <= sum_2:
            x1_test.append(X_test_combined[i,aaaa])
            y1_test.append(Y_test[i,:])
        if sum_2 <= sum_1:
            x2_test.append(X_test_combined[i,cluster_1])
            y2_test.append(Y_test[i,:])

    return x1_test, x2_test , y1_test, y2_test






