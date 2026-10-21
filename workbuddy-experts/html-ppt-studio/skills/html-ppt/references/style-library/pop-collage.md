# pop-collage · 波普拼贴

参考实现：`pop-collage.reference.html`（17 屏真实成品，可直接改内容复用）

## 调性

波普艺术的桌面拼贴感：**奶油纸底 + 三块高饱和色 + 3px 墨黑描边 + 硬投影**。
元素带轻微旋转（-1.2° ~ -4°），像贴上去的，不像排上去的。
半调网点当底纹，密度要低（opacity .10–.12），只在留白区出现。

一句话：**像一本被剪开又贴回去的杂志，不是一份 PPT。**

不适合：给外部客户的正装提案、需要极简的场合、数据极密集的分析页。

## 色板

```
--cream   #FFF2E0   纸底（整份主背景）
--paper   #FFFFFF   卡片底（需要跳出来的块）
--orange  #FF4D2E   主强调（编号、竖线、关键词）
--cobalt  #1B1AC9   重块（章节页、末页、需要压场的卡）
--yellow  #FFC93C   贴纸 / 结论条 / 数据高亮
--ink     #111111   描边 / 正文 / 深色页底
```

用法约束：
- **一页最多两个强调色**。橙色和黄色不同页混用会很吵。
- 钴蓝只给"整块"用（整页底、整张卡），不要用来当小色块点缀。
- 黄色专给"要人记住的那一句"（结论条、金句、一等奖）。一页不超过一处。

## 字体

```css
--sans:  "PingFang SC","HarmonyOS Sans SC","Microsoft YaHei","Hiragino Sans GB","Segoe UI",system-ui,sans-serif;
--serif: "Songti SC","Source Han Serif SC","Noto Serif CJK SC","SimSun",serif;
--mono:  "Cascadia Code","JetBrains Mono",Consolas,"SFMono-Regular",monospace;
```

- 正文与标题：`--sans`，标题一律 `font-weight:900`。
- 数字、日期、编号、kicker：`--mono`，`letter-spacing` 加到 .12–.22em。
- `--serif` 在参考实现里基本没用——别为了"书卷气"乱加。

## 字号阶

| 用途 | 字号 | 备注 |
|---|---|---|
| 封面主标题 | 88px / 60px | 两层，`line-height:1` |
| 章节页大字 | 72px | 旋转 -1.6° |
| 章节页背景数字 | 240px | 描边空心，`-webkit-text-stroke` |
| 页标题 | 40px（长标题 34 / 29） | 旋转 -1.7°，`letter-spacing:-.03em` |
| KPI 数字 | 88px | 单位用 `<em>` 降到 20px |
| 大日期 | 104px mono | 黄底 + 描边 + 硬投影 |
| 卡片小标题 | 18–24px | 900 |
| 正文 | 13.5–15px | `line-height:1.6` |
| kicker / 标签 | 10.5–11.5px mono | 全大写 + 宽字距 |

## 视觉语法（四件套）

```css
/* 1. 墨黑描边 */
border:3px solid var(--ink);

/* 2. 硬投影，模糊值恒为 0 */
box-shadow:8px 8px 0 var(--ink);
/* 层级越重，偏移越大：小标签 4px / 卡片 7–9px / 大图 12–14px */

/* 3. 轻微旋转 */
transform:rotate(-2deg);

/* 4. 半调网点 */
background-image:radial-gradient(#111 1.4px,transparent 1.5px);
background-size:10px 10px;opacity:.10;
```

旋转度数别超过 ±4°，超过就像手抖。

## 安全区

```
stage      1280 × 720
左右留白    72px（正文右边界 1208，内容宽 1136）
顶部        44–46px（页眉 kicker 起）
底部        note 固定 bottom:54px
```

所有绝对定位的块都以 `left:72px; width:1136px` 为默认，需要图文分栏时再切。

## 组件清单

### 通用件

| 类名 | 用途 | 关键点 |
|---|---|---|
| `.hd` | 页眉容器 | `left:72 top:44 right:72` |
| `.kick` | 黑底小标签 | 旋转 -3°，宽字距 |
| `.ttl` | 页标题 | 40px/900，旋转 -1.7°，`transform-origin:0 60%` |
| `.note` | 页脚批注 | 左边 4px 橙线，`bottom:54px` |
| `.dots` | 网点底纹 | 只放留白区，别压字 |
| `.stk` | 贴纸标签 | 黄底 + 描边 + 硬投影 |

