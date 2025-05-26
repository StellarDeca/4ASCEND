# encoding=utf-8

import random


class Plant(object):
    """
    这个类是魔力植物类,当棋子放置在魔力植物上时，棋子攻击力 + 1
    __hash__: 按照植物的坐标属性对植物实例进行哈希值的计算
    init_plants_config: 配置魔力植物的生长参数,在魔力植物实例化之前必须调用,多次调用只会执行一次
    update_soil_fertility: 更新土壤肥力并检测土壤肥力是否溢出
    grow: 很具现有战况进行魔力植物的生长
    creat_plant: 实例化魔力植物,同时检查init_plants_config方法是否运行过
    """

    _init: bool = False  # 标记是否初始化魔力植物配置


    def __init__(self, coordinate: tuple):
        """
        image: 实例化时随即决定魔力植物的图片
        coordinate: 魔力植物的坐标
        :param coordinate: 魔力植物的坐标
        """
        self.coordinate: tuple = coordinate

    def __hash__(self):
        return hash(self.coordinate)

    @classmethod
    def creat_plant(cls, coordinate: tuple) -> "Plant":
        if not cls._init:
            raise RuntimeError("魔力植物配置方法没有被调用!")
        return cls(coordinate)

    @classmethod
    def init_plants_config(cls, cfg: dict) -> None:
        """
        这个方法用于配置魔力植物的生长参数
        _grow_range: 生长范围变化值(生长范围边界到该边界上最远的魔力植物的距离)
        _max_fertility: 土壤肥力最大值
        _soil_fertility: 当前土壤肥力
        _growth_fertility: 魔力植物生长消耗的肥力
        _fertility_recharge_rate: 土壤肥力随回合数的回复速率
        """
        if not cls._init:
            cls._init = True
            cls._grow_range: tuple = cfg["grow-range"]
            cls._max_fertility: float = cfg["max-fertility"]
            cls._soil_fertility: float = cfg["soil-fertility"]
            cls._growth_fertility: float = cfg["growth-fertility"]
            cls._fertility_recharge_rate: float = cfg["fertility-recharge-rate"]

    @classmethod
    def update_soil_fertility(cls) -> bool:
        """
        更新土壤肥力并检测土壤肥力是否溢出
        :return: 肥力溢出返回True;未溢出则返回False
        """
        cls._soil_fertility += cls._fertility_recharge_rate
        if cls._soil_fertility >= cls._max_fertility:
            cls._soil_fertility = cls._max_fertility
            return True
        return False

    @classmethod
    def grow_plants(cls, growth_range: dict, chess: list, growth_plants: list) -> list["Plant"]:
        """
        获取棋子矩形区域:
            若棋盘上没有棋子,将会在整个棋盘上随机挑选位置生长魔力植物
            如果棋盘上棋子位置不为空,将在棋子矩形区域行列 + cls._grow_range 的位置随机挑选位置生长

        魔力植物的生长:
            生长时机: 在4ASCEND结束之后生长(或者肥力溢出),生长位置随机(魔力植物不会生长在已经生长魔力植物或者棋子的位置)
            生长数量: 魔力植物的生长会消耗土壤的肥力
                    每次生长都会尽可能多的消耗肥力(具体数量为最小数量到最大数量的随机值)
                    生长数量不会低于cls.base_min_grow_number(最小生长数量会随着土壤肥力而变化)
                    而且当频繁的触发4ASCEND时,肥力将会贫瘠
                    较多回合不触发4ASCEND将会导致土壤的肥力超过阈值,此时魔力植物仍会生长
            土壤肥力的计算公式:
                回合数(turn_number - cls._final_grow_turn) * 回复速率(cls._fertility_recharge_rate)

        :param growth_range: 棋盘上已生长魔力植物的范围: {horizontal: tuple, vertical: tuple}
        :param chess: 棋子对象的列表(应当包含进攻方连子与正常棋子)
        :param growth_plants: 魔力植物对象的列表
        :return: 新生长的魔力植物的列表
        """
        """计算魔力植物的生长数量"""
        max_grow_number = int(cls._soil_fertility // cls._growth_fertility)
        min_grow_number = int((cls._soil_fertility * 0.3) // cls._growth_fertility)

        """计算魔力植物的生长范围并初始化生长位置"""
        if growth_range == ((5, 5), (5, 5)):  # (5, 5)在chessboard类中定义
            grow_coordinate = [(hor, ver) for hor in range(1, 10) for ver in range(1, 10)]
        else:
            hor_range = growth_range["horizontal"]
            ver_range = growth_range["vertical"]
            max_hor, min_hor = hor_range[1] + cls._grow_range[0], hor_range[0] - cls._grow_range[1]
            max_ver, min_ver = ver_range[1] + cls._grow_range[0], ver_range[0] - cls._grow_range[1]
            max_hor, max_ver = min(max_hor, 9), min(max_ver, 9)
            min_hor, min_ver = max(min_hor, 1), max(min_ver, 1)
            grow_coordinate = [
                (hor, ver) for hor in range(min_hor, max_hor + 1) for ver in range(min_ver, max_ver + 1)
            ]

        """挑选魔力植物可用生长位置"""
        for plant in growth_plants:
            if plant.coordinate in grow_coordinate:
                grow_coordinate.remove(plant.coordinate)
        for ches in chess:
            if ches.coordinate in grow_coordinate:
                grow_coordinate.remove(ches.coordinate)

        """随机挑选位置生长魔力植物"""
        max_grow_number = min(max_grow_number, len(grow_coordinate))
        min_grow_number = max(1, min_grow_number)
        plants = list()
        for p in range(min_grow_number, max_grow_number):
            coord = random.choice(grow_coordinate)
            plant = cls.creat_plant(coord)
            grow_coordinate.remove(coord)
            plants.append(plant)

        """更新肥力"""
        cls._soil_fertility -= cls._growth_fertility * len(plants)
        return plants

