# Word 纪要生成实现（python-docx）

`word-delivery.md` 只规定排版与验收标准，本文件补充可落地的工程实现，避免每次重新踩坑。

## 运行环境（WorkBuddy 托管隔离环境）

```bash
# 虚拟环境（已存在则跳过创建）
C:/Users/lenovo/.workbuddy/binaries/python/envs/default/Scripts/pip.exe install python-docx -q
# 生成
C:/Users/lenovo/.workbuddy/binaries/python/envs/default/Scripts/python.exe build_minutes.py
```

不要全局 pip install，也不要使用系统 python。

## 必须处理的 5 个坑

1. **中文字体**：`run.font.name = '微软雅黑'` 只改西文。必须给 `w:rFonts` 同时设 `w:ascii`、`w:hAnsi`、`w:eastAsia`，否则 Word 里中文回落成宋体。
   `Normal` 样式也要设 `styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')`。
2. **列宽**：`table.autofit = False` 之后，必须对**每一行的每个 cell** 设 `cell.width`，只设表头行无效。
3. **表头底纹**：python-docx 无 API，需手工插入 `w:shd`（`w:val=clear`、`w:fill=D9E2F3`）到 `w:tcPr`。
4. **表格边框**：内置 `Table Grid` 边框偏黑。使用克制蓝色系，需手工构造 `w:tcBorders`（`w:sz=4`、`w:color=9DC3E6`）逐个单元格写入。
5. **页码**：用 `w:fldSimple`（`w:instr="PAGE"`）追加到 `section.footer.paragraphs[0]`，不要用 `PAGE` 纯文本。

## 风格基线（与 word-delivery.md 对齐）

| 元素 | 取值 |
|---|---|
| 页面 | A4，左右 2.6cm，上下 2.4 / 2.2cm |
| 正文 | 微软雅黑 10.5pt，色 `1F3864`，行距 1.5 |
| H1 | 15pt 加粗 `1F4E79`，段前 16pt |
| H2（阶段标题） | 12pt 加粗 `2E75B6`，段前 12pt |
| H3（内容概述 / 核心观点 / 原话摘录） | 10.5pt 加粗 `1F3864` |
| 原话引用 | 10pt 斜体 `2E75B6`，左缩进 0.9cm，`w:pBdr` 左侧单线 `9DC3E6` |
| 表格 | 表头底纹 `D9E2F3`，边框 `9DC3E6`，9.5pt，垂直留白 1pt，行距 1.25，表头文字色 `1F3864` |
| 页脚（页码） | 色 `8EAADB` |

表格列宽参考（A4 可用宽度 15.8cm）：

- 行动项总表（7 列）：`1.2 / 5.4 / 2.0 / 2.1 / 2.2 / 1.7 / 1.2`
- 待确认事项（5 列）：`1.4 / 4.6 / 2.0 / 5.4 / 2.4`
- 术语核对说明（4 列）：`4.4 / 3.8 / 5.4 / 2.2`
- 会议概览（2 列）：`3.2 / 12.6`

## 导出后必做：回读校验

生成完必须用 python-docx 重新打开校验，不要只靠肉眼：

```python
from docx import Document
import re
d = Document(path)
txt = '\n'.join(p.text for p in d.paragraphs)
for t in d.tables:
    for r in t.rows:
        txt += '\n' + ' | '.join(c.text for c in r.cells)
a = sorted(set(re.findall(r'\bA-\d\d\b', txt)))
r = sorted(set(re.findall(r'\bR-\d\d\b', txt)))
print('表格列数:', [len(t.columns) for t in d.tables])
print('A 缺失:', [f'A-{i:02d}' for i in range(1, N+1) if f'A-{i:02d}' not in a])
print('R 缺失:', [f'R-{i:02d}' for i in range(1, M+1) if f'R-{i:02d}' not in r])
print('阶段数:', len(re.findall(r'阶段[一二三四五六七八九十]+｜', txt)))
print('残留误识别词:', {w: txt.count(w) for w in ['workbody', 'web coding', '发言人3']})
```

校验要点：编号唯一且连续无缺号；表格列数与表头一致；阶段数符合预期；**残留误识别词计数应只在「名称与术语核对说明」表的“原始转写”列出现**，若正文阶段里也出现即说明替换漏了。

补充一条易误报的校验：判断「全文没有全局核心观点 / 金句汇总」时，**不要**用 `^(核心观点|金句)$` 这种全文正则——阶段内的 H3 小标题本就叫「核心观点」「原话摘录 / 金句」，会被误判为汇总章节。正确做法是**只取 H1 / H2 级标题**（按字号 15pt / 12pt 过滤段落）再匹配，命中集为空才算通过。

## 已存在 docx 的就地修订（用户正在预览时）

纪要交付后常被要求改几个专有词。此时**不要重新生成整个文件**——用户往往正在编辑器里预览，磁盘覆盖会与 editor_sdk 实例冲突。改为就地编辑：

1. 加载 `tencent-local-office-edit` 技能，用 `get_pool_status` 拿 `file_id`（优先用宿主注入的 `file_id`）。
2. 正文批量替换：`doc_find_and_replace`（`old_text` / `new_text` / `file_id`）。
3. 表格单元格：`doc_list_tables` 拿 `table_id` → `doc_set_table_cells`（`cells:[{row,col,text}]`，row/col 1-based；不带公共样式时加 `inherit:false`）。实测**仅传 text 不会破坏原有字号 / 字体 / 颜色**，可放心。
4. 删除表格行：`doc_delete_table_row`（table_id + 1-based row）。删多行时**从后往前删**，避免行号漂移。
5. `save_file` 落盘，**不要** `close_file`。

