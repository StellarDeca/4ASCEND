# encoding=utf-8

import json, pathlib
from ASCEND.Scripts.Utiles import calculate_line_endpoints


class ConfigManager(object):
    """
    配置文件管理类,加载并更新配置文件(单例模式)
    get_config: 获取指定的配置文件
    update_config: 更新指定的配置文件
    -----------------------------------------------------
    _load_configs: 加载配置文件
    _format_config: 根据格式化选项格式化配置文件
    __data_formate_configs: 格式化配置文件中的数据
    __assets_path_formate_config: 格式化资源的路径
    -----------------------------------------------------
    __build_chessboard_config: 计算所有线条的终点与起点
    __build_chessboard_line_config: 基于配置字典计算棋盘线条的终点与起点
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        _init: 确保__init__方法只被执行一次
        _configs_path: ASCEND文件夹的绝对路径
        _configs: 配置文件的字典 {配置文件名: 配置}
        _init_config: 配置文件的配置文件的配置,记录了所有配置文件的名称
        """
        if not hasattr(self, "_init"):
            self._init: bool = True
            self._configs = {}
            self._init_config = {}
            self._configs_path = pathlib.Path(__file__).parent.parent.parent.resolve()
            """加载并完善配置文件"""
            self._load_configs()
            self.__build_chessboard_config()

    def get_config(self, config_name: str) -> dict:
        """
        获取配置,配置不存在则抛出异常
        :param config_name: 配置名称
        :return: 配置字典
        """
        if config_name in self._configs:
            return self._configs[config_name]
        else:
            raise KeyError(f"{config_name}不在配置字典中!")

    def update_config(self, config_name: str, new_config: dict) -> None:
        """
        更新配置,不成功抛出异常
        :param config_name: 配置名称
        :param new_config: 修改后的配置字典
        """
        if config_name in self._configs:
            self._configs[config_name] = new_config
        else:
            raise KeyError(f"{config_name}不在配置字典中!")

    @classmethod
    def create_config_manager(cls):
        return cls()


    """私有化方法"""
    @staticmethod
    def __data_formate_config(config: dict) -> dict:
        """
        格式化配置文件中的数据,将配置文件中的数组转换为元组
        :param config: 配置字典
        """
        stack: list[dict] = [config]
        while stack:
            dict_ = stack.pop(-1)
            for key, value in dict_.items():
                if key == "format":
                    continue
                if isinstance(value, list):
                    if all(isinstance(item, list) for item in value):
                        for index_ in range(0, len(value)):
                            value[index_] = tuple(value[index_])
                    else:
                        dict_[key] = tuple(value)
                elif isinstance(value, dict):
                    stack.append(value)
        return config

    @staticmethod
    def __assets_path_formate_config(config: dict, assets_path: pathlib.Path) -> dict:
        """
        根据传入的路径负责将资源路径进行格式化,变为绝对路径
        :param config: 配置字典
        """
        for key, value in config.items():
            if key == "format":
                continue
            elif isinstance(value, dict):
                stack: list[dict] = [value]
                while stack:
                    value_ = stack.pop(-1)
                    for k, v in value_.items():
                        if isinstance(v, str):
                            value[k] = assets_path / v
                        elif isinstance(v, dict):
                            stack.append(v)
            else:
                config[key] = assets_path / value
        return config

    @staticmethod
    def __build_chessboard_line_config(config: dict) -> dict[str: tuple]:
        """
        进一步完善棋盘的配置
        这个函数将计算
            y = kx + b  # (middle_x, middle_y)在直线上
        {
            (x - middle_x) ^ 2 + (y - middle_y) ^ 2 = (lengths / 2) ^ 2
        方程的解,这个方程的两个解即为该直线的起点与终点
        返回{"start": line_start, "end": line_end}的str:list[tuple]的字典
        :param config:横线或竖线的配置字典
        :return: 完善之后的配置字典
        """

        """读取直线的斜率、长度、中点坐标, 长度列表、斜率列表与中点列表长度相同,均为线条的数量"""
        slops: list[float] = config["slops"]
        lengths: list[int] = config["lengths"]
        middles: list[tuple[int, int]] = config["middle"]
        proportions: list[float] = config["proportions"]

        """计算经过中点的直线斜率"""
        if len(slops) != len(middles) != len(lengths):
            raise ValueError(
                "计算直线的起始点与终止点时," +
                "斜率slops与中点坐标列表middle的元素必须一一对应!"
            )
        else:
            line_start, line_end = [], []
            for index_ in range(0, len(slops)):
                middle_x, middle_y = middles[index_]
                slop = slops[index_]
                length = lengths[index_]
                proportion = proportions[index_]
                line_b = middle_y - slop * middle_x

                """求解坐标"""
                start = sorted(
                    calculate_line_endpoints(
                        middles[index_], length * proportion, slop, line_b
                    ),
                    key=lambda point: point[1]
                )[0]
                end = sorted(
                    calculate_line_endpoints(
                        middles[index_], length * (1 - proportion), slop, line_b
                    ),
                    key=lambda point: point[1]
                )[1]
                line_start.append(start)
                line_end.append(end)
        return {"start": line_start, "end": line_end}

    def __build_chessboard_config(self) -> None:
        """更新棋盘的配置字典,基于线条的中点与长度计算线条的起点与终点"""
        chessboard_config = self.get_config("chessboard")
        for key in ("horizontal", "vertical"):
            line_config = chessboard_config[key]
            result_ = self.__build_chessboard_line_config(line_config)
            for key_ in result_.keys():
                chessboard_config[key][key_] = result_[key_]
        self.update_config("chessboard", chessboard_config)

    def _format_config(self, config: dict) -> dict:
        """根据格式化选项格式化配置文件"""
        if (format_config := config['format'])["data"]:
            new_config = self.__data_formate_config(config)
        elif format_config["path"]:
            parent_path = self._configs_path / "Assets"
            new_config = self.__assets_path_formate_config(config, parent_path)
        else:
            new_config = config
        return new_config

    def _load_configs(self) -> None:
        """根据Configs/init.json加载所有的配置文件"""
        with open(self._configs_path / "Configs" / "init.json", "r", encoding="utf-8") as configs_f:
            self._configs: dict = json.load(configs_f)

        for key, value in self._configs.items():
            config_path = self._configs_path / "Configs" / value
            with open(config_path, "r", encoding="utf-8") as config_f:
                config = json.load(config_f)
                new_config = self._format_config(config)
                self._configs[key] = new_config

