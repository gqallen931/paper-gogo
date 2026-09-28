# Starter Messages

- `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，判断当前 step；如果这只是首次总目标请求，不要执行 S0，只给出进入 S0-PAPER-FOUNDATION 的可复制提示词；如果用户明确要求执行某个 step，只执行本轮用户明确要求的一个 step，完成后停下并给出下一步可复制提示词。`
- `如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro 根据当前状态只建议下一步提示词，不要自动执行下一步。`
- `额外说明这个 skill 的设计初衷是什么。`
- `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，进入 S0-PAPER-FOUNDATION。请先建立项目状态、确认运行环境、输入材料、画幅和候选数量默认值；如果输入包含 PDF/LaTeX/论文正文/详细方法描述，请只基于允许读取的论文内容生成并打印 paper-foundation-report.md；不要生成任何目标论文图像；完成 S0 后停止，只给出 S1-FIGURE-STRATEGY 的可复制提示词。`
- `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，进入 S1-FIGURE-STRATEGY，根据论文材料和 S0-PAPER-FOUNDATION 深读记录给出图类型、读者效果和全局探索方向建议。`
- `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，进入 S2-SKETCH-EXPLORE，使用规定生图路径逐张单独生成至少 6 张全局探索草图；这些草图必须对应 S1 已经给出的前置文本候选介绍，要求从不同分类角度发散、默认少文字公式和不必要符号、图标清晰且第一眼有冲击；若采用故事性草图，故事必须贴近论文本身并用常见概念连接论文机制。完成 S2 后明确说明本阶段结束，未执行 S3。`
- `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，进入 S3-DIRECTION-SELECT，评估 S2 的低保真草图并选择进入局部细化的结构方向；完成后不要进入 S4，但必须给出 S4-CANDIDATE-BRIEF 的下一步提示词，并在共享部分外提供两个分支：A 后续参考图继续保持手绘特色；B 后续参考图更倾向于清晰正式、语义精准、图文共生的论文图，默认选择 B。同时给出默认 B 的可复制提示词，以及带 <填写心仪方案ID或描述> 占位符的自填方案提示词。完成 S3 后明确说明本阶段结束，未执行 S4。`
- `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，进入 S5-CANDIDATE-IMAGE，按 S4-CANDIDATE-BRIEF 的候选矩阵逐张单独生成正式 raster 候选架构图；默认使用正规论文 schematic 风格，避免手绘、白板、sketch-note、漫画和 storyboard 风格；仍然生成图片，不生成 SVG；图标以更好体现论文内涵为标准，箭头、颜色、核心创新视觉锚点和 caption 分工必须精准。完成 S5 后明确说明本阶段结束，未执行 S6。`
- `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，进入 S6-FINAL-SELECT，从 S5-CANDIDATE-IMAGE 中选出最终图，给出选中路径/展示、选择理由、论文事实核对、figure title、style-aware caption、legend、正文引用句和 manuscript revision note；完成 S6 后明确说明本阶段结束，未执行 S7，并只给出 S7-FINAL-JOINT-AUDIT 的下一步提示词。`
- `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，进入 S7-FINAL-JOINT-AUDIT。若已有旧 S7 产物或记录，先删除旧 S7 outputs、注销旧 S7 active records、在 state/project-state.json 登记 cleanup event，然后执行一次有边界的图文联合终审：把最终图和 caption/legend/正文引用句作为整体，检查论文事实、模型、算法、流程、数学、核心创新锚点、箭头、颜色、图标、符号/公式必要性、caption 风格匹配和 reviewer readiness；给出 PASS/TEXT-REPAIR/IMAGE-REPAIR/DIRECTION-REPAIR verdict。`
