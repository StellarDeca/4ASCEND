# encoding=utf-8

import time
from abc import ABC


class BaseRevolveAnimation(ABC):
    """
    旋转动画类,计算动画随时间旋转的角度
    update_revolve_angle: 更新旋转角度
    _get_scaled_delta: 计算时间差
    """

    def __init__(self, revolve_rate: float, rev: bool):
        """
        :param revolve_rate: 旋转速率
        :param rev: 旋转方向(True顺时针旋转;False逆时针旋转)
        ------------------------------------------------
        angle: 当前旋转的角度
        _revolve_rate: 旋转速率
        _last_time: 上次旋转的时间
        """
        self._rev = rev
        """初始化属性"""
        self.angle = 0
        self._last_time = time.time()
        self._revolve_rate = revolve_rate

    def update_revolve_angle(self):
        """基于时间差更新旋转角度"""
        delta_time = self._get_scaled_delta()
        if self._rev:
            self.angle = (self.angle + self._revolve_rate * delta_time) % 360
        else:
            self.angle = (self.angle - self._revolve_rate * delta_time) % 360

    """私有化方法"""
    def _get_scaled_delta(self) -> float:
        """
        计算当前与上次计算动画位置的时间差,用于修行帧率带来的位置偏差
        :return: 时间差
        """
        now = time.time()
        delta_time = now - self._last_time
        self._last_time = now
        return delta_time


class ClockwiseRevolveAnimation(BaseRevolveAnimation):
    """顺时针旋转类"""

    def __init__(self, revolve_rate: float):
        super().__init__(revolve_rate, True)

    @classmethod
    def create_clockwise_revolve_animation(cls, revolve_rate: float):
        return cls(revolve_rate)


class AntiClockwiseRevolveAnimation(BaseRevolveAnimation):
    """逆时针旋转类"""

    def __init__(self, revolve_rate: float):
        super().__init__(revolve_rate, False)

    @classmethod
    def create_clockwise_revolve_animation(cls, revolve_rate: float):
        return cls(revolve_rate)

