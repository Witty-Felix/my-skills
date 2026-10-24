# 视觉风格库

**这一层只管「长什么样」**：形状语言、装饰密度、留白节奏、字体性格、质感与抬升。
它**不管**论证怎么排、页序怎么走、证据要多硬——那是 `../style-library/`（表达方法）的事。

两者正交，可任意组合：`operating-review` 的骨架 + `dark-tech` 的皮，或者 `mbb-consulting` 的骨架 + `pop-collage` 的皮。

---

## 一、共 22 种

18 种来自转换内核（`deckcore`，源自 ppt-master）的视觉风格 catalog（`../../../../deckcore/references/visual-styles/`），
1 种（`pop-collage`）是本包自带、带完整页面原型与参考实现的原创皮，
1 种（`award-gold`）是按 Style Contract 落地的首发契约皮，
1 种（`cartoon-mascot`）是按 Style Contract 落地的契约皮（2026-10-24，源自 cartoon-mascot 风格规则草案 v0.8），
1 种（`soft-sticker`）是按 Style Contract 落地的契约皮（2026-10-24，从 11 页贴纸插画样张提取，导入 cartoon-mascot 的六条结构纪律）。

### 1.1 本包自带（有完整规范 + 参考实现）

> ⚠️ **机制约定**：所有皮必须遵守 `_style-contract.md`（三层 token / 类名前缀 / 每皮独立 assets+fonts 目录）。
> 新皮按契约落地；`pop-collage` 为存量皮，迁移待办。

| id | 名称 | 适合什么场合 | 一句话内核 | 规格 |
|---|---|---|---|---|
| `pop-collage` | 波普拼贴 | 汇报、复盘、对内宣讲，要有记忆点的场合 | 奶油纸底 + 硬投影 + 贴纸感，强对比、有点吵 | `pop-collage.md` |
| `award-gold` | 鎏金颁奖 | 颁奖典礼、表彰大会、庆功场合 | 深色鎏金氛围 + 金标题/白英文注/黄人名三层节奏，图贴边、文分区 | `award-gold.md` |
| `cartoon-mascot` | 卡通形象风 | 课程/讲座/活动介绍、内轻汇报，需要亲和的场合 | 卡通角色当演员 + 白卡承载信息 + 色板从角色吸附，动作由文案推导 | `cartoon-mascot.md` |
| `soft-sticker` | 贴纸插画风 | 对外宣讲、培训、攻略型内容，要亲和又要成体系 | 蓝紫单色调 + 深色块压信息 + 角色贴纸破框出血 | `soft-sticker.md` |

- 参考实现：`pop-collage.reference.html`（18 屏，可直接改内容复用）；`award-gold.reference.html`（5 屏，虚构内容）；`cartoon-mascot.reference.html`（6 屏，虚构内容）；`soft-sticker` 参考实现待建（规范与 10 类原型已就绪）
- 配图素材：`assets/`（**共享区已冻结，仅供 pop-collage**；award-gold 素材在 `award-gold/assets/`；cartoon-mascot 素材在 `cartoon-mascot/assets/`）

### 1.2 内置 catalog（18 种）

规格文件在 `../../../../deckcore/references/visual-styles/<id>.md`，
索引与分组见同目录 `_index.md`。**这一层不定义 HEX**，色值在制作阶段单独确认。

