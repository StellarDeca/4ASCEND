# 4ASCEND
一个基于五子棋规则改编的双人对战棋类游戏，仅仅支持 Windows 平台。

## 🎮 项目说明
本项目为学习用途开发，包含基础的游戏逻辑与界面交互

## 📁 项目结构简要
- `ASCEND`程序主要资源文件夹
  - `Assets/`：包含游戏素材（详情请翻阅Assets目录下的Assets.md文件）
  - `Scripts/`：主要游戏元素模块
  - `Configs/`：配置文件（详情请翻阅Configs目录下的Configs.md文件）
  - `Manager/`: 主要游戏逻辑模块
  - `Help/`: 游戏教程模块
- `main.py`主程序文件
- `Icon.ico`程序图标文件

## 📢 使用声明
本项目仅供个人学习与研究使用，**禁止任何形式的商业用途**。
部分美术资源以及全部音效资源来源于 **@AliceInCradle**，版权归原作者所有。
若擅自将本项目或相关资源用于商业用途，所引发的法律责任将由使用者自行承担，与本项目作者无关。
如有版权方发现侵权，请及时联系删除。

## ♫ 关于背景音乐
**受到版权方的要求，本项目的Windows Exe程序及源代码并未包含BGM，仅仅包含经过许可的音效。**
### 如何设置自定义的BGM？
首先，请克隆仓库或者在[Releases](https://github.com/StellarDeca/4ASCEND/releases) 页面下载源代码。
将**WAV**格式的音频文件保存至目录ASCEND\Assets\Audios\BackGroundMusic下，并命名为bgm.wav。
### 如何重新对代码打包？
首先确保电脑上安装了Python 3.10及以上的版本，并安装库pygame-ce 2.5及以上的版本，pyinstaller 6.11及以上的版本。
使用pyinstaller命令进行打包（注意仅仅替换路径即可）：
```powershell
pyinstaller --noconfirm --onefile --windowed --icon "EXE程序ICON图标的绝对路径" --add-data "Assets资源文件夹的绝对路径;./ASCEND/Assets" --add-data "Configs配置文件夹的绝对路径;./ASCEND/Configs" --add-data "Help教程文件夹的绝对路径;./ASCEND/Help"  "main.py程序主文件的绝对路径"
```
## 📦 下载方式
请前往 [Releases](https://github.com/StellarDeca/4ASCEND/releases) 页面下载已打包的 Windows 可执行文件。

