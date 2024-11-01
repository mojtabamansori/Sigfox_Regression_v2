import numpy as np

def split_data_by_line(data, coords):
    # مرکز دو کلاستر
    center_0_x, center_0_y = coords[0]
    center_1_x, center_1_y = coords[1]

    # محاسبه شیب خط بین دو مرکز و شیب عمود
    slope = (center_1_y - center_0_y) / (center_1_x - center_0_x)
    perpendicular_slope = -1 / slope

    # محاسبه نقطه میانی بین دو مرکز
    mid_x = (center_0_x + center_1_x) / 2
    mid_y = (center_0_y + center_1_y) / 2

    # تعیین نقاط بالا و پایین خط عمود
    above_line = []
    below_line = []
    above_line_coords = []
    below_line_coords = []

    for i, (x, y) in enumerate(coords):
        # بررسی موقعیت نقطه نسبت به خط عمود
        if y > perpendicular_slope * (x - mid_x) + mid_y:
            above_line.append(data[i])
            above_line_coords.append(coords[i])
        else:
            below_line.append(data[i])
            below_line_coords.append(coords[i])

    # تبدیل به آرایه numpy
    above_line = np.array(above_line)
    below_line = np.array(below_line)
    above_line_coords = np.array(above_line_coords)
    below_line_coords = np.array(below_line_coords)

    return above_line, below_line, above_line_coords, below_line_coords