| 分组 | id | 一句话内核 |
|---|---|---|
| 企业 / 产品 | `swiss-minimal` | 网格锁死、锐利几何、大留白、近乎零装饰 |
| | `soft-rounded` | 圆角卡片、轻抬升、友好节奏 |
| | `glassmorphism` | 磨砂玻璃面板、渐变光、悬浮深度 |
| | `dark-tech` | 深色画布、发光强调、几何精度 |
| | `blueprint` | 深色纸上细线稿、等轴测、工程标注 |
| 编辑 / 出版 | `editorial` | 多栏、细分隔线、衬线/无衬线交错 |
| | `photo-editorial` | 满版影像主导，文字只做点题与图注（无合适图时回退 `editorial`） |
| | `data-journalism` | 多栏密排、微型图表、源注行 |
| | `brutalist` | 报纸密度、粗线框、结构外露 |
| 表现 / 印刷 | `memphis` | 撞色色块、几何彩屑、粗描边 |
| | `zine` | 套色错位、半调网点、有限色板、印刷颗粒 |
| | `vintage-poster` | 五六十年代几何色块、半调、纸感 |
| | `paper-cut` | 层叠纸片、柔和层间投影、手感 |
| 手绘 / 笔触 | `sketch-notes` | 暖纸底、墨线涂鸦、淡彩块 |
| | `ink-notes` | 浅底、黑墨手绘、克制语义色 |
| | `chalkboard` | 深板岩底、粉笔笔触、柔彩点缀 |
| | `ink-wash` | 宣纸留白、笔触、印章点睛 |
| 特殊 | `pixel-art` | 严格像素栅格、块状造型、有限色板 |

> 本包自带的四张皮（`pop-collage` / `award-gold` / `cartoon-mascot` / `soft-sticker`）都带页面原型表；前三张另有参考 HTML，`soft-sticker` 参考实现待建。18 种 catalog 皮只有「视觉语法 + 性格」规范，页面按规范现场生成。

---

## 二、怎么选

1. **先定场合，再定气质。** 给谁看、在哪放、投影还是打印，决定能承受多少密度与装饰。
2. **不要按「好看」选，按「该让听众感到什么」选。** 要稳 → `swiss-minimal` / `mbb` 系；要未来感 → `dark-tech` / `glassmorphism`；要温度 → `pop-collage` / `paper-cut` / `sketch-notes`。
3. **一层只选一个皮。** 一份稿子只允许一套视觉语法，混用会像出自不同的人手。
4. **没指定就问一句。** 别问成考卷——一次问完，用户说「你定」就按场合最贴的选。

### 组合规则

- 皮与骨架**各选一个**，互不影响。
- 走 PPTX 时**不交给任何人**：自己按这份皮的规格写 SVG，表达方法决定页序；引擎只做校验与转换。
- 用户要一个库里没有的皮 → 明说没有，请他给参考（截图 / 网站 / 现有 HTML），**不要现编**。

---

## 三、逐页生图时，风格怎么进 prompt

选定的皮要拆成 prompt 的四个要素，**每页只改「画什么」，不改「怎么画」**——否则 15 页会像出自不同的人手。

| 要素 | 从风格的哪来 | 例子（`pop-collage`） |
|---|---|---|
| 质感 | 调性 | 波普拼贴、剪贴杂志感、贴纸感、有点吵 |
| 色板 | 色板那几个变量 | 奶油底 + 橙 / 钴蓝 / 黄，统一 3px 墨黑描边 |
| 图形语法 | 视觉语法 | 粗描边、硬投影、轻微旋转、半调网点 |
| 构图密度 | 安全区与页面原型 | 大标题占半版，留白大，不塞满 |

**文字不写进 prompt。** 生图只出视觉，页面上要读的字必须是原生文本框（见 J-18）。

---

## 四、加新视觉皮的规矩

1. 必须有一份**真实跑通的 HTML**（不是描述），命名为 `<id>.reference.html`。
2. 写 `<id>.md`，至少包含：调性、色板、字号阶、视觉语法、安全区、组件清单、页面原型、交互、坑。
3. 在本文档 §1.1 加一行；若属于 catalog 家族，则在 `deckcore/references/visual-styles/_index.md` 登记。
4. 不要把新皮塞进旧皮的 md 里——一个文件只管一个皮。

### 出处与许可

18 种 catalog 视觉风格随转换内核（`deckcore`）一同分发，来自开源项目 [ppt-master](https://github.com/hugohe3/ppt-master)（MIT License, Copyright (c) 2025-2026 Hugo He），原许可全文见 `../../../../deckcore/LICENSE`（完整来源见 `../../../../deckcore/CREDITS.md`）。
`pop-collage` 为本包原创。
