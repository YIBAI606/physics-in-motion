# physics-in-motion

Code-driven visualizations for quantum mechanics and thermal statistical physics.

用代码制作每一帧的科学可视化视频。下设量子力学、热力学与统计物理两个系列，每个系列分别制作长视频和短视频。

风格参考 3Blue1Brown：用视觉建立直觉，让动画参与推理。内容不限定教材，先启动热统试制。

## 项目入口
- [项目立项 v0.1](docs/project-charter.md)
- [制作规范 v0.1](docs/production-guide.md)
- [热统系列与首期候选](series/thermal-statistical/README.md)
- [量子力学系列](series/quantum/README.md)
- [共享组件](shared/README.md)

## 当前阶段
已完成立项及仓库结构初始化。首期热统内容仍为候选提案，尚无模拟代码或渲染成片。
下一步核查试播模型与文献，再制作关键画面原型。

## 目录
```text
docs/                        # 立项与制作规范
series/
  thermal-statistical/       # 热统
  quantum/                   # 量子力学
shared/                      # 共用视觉及动画组件
```

技术栈、画幅、帧率、配音和发布平台待试播阶段确定。
生成数据和渲染文件不纳入 Git；工具链确定后补充可复现运行说明。
