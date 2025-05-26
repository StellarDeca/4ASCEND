# encoding=utf-8

from typing import Literal
chess_type_ = Literal["White", "Black"]


class ChessBoard(object):
    """
    这个类是游戏的棋盘类,管理棋盘上的棋子实例,并检测连子
    append_chess: 添加棋子
    check_coiled_chess: 连子检测
    update_chess_range: 在4ASCEND结束后更新棋盘棋子范围
    --------------------------------------------------
    _check_coiled_hor: 棋盘的横行连子检查
    _check_coiled_ver: 棋盘的竖行连子检查
    _check_left_diagonal: 棋盘的左对角线连子检查
    _check_right_diagonal: 棋盘的右对角线连子检查
    __check_coiled_line: 检测指定的棋子列表中的连子
     __update_chess_range: 添加棋子时更新棋盘上棋子范围
    _check_coiled_repeat: 对检查后得到的连子列表进行去重
    """

    def __init__(self):
        """
        chessboard: 棋盘的二维数组,数组中为None或者是棋子对象
        chess_range: 棋盘上棋子的范围
        """
        self.chessboard: list[list] = [
            [None for _ in range(0, 9)] for _ in range(0, 9)
        ]
        self.chess_range: dict[Literal["horizontal", "vertical"], tuple] = {
            "horizontal": (5, 5),
            "vertical": (5, 5)
        }

    @classmethod
    def create_chessboard(cls) -> "ChessBoard":
        return cls()

    def update_chess_range(self, chess: list) -> None:
        """
        在4ASCEND结束后更新棋盘上的棋子范围
        棋盘为空恢复默认范围
        :param chess: 棋子对象列表
        """
        if chess:
            for chess_ in chess:
                hor, ver = chess_.coordinate
                max_hor, min_hor = self.chess_range["horizontal"]
                max_ver, min_ver = self.chess_range["vertical"]

                if hor > max_hor:
                    self.chess_range["horizontal"] = (min_hor, hor)
                elif hor < min_hor:
                    self.chess_range["horizontal"] = (hor, max_hor)

                if ver > max_ver:
                    self.chess_range["vertical"] = (min_ver, ver)
                elif ver < min_ver:
                    self.chess_range["vertical"] = (ver, min_ver)
        else:
            self.chess_range["horizontal"] = (5, 5)
            self.chess_range["vertical"] = (5, 5)

    def append_chess(self, chess) -> bool:
        """
        根据坐标向棋盘列表中添加棋子对象,坐标为(行,列),均从1开始计数,
        同时调用_update_chess_range更新棋子在棋盘上的范围
        :param chess: 棋子对象
        :return: 添加成功则返回True,不成功则返回False
        """
        coordinate = chess.coordinate
        hor, ver = coordinate[0] - 1, coordinate[1] - 1
        if self.chessboard[hor][ver] is None:
            self.chessboard[hor][ver] = chess
            self.__update_chess_range(coordinate)
            return True
        else:
            return False

    def remove_chess(self, chess) -> None:
        """
        根据传入的坐标删除棋盘上对应的棋子实例
        : chess: 棋子对象
        """
        coordinate = chess.coordinate
        hor, ver = coordinate[0] - 1, coordinate[1] - 1
        if self.chessboard[hor][ver] is not None:
            self.chessboard[hor][ver] = None
            self.__update_chess_range(coordinate)
        else:
            raise ValueError("棋盘列表第%d行,第%d列为空,无法删除该位置的棋子!(从1~9)" % coordinate)

    def check_coiled_chess(self, chess_type: chess_type_) -> list:
        """
        检查四连及以上的子
        行检测与列检测相同，斜向检测只需要将对角线上的元素重新组成一个行列表进行检测
        :param chess_type: 被检查棋子的颜色
        :return: 棋子对象的列表
        """

        """连子检测"""
        coiled_chess = []
        coiled_chess.extend(self._check_coiled_hor(chess_type))
        coiled_chess.extend(self._check_coiled_ver(chess_type))
        coiled_chess.extend(self._check_right_diagonal(chess_type))
        coiled_chess.extend(self._check_left_diagonal(chess_type))
        """连子去重"""
        result = self._check_coiled_repeat(coiled_chess)
        return result


    """私有方法"""
    def __update_chess_range(self, coordinate: tuple) -> None:
        """
        根据新棋子坐标更新棋子的所处范围,为矩形区域
        :param coordinate: 棋子的坐标,参数默认为无
        """
        """在添加棋子时更新棋盘上的棋子范围"""
        hor, ver = coordinate
        if (not 1 <= hor <= 9) or (not 1 <= ver <= 9):
            raise ValueError("棋子范围必须是1~9!")

        max_hor, min_hor = self.chess_range["horizontal"]
        max_ver, min_ver = self.chess_range["vertical"]

        if hor > max_hor:
            self.chess_range["horizontal"] = (min_hor, hor)
        elif hor < min_hor:
            self.chess_range["horizontal"] = (hor, max_hor)

        if ver > max_ver:
            self.chess_range["vertical"] = (min_ver, ver)
        elif ver < min_ver:
            self.chess_range["vertical"] = (ver, min_ver)

    @staticmethod
    def __check_coiled_line(hor_chess: list, chess_type: chess_type_) -> list:
        """
        单行连子检查,横竖斜向检查均可化为横向检查
        :param hor_chess:被检查的按顺序存储棋子的列表
        :return:返回储存连子的列表
        """
        """棋子列表长度小于4直接返回空表"""
        if len(hor_chess) < 4:
            return list()

        """棋子列表长度大于4进行连子检测"""
        coiled_number = 0  # 计数器
        coiled_chess = []  # 结果列表
        coiled_mid = []  # 中间列表
        for vertical in range(0, len(hor_chess)):
            """
            当尝试判断None.chess_type_ == self.chess_type时,会引发AttributeError,
            所以提前判断当前位置是不是None,
                如果为None,说明当前的连续检测已经中断,需要检查连续棋子的数量
            无论有无四连棋子,均将计数器、中间列表置空
            """
            if (chess := hor_chess[vertical]) is None:
                if coiled_number >= 4:
                    coiled_chess.extend(coiled_mid)
                coiled_number, coiled_mid = 0, []
                continue

            # 执行到这里时,chess已经不会再是None
            if chess.chess_type == chess_type:  # 通过实例去访问类属性type.chess
                coiled_number += 1
                coiled_mid.append(chess)
                """
                当计数器达到8时,4-1-4的情况已经检测出来,
                此时,即使满足添加元素条件,检测下一个棋子的分支都将无法触发(即无法检查第9个棋子)
                所以将检测分支写在添加分支中,但是当计数器达到4后,都需要判断下一个元素是否中断
                中断则输出元素到结果列表中,不中断则继续添加元素
                """
                try:
                    """
                    遍历到列表的最后一个元素引发IndexError
                    如果不是列表的最后一个元素,但是下一个元素没有chess_type属性(None),
                    引发AttributeError
                    """
                    if hor_chess[vertical + 1].chess_type == chess_type:
                        continue
                    # 执行此判断时,column的下一个一定不是None,而且是中断的
                    elif coiled_number >= 4:
                        coiled_chess.extend(coiled_mid)
                    coiled_number, coiled_mid = 0, []

                except (IndexError, AttributeError):
                    # 此时必定中断,连子大于等于4个时,输出连子
                    if coiled_number >= 4:
                        coiled_chess.extend(coiled_mid)
                    coiled_number, coiled_mid = 0, []
        return coiled_chess

    def _check_coiled_hor(self, chess_type: chess_type_) -> list:
        """
        检查每一行,将连子添加到coiled_chess连子列表中
        :param chess_type: 被检查棋子的颜色
        """
        hor_chess = []
        for hor in range(9):
            l1 = self.__check_coiled_line(self.chessboard[hor], chess_type)
            if l1:
                hor_chess.extend(l1)
            else:
                continue
        return hor_chess

    def _check_coiled_ver(self, chess_type: chess_type_) -> list:
        """
        检测每一列,将连子添加到coiled_chess连子列表中
        :param chess_type: 被检查棋子的颜色
        :return:返回储存连子的列表
        """
        ver_chess = []
        for ver in range(9):
            check_column_list = []
            for hor in range(9):
                check_column_list.append(self.chessboard[hor][ver])
            """链子检测"""
            l2 = self.__check_coiled_line(check_column_list, chess_type)
            if l2:
                ver_chess.extend(l2)
            else:
                continue
        return ver_chess

    def _check_right_diagonal(self, chess_type: chess_type_) -> list:
        """
        主(右)对角线上(方向：↘️)的元素索引之差是一个定值,这个定值只与这条对角线上的元素个数有关
        规定右上角为1,到最长的主对角线为9,这时,主对角线元素个数与主对角线在列表上的索引相等,
        于是得到了行hor与列ver的关系：ver = hor + 9 - coordinate(主对角线的索引)
        tip：
            hor在遍历中的结束条件：hor是从0开始自增1,当hor自增的次数与元素个数相同时,就判断这条主对角线遍历结束
            <==> {hor | range(0, coordinate, 1)}

            由于右下角的对角线 与 右上角的对角线 关于 最长的主对角线对称(hor == ver),
            所以只需要将hor与ver互换,就得到了右下角的元素。
            但是：最长的主对角线对称(hor == ver)在对称时保持不变,也就是说：它被遍历了两次。
            解决：对称前判断hor与ver是否相等
        :param chess_type: 被检查棋子的颜色
        :return:返回储存连子的列表
        """
        right_diagonal_list = []
        for num in range(4, 9 + 1):
            diag1, diag2 = [], []
            for hor in range(0, num):
                ver = hor + 9 - num
                if ver == hor:
                    diag1.append(self.chessboard[hor][ver])
                else:
                    diag1.append(self.chessboard[hor][ver])
                    diag2.append(self.chessboard[ver][hor])

            l1 = self.__check_coiled_line(diag1, chess_type)
            l2 = self.__check_coiled_line(diag2, chess_type)
            if l1:
                right_diagonal_list.extend(l1)
            if l2:
                right_diagonal_list.extend(l2)

        return right_diagonal_list

    def _check_left_diagonal(self, chess_type: chess_type_) -> list:
        """
        左(副)对角线(方向：↗️)上的元素索引值之和是一个定值,这个定值与元素所在的对角线位置有关：
            要遍历整条对角线上的元素,只需要找到所有的(i, K)组合,让i + k = 定值
            tip:对于9*9大小列表,定值为0-16,注意i,k均不能超过列表的索引
        元素的顺序：
            对角线上相邻元素的索引总是相差1,所以,按照索引相差为1的方式穷举所有可能,再按照这个顺序遍历,
            得到的元素顺序就可以保持不变
        :param chess_type: 被检查棋子的颜色
        :return:返回储存连子的列表
        """
        left_diagonal_list = []
        for constant in range(0, 16 + 1):
            diag1 = []
            for hor in range(0, constant + 1):
                ver = constant - hor
                if hor > 8 or ver > 8:
                    continue
                else:
                    diag1.append(self.chessboard[hor][ver])

            l = self.__check_coiled_line(diag1, chess_type)
            if l:
                left_diagonal_list.extend(l)
            else:
                continue
        return left_diagonal_list

    @staticmethod
    def _check_coiled_repeat(coiled_chess: list) -> list:
        """
        定义去重函数：在横竖斜均检查完毕后,
        list_all中会包含重复的棋子(id相同),需要将重复的棋子去掉
        :param coiled_chess: 棋子列表
        :return:返回储存连子的列表
        """
        index_ = 0
        while index_ < len(coiled_chess):
            # 以index_为界,将列表分为已去重和未去重两部分,index_为待检测部分
            inner_index = index_ + 1
            while inner_index < len(coiled_chess):
                """
                当inner_index位置的元素被删除后,
                原本inner_index+1位置元素的索引变为inner_index,这时就需要再次检测inner_index位置的元素
                """
                if coiled_chess[index_] is coiled_chess[inner_index]:
                    coiled_chess.pop(inner_index)
                else:
                    inner_index += 1
            index_ += 1
        return coiled_chess

