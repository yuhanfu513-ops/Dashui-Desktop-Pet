# 大水桌宠

macOS 透明桌宠，以提供的人物图片作为形象，播放从两个视频里切出的原声。

- 点击人物，随机播放一段；说话时上下压缩回弹，并显示对应文字。
- 拖动人物可移动；右键可挑选语音、停止播放、调整音量和人物大小、移回屏幕右下角或退出。
- 默认音量 65%。许家印桌宠播放“邦友跳舞”时，已打开的大水桌宠会一起跳。
- 两个视频目前使用 8 段，详见 `音频切分记录.md`；视频结尾如果本来就截断，无法补全未录到的内容。
- 打开桌宠管理中心可勾选、召唤或关闭大水桌宠。

## 安装

从 [Releases](https://github.com/yuhanfu513-ops/Dashui-Desktop-Pet/releases/latest) 下载 `Dashui-Desktop-Pet-macOS.zip`，解压后将应用拖进“应用程序”。

## 构建

需要 Apple Silicon 和 macOS 14 及更新版本。安装 Apple Command Line Tools 后运行 `./build.sh`，产物在 `build/大水桌宠.app`。复制到“应用程序”即可运行。程序离线运行，语音和头像放在 `Assets/`。

`Tools/` 中是针对原视频使用的素材处理脚本：重新切片需要另行提供原视频或对应 WAV，以及 NumPy；语音识别脚本还需要 faster-whisper 和本地模型。原始视频与临时工作文件不包含在仓库中。

## 许可

程序代码以 [MIT](LICENSE) 发布；交互实现参考好事桌宠及 SunPet，保留第三方许可 `LICENSE-GoodThing`、`LICENSE-SunPet`。人物图片和音频素材来自用户提供的文件，不属于代码的 MIT 许可。
