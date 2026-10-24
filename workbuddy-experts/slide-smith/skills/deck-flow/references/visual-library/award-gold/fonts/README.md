# award-gold / fonts

**本目录不存放字体文件。** 本皮专属字体体积大、授权受限，不随专家包分发；
`award-gold.reference.html` 已改为系统字体栈回落，版式与字号阶不受影响。
需要还原原字形时，按下面清单自行下载安装到本机，再补 `@font-face`。

## 字体清单与获取方式

| 字体 | 体积 | 许可状态 | 获取方式 |
|---|---|---|---|
| 庞门正道粗书体（`PangMenZhengDaoCuShu.ttf`） | 11.1 MB | **个人非商用免费；商用需取得授权**（权利人：庞门正道） | 庞门正道字体发布页，本机安装 |
| 阿里妈妈数黑体 Bold（`AlimamaShuHeiTi-Bold.ttf` / `.woff2`） | 1.3 / 0.6 MB | **免费商用**（阿里巴巴官方发布，以官方发布页条款为准） | <https://fonts.alibabagroup.com/> |

## 没装字体时的回落

参考实现的字体栈已写好回落顺序，直接打开不缺字：

```
--ag-font-display:"庞门正道粗书体","Noto Serif SC","Source Han Serif SC","Songti SC","KaiTi",serif;
--ag-font-body:"阿里妈妈数黑体","Noto Sans SC","PingFang SC",sans-serif;
```

## 使用约束

1. **庞门正道粗书体**：仅限个人学习 / 非商业演示。对外交付、客户提案、商业发布前，必须①购买商用授权，或②替换为已授权字体（推荐 `Noto Serif SC` 900，风格接近且 OFL 免费商用）。**不要把它放进本目录随包分发。**
2. **阿里妈妈数黑体**：可免费商用，但不得单独售卖字体本身；随稿交付时保留本说明。
3. 字体**只允许被本皮引用**（`--ag-font-display` / `--ag-font-body`），其他皮引用即跨皮共享资产，违反 `_style-contract.md` §三。
4. 若替换或补装字体，同步改 `award-gold.reference.html` 的 `@font-face` 与 F 层变量，并在此表更新许可状态。

## 来源

- 庞门正道粗书体：庞门正道字体发布页（商用授权需联系权利人）
- 阿里妈妈数黑体：<https://fonts.alibabagroup.com/>

> 本文件是**发布前必读**：包内不带任何商用授权凭证。字体许可由使用方在交付场景下自行确认。
