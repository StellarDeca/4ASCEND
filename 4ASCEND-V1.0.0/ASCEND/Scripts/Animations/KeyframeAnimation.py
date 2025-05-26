# encoding=utf-8

import time


class KeyframeAnimation(object):
    """
    关键帧动画类,基于时间差计算当前关键帧动画对应的索引(1开始)
    update_keyframe_animation_count: 更新关键帧动画的索引
    -------------------------------------------------
    _get_scaled_delta: 计算时间差
    """

    def __init__(self, cfg: dict):
        """
        基于传入的配置字典进行初始化
        :param cfg: 配置字典
        --------------------------
        frame_count: 关键帧动画的索引
        --------------------------
        _last_time: 上次计算关键帧动画索引的时间
        _base_delta_time: 动画的基准时间
        _frame_rate: 动画的切换速度
        _total_frames: 动画的总帧数
        """
        self.frame_count: int = 1
        self._last_time = time.time()
        self._base_delta_time = 1 / cfg["base-fps"]
        self._frame_rate = cfg["frame-rate"]
        self._total_frames = cfg["total-frames"]

    @classmethod
    def create_keyframe_animation(cls, cfg: dict):
        return cls(cfg)

    def update_keyframe_animation_count(self) -> int:
        """基于时间更新动画的索引"""
        frame_rate = self._frame_rate * self._get_scaled_delta()
        self.frame_count = round(frame_rate + self.frame_count) % (self._total_frames + 1)
        return self.frame_count

    """私有化方法"""
    def _get_scaled_delta(self) -> float:
        """
        计算当前与上次计算动画位置的时间差,用于修行帧率带来的位置偏差
        :return: 时间差
        """
        now = time.time()
        delta_time = now - self._last_time
        self._last_time = now
        return min(delta_time, self._base_delta_time * 2)

