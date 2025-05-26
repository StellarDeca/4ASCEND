# encoding=utf-8

import pygame
import datetime
from sys import exit
from time import sleep
from pathlib import Path
from copy import deepcopy
from ASCEND import GameStatusManager, GameCanvasManager, GameAudiosManager


class ASCEND:
    """
    游戏主控制器
    UI_NAMES: UI状态的字典key
    START_BUTTONS: 起始UI的按钮key
    SUSPEND_BUTTONS: 暂停界面的按钮key
    END_BUTTONS: 结算UI的按钮key
    ui_flags: 游戏所处界面的标志

    --------------------------------------------------------------
    FrameStatusManager: 帧画布管理类,管理帧画布的渲染标志与已经渲染好的画布
    ButtonManager: 按钮选择管理类

    --------------------------------------------------------------
    start: 游戏的起始
    check_game_over: 检测胜利状态并设置界面状态
    process_input: 监听键盘输入
    render_frame: 渲染帧画布

    --------------------------------------------------------------
    _get_ui_status_flag: 获取UI标志
    _update_ui_flag: 更新UI标志

    --------------------------------------------------------------
    _init_constant_frame: 初始化基础帧画布

    --------------------------------------------------------------
    _play_turn: 游戏的回合处理
    _reset_playing: 重置游戏状态

    --------------------------------------------------------------
    _render_start_frame: 绘制起始界面UI
    _render_playing_frame: 绘制对局帧画布
    _render_end_frame: 绘制结算UI

    --------------------------------------------------------------
    _render_start_frame: 起始UI按键处理
    _handle_playing_input: 游戏对局的按键处理
    _handle_end_input: 结算UI的按键处理
    --------------------------------------------------------------
    _open_help_server(): 打开游戏规则html
    _deep_equal: 通过比较hash值来判断 a 与 b是否相同
    """
    UI_NAMES = ("playing", "start", "suspend", "end")
    START_BUTTONS = ("start-play", "help", "over")
    SUSPEND_BUTTONS = ("continue-play", "over")
    END_BUTTONS = ("replay", "over")
    ui_flags = {key: key == "start" for key in UI_NAMES}

    class FrameStatusManager:
        """
        帧画布管理类,管理帧画布的渲染标志与已经渲染好的画布
        get_constant_frame: 获取基本帧画布
        get_ui_canvas: 获取指定的画布
        get_ui_flag: 获取指定的画布标志
        -----------------------------------------
        update_ui_canvas: 更新指定的画布
        update_ui_flag: 更新指定的画布标志
        -----------------------------------------
        reset: 重置当前类的实例
        """
        def __init__(self, constant_canvas: pygame.Surface):
            """
            _constant_frame: 基本画布,一局游戏绘制一次
            _ui_canvas: ui画布,一些ui不需要此属性(start-ui)
            _ui_flag: ui画布标志,一些ui不需要此属性(start-ui)
            """
            self._constant_frame = constant_canvas

            ui_names = ("suspend", "end")
            self._ui_canvas: dict = {k : None for k in ui_names}
            self._ui_flag: dict = {k: False for k in ui_names}

        """获取指定的标志、画布、与元素"""
        @property
        def get_constant_frame(self) -> pygame.Surface: return deepcopy(self._constant_frame)

        def get_ui_canvas(self, name: str) -> pygame.Surface: return deepcopy(self._ui_canvas[name].copy())

        def get_ui_flag(self, name: str) -> bool: return self._ui_flag[name]

        """修改指定的标志、画布与元素"""
        def update_ui_canvas(self, name: str, canvas: pygame.Surface) -> None:
            self._ui_canvas[name] = canvas

        def update_ui_flag(self, name: str, flag: bool) -> None:
            self._ui_flag[name] = flag

        @classmethod
        def reset(cls, constant_canvas):
            return cls(constant_canvas)

    class ButtonManager:
        """
        按钮选择管理类,处理按钮的选中事件,每一个界面都应当实例化一个按钮选择管理类
        move_next: 选择下一个按钮
        move_up: 选择上一个按钮
        current: 获取指定按钮的状态
        current_status: 获取所有按钮的选中状态
        -------------------------------------
        _update_status: 更新按钮的选中状态
        -------------------------------------
        reset: 重置当前类的实例
        """

        def __init__(self, buttons: tuple):
            self._buttons = buttons
            self._index = None
            self._status = {btn: False for btn in buttons}

        def move_next(self) -> None:
            self._index = 0 if self._index is None else (self._index + 1) % len(self._buttons)
            self._update_status()

        def move_up(self) -> None:
            self._index = -1 if self._index is None else (self._index - 1) % len(self._buttons)
            self._update_status()

        def current(self, btn_name: str) -> bool: return self._status[btn_name]

        @property
        def current_status(self) -> dict: return self._status

        def _update_status(self) -> None:
            self._status = {btn: (btn == self._buttons[self._index]) for btn in self._buttons}

        @classmethod
        def reset(cls, buttons: tuple):
            return cls(buttons)

    def __init__(self):
        """
        初始化pygame模块,
        clock: 时钟对象,主要用于控制帧率
        windows_size: 屏幕尺寸
        windows: 主窗口
        ---------------------------------------
        status: 游戏状态管理类实例
        canvas: 画布管理类实例
        audios: 音频管理类实例
        frames: 帧画布管理类实例
        start_buttons: 起始UI按钮管理类
        end_buttons: 结算UI按钮管理类
        """
        pygame.init()
        """初始化游戏属性"""
        _size_ = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.windows_size = (_size_.current_w, _size_.current_h)
        self.windows = pygame.display.set_mode(self.windows_size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED)

        """设置窗口标题与窗口图标"""
        icon_path = "./Icon.ico"
        icon = pygame.image.load(Path(__file__).parent / icon_path)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("4ASCEND")

        """初始化游戏管理类"""
        self.status = GameStatusManager.create_status_manager()
        self.canvas = GameCanvasManager.create_canvas_manager()
        self.audios = GameAudiosManager.create_audios_manager()
        self.frames = self.FrameStatusManager(self._init_constant_frame())

        self.start_buttons = self.ButtonManager(self.START_BUTTONS)
        self.suspend_buttons = self.ButtonManager(self.SUSPEND_BUTTONS)
        self.end_buttons = self.ButtonManager(self.END_BUTTONS)

    def start(self):
        """游戏主循环,循环外播放主BGM与进入游戏的音效"""
        self.audios.play_bgm("ascend_bgm")
        sleep(0.2)
        self.audios.play_audio_clip("enter")
        while True:
            """先检测按键,后绘制帧图像"""
            self.check_game_over()
            self.process_input()
            frame = self.render_frame()
            self.windows.blit(frame, frame.get_rect(center=self.windows.get_rect().center))
            pygame.display.flip()
            self.clock.tick(90)

    def check_game_over(self):
        """检测胜利状态并设置界面状态,并播放结算音效"""
        if self.status.winner is not None and self._get_ui_status_flag("playing"):
            self._update_ui_flag("end")
            self.audios.play_audio_clip("end")

    def process_input(self):
        """根据UI状态监听键盘输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                current_ui = next(k for k, v in self.ui_flags.items() if v)
                getattr(self, f"_handle_{current_ui}_input")(event)

    def render_frame(self):
        """根据UI状态渲染帧画布"""
        current = next(k for k, v in self.ui_flags.items() if v)
        render_method = getattr(self, f"_render_{current}_frame")
        return pygame.transform.scale(render_method(), self.windows_size)

    """私有化方法"""
    @classmethod
    def _get_ui_status_flag(cls, ui_name: str) -> bool: return cls.ui_flags[ui_name]

    @classmethod
    def _update_ui_flag(cls, ui_name: str) -> None:
        cls.ui_flags = {k: (k == ui_name) for k in cls.UI_NAMES}

    """初始化基础帧画布"""
    def _init_constant_frame(self) -> pygame.Surface:
        """初始化基本画布,结算界面基本画布将在胜利方出现后渲染"""
        frame = self.canvas.create_canvas()
        base_canvas = [
            self.canvas.draw_background(),
            self.canvas.draw_chessboard(),
            self.canvas.draw_playing_players()
        ]
        for sur in base_canvas:
            frame.blit(sur, (0, 0))
        return frame

    """游戏游玩逻辑"""
    def _play_turn(self):
        """游戏的回合管理,同时处理音效播放"""
        status = self.status

        """玩家轮换与棋子创建"""
        opponent = "Black" if status.turn_chess == "White" else "White"
        turn_chess = status.creat_chess()

        """4ASCEND状态管理"""
        if status.chessboard.append_chess(turn_chess):
            status.chess.append(turn_chess)

            """播放落子音效"""
            self.audios.play_chess_audio_clip(opponent)

            if status.ascend:
                """播放防守音效"""
                self.audios.play_audio_clip("defend")

                """防守方回合处理"""
                status.defender_coiled = status.chessboard.check_coiled_chess(turn_chess.chess_type)
                if status.has_defender_overlapping_chess(turn_chess):
                    self.audios.play_audio_clip("back-attack")

                if status.defender_coiled:
                    status.handle_defender_ascend_status()
                else:
                    status.handle_defender_not_ascend_status(turn_chess)

                """更新游戏状态,并根据魔力植物的生长情况播放生长音效"""
                status.chessboard.update_chess_range(status.chess)
                status.update_player_hp()
                if status.grow_plants():
                    self.audios.play_audio_clip("grow")

                """重置4ASCEND状态"""
                status.attacker_coiled.clear()
                status.defender_coiled.clear()
                status.ascend = False

            else:
                """正常回合处理"""
                if result := status.chessboard.check_coiled_chess(turn_chess.chess_type):
                    self.audios.play_audio_clip("attack")
                    status.attacker_coiled = result
                    status.handle_attacker_ascend_status()
                    status.ascend = True
                else:
                    """更新土壤肥力,并根据魔力植物的生长情况播放生长音效(落子进入4ASCEND态势必定不会触发生长)"""
                    if status.update_plant_soil_fertility() and status.grow_plants():
                        self.audios.play_audio_clip("grow")

            """回合轮换"""
            status.turn_chess = opponent
            status.turn_number += 1
            status.check_winner()

    def _reset_playing(self):
        """重置游戏状态,重开对局"""
        self.status = GameStatusManager.reset()
        self.canvas = GameCanvasManager.reset()
        self.frames = self.FrameStatusManager.reset(self._init_constant_frame())
        self.start_buttons = self.ButtonManager.reset(self.START_BUTTONS)
        self.suspend_buttons = self.ButtonManager.reset(self.SUSPEND_BUTTONS)
        self.end_buttons = self.ButtonManager.reset(self.END_BUTTONS)
        self._update_ui_flag("playing")

    """游戏帧渲染逻辑"""
    def _render_start_frame(self) -> pygame.Surface:
        """绘制起始界面UI"""
        start = self.canvas.draw_start_ui(self.start_buttons.current_status)
        return start

    def _render_suspend_frame(self) -> pygame.Surface:
        if not self.frames.get_ui_flag("suspend"):
            """绘制当前棋盘所有元素"""
            frame = self._render_playing_frame()

            """绘制暂停界面ui"""
            total_seconds = (datetime.datetime.now() - self.status.start_time).total_seconds()
            min_, sec = divmod(total_seconds, 60)
            game_time = "{0}分{1}秒".format(int(min_), int(sec))
            game_statues = {
                "start-time": self.status.start_time,
                "game-time": game_time,
                "turn-number": self.status.turn_number
            }
            suspend = self.canvas.draw_suspend_text_line(game_statues)
            frame.blit(suspend, suspend.get_rect(center=frame.get_rect().center))

            """更新基本帧与暂停界面绘制flag"""
            self.frames.update_ui_canvas("suspend", frame)
            self.frames.update_ui_flag("suspend", True)

        suspend = self.frames.get_ui_canvas("suspend")
        buttons = self.suspend_buttons.current_status
        suspend_ui = self.canvas.draw_suspend_ui(buttons, suspend)
        return suspend_ui

    def _render_playing_frame(self):
        """渲染顺序：plants → chess → ascend-tip → players-hp → 其他"""
        draw_function = {
            "chess": self.canvas.draw_chess,
            "plants": self.canvas.draw_plants,
            "players-hp": self.canvas.draw_players_hp,
            "ascend-tip": self.canvas.draw_ascend_tip,
            "coordinate-tip": self.canvas.draw_coordinate_tip,
            "turn-sign": self.canvas.draw_turn_sign,
        }
        draw_function_data = {
            "chess": {
                "chess": self.status.chess,
                "plants": self.status.plants,
            },
            "plants": {"plants": self.status.plants},
            "players-hp": {
                "players_hp": {
                    "white-hp": self.status.player_white.hit_point,
                    "black-hp": self.status.player_black.hit_point,
                }
            },
            "ascend-tip": {"ascend_chess": self.status.attacker_coiled},
            "coordinate-tip": {"coordinate": self.status.coordinate_tip.coordinate},
            "turn-sign": {"turn_chess": self.status.turn_chess}
        }

        frame = self.frames.get_constant_frame
        for key in ("plants", "chess", "ascend-tip", "players-hp", "coordinate-tip", "turn-sign"):
            draw_function_data[key]["canvas"] = frame
            frame = draw_function[key](**draw_function_data[key])

        return frame

    def _render_end_frame(self) -> pygame.Surface:
        """绘制结算UI帧画布,基础画布仅仅绘制一次"""
        if not self.frames.get_ui_flag("end"):
            """绘制当前棋盘所有元素"""
            frame = self._render_playing_frame()

            """绘制结算界面ui"""
            game_statues = {
                "white-hp": self.status.player_white.hit_point,
                "black-hp": self.status.player_black.hit_point,
                "start-time": self.status.start_time,
                "game-time": self.status.game_time,
                "turn-number": self.status.turn_number
            }
            result = self.canvas.draw_result_text_line(self.status.winner, game_statues)
            frame.blit(result, result.get_rect(center=frame.get_rect().center))

            """更新UI画布与结算界面flag"""
            self.frames.update_ui_canvas("end", frame)
            self.frames.update_ui_flag("end", True)

        result = self.frames.get_ui_canvas("end")
        buttons = self.end_buttons.current_status
        result_ui = self.canvas.draw_result_ui(self.status.winner, buttons, result)
        return result_ui

    """键盘输入处理"""
    def _handle_start_input(self, event) -> None:
        """
        起始UI的按键处理与部分音效播放
        :param event: 按键事件
        """
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.start_buttons.move_up()
            self.audios.play_audio_clip("choose")
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.start_buttons.move_next()
            self.audios.play_audio_clip("choose")
        elif event.key in (pygame.K_RETURN, pygame.K_z):
            if self.start_buttons.current("start-play"):
                self._update_ui_flag("playing")
                self.audios.play_audio_clip("start")
            elif self.start_buttons.current("help"):
                self._open_help_server()
            elif self.start_buttons.current("over"):
                exit()

    def _handle_playing_input(self, event) -> None:
        """
        游戏对局的按键处理
        :param event: 按键事件
        """
        if self.status.winner is None:
            if event.key in (pygame.K_RETURN, pygame.K_z):
                self._play_turn()
            elif event.key in (pygame.K_w, pygame.K_UP):
                self.status.coordinate_tip.up_next()
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.status.coordinate_tip.down_next()
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                self.status.coordinate_tip.left_next()
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.status.coordinate_tip.right_next()
            elif event.key == pygame.K_ESCAPE:
                self._update_ui_flag("suspend")

    def _handle_suspend_input(self, event) -> None:
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.suspend_buttons.move_up()
            self.audios.play_audio_clip("choose")
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.suspend_buttons.move_next()
            self.audios.play_audio_clip("choose")
        elif event.key in (pygame.K_RETURN, pygame.K_z):
            if self.suspend_buttons.current("continue-play"):
                self._update_ui_flag("playing")
                self.frames.update_ui_flag("suspend", False)
                self.audios.play_audio_clip("enter")
            elif self.suspend_buttons.current("over"):
                exit()
        elif event.key == pygame.K_ESCAPE:
            self._update_ui_flag("playing")
            self.frames.update_ui_flag("suspend", False)
            self.audios.play_audio_clip("enter")

    def _handle_end_input(self, event) -> None:
        """
        结算UI的按键处理与部分音效播放
        :param event: 按键事件
        """
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.end_buttons.move_up()
            self.audios.play_audio_clip("choose")
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.end_buttons.move_next()
            self.audios.play_audio_clip("choose")
        elif event.key in (pygame.K_RETURN, pygame.K_z):
            if self.end_buttons.current("replay"):
                self._reset_playing()
                self.audios.play_audio_clip("start")
            elif self.end_buttons.current("over"):
                exit()

    """游戏规则查看方法"""
    @staticmethod
    def _open_help_server():
        """启动本地HTTP服务器并打开游戏教程html"""
        import threading, socket, webbrowser
        from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

        """html文件路径"""
        help_dir = Path(__file__).parent / "ASCEND/Help"
        help_file = help_dir / "help.html"

        """获取可用端口,并设置处理器"""
        with socket.socket() as s:
            s.bind(('', 0))
            port = s.getsockname()[1]

        class SilentHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(help_dir), **kwargs)

            def log_message(self, *args): pass

        """启动线程服务并使用浏览器打开html文件"""
        server = ThreadingHTTPServer(('127.0.0.1', port), SilentHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        return webbrowser.open(f"http://localhost:{port}/{help_file.name}")

    """深度比较"""
    @staticmethod
    def _deep_equal(data, other) -> bool:
        """通过比较hash值来判断data与other是否相同"""
        if isinstance(data, list) and isinstance(other, list):
            if len(data) != len(other):
                return False
            for v1, v2 in zip(data, other):
                if hash(v1) != hash(v2):
                    return False
            return True
        elif isinstance(data, dict) and isinstance(other, dict):
            for k1, k2 in zip(data.keys(), other.keys()):
                if k1 != k2 or hash(data[k1]) != hash(other[k2]):
                    return False
            return True
        else:
            if data == other:
                return True
            else:
                return False


if __name__ == "__main__":
    ASCEND().start()

