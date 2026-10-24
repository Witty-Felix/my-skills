# 幻灯匠 · 汇报演示制作专家

把资料拆成大纲、逐页分镜与成片演示。四步审核，判断有据，风格可换，**形态三选一**。

## 类型

Agent 型（单个 AI 专家）

## 功能

- **四步门禁**：收料 → 大纲（等审）→ 逐页内容（等审）→ 出页面。不通过不动下一步。
- **偏好库**：把每次取舍沉淀成条目（如「抓大放小」「大纲不写配色」「数据不混批次」），出大纲/分镜前按条目跟用户确认，只问这次碰得到的，最多 6 条。
- **两层记忆**：公共层随包分发；个人层放在本机 `~/.workbuddy/ppt-private/judgments.local.md`，可以写具体项目与真实数据，不会进包、不外发。
- **两套风格库，分开选、也分时问**：**视觉皮** 22 种（本包自带 4 种：`pop-collage` 波普拼贴〔18 屏参考实现 + 14 种页面原型〕、`award-gold` 鎏金颁奖、`cartoon-mascot` 卡通形象、`soft-sticker` 贴纸插画；另含 `ppt-master` catalog 的 18 种：`dark-tech`、`swiss-minimal`、`glassmorphism`、`blueprint`、`data-journalism` …）；**表达方法** 14 种（MBB 咨询、投资人路演、经营回顾、产品发布…）。皮决定长什么样，方法决定怎么论证，两者可任意组合。**表达方法在 Step 1 问（定页序），视觉皮在 Step 4 制作前问（定长相）**——审稿阶段不写颜色，皮早问没有落点。
- **三种产出形态**：HTML 放映页（默认，1280×720 固定舞台，等比缩放，键盘/滚轮/触摸翻页，`N` 看讲稿，`F` 全屏）/ 可编辑 PPTX（PowerPoint 里能继续改）/ 逐页生图 PPTX（每页先用宿主内置生图铺视觉再合成，文字保持原生）。**内容只有一份，出处永远是《逐页内容》。用户说「PPT」就绝不给 HTML。**
- **审稿交 HTML，不交 md**：大纲与逐页内容都产出带排版的 HTML，浏览器打开即终稿形态；**所有产出文件中文命名**（`需求简报.md` / `<项目名>-大纲.html` / `<项目名>-逐页内容.html` / `<项目名>-放映页.html`），一眼看得出是什么。

## 文件结构

```
agents/slide-smith.md              主 Agent：角色、四步铁律、偏好库用法
skills/
  deck-flow/
    SKILL.md                       详细流程与门禁
    references/
      judgment-library.md          ★ 偏好库（越用越准，公共层）
      step4-build.md               构建与自检规范
      visual-library/              视觉风格库（22 种：管长什么样）
        README.md                  视觉索引（本包 4 种 + catalog 18 种）+ 选型 + 生图 prompt 四要素
        pop-collage.md             POP 风格规范（色板/字号阶/组件/页面原型）
        pop-collage.reference.html POP 示例稿（18 屏，脱敏+虚构内容，本地配图）
        assets/                    示例稿用的本地插图
      style-library/               表达方法库（14 种：管怎么论证）
        README.md                  方法索引 + 选型速查
    templates/
      brief.md                     需求简报模板
      大纲模板.html                 大纲审阅模板（中文命名，浏览器直接打开）
      逐页内容模板.html             逐页内容审阅模板（section 结构固定，供 Step 4 取内容）
deckcore/                         SVG → 原生 PPTX 转换内核（已拆散融入，不是 skill）
  scripts/                        转换器 / 质量校验 / 项目管理（493 文件）
  references/                     书写契约 + 18 份视觉皮规格
  sounds/                         音效词表与索引（无音频）
  LICENSE · CREDITS.md            MIT 原许可 + 来源与改动说明
scripts/
  build_pptx.py                    专家主入口：跑 deckcore 出可编辑 PPTX
```

