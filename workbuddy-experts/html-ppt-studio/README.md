# 幻灯匠 · HTML PPT 制作专家

把资料拆成大纲、逐页分镜和可直接放映的 HTML 演示页。四步审核，判断有据，风格可换。

## 类型

Agent 型（单个 AI 专家）

## 功能

- **四步门禁**：收料 → 大纲（等审）→ 逐页内容（等审）→ 出页面。不通过不动下一步。
- **判断库**：把过往每次取舍沉淀成条目（如「大纲不写配色」「数据不混批次」「过程细节默认不写」），每次出大纲/分镜前按条目跟他确认，只问这次碰得到的，最多 6 条。
- **风格库**：目前沉淀了 `pop-collage`（波普拼贴），带一份 17 屏真实参考实现，可直接改内容复用。后续可继续加风格。
- **产出形态**：只做 HTML 放映页（1280×720 固定舞台，等比缩放，键盘/滚轮/触摸翻页，`N` 看讲稿，`F` 全屏），不产出 PPTX。

## 文件结构

```
agents/html-ppt-studio.md          主 Agent：角色、四步铁律、判断库用法
skills/html-ppt/
  SKILL.md                         详细流程与门禁
  references/
    judgment-library.md            ★ 判断库（越用越准）
    step4-build.md                 构建与自检规范
    style-library/
      README.md                    风格索引
      pop-collage.md               POP 风格规范
      pop-collage.reference.html   POP 参考实现（17 屏）
  templates/
    brief.md / outline.md / slidespec.md
```

## 使用示例

- 我有一份资料，想做成一份 HTML 汇报 PPT
- 先按判断库出大纲，我审完再动逐页内容
- 用 POP 风格把这批内容做成放映页

## 怎么让它变准

每次你砍掉或修正了什么，它应该自己写回 `judgment-library.md`。
如果发现它没记，直接说：「把这条记进判断库。」

## 头像

头像已放在 `avatars/` 下。替换要求：PNG/JPG，512×512，≤500KB。

## 安装

```
C:\Users\Witty-Felix\.workbuddy\plugins\marketplaces\my-experts\plugins\html-ppt-studio\
```

```bash
python scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
python scripts/package_expert.py <expert-dir>
```