### 页面原型（14 种，够覆盖绝大多数汇报）

| # | 原型 | 类名 | 什么时候用 |
|---|---|---|---|
| 1 | 封面 | `.cv__*` | 左文右图，图带白框 + 14px 投影 + 2.1° 旋转 |
| 2 | 目录 | `.toc__c` / `.toc__c--b` | 双栏卡，右卡钴蓝底、上移 10px 制造错位 |
| 3 | 章节页 | `.part` / `.part--ink` | 满版色 + 240px 描边数字 + 72px 标题 + 引言 |
| 4 | KPI 三宫格 | `.kpi__c` / `--o` `--c` `--y` | 三个数字，卡依次下移 0/22/44px |
| 5 | 时间轴 | `.tl__bar` `.tl__i` `.tl__n` | 5 个点以内，右侧接一个"下一步"块 |
| 6 | 导师/角色卡 | `.mt__c` | 三列，中间那张上移 12px |
| 7 | 双列清单 | `.grid2` `.wk__i` `.wk__a` | 15 条以内；超过就拆页 |
| 8 | 通栏清单 | `.grid2--wide` | 10 条以内，行高更大 |
| 9 | 日期 + 正文行 | `.row__d` (196px) `.row__b` | 3–4 行，日期栏黑底黄字 |
| 10 | 大日期 + 网格 | `.pk__big` `.pk__tiles` | 左边一个时间锚点，右边 2×2 卡片 |
| 11 | 对比小结 | `.sum__r` `.sum__k` `.sum__f` | 两行对比 + 底部三块流程条 |
| 12 | 编号条目 | `.pn__i` `.pn__n` | 2 条最舒服，3 条要 `--tight` |
| 13 | 奖励 / 阶梯 / 系统图 / 金字塔 | `.aw__c` / `.lad__s` / `.sys__c` / `.pyr__t` | 有"关系"要表达时用图，不用文字 |
| 14 | 结尾 | `.end__*` | 满版钴蓝 + 金句 + NEXT 步骤条 + 谢谢 |

## 交互引擎

固定在参考实现底部 `<script>` 里，**原样保留，不要改**：

- `#stage` 1280×720，`transform-origin:center`，`fit()` = `min(vw/1280, vh/720)`
- `.slide.is-active` 控制显隐，`opacity` 过渡 .42s
- 键盘：← → ↑ ↓ Space Enter 翻页，Home/End 跳首尾，`F` 全屏，`N` 讲稿
- 滚轮翻页带 520ms 锁；触摸左右滑 50px 触发
- 讲稿从 `data-note` 读取，按 `N` 从底部抽屉弹出
- URL `#n` 直达第 n 页

入场动画两个类：
- `.r` — 带位移（`translateY(14px)` → `none`），按兄弟序号错开 60ms
- `.rf` — 只动 opacity

## 坑（都是踩过的）

1. **`.r` 会覆盖 `transform`**。任何靠 `translateX(-50%)` 居中的块（金字塔、错位卡），必须用 `.rf`，否则整块错位。
2. **选择器要写在 section 的真实类名上**。`.kpi .note{}` 不命中 `s-kpi`，`.note` 会落回静态位置跑到页顶。兜底统一写 `.note{position:absolute;bottom:54px}`。
3. **240px 描边数字会和引言互撞**。数字固定 `bottom:-56px`，引言必须放 `top:382px`。
4. **封面画框比例必须等于图片比例**，否则 `object-fit:cover` 会裁掉两侧。参考实现是 612×416（内框 588×392 ≈ 3:2）。
5. **不要引第三方图片域名**，会卡导入与离线打开。要么本地图，要么已授权直链。
6. **无头截图一次别超过 6 张**，18 张会超时。

## 改内容时改哪里

| 要改 | 改哪 |
|---|---|
| 文案 | 各 `<section>` 里的文字节点 |
| 页数 | 增删 `<section class="slide">`，HUD 计数自动跟随 |
| 讲稿 | 对应 section 的 `data-note` |
| 配色 | `:root` 里 6 个变量 |
| 新增页面类型 | 在 `<style>` 末尾追加 `.xxx` 块，参考已有原型的定位数值 |

## 打印

参考实现带 `@page{size:1280px 720px;margin:0}`，浏览器打印即一屏一页，可直接存 PDF。
