# encoding=utf-8


"""二元一次方程求解函数"""
def calculate_line_endpoints(main_coordinate: tuple, distance, slop, line_b) -> list[tuple]:
    """
    一元二次方程的求解函数,用于根据棋盘中点与线条长度计算线条的起始点与终止点的坐标
    :param main_coordinate:中心点坐标的元组
    :param distance:所求点到中心点的距离
    :param slop:中心点所在直线的斜率
    :param line_b:中心点所在直线的截距
    :return: 线条起点与终点坐标的列表
    """
    import math
    """一元二次方程的系数"""
    x, y = main_coordinate
    a = 1 + slop ** 2
    b = 2 * (-1 * x + slop * (line_b - y))
    c = x ** 2 + (line_b - y) ** 2 - distance ** 2

    if (check_ := b ** 2 - 4 * a * c) > 0:
        sub_x1 = round((-b + math.sqrt(check_)) / (2 * a))
        sub_y1 = round(slop * sub_x1 + line_b)

        sub_x2 = round((-b - math.sqrt(check_)) / (2 * a))
        sub_y2 = round(slop * sub_x2 + line_b)
        return [(sub_x1, sub_y1), (sub_x2, sub_y2)]

    elif check_ == 0:
        sub_x1 = round((-b + math.sqrt(check_)) / (2 * a))
        sub_y1 = round(slop * sub_x1 + line_b)
        return [(sub_x1, sub_y1)]

    else:
        error = f"""
            -------debug on ./Assets/Scripts/Utiles/Math.py -> line number 42----------
            要求解的方程为:\n\t(x - {x}) ^ 2 + (y - {y}) ^ 2 = {distance} ^ 2
            {{\n\t y = {slop} * x + {line_b}\n方程系数为:A:{a}, B:{b}, C:{c}
            判别式B ^ 2 - 4 * A * C = {check_}
        """
        raise ValueError(f"二元一次方程判别式小于0,无实数解\n{error}")

