# encoding=utf-8

from random import choice
from typing import Literal
from abc import ABC, abstractmethod


class ChessBase(ABC):
    """
    这是黑白棋子的基类,黑白棋子均继承自此类
    creat_chess: 实例化方法,创建一个棋子的实例
    __hash__: 按照棋子类型与坐标对棋子实例进行哈希值的计算
    """
    chess_type: Literal["White", "Black"]

    @abstractmethod
    def __init__(self, coordinate: tuple[int, int]):
        """
        chess_type_:棋子的颜色
        coordinate:棋子在棋盘上的坐标
        attack:棋子的攻击力
        image_angle:图像绕中心旋转的角度
        """
        self.chess_type: Literal["White", "Black"]
        self.image_angle: int
        self.coordinate: tuple[int, int] = coordinate
        self.attack: int = 1
        pass

    def __hash__(self):
        return hash((self.chess_type, self.coordinate))

    @classmethod
    def create_chess(cls, coordinate: tuple[int, int]) -> "ChessBase":
        return cls(coordinate)


class BlackChess(ChessBase):
    """黑色棋子类"""
    chess_type: Literal["White", "Black"] = "Black"

    def __init__(self, coordinate: tuple[int, int]):
        self.chess_type: Literal["White", "Black"] = "Black"
        self.image_angle = choice([0, 90, 180, 270])
        self.coordinate = coordinate
        self.attack: int = 1


class WhiteChess(ChessBase):
    """白色棋子类"""
    chess_type: Literal["White", "Black"] = "White"

    def __init__(self, coordinate: tuple[int, int]):
        self.chess_type: Literal["White", "Black"] = "White"
        self.image_angle = choice([0, 90, 180, 270])
        self.coordinate = coordinate
        self.attack: int = 1

