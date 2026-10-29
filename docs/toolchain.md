# 工具链评估 v0.1

日期：2026-10-30
状态：已在一台 8 核 / 16 GiB / 无 GPU 的 Ubuntu 22.04 机器上实测

## 结论先说

**第一期用 matplotlib + ffmpeg 出片，Manim 暂缓。**

理由不是 Manim 不好，而是那台渲染机的系统包处于破损状态（`apt` 报 held broken packages），装不上 `libpango1.0-dev`，因而无法编译 `manimpango`。修系统包有引出其他问题的风险，而 matplotlib 现在就能跑。

## 实测数据

在一台 8 核 / 16 GiB / 无 GPU 的机器上，用 matplotlib 3.10.8 渲染一段代表性画面（二维热图演化 + LaTeX 公式标题，1920×1080）：

| 项目 | 数值 |
| --- | --- |
| 帧数 | 150 帧（5 秒 @30fps） |
| 渲染耗时 | 15.43 秒 |
| 单帧耗时 | 0.103 秒 |
| 编码耗时 | 2.12 秒（libx264，CRF 20） |
| 成片大小 | 553 KB |

按此换算 10 分钟长视频（18000 帧）：

- 单进程：约 31 分钟
- 8 核多进程：约 5–7 分钟（matplotlib 单线程，靠进程并行）

渲染不是瓶颈；时间主要花在设计画面上。

## 候选方案对比

### A. matplotlib + ffmpeg（当前采用）

优点：环境已就绪；数值模拟天然契合；出帧逻辑可控，便于多进程。
缺点：没有镜头语言，运镜、渐变、转场都要自己写；3D 需 mplot3d，效果有限。

### B. Manim Community

优点：镜头语言成熟，MathTex 公式排版最好，社区示例多。
缺点：模拟逻辑要包进 Scene；依赖 cairo/pango，当前机器装不上；渲染比 matplotlib 重。

### C. Blender + bpy（未评估）

适合高质量 3D 与材质，学习成本最高，与"代码驱动每一帧"的目标偏离较大。暂不纳入。

## 工程约定

### 运行环境

渲染机的 `$HOME`（`/var/lib/yibai-home`）不可写，必须显式指定可写目录，否则 matplotlib 会把缓存建到 `/tmp` 并每次重建：

```bash
export HOME=/tmp/yibai
export MPLCONFIGDIR=/tmp/yibai/.mpl
```

### 磁盘

帧序列默认保留在 `generated/`（已在 `.gitignore` 中排除），**渲染完成后删除**。
10 分钟 1080p30 的 PNG 序列约 5–6 GB，磁盘只有 35 GB 可用，不清会很快占满。

### 目录

```text
shared/            共用样式、公式渲染、时间轴、镜头组件
series/<name>/    每期的脚本、分镜、模拟入口
generated/        模拟数据与帧序列（不进 Git）
renders/          成片（不进 Git）
```

### 复现

每期提供单一入口，参数（随机种子、精度、分辨率）由命令行传入：

```bash
python -m pim.ep01 --seed 42 --fps 30 --size 1920x1080
```

## 待定

- 是否修复渲染机的 apt，以启用 Manim（需评估影响面）
- 画幅与帧率（16:9 1080p60 或 1080p30）
- 旁白与字幕的生成方式
- 许可证（代码与视频分别选择）
