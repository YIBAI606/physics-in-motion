# EP03 核心解释样片 v1

40秒，1920×1080，30fps，静音含字幕。是独立关键镜头样片，不表示完整十分钟视频已完成。

## 模型
一维、常物性、半无限体、完美接触，无血流、无接触热阻。皮肤初温32°C，材料22°C。教学参数：皮肤e=1200、alpha=1.1e-7；金属e=8000、alpha=1.2e-5；木材e=450、alpha=1.3e-7。SI单位，非具体材料实测数据。
Tc=(e_skin*32+e_material*22)/(e_skin+e_material)
T(x,t)=Ti+(Tc-Ti)*erfc(x/(2 sqrt(alpha*t)))
曲线追踪皮肤内0.15mm，不是界面，也不是统一感受器深度。
两侧都显示2mm，统一22–32°C色标。视频10–30秒映射模型0–5秒；不是实时录像。15秒出现观察点和其已发生的曲线历史，此后同步更新。30秒后保持最终状态供解释。
温度场可以解释触感的一个物理因素，不能单独预测主观冷感。

## 交付
core-40s-review.mp4、render.py、voiceover.txt、captions.srt、timeline.json、model.csv、review-sheet.jpg。
最终以剪映实际配音校准镜头时间。
