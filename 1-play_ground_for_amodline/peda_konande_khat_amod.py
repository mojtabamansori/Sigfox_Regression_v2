import pandas as pd
import matplotlib.pyplot as plt

# مسیر فایل اکسل
file_path = '../Dataset/GATEWAY_POINT_UPDATED.xlsx'

# خواندن فایل اکسل
df = pd.read_excel(file_path)

# محاسبه مرکز کلاستر 0
cluster_0 = df[df['cluster'] == 0]
center_0_x = cluster_0['centroid_x'].mean()
center_0_y = cluster_0['centroid_y'].mean()

# محاسبه مرکز کلاستر 1
cluster_1 = df[df['cluster'] == 1]
center_1_x = cluster_1['centroid_x'].mean()
center_1_y = cluster_1['centroid_y'].mean()

# محاسبه نقطه میانی بین دو مرکز
mid_x = (center_0_x + center_1_x) / 2
mid_y = (center_0_y + center_1_y) / 2

# محاسبه شیب خط بین دو مرکز
slope = (center_1_y - center_0_y) / (center_1_x - center_0_x)

# محاسبه شیب عمود بر خط (شیب عمود = -1 / شیب خط اصلی)
perpendicular_slope = -1 / slope

# طول خط عمود برای نمایش
line_length = 0.1  # مقدار دلخواه برای طول خط عمود

# محاسبه مختصات نقاط برای رسم خط عمود
x1 = mid_x - line_length / 2
x2 = mid_x + line_length / 2
y1 = mid_y - (line_length / 2) * perpendicular_slope
y2 = mid_y + (line_length / 2) * perpendicular_slope

# رسم نقاط کلاسترها
plt.figure(figsize=(8, 6))
plt.scatter(cluster_0['X1'], cluster_0['Y1'], color='blue', label='Cluster 0')
plt.scatter(cluster_1['X1'], cluster_1['Y1'], color='green', label='Cluster 1')

# رسم مراکز کلاسترها
plt.scatter(center_0_x, center_0_y, color='red', s=100, marker='X', label='Center of Cluster 0')
plt.scatter(center_1_x, center_1_y, color='purple', s=100, marker='X', label='Center of Cluster 1')

# رسم خط نقطه‌چین بین مراکز کلاسترها
plt.plot([center_0_x, center_1_x], [center_0_y, center_1_y], 'k--', label='Connection Line')

# رسم خط عمود در نقطه میانی
plt.plot([x1, x2], [y1, y2], 'r-', label='Perpendicular Line')

# تنظیم محدوده محورها
plt.xlim(3.6, 4.2)
plt.ylim(50, 52)

# افزودن عنوان و نمایش لیبل‌ها
plt.xlabel('X1')
plt.ylabel('Y1')
plt.title('Scatter Plot of Clusters with Centers, Connection Line, and Perpendicular Line')
plt.legend()
plt.grid(True)
plt.show()
