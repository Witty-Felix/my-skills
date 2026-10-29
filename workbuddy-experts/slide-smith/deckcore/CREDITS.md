# 第三方来源与许可

## ppt-master（SVG → 原生 PPTX 转换内核）

本专家 `deckcore/scripts/` 与 `deckcore/references/` 中的**转换内核**来自开源项目：

| 项 | 内容 |
|---|---|
| 项目 | ppt-master |
| 作者 | Hugo He |
| 版权 | Copyright (c) 2025-2026 Hugo He |
| 许可 | MIT |
| 仓库 | https://github.com/hugohe3/ppt-master |
| 上游版本 | v6.7.2 |

原许可全文见同目录 [`LICENSE`](./LICENSE)。

### 我们做了什么改动

这份内核**不是原样分发**，而是被拆散后融进本专家：

1. **去掉上游的 skill 打包形态**：删除了上游 `SKILL.md`、`SPONSORS.md`、`SPONSORS_CN.md`，以及强制「必须保持完整官方发行包」的 `attribution_guard.py`。
2. **清除了 10 个入口文件里的完整性自检调用**（`require_skill_integrity`），使脚本可以脱离上游目录结构单独运行。
3. **只需转换能力**：路由、Strategist、`design_spec.md`、`spec_lock.md`、确认页等整套工作流**全部移除**，只保留 `svg_to_pptx` / `svg_quality` / `project_management` 及其依赖。
4. **视觉皮规格**（`references/visual-styles/` 下 2 份）与**表达方法规格**（`templates/styles/` 下 14 份）原样保留，供风格库引用。
5. `references/shared-standards-core.md` 等 SVG 书写契约原样保留，是写页的硬性依据。

### 为什么可以这么做

MIT 许可允许修改、拆分、再分发，**条件是保留版权声明与许可文本**。这两样都在本文件与 `LICENSE` 里。

### 如果你的分发场景需要更保守

把下面这些从备份恢复即可还原成完整上游形态（备份路径见项目记忆）：
`SKILL.md`、`SPONSORS.md`、`SPONSORS_CN.md`、`scripts/attribution_guard.py`，以及 10 个入口文件里的 guard 调用。

---

## 音效词表与索引

`references/…` 之外，若将来恢复 `templates/sounds/`：词表与索引来自 Kenney（CC0-1.0）与 BigSoundBank，许可声明见对应目录的 `CC0-1.0.txt` 与 `THIRD_PARTY_NOTICES.md`。
