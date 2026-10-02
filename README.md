# my-skills

个人 Agent Skills 集合。每个技能遵循 Agent Skills 规范：一个 `SKILL.md` 作为入口（触发条件 + 执行流程），配套 `references/` 存放按需加载的细则文档。

## 技能列表

| 技能 | 说明 |
| --- | --- |
| [`meeting-minutes-professional`](./meeting-minutes-professional) | 会议纪要专业总结。把会议转写稿、原始记录或聊天导出整理为事实忠实、可追溯、可执行的正式中文会议纪要，并按规范导出 Word 文档。含专有词校对、相对时间处理、导出后回读校验与降级处理规则。 |
| [`project-init`](./project-init) | 全局项目初始化：检查并执行 `codegraph init`，并把经验沉淀工作流接入项目级 `AGENTS.md`。 |
| [`experience-capture`](./experience-capture) | 全局经验教训沉淀：经过用户确认后，把已验证、可复用的问题解决方案创建为当前项目的 Skill。 |

## 安装方式

把技能目录整体复制到本机 Agent Skills 目录即可：

- WorkBuddy / CodeBuddy：`~/.workbuddy/skills/`
- Claude Code：`~/.claude/skills/`
- Codex：`~/.codex/skills/`

`project-init` 和 `experience-capture` 是全局 Skill。它们生成的具体项目经验 Skill，默认写入当前项目的 `.agents/skills/<solution-slug>/SKILL.md`，不会自动污染全局 Skill 集合。

## 使用流程

```text
开始处理任意项目
        ↓
调用全局 project-init
        ↓
检查项目根目录是否存在 .codegraph
        ↓
没有 .codegraph → 自动执行 codegraph init
        ↓
确保当前项目 AGENTS.md 接入 experience-capture
        ↓
继续执行项目任务
        ↓
遇到非简单、非显而易见且可复用的问题并解决
        ↓
调用全局 experience-capture
        ↓
判断是否值得沉淀
        ↓
检查当前项目是否已有相同 Skill
        ↓
展示候选 Skill 方案
        ↓
用户确认
        ↓
调用 skill-creator
        ↓
创建或更新当前项目 .agents/skills/<solution-slug>/SKILL.md
```

`project-init` 会自动执行 `codegraph init`，不需要用户确认。`experience-capture` 在创建或修改具体项目 Skill 之前，必须先取得用户确认。

## 目录结构

```
my-skills/
└── meeting-minutes-professional/
    ├── SKILL.md                    # 技能主文件
    └── references/
        ├── minutes-standard.md     # 会议结构、提炼规则、文档模板
        ├── glossary-workflow.md    # 专有词收集与受控校对
        ├── word-delivery.md        # Word 交付、排版与验收
        ├── docx-generation.md      # python-docx 实现与导出校验
        └── degradation.md          # 输入缺失与失败降级
```

## 许可

个人自用，暂未声明开源许可。
