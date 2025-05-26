# encoding=utf-8

from typing import Literal
from abc import ABC, abstractmethod


class PlayerBase(ABC):
    """
    这个类是玩家基类,黑白棋子对应的玩家均继承此类
    creat_player方法: 创建玩家实例
    """
    player_type: Literal["PlayerBlack", "PlayerWhite"]

    @abstractmethod
    def __init__(self, cfg: dict):
        """
        :param cfg: 玩家的配置字典
        player_type: 玩家的阵营(黑棋魔族阵营,白棋精灵阵营)
        hit_point: 玩家的实际血量,初始为最大血量(不会为负)
        """
        self.player_type: Literal["PlayerBlack", "PlayerWhite"]
        self.hit_point: int

    @classmethod
    def create_player(cls, cfg: dict) -> "PlayerBase":
        return cls(cfg)


class PlayerBlack(PlayerBase):
    """黑棋(魔族阵营)玩家类"""
    player_type: Literal["PlayerBlack", "PlayerWhite"] = "PlayerBlack"

    def __init__(self, cfg: dict):
        self.player_type: Literal["PlayerBlack", "PlayerWhite"] = "PlayerBlack"
        self.hit_point: int = cfg["player-black-hp"]


class PlayerWhite(PlayerBase):
    """白棋(精灵阵营)玩家类"""
    player_type: Literal["PlayerBlack", "PlayerWhite"] = "PlayerWhite"

    def __init__(self, cfg: dict):
        self.player_type: Literal["PlayerBlack", "PlayerWhite"] = "PlayerWhite"
        self.hit_point: int = cfg["player-white-hp"]

