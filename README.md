# physics-in-motion

Code-driven visualizations for quantum mechanics and thermal statistical physics.

用代码制作每一帧的科学可视化视频。下设量子力学、热力学与统计物理两个系列，每个系列分别制作长视频和短视频。

风格参考 3Blue1Brown：用视觉建立直觉，让动画参与推理。内容不限定教材，先启动热统试制。

## 项目入口
- [项目立项 v0.1](docs/project-charter.md)
- [制作规范 v0.2](docs/production-guide.md)
- [下一期制作模板](templates/episode/README.md)
- [交付检查表](templates/episode/release-checklist.md)
- [第一期复盘](docs/ep01-retrospective.md)
- [工具链评估 v0.1](docs/toolchain.md)
- [热统系列与首期候选](series/thermal-statistical/README.md)
- [量子力学系列](series/quantum/README.md)
- [共享组件](shared/README.md)

## 当前阶段
用户已确认热统第一期完成。首期围绕微观状态计数、宏观能量分配与相对涨落，最终音画同步交付约 3 分 19 秒、1080p。

已整理制作规范、第一期复盘及下一期模板。是否已在 B 站或抖音正式发布尚未核实。统一动画组件库与自动脚手架仍待实现。

下一期从选题卡和科学核验表开始，完成脚本与关键片段原型后，先锁定实际配音，再安排整片动画节奏。

## 目录
```text
docs/                        # 立项、制作规范与复盘
templates/episode/           # 选题、分镜、时间轴与交付模板
series/
  thermal-statistical/       # 热统
  quantum/                   # 量子力学
shared/                      # 共用视觉及动画组件
```

首期采用 HTML Canvas、Chromium 和 FFmpeg，横屏输出 30 fps，配音由用户选择的外部 AI 工具完成。首发平台规划为 B 站与抖音；竖屏短视频单独设计。

生成数据、大型媒体与模型权重不直接纳入本仓库。源码需保留实际运行依赖和重建命令；第一期试制代码尚需整理为独立、可复用的工程。
