# encoding=utf-8

import pygame
from typing import Any
from copy import deepcopy
from .ConfigManager import ConfigManager


class AssetsManager(object):
    """
    这个类基于配置文件进行资源的管理
    get_font: 获取字体资源
    get_audio: 获取音频资源
    get_image: 获取图像资源
    uninstall_asset: 卸载资源
    get_keyframe: 获取关键帧动画资源
    get_alpha_image: 获取指定透明度的图片
    ---------------------------------------------
    __get_value: 查找key在dict中的值
    _load_font: 加载字体资源
    _load_audio: 加载音频资源
    _load_image: 加载图像资源
    _load_keyframe: 加载关键帧动画资源
    _set_alpha_image: 设置图片的透明度
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        _assets: 存放资源的字典
        _config_manger: 配置管理器
        _init: 确保__init__方法只被执行一次

        """
        if not hasattr(self, "_init"):
            self._assets: dict = {}
            self._init: bool = True
            self._config_manger = ConfigManager.create_config_manager()

    @classmethod
    def create_assets_manager(cls):
        return cls()

    def get_image(self, image_name: str) -> pygame.Surface:
        """
        获取资源,资源不存在则尝试加载
        :param image_name: 资源名称
        :return: 资源本体
        """
        name = "image-{}".format(image_name)
        if name not in self._assets:
            self._load_image(image_name)
        return deepcopy(self._assets[name])

    def get_audio(self, audio_name: str) -> pygame.mixer.Sound:
        """
        获取资源,资源不存在则尝试加载
        :param audio_name: 资源名称
        :return: 资源本体
        """
        name = "audio-{}".format(audio_name)
        if name not in self._assets:
            self._load_audio(audio_name)
        return self._assets[name]

    def get_keyframe(self, keyframe_name: str) -> pygame.Surface:
        """
        获取资源,资源不存在则尝试加载
        :param keyframe_name: 资源名称
        :return: 资源本体
        """
        name = "keyframe-{}".format(keyframe_name)
        if name not in self._assets:
            self._load_keyframe(keyframe_name)
        return self._assets[name]

    def get_font(self, font_name: str, font_size: int) -> pygame.font.Font:
        """
        获取资源,资源不存在则尝试加载
        :param font_name: 资源名称
        :param font_size: 字体大小
        :return: 资源本体
        """
        key = "font-{0}-{1}".format(font_name, font_size)
        if key not in self._assets:
            self._load_font(font_name, font_size)
        return self._assets[key]

    def uninstall_asset(self, asset_name: str) -> None:
        """
        卸载指定的资源
        :param asset_name: 资源名称
        """
        if asset_name not in self._assets:
            raise RuntimeError("卸载的资源{0}未加载!".format(asset_name))
        self._assets.pop(asset_name)

    def get_alpha_image(self, image_name: str, image: pygame.Surface, alpha: float) -> pygame.Surface:
        if image_name not in self._assets:
            self._set_alpha_image(image_name, image, alpha)
        return deepcopy(self._assets["image-alpha-{}".format(image_name)])


    """私有化方法"""
    @staticmethod
    def __get_value(key, cfg: dict) -> Any:
        """
        递归的查找给定的键在字典中是否存在
        :param key: 带查找的键
        :param cfg: 被查找的字典
        :return: key在cfg中的值 | None
        """
        stack: list[dict] = [cfg]
        while stack:
            k = stack.pop(-1)
            if key in k:
                return k[key]
            else:
                for v in k.values():
                    if isinstance(v, dict):
                        stack.append(v)
        return None

    def _load_image(self, image_name: str) -> None:
        """
        加载指定的资源,资源不存在抛出异常
        :param image_name: 资源名称
        """
        if (image_path := self.__get_value(image_name, self._config_manger.get_config("images"))) is None:
            raise RuntimeError("图片资源{0}不存在!".format(image_name))
        asset_size = self.__get_value(image_name, self._config_manger.get_config("img-size"))
        image = pygame.image.load(image_path)
        result = pygame.transform.scale(image, asset_size)
        self._assets["image-{}".format(image_name)] = result

    def _load_font(self, font_name: str, font_size: int) -> None:
        if (font_path := self.__get_value(font_name, self._config_manger.get_config("font"))) is None:
            raise RuntimeError("字体资源{0}不存在!".format(font_name))
        self._assets["font-{0}-{1}".format(font_name, font_size)] = pygame.font.Font(font_path, font_size)

    def _load_keyframe(self, keyframe_name: str) -> None:
        if (keyframe_path := self.__get_value(keyframe_name, self._config_manger.get_config("keyframes"))) is None:
            raise RuntimeError("关键帧资源{0}不存在!".format(keyframe_name))
        keyframe_size = self.__get_value(keyframe_name, self._config_manger.get_config("keyframes-size"))
        keyframe_img = pygame.image.load(keyframe_path)
        result = pygame.transform.scale(keyframe_img, keyframe_size)
        self._assets["keyframe-{}".format(keyframe_name)] = result

    def _load_audio(self, audio_name: str) -> None:
        if (audio_path := self.__get_value(audio_name, self._config_manger.get_config("audios"))) is None:
            raise RuntimeError("音频资源{}不存在!".format(audio_name))
        self._assets["audio-{}".format(audio_name)] = pygame.mixer.Sound(audio_path)

    def _set_alpha_image(self, image_name: str, image: pygame.Surface, alpha: float) -> None:
        """
        将传入的图像中非透明的部分处理为指定的透明度
        :param image: 待处理的图像
        :param alpha: 指定的透明度
        :return: 处理后的图像
        """
        """校验alpha"""
        if alpha > 1.0 or alpha < 0.0:
            raise RuntimeError(f"透明度{alpha}应在0.0到1.0之间!")

        """逐个像素进行处理"""
        new_image = image.copy()
        width, height = new_image.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = new_image.get_at((x, y))
                if pixel[3] != 0:
                    new_image.set_at((x, y), (pixel[0], pixel[1], pixel[2], int(alpha * 255)))
        self._assets["image-alpha-{}".format(image_name)] = new_image

