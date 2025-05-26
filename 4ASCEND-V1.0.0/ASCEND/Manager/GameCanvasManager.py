# encoding=utf-8

import pygame
from random import choice
from ASCEND.Manager.BaseManager import AssetsManager
from ASCEND.Manager.BaseManager import ConfigManager
from ..Scripts.Animations import HorizontalAnimation, VerticalAnimation
from ..Scripts.Animations import ClockwiseRevolveAnimation, AntiClockwiseRevolveAnimation


class GameCanvasManager(object):
    """
    这个类是画布管理类,绘制游戏中的元素,使用单例模式
    create_canvas: 返回指定尺寸的透明画布,不指定尺寸则使用默认标准参数
    ----------------------------------------------------------
    draw_background: 绘制背景图
    draw_chessboard: 绘制棋盘
    draw_playing_players: 绘制游戏中的玩家头像
    draw_result_text_line: 渲染结算界面文本
    draw_suspend_text_line: 渲染暂停界面文本
    ----------------------------------------------------------
    draw_chess: 绘制棋子
    draw_plants: 绘制魔力植物
    draw_players_hp: 绘制玩家血量
    draw_ascend_tip: 绘制ASCEND棋子的坐标提示
    ----------------------------------------------------------
    draw_start_ui: 绘制开始界面
    draw_turn_sign: 绘制回合标志
    draw_result_ui: 绘制结算界面的玩家头像
    draw_suspend_ui: 绘制暂停界面UI
    draw_coordinate_tip: 绘制放置棋子的坐标提示
    ----------------------------------------------------------
    _calculate_line_intersection: 计算直线交点的坐标
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        _init: 确保__init__只被运行一次
        _config_manager: 配置管理器
        _assets_manager: 资源管理器
        _chessboard_size: 棋盘尺寸
        _positions: 棋盘上各个交点的坐标 {tuple(hor, ver): tuple(x, y)}
        ---------------------------------------------------------------
        _coordinate_tip: 棋子坐标提示的动画类
        _turn_sign: 游戏回合标志的动画类
        _result: 游戏结算界面的动画类,将会在结算时初始化
        """
        if not hasattr(self, "_init"):
            self._init = True
            self._config_manager = ConfigManager.create_config_manager()
            self._assets_manager = AssetsManager.create_assets_manager()
            self._positions: dict = self._calculate_line_intersection()
            self._chessboard_size = self._config_manager.get_config("chessboard")["base-size"]

            """动画精灵类"""
            self._coordinate_tip = ClockwiseRevolveAnimation.create_clockwise_revolve_animation(
                self._config_manager.get_config("coordinate-tip")["revolve-rate"]
            )
            self._turn_sign = {
                "white": VerticalAnimation.create_vertical_animation(
                    self._config_manager.get_config("turn-sign"), "white", True
                ),
                "black": VerticalAnimation.create_vertical_animation(
                    self._config_manager.get_config("turn-sign"), "black", False
                )
            }
            self._result = None

    @classmethod
    def create_canvas_manager(cls):
        return cls()

    @classmethod
    def reset(cls):
        cls._instance = None
        return cls.create_canvas_manager()

    def create_canvas(self, size: tuple = None) -> pygame.Surface:
        """
        绘制标准棋盘尺寸大小的透明画布,并使用背景图覆盖
        :return: 指定大小的透明画布
        """
        if size is None:
            size = self._chessboard_size
        return pygame.Surface(size, pygame.SRCALPHA).convert_alpha()

    """静态层-只绘制一次"""
    def draw_background(self) -> pygame.Surface:
        """
        绘制背景图
        :return: 绘制背景图
        """
        return self._assets_manager.get_image("background")

    def draw_chessboard(self) -> pygame.Surface:
        """
        绘制正常状态下的棋盘
        :return: 棋盘画布
        """
        """读取棋盘配置"""
        chessboard_cfg = self._config_manager.get_config("chessboard")

        line_color = chessboard_cfg["line"]["color"]
        line_width = chessboard_cfg["line"]["width"]

        horizontal_start = chessboard_cfg["horizontal"]["start"]
        horizontal_end = chessboard_cfg["horizontal"]["end"]

        vertical_start = chessboard_cfg["vertical"]["start"]
        vertical_end = chessboard_cfg["vertical"]["end"]

        """绘制横线与竖线"""
        canvas = self.create_canvas()
        for line_ in range(0, 9):
            pygame.draw.line(
                canvas, line_color,
                horizontal_start[line_],
                horizontal_end[line_],
                line_width
            )
            pygame.draw.line(
                canvas, line_color,
                vertical_start[line_],
                vertical_end[line_],
                line_width
            )
        return canvas

    def draw_playing_players(self) -> pygame.Surface:
        """
        根据配置文件中的位置放置玩家头像与血条
        :return: 玩家头像画布
        """
        canvas = self.create_canvas()
        player_cfg = self._config_manager.get_config("players-ui")

        player_white = self._assets_manager.get_image("White-normal")
        player_black = self._assets_manager.get_image("Black-normal")
        canvas.blit(player_white, player_cfg["player-white-position"])
        canvas.blit(player_black, player_cfg["player-black-position"])
        return canvas

    def draw_result_text_line(self, winner: str, game_status: dict) -> pygame.Surface:
        """格式化并渲染结算文本"""
        res_ui = self._assets_manager.get_image("result-select")
        text_cfg = self._config_manager.get_config("result-ui")["text"]
        winner_format = {
            "white_hp": game_status["white-hp"],
            "black_hp": game_status["black-hp"],
        }
        body_format = {
            "date": game_status["start-time"].strftime("%Y/%m/%d/%H/%M"),
            "game_time": game_status["game-time"],
            "turn_number": game_status["turn-number"]
        }

        text_dict = {
            "tittle": text_cfg["tittle"],
            "winner": text_cfg["white-win"].format(**winner_format) if winner == "White" else text_cfg[
                "black-win"].format(**winner_format),
            "body": text_cfg["body"].format(**body_format),
        }
        text_cfg["color"]["winner"] = text_cfg["color"]["white-win"] if winner == "White" else text_cfg["color"][
            "black-win"]
        for key, value in text_dict.items():
            font = self._assets_manager.get_font(text_cfg["font"], text_cfg["size"][key])
            res_ui.blit(font.render(value, True, text_cfg["color"][key]), text_cfg["position"][key])

        """渲染分割线"""
        line_cfg = self._config_manager.get_config("result-ui")["line"]
        pygame.draw.line(
            res_ui, line_cfg["color"], line_cfg["start"], line_cfg["end"], line_cfg["width"]
        )
        return res_ui

    def draw_suspend_text_line(self, game_status: dict) -> pygame.Surface:
        """格式化并渲染结算文本"""
        res_ui = self._assets_manager.get_image("result-select")
        text_cfg = self._config_manager.get_config("suspend-ui")["text"]

        body_format = {
            "date": game_status["start-time"].strftime("%Y/%m/%d/%H/%M"),
            "game_time": game_status["game-time"],
            "turn_number": game_status["turn-number"]
        }
        text_dict = {
            "tittle": text_cfg["tittle"],
            "body": text_cfg["body"].format(**body_format),
        }
        """渲染文本"""
        for key, value in text_dict.items():
            font = self._assets_manager.get_font(text_cfg["font"], text_cfg["size"][key])
            res_ui.blit(font.render(value, True, text_cfg["color"][key]), text_cfg["position"][key])

        """渲染分割线"""
        line_cfg = self._config_manager.get_config("suspend-ui")["line"]
        pygame.draw.line(
            res_ui, line_cfg["color"], line_cfg["start"], line_cfg["end"], line_cfg["width"]
        )
        return res_ui

    """动态层-逐帧更新"""
    def draw_plants(self, plants: list, canvas: pygame.Surface) -> pygame.Surface:
        """
        根据植物有无图像属性为其随机选择图像属性并绘制植物
        :param plants: 魔力植物的列表
        :param canvas: 帧画布,默认为None,此时使用新创建的画布
        :return: 魔力植物的画布
        """
        blit_list = []
        for plant in plants:
            if not hasattr(plant, "image"):
                plant.image = choice(["plant{0}".format(i) for i in range(1, 7 + 1)])

            """获取植物图像与中心点坐标"""
            plant_image = self._assets_manager.get_image(plant.image)
            plant_boundary = self._assets_manager.get_image(plant.image + "-boundary")
            plant_x, plant_y = plant_image.size
            position_x, position_y = self._positions[plant.coordinate]
            """绘制植物与植物边界,保证植物边缘图像在上层"""
            plant_image.blit(plant_boundary, (0, 0))
            blit_list.append((plant_image, (position_x - plant_x / 2, position_y - plant_y * 0.87)))

        if canvas is None:
            canvas = self.create_canvas()
        canvas.blits(blit_list)
        return canvas

    def draw_players_hp(self, players_hp: dict, canvas: pygame.Surface) -> pygame.Surface:
        """
        :param players_hp: 玩家血量的字典{"white-hp": hp}
        :param canvas: 帧画布,默认为None,此时使用新创建的画布
        :return: 帧画布
        """
        bg_image = {
            "start": pygame.transform.rotate(
                self._assets_manager.get_image("background-boundary"), 180
            ),
            "middle": self._assets_manager.get_image("background-middle"),
            "end": self._assets_manager.get_image("background-boundary"),
        }
        white_image = {
            "start": pygame.transform.rotate(
                self._assets_manager.get_image("white-boundary"), 180
            ),
            "middle": self._assets_manager.get_image("white-middle"),
            "end": self._assets_manager.get_image("white-boundary"),
        }
        black_image = {
            "start": pygame.transform.rotate(
                self._assets_manager.get_image("black-boundary"), 180
            ),
            "middle": self._assets_manager.get_image("black-middle"),
            "end": self._assets_manager.get_image("black-boundary"),
        }

        def __draw_players_hp(now_hp: int, max_hp: int, images: dict, pos: tuple, ori: int) -> None:
            """
            :param now_hp:玩家当前血量
            :param max_hp: 玩家的最大血量
            :param images: 玩家血条样式贴图
            :param pos: 血条的起始位置(x, y)
            :param ori: 血条的方向
            """
            blit_list = []
            start_x, start_y = pos
            ima_size = self._assets_manager.get_image("background-middle").size
            for hp in range(0, now_hp):
                new_pos = (start_x + ori * hp * (ima_size[0] / 2), start_y - hp * (ima_size[1] / 2))
                if hp == 0:
                    blit_list.append((images["start"], new_pos))
                elif hp == now_hp:
                    blit_list.append((images["end"], new_pos))
                else:
                    blit_list.append((images["middle"], new_pos))
            for num in range(now_hp, max_hp):
                new_pos = (start_x + ori * num * (ima_size[0] / 2), start_y - num * (ima_size[1] / 2))
                if num == 0:
                    blit_list.append((bg_image["start"], new_pos))
                elif num == max_hp:
                    blit_list.append((bg_image["end"], new_pos))
                else:
                    blit_list.append((bg_image["middle"], new_pos))
            canvas.blits(blit_list)

        players_cfg = self._config_manager.get_config("players")
        hp_cfg = self._config_manager.get_config("players-ui")

        """绘制白棋血量"""
        max_white_hp = players_cfg["player-white-hp"]
        white_position = hp_cfg["player-white-hp-position"]
        __draw_players_hp(players_hp["white-hp"], max_white_hp, white_image, white_position, +1)
        """绘制黑棋血量"""
        max_black_hp = players_cfg["player-black-hp"]
        black_position = hp_cfg["player-black-hp-position"]
        __draw_players_hp(players_hp["black-hp"], max_black_hp, black_image, black_position, -1)
        return canvas

    def draw_ascend_tip(self, ascend_chess: list, canvas: pygame.Surface) -> pygame.Surface:
        """
        绘制ascend连子提示
        :param ascend_chess: 连子列表
        :param canvas: 帧画布,默认为None,此时使用新创建的画布
        :return: 棋盘列表
        """
        blit_list = []
        for chess in ascend_chess:
            ascend_tip = self._assets_manager.get_image("ascend-tip-{0}".format(chess.chess_type.lower()))
            x, y = self._positions[chess.coordinate]
            ascend_tip = self._assets_manager.get_alpha_image("ascend-tip", ascend_tip, 0.85)
            image_rect =ascend_tip.get_rect(center=(x, y))
            blit_list.append((ascend_tip, image_rect))
        canvas.blits(blit_list)
        return canvas

    def draw_chess(self, chess: list, plants: list, canvas: pygame.Surface) -> pygame.Surface:
        """
        基于棋盘的交点放置棋子,将魔力植物上的棋子变为半透明
        根据植物有无图像属性为其随机选择图像属性并绘制植物
        :param chess: 棋子对象的列表
        :param plants: 魔力植物对象的列表
        :param canvas: 帧画布,默认为None,此时使用新创建的画布
        :return: 帧画布
        """
        blit_list = []
        """获取棋子贴图与中心点坐标"""
        white_chess = self._assets_manager.get_image("white-chess")
        black_chess = self._assets_manager.get_image("black-chess")
        white_chess_alpha = self._assets_manager.get_alpha_image("white-chess", white_chess, 0.87)
        black_chess_alpha = self._assets_manager.get_alpha_image("black-chess", black_chess, 0.74)
        white_center_x, white_center_y = ((size_ - 1) / 2 for size_ in white_chess.size)
        black_center_x, black_center_y = ((size_ - 1) / 2 for size_ in black_chess.size)

        """绘制棋子"""
        chess_coords = {chess_.coordinate: chess_ for chess_ in chess}
        plant_coords = {plant.coordinate: plant for plant in plants}
        overlapping_coord = set(chess_coords.keys()).intersection(set(plant_coords.keys()))

        def single_chess_rect(chess_, chess_type, alpha: bool = False) -> tuple:
            """
            绘制单个棋子的函数，包括透明处理和旋转
            :param chess_: 棋子对象
            :param chess_type: 棋子类型 (白棋/黑棋)
            :param alpha: 是否需要半透明
            """
            """选择对应的棋子贴图"""
            if chess_type == "White":
                chess_image = white_chess_alpha if alpha else white_chess
                center_x, center_y = white_center_x, white_center_y
            else:
                chess_image = black_chess_alpha if alpha else black_chess
                center_x, center_y = black_center_x, black_center_y

            """旋转棋子"""
            rotated_chess = pygame.transform.rotate(chess_image, chess_.image_angle)

            """计算绘制位置,并绘制棋子"""
            position_x, position_y = self._positions[chess_.coordinate]
            return rotated_chess, (position_x - center_x, position_y - center_y)

        """绘制重合区域与普通的棋子"""
        for coord in overlapping_coord:
            chess_ = chess_coords[coord]
            blit_list.append(single_chess_rect(chess_, chess_.chess_type, alpha=True))
            del chess_coords[coord]
        for coord in chess_coords:
            chess_ = chess_coords[coord]
            blit_list.append(single_chess_rect(chess_, chess_.chess_type, alpha=False))

        canvas.blits(blit_list)
        return canvas

    def draw_start_ui(self, button_status: dict) -> pygame.Surface:
        """绘制结算界面按钮"""
        start = self._assets_manager.get_image("start-ui")
        button_cfg = self._config_manager.get_config("start-ui")["buttons"]
        start_ui = self._draw_buttons(button_cfg, button_status, start)
        return start_ui

    def draw_result_ui(self, winner: str, button_status: dict, canvas: pygame.Surface) -> pygame.Surface:
        """
        在基础结算界面上绘制结算玩家头像
        :param winner: 胜利方
        :param canvas: 帧画布
        :param button_status: 各个按钮的状态,True表示按钮被选中
        :return: 完整的结算界面
        """
        """绘制结算界面玩家动画"""
        loser = "Black" if winner == "White" else "White"
        if self._result is None:
            player_cfg = self._config_manager.get_config("result-players")["players"]
            self._result = {
                "winner": VerticalAnimation.create_vertical_animation(
                    player_cfg, winner, False
                ),
                "loser": HorizontalAnimation.create_horizontal_animation(
                    player_cfg, loser, False
                )
            }
        images = {
            "winner": self._assets_manager.get_image("{0}-winner".format(winner)),
            "loser": self._assets_manager.get_image("{0}-loser".format(loser))
        }
        for key in ["winner", "loser"]:
            self._result[key].update_position()
            canvas.blit(images[key], self._result[key].position)

        """绘制结算界面按钮"""
        button_cfg = self._config_manager.get_config("result-ui")["buttons"]
        result_ui = self._draw_buttons(button_cfg, button_status, canvas)
        return result_ui

    def draw_suspend_ui(self, button_status: dict, canvas: pygame.Surface) -> pygame.Surface:
        """
        在基础暂停界面的基础上绘制按钮
        :param button_status: 各个按钮的状态,True表示按钮被选中
        :param canvas: 帧画布
        :return: 渲染后的帧画布
        """
        """绘制结算界面按钮"""
        button_cfg = self._config_manager.get_config("suspend-ui")["buttons"]
        suspend_ui = self._draw_buttons(button_cfg, button_status, canvas)
        return suspend_ui

    def draw_coordinate_tip(self, coordinate: tuple, canvas: pygame.Surface) -> pygame.Surface:
        """
        绘制放置棋子位置的提示光圈（优化旋转中心版）
        :param coordinate: 光圈对象在棋盘上的坐标
        :param canvas: 帧画布
        :return: 更新后的帧画布
        """

        """旋转提示光圈"""
        coordinate_tip_image = self._assets_manager.get_image("coordinate-tip")
        position_x, position_y = self._positions[coordinate]
        rotated_image = pygame.transform.rotozoom(
            coordinate_tip_image,
            -self._coordinate_tip.angle,  # 使用负号保持顺时针旋转
            1.0  # 保持原尺寸
        )

        """更新当前旋转角度并定位旋转后的图像中心"""
        self._coordinate_tip.update_revolve_angle()
        image_rect = rotated_image.get_rect(center=(position_x, position_y))
        canvas.blit(rotated_image, image_rect.topleft)
        return canvas

    def draw_turn_sign(self, turn_chess: str, canvas: pygame.Surface) -> pygame.Surface:
        """
        根据在主画布上的位置绘制回合标志
        :param turn_chess: 当前回合方
        :param canvas: 帧画布
        :return: 帧画布
        """
        turn_chess = turn_chess.lower()
        chess_turn_sign = self._turn_sign[turn_chess]
        turn_sign = self._assets_manager.get_image("{}-sign".format(turn_chess))
        chess_turn_sign.update_position()

        """绘制到帧画布上"""
        canvas.blit(turn_sign, chess_turn_sign.position)
        return canvas

    """私有方法"""
    def _calculate_line_intersection(self) -> dict:
        """
        计算交点的坐标
        :return: {(hor, ver): position}的字典
        """

        """读取配置"""
        chessboard_config = self._config_manager.get_config("chessboard")
        horizontal_mid = chessboard_config["horizontal"]["middle"]
        horizontal_slops = chessboard_config["horizontal"]["slops"]
        vertical_mid = chessboard_config["vertical"]["middle"]
        vertical_slops = chessboard_config["vertical"]["slops"]

        """计算交点"""
        position = dict()
        for hor in range(0, 9):
            b_hor = horizontal_mid[hor][1] - horizontal_slops[hor] * horizontal_mid[hor][0]
            for ver in range(0, 9):
                b_ver = vertical_mid[ver][1] - vertical_slops[ver] * vertical_mid[ver][0]
                x = (b_ver - b_hor) / (horizontal_slops[hor] - vertical_slops[ver])
                y = x * vertical_slops[ver] + b_ver
                position[(hor + 1, ver + 1)] = (round(x), round(y))
        return position

    def _draw_buttons(self, cfg: dict, status: dict, canvas: pygame.Surface) -> pygame.Surface:
        """
        根据配置与状态绘制按钮
        :param cfg: 按钮配置
        :param status: 按钮状态,True为选中状态
        :param canvas: 绘制画布
        :return: 绘制后的画布
        """
        """绘制结算界面按钮"""
        text_cfg = cfg["text"]

        for key, value in status.items():
            button_normal = self._assets_manager.get_image("button-normal")
            button_select = self._assets_manager.get_image("button-select")
            font = self._assets_manager.get_font(text_cfg["font"], text_cfg["size"])

            string = font.render(text_cfg[key], True, text_cfg["color"][key])
            if value:
                button_select.blit(string, text_cfg["position"][key])
                canvas.blit(button_select, cfg["position"][key])
            else:
                button_normal.blit(string, text_cfg["position"][key])
                canvas.blit(button_normal, cfg["position"][key])
        return canvas

