# encoding=utf-8

from datetime import datetime
from ..Scripts.Items import Plant
from typing import Literal, Optional
from ..Scripts.Items import ChessBoard
from ..Scripts.Items import CoordinateTip
from ASCEND.Manager.BaseManager import ConfigManager
from ..Scripts.Items import PlayerBlack, PlayerWhite
from ..Scripts.Items import ChessBase, BlackChess, WhiteChess


class GameStatusManager(object):
    """
    游戏逻辑管理类,记录游戏状态与各个子模块(单例模式)
    check_winner: 胜利者判定
    update_player_hp: 更新玩家血量
    -------------------------------------------------------------------
    grow_plants: 生长魔力植物
    update_plant_soil_fertility: 更新土壤肥力并检测肥力是否溢出
    -------------------------------------------------------------------
    creat_chess: 创建棋子实例
    handle_attacker_ascend_status: 进攻方的4ASCEND状态游戏逻辑
    handle_defender_ascend_status: 防守方进入4ASCEND状态的游戏逻辑
    has_defender_overlapping_chess: ascend状态下有无重叠棋子
    handle_defender_not_ascend_status: 防守方无法进入4ASCEND状态的游戏逻辑
    -------------------------------------------------------------------
    __built_game_time: 计算游戏对局时长
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        _config_manager: 配置管理器
        _init: 确保__init__方法只被执行一次
        -------------------------------------------
        chessboard: 棋盘类的实例
        player_black: 黑棋玩家实例
        player_white: 白棋玩家实例
        coordinate_tip: 提示光圈的实例
        chess: 储存所有已有棋子实例的列表
        plants: 储存所有魔力植物实例的列表
        attacker_coiled: 储存4ASCEND进攻方连子的列表
        defender_coiled: 储存4ASCEND防守方连子的列表
        --------------------------------------------
        game_time: 游戏单局时长
        turn_chess: 回合方标记
        ascend: 4ASCEND状态标记
        start_time: 游戏开始的时间
        attacker_attack: 进攻方连子攻击力
        defender_attack: 防守方连子攻击力
        turn_number: 游戏的回合数(每落一子 +1)
        """
        if not hasattr(self, "_init"):
            self._init = True
            self._config_manager = ConfigManager.create_config_manager()

            """初始化游戏对象与配置"""
            players_cfg = self._config_manager.get_config("players")
            Plant.init_plants_config(self._config_manager.get_config("plants"))

            self.plants: list[Plant] = list()
            self.chess: list[ChessBase] = list()
            self.attacker_coiled: list[ChessBase] = list()
            self.defender_coiled: list[ChessBase] = list()
            self.chessboard: ChessBoard = ChessBoard.create_chessboard()
            self.player_black: PlayerBlack = PlayerBlack.create_player(players_cfg)
            self.player_white: PlayerWhite = PlayerWhite.create_player(players_cfg)
            self.coordinate_tip: CoordinateTip = CoordinateTip.create_coordinate_tip()

            """初始化游戏状态属性"""
            self.game_time = None
            self.ascend: bool = False
            self.turn_number: int = 0
            self.attacker_attack: int = 0
            self.defender_attack: int = 0
            self.start_time = datetime.now()
            self.turn_chess: Literal["White", "Black"] = "White"
            self.winner: Optional[Literal["White", "Black"]] = None

    @classmethod
    def create_status_manager(cls):
        return cls()

    @classmethod
    def reset(cls):
        cls._instance = None
        return cls.create_status_manager()

    """玩家相关方法"""
    def check_winner(self) -> None:
        """
        血量为零者判负,无赢家返回None
        检查棋盘是否为满,棋盘满则判定白色棋子胜利
        """
        def check_chessboard_full(chessboard: list[list]) -> bool:
            """
            检查棋盘是否已满
            :param chessboard: 棋盘列表
            :return: 满返回True;不满返回False
            """
            for hor in range(0, 9):
                for ver in range(0, 9):
                    if chessboard[hor][ver] is None:
                        return False
            return True

        if self.player_black.hit_point == 0 or check_chessboard_full(self.chessboard.chessboard):
            self._build_game_time()
            self.winner = "White"
        elif self.player_white.hit_point == 0:
            self._build_game_time()
            self.winner = "Black"

    def update_player_hp(self) -> None:
        """这个方法在4ASCEND结束后更新玩家血量,同时确保血量非负"""
        defender_player = self.player_white if self.turn_chess == "White" else self.player_black
        attacker_player = self.player_black if self.turn_chess == "White" else self.player_white

        final_hp_change = self.attacker_attack - self.defender_attack
        if final_hp_change > 0:
            defender_player.hit_point -= final_hp_change
            if defender_player.hit_point <= 0:
                defender_player.hit_point = 0
        elif final_hp_change < 0:
            attacker_player.hit_point += final_hp_change
            if attacker_player.hit_point <= 0:
                attacker_player.hit_point = 0

        """重置连子的总攻击力"""
        self.defender_attack, self.attacker_attack = 0, 0

    """魔力植物相关方法"""
    def grow_plants(self) -> bool:
        """生长魔力植物,同时返回生成是否成功"""
        chess = []
        for c in [self.chess, self.attacker_coiled]:
            chess.extend(c)
        plants = Plant.grow_plants(
            self.chessboard.chess_range,
            chess,
            self.plants
        )

        if plants:
            self.plants.extend(plants)
            return True
        else:
            return False

    @staticmethod
    def update_plant_soil_fertility() -> bool:
        return Plant.update_soil_fertility()

    """棋子相关方法"""
    def creat_chess(self) -> ChessBase:
        if self.turn_chess == "White":
            return WhiteChess.create_chess(self.coordinate_tip.coordinate)
        else:
            return BlackChess.create_chess(self.coordinate_tip.coordinate)

    def handle_defender_ascend_status(self) -> None:
        """
        防守方的4ASCEND状态处理方法,此方法处理防守方进入4ASCEND状态(未进入另行处理)
        将位置重叠的进攻方魔力植物纳为己有
        将被连子占据的魔力植物删除(被防守方占据的进攻方魔力植物若也被连子占据,需同样删除)
        """

        """生成坐标到植物、棋子的字典映射"""
        attacker_coords = {attacker.coordinate: attacker for attacker in self.attacker_coiled}
        defender_coords = {defender.coordinate: defender for defender in self.defender_coiled}
        plants_coords = {plant.coordinate: plant for plant in self.plants}

        """更新重叠防守方攻击力并移除进攻方重叠棋子"""
        overlapping_coords = set(attacker_coords.keys()).intersection(set(defender_coords.keys()))
        for coord in overlapping_coords:
            self.attacker_coiled.remove(attacker_coords[coord])
            del attacker_coords[coord]
            if coord in plants_coords:
                defender_coords[coord].attack += 1

        """计算双方攻击力"""
        self.attacker_attack = sum(defender.attack for defender in attacker_coords.values())
        self.defender_attack = sum(attacker.attack for attacker in defender_coords.values())

        """从棋盘上删除防守方连子"""
        for defender_chess in defender_coords.values():
            self.chessboard.remove_chess(defender_chess)
            self.chess.remove(defender_chess)

        """删除连子占据的魔力植物"""
        coords = list(attacker_coords.keys()) + list(defender_coords.keys())
        for coord in coords:
            if coord in plants_coords:
                self.plants.remove(plants_coords[coord])

    def handle_attacker_ascend_status(self) -> None:
        """进攻方的4ASCEND状态处理方法,从棋盘上删除进攻方棋子"""
        for attacker in self.attacker_coiled:
            self.chessboard.remove_chess(attacker)
            self.chess.remove(attacker)

    def has_defender_overlapping_chess(self, turn_chess: ChessBase) -> bool:
        """
        判断防守方是否存在与进攻方重叠的棋子
        :param turn_chess: 当前回合的落子
        :return: 存在重叠返回True，否则返回False
        """
        attacker_coords = { attacker.coordinate for attacker in self.attacker_coiled}
        defender_coords = {turn_chess.coordinate, }
        overlapping_coords = attacker_coords.intersection(defender_coords)
        return len(overlapping_coords) > 0

    def handle_defender_not_ascend_status(self, defender_chess: ChessBase) -> None:
        """
        防守方无法形成4ASCEND时,防守方无四连子
        将位置重叠的进攻方魔力植物纳为己有
        将被连子占据的魔力植物删除(被防守方占据的进攻方魔力植物若也被连子占据,需同样删除)
        :param defender_chess: 防守方棋子
        """
        """生成坐标到植物、棋子的字典映射"""
        attacker_coords = {attacker.coordinate: attacker for attacker in self.attacker_coiled}
        plants_coords = {plant.coordinate: plant for plant in self.plants}

        """更新重叠防守方攻击力并移除进攻方重叠棋子"""
        if (coord := defender_chess.coordinate) in attacker_coords:
            self.attacker_coiled.remove(attacker_coords[coord])
            del attacker_coords[coord]
            if coord in plants_coords:
                defender_chess.attack += 1

        """计算进攻方棋子攻击力"""
        self.attacker_attack = sum(defender.attack for defender in attacker_coords.values())

        """删除连子占据的魔力植物"""
        overlapping_coord = set(attacker_coords.keys()).intersection(set(plants_coords.keys()))
        for coord in overlapping_coord:
            self.plants.remove(plants_coords[coord])

    """私有化方法"""
    def _build_game_time(self) -> None:
        """计算游戏对局时长"""
        if self.game_time is None:
            end_time = datetime.now()
            total_seconds = (end_time - self.start_time).total_seconds()
            min_, sec = divmod(total_seconds, 60)
            self.game_time = "{0}分{1}秒".format(int(min_), int(sec))

