# encoding=utf-8


class CoordinateTip:
    """
    这个类是指示光圈的类,负责在棋盘上移动指示光圈,并处理光圈越界的情况
    up_next: 上移
    down_next: 下移
    right_next: 右移
    left_next: 左移
    """

    def __init__(self):
        """
        初始化指示光圈的位置起始默认位置为 (5, 5)
        image_angle: 指示光圈图像的旋转角度
        coordinate: 指示光圈在棋盘上的坐标
        rotate_rate: 指示光圈的的旋转速率,逐帧增加
        """
        self.image_angle: int = 0
        self.coordinate: tuple[int, int] = (5, 5)

    @classmethod
    def create_coordinate_tip(cls) -> "CoordinateTip":
        return cls()

    def up_next(self) -> None:
        """
        将指示光圈向上移动一格,越过边界则跳到最底部
        """
        row = self.coordinate[0] - 1
        if row <= 0:
            self.coordinate = (9, self.coordinate[1])  # 列保持不变,行变为 9
        else:
            self.coordinate = (row, self.coordinate[1])

    def down_next(self) -> None:
        """
        将指示光圈向下移动一格,越过边界则跳到最顶部
        """
        row = self.coordinate[0] + 1
        if row > 9:
            self.coordinate = (1, self.coordinate[1])  # 列保持不变,行变为 1
        else:
            self.coordinate = (row, self.coordinate[1])

    def right_next(self) -> None:
        """
        将指示光圈向右移动一格,越过边界则跳到最左边
        """
        column = self.coordinate[1] + 1
        if column > 9:
            self.coordinate = (self.coordinate[0], 1)  # 行保持不变,列变为 1
        else:
            self.coordinate = (self.coordinate[0], column)

    def left_next(self) -> None:
        """
        将指示光圈向左移动一格,越过边界则跳到最右边
        """
        column = self.coordinate[1] - 1
        if column <= 0:
            self.coordinate = (self.coordinate[0], 9)  # 行保持不变,列变为 9
        else:
            self.coordinate = (self.coordinate[0], column)

