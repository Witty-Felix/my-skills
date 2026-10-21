# Step 4 · 构建 HTML 放映页

前置：`slidespec.md` 已通过审核，风格已确认。

## 1. 起手

```bash
mkdir -p "<workspace>/ppt/<slug>"
cp "<SKILL_DIR>/references/style-library/<style>.reference.html" \
   "<workspace>/ppt/<slug>/<slug>.html"
```

**从参考实现改，不从零写。** 引擎、HUD、讲稿抽屉、`@page` 全都在里面，重写只会引入 bug。

## 2. 清空内容，保留骨架

删掉所有 `<section class="slide">`，只留：

- `<style>` 全部（组件样式）
- `<div id="stage">`
- `<div class="hud">` 与 `<div class="notes">`
- `<script>` 全部

然后按 `slidespec.md` 一页一页加 `<section>`。

## 3. 每个 section 的结构

```html
<section class="slide s-<原型>" data-note="<讲稿原文>">
  <header class="hd r">
    <p class="kick">PART 01 · 小节名</p>
    <h2 class="ttl">结论式页标题</h2>
  </header>

  <div class="<组件> r">
    ...
  </div>

  <p class="note r"><b>注</b>补充说明</p>
</section>
```

三条硬规则：

1. **`data-note` 必须有**，没讲稿就写空字符串——HUD 会显示「本页无讲稿」，那是提示不是错误。
2. **需要动效的元素加 `.r`（带位移）或 `.rf`（只透明度）**。靠 `transform` 定位的块只能用 `.rf`。
3. **页序即 `slidespec` 顺序**，不重排。

## 4. 原型选择

先看 `slidespec` 的一行「版式」，对照 `style-library/<style>.md` 的「页面原型」表选最接近的那个。
没有完全匹配的：

- 优先**换成最接近的原型**，别发明新组件。
- 实在不行才新增，新增的样式追加到 `<style>` 末尾，类名加前缀防撞。

## 5. 配图

- 默认**不配图**。他要求配才配。
- 生成图（ImageGen）→ 四边**等量**裁 8% 去水印 → 缩到 760–1100 宽。
  ⚠️ 只裁右下会让构图偏心。
- 图片存 `ppt/<slug>/assets/`，HTML 用相对路径引用。
- **不要引第三方图床域名。**
- 图框比例必须等于图片比例，否则 `object-fit:cover` 会裁掉两侧。

## 6. 自检

### 6.1 结构自检（不开浏览器）

```bash
# section 数量
grep -c '<section class="slide' "<slug>.html"
# 每页是否都有 data-note
grep -c 'data-note=' "<slug>.html"
# 是否残留第三方域名
grep -Eoi '<img[^>]+>' "<slug>.html" | grep -Eoi '(https?:)?//[^/"'"'"' ]+' | grep -Eiv 'codebuddy|workbuddy'
```

三项数字对不上就回去改。

### 6.2 视觉自检（必做）

无头 Edge 逐页截图，**一次 4–6 张**，别批量超时：

```bash
"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu \
  --hide-scrollbars --window-size=1280,720 --virtual-time-budget=3500 \
  --screenshot="shot-01.png" "file:///<urlencoded-html>#1"
```

每张图看三件事：

| 看什么 | 不合格的样子 |
|---|---|
| 溢出 | 文字出框、卡片被切、底部压到 HUD |
| 错位 | 该居中的偏左、该对齐的参差、层级颠倒 |
| 呼吸 | 字挤成一团、块贴边、留白被占满 |

**没看过截图不算做完。** 至少看：首屏、末屏、每个章节页、最密的那一页。

### 6.3 翻页自检

键盘 ← → 走一遍，确认：无跳页、无重复、`N` 能开讲稿、`F` 能全屏。

## 7. 可选：上线

只有他明确说「发出去」才做。

```bash
LIB="E:/User_Felix/AI/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library"

# 质量门禁（固定 1280×720 舞台的告警属固有，可 ack）
python "$LIB/page/lint_page_quality.py" --html "<slug>.html" \
  --ack "固定 1280x720 舞台等比缩放，多列栅格位于舞台内部"

# 导入 / 覆盖更新
python "$LIB/page/import_html.py" "<slug>.html"
```

导入后 `data-page-node-id` 会被重写，评论锚点跨版本失效——**改版前先记下当前 nodeId**。

## 8. 交付

```
✅ <slug>.html
📄 　 页 · 风格 <style>
⌨️  ← → 翻页 · N 讲稿 · F 全屏
📁 <绝对路径>
```

再加一句结构说明，≤100 字。
