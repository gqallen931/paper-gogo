# 世界模型工作法 🧠
### World-Model Method — 让 AI「规划出」答案，而不是「顺嘴生成」

> 普通 AI 是**一个字接一个字往下写**——流畅，但没想清楚。
> 这个小工具（Claude Skill）让 AI 换一种干活方式：**先定目标 → 在脑子里建模 → 预测几条路各自的后果 → 挑出最优的整条路 → 最后才动笔。**
> 产出是**「规划出来的」**，不是**「生成出来的」**。

<details>
<summary><b>🌍 English TL;DR (click)</b></summary>

**World-Model Method** is a Claude Skill that switches the assistant from default token-by-token generation into an objective-driven, plan-first working mode: define an explicit goal + cost, build an abstract model of the situation, predict the consequences of several candidate approaches, search/optimize for the best full plan, then render the output last. It operationalizes Yann LeCun's world-model / JEPA / *"A Path Towards Autonomous Machine Intelligence"* ideas as a reusable prompt-level method for any non-trivial task — writing, decisions, strategy, problem-solving, design. MIT-licensed.
</details>

---

## 这是干嘛的？（一句话）

**让 AI 干重要的活之前，先像人一样"想清楚"再下手。**

不是顺着第一个想法写到底，而是：想明白要什么、把情况摸清、列几条路比一比、挑最好的那条、再展开成成品。

## 为什么要做？

现在的大模型本质是"**预测下一个字**"——所以它默认就是顺嘴往下接，看着通顺，但常常**没定目标、没比方案、没预演后果**。简单问题无所谓，但碰到**重要的、有多种做法、做错代价大**的事，这种"顺嘴生成"就容易给你一个"能用但不够好、甚至埋了坑"的答案。

这个工作法的灵感来自 **杨立昆（Yann LeCun）** 提出的"世界模型 / 自主机器智能"——他认为真正的智能不是顺嘴接话，而是**对世界建模、预测后果、朝目标规划**。我们把他这套思路，翻译成了一个**任何任务都能套用的干活流程**。

## 六步法（大白话）

1. **定目标**：先问清楚——成功长什么样？要避免什么？有什么死规矩不能破？
2. **建模**：把这件事的关键要素、关系、约束摸一遍（先别急着写）。
3. **预测后果**：想 2–4 种做法，每种**推演一下会导致什么**。
4. **挑路**：不拿第一个想法就跑，对照目标把几条路比一比，选最优的整条。
5. **动笔**：到这一步**才**把选中的方案展开成具体成品。
6. **自检**：对照目标和死规矩查一遍，不合格就回去重来。

> 简单说：**前 4 步在"想"，第 5 步才"写"，第 6 步再"查"。** 普通 AI 直接跳到第 5 步。

## 怎么用？

### 方式一：当成 Claude 技能（推荐）
把 `world-model-method/` 放进你的 Claude 技能目录，然后说：

> 「**用世界模型工作法，帮我做 ___**」（比如：定个内容策略 / 做个决策 / 解决这个难题）

它会自动走完六步，先给你"规划"，再给"成品"，最后自检。

### 方式二：当成一张思考清单
不用 AI 也行——重要的事，自己拿这六步问一遍。**光是逼自己"先定目标、再比两条路"，就能少踩很多坑。**

## 它会给你什么（输出长这样）

```
【目标 & 成本】成功标准 / 要最小化什么 / 硬约束
【世界模型】关键要素 · 关系 · 动态 · 约束
【候选路径 & 后果预测】方案A→后果  方案B→后果  …
【选择】选哪条 + 为什么
──── 以下是渲染出的成品 ────
<具体产出>
【自检】对照目标过没过
```

👉 完整对比示例（默认生成 vs 工作法）见 [`examples/example-content-strategy.md`](./examples/example-content-strategy.md)。

## 适合谁

- ✍️ 做内容/方案的人：让产出比"AI 顺嘴写的"更有章法
- 🧭 要做决策、定策略的人：先比几条路再拍板
- 🧩 解复杂问题的人：把"想清楚"这件事流程化

## 诚实说明

- 这是把 LeCun 的思路**翻译成"怎么用 AI"的工作法**，**不是**真的换了底层神经网络架构——别理解成"现在跑的是世界模型"。
- 它**拿速度换深思**：好处是少踩坑、方案更优；代价是慢、啰嗦。**简单活别用，杀鸡不用牛刀。**
- 它不保证答案绝对正确，只保证**想得更结构化**——复杂任务里，这通常就够把次品挡在门外。

## 致谢 & 来源

灵感来自 Yann LeCun《A Path Towards Autonomous Machine Intelligence》(2022) 与 Meta V-JEPA 2 (2025) 所代表的"世界模型"路线。本项目是对这些**公开思路的再加工**，不复制任何第三方原始内容。

## License

[MIT](./LICENSE) — 随便用，注明出处即可。
