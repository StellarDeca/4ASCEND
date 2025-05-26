# encoding=utf-8

import math
import time
from abc import ABC
from typing import Literal


class BaseMoveAnimation(ABC):
    """
    这个类是移动的动画类,模拟便加速直线运动来计算动画对象的位置,动画与时间有关而与帧率几乎无关
    update_position: 更新动画对象的位置
    -------------------------------------------------------------------------
    _calculate_speed_acceleration: 计算位置对应的加速度
    _get_scaled_delta: 计算时间差1
    """

    def __init__(self, cfg: dict, pos_key: str, reverse: bool, rev: bool):
        """
        基于传入的配置字典进行配置
        :param cfg: 配置字典
        :param reverse: 设定动画对象的反转属性
        :param rev: 设定动画运动方向(True竖直运动;False水平运动)
        ------------------------------------------------------
        position: 动画对象的坐标
        ------------------------------------------------------
        _last_time: 上次计算动画位置的时间
        _rate: 动画坐标变换的速度
        _move_direction: 速度方向(向上,向右为正方向)
        _base_delta_time: 动画的基准时间
        _max_acceleration: 移动的最大加速度
        _max_pos: 最大位移边界
        _min_pos: 最小位移边界
        """
        self._rev = rev
        self.reverse: bool = reverse

        """设定基准参数"""
        self._last_time = time.time()
        self._rate: float = cfg["max-rate"]
        self._move_direction: Literal[-1, 1] = 1
        self._base_delta_time = 1 / cfg["base-fps"]
        self.position: tuple[int, int] = cfg["position"][pos_key]
        self._max_acceleration: float = cfg["max-acceleration"]
        if rev:
            self._max_pos = self.position[1] + cfg["move-range"]
            self._min_pos = self.position[1] - cfg["move-range"]
        else:
            self._max_pos = self.position[0] + cfg["move-range"]
            self._min_pos = self.position[0] - cfg["move-range"]

    def update_position(self):
        """基于时间更新位置"""
        delta_time = self._get_scaled_delta()

        if self._rev:
            self._rate += self._calculate_speed_acceleration(self.position[1]) * delta_time
            new_y = self.position[1] + self._rate * self._move_direction * delta_time
            if new_y >= self._max_pos:
                new_y = self._max_pos
                self._move_direction = -1
            elif new_y <= self._min_pos:
                new_y = self._min_pos
                self._move_direction = 1
            self.position = (self.position[0], new_y)

        else:
            self._rate += self._calculate_speed_acceleration(self.position[0]) * delta_time
            new_x = self.position[0] + self._rate * self._move_direction * delta_time
            if new_x >= self._max_pos:
                new_x = self._max_pos
                self._move_direction = -1
            elif new_x <= self._min_pos:
                new_x = self._min_pos
                self._move_direction = 1
            self.position = (new_x, self.position[1])

    """私有方法"""
    def _calculate_speed_acceleration(self, pos: int) -> float:
        """
        基于当前的pos坐标计算加速度
        :param pos: 当前的运动方向坐标
        :return: 返回当前位置对应的加速度
        """
        progress = (pos - self._min_pos) / (self._max_pos - self._min_pos)
        radian = progress * math.pi - math.pi / 2
        return self._max_acceleration * math.sin(radian)

    def _get_scaled_delta(self) -> float:
        """
        计算当前与上次计算动画位置的时间差,用于修行帧率带来的位置偏差
        :return: 时间差
        """
        now = time.time()
        delta_time = now - self._last_time
        self._last_time = now
        return min(delta_time, self._base_delta_time * 2)


class HorizontalAnimation(BaseMoveAnimation):
    """水平移动动画类"""

    def __init__(self, cfg: dict, pos_key: str, reverse: bool):
        super().__init__(cfg, pos_key, reverse, False)

    @classmethod
    def create_horizontal_animation(cls, cfg: dict, pos_key: str, reverse: bool):
        return cls(cfg, pos_key, reverse)


class VerticalAnimation(BaseMoveAnimation):
    """竖直移动动画类"""

    def __init__(self, cfg: dict, pos_key: str, reverse: bool):
        super().__init__(cfg, pos_key, reverse, True)

    @classmethod
    def create_vertical_animation(cls, cfg: dict, pos_key: str, reverse: bool):
        return cls(cfg, pos_key, reverse)

