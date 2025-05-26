# encoding=utf-8

import pygame
from ASCEND.Manager.BaseManager import ConfigManager
from ASCEND.Manager.BaseManager import AssetsManager


class GameAudiosManager(object):
    """
    游戏的音频资源管理类,播放音频资源(单例模式)
    play_bgm: 根据bgm的名称播放背景音乐
    play_audio_clip: 根据音效名称播放音效
    play_chess_audio_clip: 播放棋子的落子音效
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化音频模块并初始化声道数量为8
        _init: 确保__init__方法只被运行一次
        _bgm_channel: 背景音乐声道
        _sfx_channels: 音效声道
        _config_manger: 配置文件管理器
        _assets_manager: 资源管理器
        """
        if not hasattr(self, "_init"):
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)

            self._init: bool = True
            self._bgm_channel = pygame.mixer.Channel(0)
            self._sfx_channels = [pygame.mixer.Channel(i) for i in range(1, 8)]
            self._config_manger: ConfigManager = ConfigManager.create_config_manager()
            self._assets_manager: AssetsManager = AssetsManager.create_assets_manager()

    @classmethod
    def create_audios_manager(cls):
        return cls()

    def play_bgm(self, bgm_name: str) -> None:
        """
        根据bgm的名称播放背景音乐
        :param bgm_name: 背景音乐名称
        """
        try:
            bgm = self._assets_manager.get_audio(bgm_name)
        except (pygame.error, FileNotFoundError):
            return None
        bgm.set_volume(0.5)
        self._bgm_channel.play(bgm, loops=-1)

    def play_audio_clip(self, clip_name: str, loops: int = 1) -> None:
        """
        根据音效名称播放音效,并自动分配可用的声道
        :param clip_name: 音效名称
        :param loops: 音效的循环次数,默认为一次；为-1时为循环播放
        """
        try:
            audio_clip = self._assets_manager.get_audio(clip_name)
        except (pygame.error, FileNotFoundError):
            return None
        audio_clip.set_volume(0.5)
        for channel in self._sfx_channels:
            if not channel.get_busy():
                channel.play(audio_clip, loops=loops - 1)
                break

    def play_chess_audio_clip(self, chess_type: str, loops: int = 1) -> None:
        """
        播放棋子的落子音效
        :param chess_type: 棋子类型
        :param loops: 播放次数,默认为1
        """
        clip_map = {
            "White": "put-white",
            "Black": "put-black"
        }
        self.play_audio_clip(clip_map[chess_type], loops=loops)