### 连带影响清单（改一个专有词时必须同步四处）

- 正文阶段里的「内容概述 / 原话摘录」文本；
- 行动项总表对应行的待办 / 负责人 / **状态**（原为「待核对」的要改回「待推进」）；
- 待确认事项表——该词对应的 R 行应**整行删除**，随后把剩余 R 编号**从小到大依次重排**保持连续；
- 各阶段末尾「关联事项：…」的编号引用，需同步重排或移除已解决编号。

**重排顺序**：先删除 / 移除旧 R 编号，再按 `R-05→R-03、R-06→R-04…` 从小到大逐个全局替换，目标号均已腾空，不会互相覆盖。

## 同时维护 Markdown 孪生版时的坑

若另外输出 .md（例如供 Obsidian 知识库），**不要用同一套纯文本子串同时替换 docx 和 md**：md 里的 `**关联事项**：` 含加粗标记，`关联事项：` 这个子串在 md 中不匹配，会静默漏替换；而编号重排仍会执行，最终导致编号指向错位。

处理办法：对 md 单独按带标记的真实文本替换（如 `**关联事项**：A-09、…、R-03` → 去掉 `、R-03`），替换后**必须把两份文档的「关联事项」列表归一化后逐条比对**，而不是只比对词频。

## 相对时间的处理

转写稿常只说「明天 / 后天 / 这两天」而不给绝对日期。不要自行换算成具体日期：

- 行动项「截止时间」列写 `会议次日（原文「明天」）`、`会议第三日（原文「后天」）`。
- 会议概览「会议日期」写 `原始记录未明确（转写稿未标注日期；本稿整理时间为 YYYY 年 M 月 D 日）`。
- 在待确认事项里加一条 `R-xx：会议日期未在转写稿中标注`。

## 待办事项 Excel 导出（openpyxl）

生成 .docx 后，立即用**同一份数据源**再导出一份「待办事项.xlsx」，让 Word 与 Excel 永远同步、不重复维护。

### 运行环境

openpyxl 装在与 python-docx 相同的托管 venv 中（见文首「运行环境」节）。如缺失：

```bash
C:/Users/lenovo/.workbuddy/binaries/python/envs/default/Scripts/pip.exe install openpyxl -q
```

### 单一数据源（关键）

在脚本里把两张表的数据抽成模块级变量，Word 的 `table()` 与 Excel 的 `build_excel()` 都读它们：

```python
ACTION_HEADERS = ["编号", "待办事项", "负责人", "截止时间", "预期交付物", "来源阶段", "状态"]
ACTION_ROWS = [ ["A-01", ...], ... ]          # 与 Word 行动项总表同源
R_HEADERS = ["编号", "事项", "当前状态", "需要确认的内容", "来源阶段"]
R_ROWS = [ ["R-01", ...], ... ]               # 与 Word 待确认表同源
table(ACTION_HEADERS, ACTION_ROWS, [...])      # Word
build_excel(ACTION_HEADERS, ACTION_ROWS, R_HEADERS, R_ROWS, XLSX_OUT)  # Excel
```

### build_excel 行为约定

- 工作表 1「待办事项」：表头 = ACTION_HEADERS + 追加一列 `完成时间（跟踪）`（空值，供后续打勾/填日期）；数据行 = ACTION_ROWS。
- 工作表 2「待确认事项」：表头 = R_HEADERS；数据行 = R_ROWS。
- 每个工作表第 1 行是合并的蓝色标题行（微软雅黑加粗 `C_HEAD`）；第 2 行是表头（底纹 `SHADE`=D9E2F3、字体 `C_TEXT`=1F3864 加粗、边框 `BORDER`=9DC3E6）；数据行字体 `C_TEXT`、边框 `BORDER`，编号列居中、其余左对齐；`冻结窗格` 设在 `A3`，`auto_filter` 覆盖表头行到末行。
- 列宽按内容粗设（待办 8 列约 `[7,42,16,18,20,14,10,16]`，待确认 5 列约 `[8,40,12,42,14]`）。

### 导出后必做：回读校验

```python
from openpyxl import load_workbook
wb = load_workbook(XLSX_OUT)
assert wb.sheetnames == ['待办事项', '待确认事项'], wb.sheetnames
ws = wb['待办事项']
assert [c.value for c in ws[2]][:7] == ACTION_HEADERS, '待办表头不一致'
assert ws.max_row == 2 + len(ACTION_ROWS), '待办行数不符'
assert ws.cell(row=2, column=1).fill.fgColor.rgb.endswith('D9E2F3'), '表头底纹应为蓝色'
assert ws.max_column == 8, '待办应含完成时间跟踪列'
ws2 = wb['待确认事项']
assert [c.value for c in ws2[2]] == R_HEADERS
assert ws2.max_row == 2 + len(R_ROWS)
print('XLSX 校验通过')
```

校验要点：工作表名正确、行数与数据源一致、表头底纹为蓝色、待办事项含 8 列（含跟踪列）。