**图标库已移除**：`templates/icons/`（12,029 文件 / 9.8MB）已于 v2.1.1 删除。页面上的图标改用**内联 SVG `<path>`**，导出后是原生可编辑形状（见判断库 J-25）。需要成套图标时用宿主生图出一张 sheet 再切图。

## 关于转换内核（deckcore）

`deckcore/` 是 **SVG → 原生 PPTX 的转换内核**，源自开源项目 [ppt-master](https://github.com/hugohe3/ppt-master)（MIT License, Copyright (c) 2025-2026 Hugo He）。

**它已经被拆散融进本专家，不再是别人的 skill**：

- 删掉了上游的 `SKILL.md`、「必须保持官方发行包」的完整性校验（`attribution_guard.py`），以及 10 个入口文件里的自检调用
- 去掉整套工作流：routing、Strategist、`design_spec.md`、`spec_lock.md`、确认页
- 只留三件事：**写页的契约**（`deckcore/references/shared-standards-core.md`）、**质量校验**、**导出**
- 18 份视觉皮规格与 14 份表达方法规格按用途归位：皮留在 `deckcore/references/visual-styles/`，表达方法移进 `skills/deck-flow/references/style-library/specs/`

MIT 允许修改与再分发，**条件是保留版权与许可**。原许可全文在 `deckcore/LICENSE`，来源与全部改动记在 `deckcore/CREDITS.md`。

调用一律走专家自己的入口：`python scripts/build_pptx.py <workspace> <slug>`。**不要直接调 `deckcore` 里的脚本。**

**分发安全**：上游自带的 `.env` 含作者的真实凭据，**未随包分发**。内置副本的生图已改走宿主 ImageGen，本来就不读它。本机 `~/.workbuddy/skills/ppt-master/` 那份保留原样，需要时可自行配置。

**音效不在包内**：分发副本保留了音效的词表、索引与第三方许可声明（音效规划照常可用），但**不含 186 个 WAV 音频文件**（11.8MB）。音效默认关闭、导出链路本来就不读该目录，所以不影响任何常规产出；确需音效时 `sound_sync.py` 会给出恢复指引。

**两份副本**：内置副本与本机 `~/.workbuddy/skills/ppt-master/` 是各自独立的副本，差异分两类——**12 个文件有本地定制**（10 处生图规则 + 2 处音效说明），外加**本机多 186 个音效 WAV**（分发副本已剔除）。上游升级时由发布者在打包流程里重新同步并重放那 12 处本地定制，包内不带同步脚本。

## 使用示例

- 我有一份资料，想做成一份汇报 PPT
- 先按偏好库出大纲，我审完再动逐页内容
- 用 POP 风格把这批内容做成可编辑的 PPTX
- 这份要做成网页版，别人点链接就能看

## 怎么让它变准

每次你砍掉或修正了什么，它应该自己写回偏好库。
如果发现它没记，直接说：「把这条记进判断库。」

## 关于示例稿

`pop-collage.reference.html` 是一份**脱敏 + 虚构改写稿**：已去掉真实人名、品牌名与机构名，数字也做了替换；后半段「后续规划」为**纯虚构场景**，不对应任何真实计划。

保留下来的是版式、字号阶、组件用法和一套通用的汇报叙事骨架。它只用来演示风格怎么落地，**不要**把里面的成果数字或规划当成真实案例引用。替换内容时从封面改到结尾页即可，样式与交互引擎不用动。

## 头像

头像已放在 `avatars/` 下。替换要求：PNG/JPG，512×512，≤500KB。

## 安装与打包

```bash
python scripts/validate_expert.py <expert-dir>
python scripts/register_expert.py <expert-dir>
python scripts/package_expert.py <expert-dir>
```

这三个脚本位于 WorkBuddy 内置的 `expert-manager` skill 下，**不在本包内**——它们是**发布者打包用**的，终端用户不需要。

运行依赖（Python 库、无头浏览器）开工前实测一遍：`deckcore/scripts/` 的脚本全部随包分发，缺的是本机环境里的 `python-pptx` / `Pillow` 这类库。
