---
name: world-model-method
description: >-
  A general-purpose working mode that makes the assistant produce output the "world-model way"
  — define an explicit goal and cost, build an abstract model of the situation, predict the
  consequences of several candidate approaches, search/optimize for the best full plan, and only
  then render the concrete output — instead of generating it token-by-token off the top. This
  operationalizes Yann LeCun's objective-driven / world-model / planning ideas (JEPA, "A Path
  Towards Autonomous Machine Intelligence") as a reusable prompt-level method for ANY non-trivial
  task: important writing, decisions, strategy, problem-solving, system design, planning.
  Trigger when the user says "用世界模型工作法 / 按 LeCun 那套来做 / 别顺嘴生成，给我规划出来的 / 想清楚再答 /
  objective-driven / plan it, don't just write it", or when a task is complex enough that deliberation
  and comparing alternatives clearly beats a first-draft answer.
---

# 世界模型工作法 (World-Model Method)

**默认的大模型是"一个 token 接一个 token 顺嘴生成"。这个 skill 让 AI 换一种产出方式**——像 LeCun 设想的自主智能那样：先理解情境、定目标，在抽象层预测后果、搜索规划出整条路径，**最后**才渲染成具体产出。

> 一句话区别：产出是**"规划出来的"**，不是**"生成出来的"**。

---

## 什么时候开这个模式

- ✅ **用**：复杂、后果重要、有多条可行方案、值得想清楚的活——写重要文案/方案、做决策、定策略、解难题、设计系统、写关键代码。
- ❌ **不用**：闲聊、查事实、简单改写、赶时间的小活。这是 System-2，慢而稳，杀鸡不必用牛刀。

---

## 核心循环（把 LeCun 的自主智能架构翻成 6 步工作法）

LeCun 在《A Path Towards Autonomous Machine Intelligence》(2022) 里设想的智能体有几个模块：**感知 → 世界模型 → 成本 → 行动者 → 配置器**。把它翻译成你能直接用的步骤：

1. **定目标 + 成本函数（Objective & Cost）**
   先问："成功长什么样？怎么算好/坏？硬约束是什么？" 写下**可衡量的目标**和**要最小化的代价**。没有目标就没有方向感——这正是 LeCun 说大模型缺的东西。

2. **感知 + 建世界模型（Perceive & Model）**
   在抽象层把情境拆成：关键要素、它们的关系、动态怎么变、有哪些约束。理解这件事的"物理规则"。**这一步不产出任何成品。**

3. **预测后果（Predict）**
   生成 **2–4 条候选路径/方案**，对每一条在脑内推演："它会导向什么结果？哪里会崩？代价多大？" 这是世界模型的核心动作——预测行为的后果。

4. **搜索 + 规划（Search & Plan）**
   **不要拿第一个顺手的想法就跑。** 在方案空间里按成本函数比选，挑出整条最优路径。复杂任务**分层**：先定高层骨架，再细化每一步（对应 H-JEPA 的分层规划）。

5. **渲染（Render）**
   到这一步**才**把选中的抽象方案展开成具体产出（文章 / 方案 / 代码 / 决策）。

6. **校验（Verify）**
   对照第 1 步的目标和约束自检。不达标？回到第 3 或第 4 步重来，而不是硬把次品交出去。

---

## 让它区别于普通"想一步步来"的 5 条原则

1. **目标驱动**：永远先有显式的目标 + 成本，再动手。
2. **表征先于细节**：先在概念层规划，别一上来抠字句——这是"预测表征、不预测像素"的工作版。
3. **比选 > 续写**：至少预测并比较 **2 条**路径，而不是顺着第一个想法写到底。
4. **渲染放最后**：成品 = "被选中方案的渲染"，且和规划过程**显式分开**。
5. **硬约束当护栏**：不可逾越的约束在第 1 步就钉死，当架构级护栏，而不是事后补丁。

---

## 默认输出格式

先给一段"规划"，再给成品，让"规划出来的"看得见：

```
【目标 & 成本】成功标准 / 要最小化什么 / 硬约束
【世界模型】关键要素 · 关系 · 动态 · 约束（抽象、精炼，不堆细节）
【候选路径 & 后果预测】
  方案 A → 预测后果 / 代价
  方案 B → 预测后果 / 代价
  （方案 C …）
【选择】选哪条 + 为什么（对照成本函数）
──────── 以下是渲染出的成品 ────────
<具体产出>
【自检】对照目标/约束过没过；不过则指出并修正
```

> 赶时间、或用户只要成品时，可把规划部分压成几行——但**六步不能跳**，区别就在这。

---

---

## 诚实说明

- 这是把 LeCun 的**目标驱动 / 世界模型 / 规划**思路**翻译成提示词层面的工作法**——改的是"**怎么用** AI"，**不是**真的换了 JEPA 神经网络架构。别把它当成"我现在跑的是世界模型"。
- 它拿**深思和比选换速度**：好处是少踩坑、方案更优；代价是慢、啰嗦。值不值，看任务大小。
- 它不保证答案正确，只保证**想得更结构化**——复杂任务里这通常就够把次品挡在门外了。
- 参考：Yann LeCun, *A Path Towards Autonomous Machine Intelligence* (2022)；Meta V-JEPA 2 (2025)。
