# my-skills

个人 Agent Skills 集合。每个技能遵循 Agent Skills 规范：一个 `SKILL.md` 作为入口（触发条件 + 执行流程），配套 `references/` 存放按需加载的细则文档。

## 技能列表

| 技能 | 说明 |
| --- | --- |
| [`meeting-minutes-professional`](./meeting-minutes-professional) | 会议纪要专业总结。把会议转写稿、原始记录或聊天导出整理为事实忠实、可追溯、可执行的正式中文会议纪要，并按规范导出 Word 文档。含专有词校对、相对时间处理、导出后回读校验与降级处理规则。 |

## 安装方式

把技能目录整体复制到本机 Agent Skills 目录即可：

- WorkBuddy / CodeBuddy：`~/.workbuddy/skills/`
- Claude Code：`~/.claude/skills/`

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
