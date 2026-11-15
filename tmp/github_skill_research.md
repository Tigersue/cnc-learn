# GitHub 技能调查：走心机学习与识图编程

核查日期：2026-11-04。仅浏览一手 GitHub 仓库及实际技能文件；没有安装技能、下载依赖或执行第三方代码。

搜索包含 `SKILL.md CNC`、`SKILL.md lathe FANUC`、`SKILL.md Swiss-type`、`SKILL.md Tsugami`、`SKILL.md engineering drawing`、`SKILL.md turning machining`。在本次检索范围内，没有找到已核实、能够直接用于津上 S205A/S206A 双通道生产编程的成熟公开 SKILL；这不是断言 GitHub 上绝不存在此类项目。

## 可借鉴的实际 Agent Skills

| 项目与技能 | 许可核查 | 有用之处 | 本项目采用边界 |
|---|---|---|---|
| [earthtojake/text-to-cad：dfm](https://github.com/earthtojake/text-to-cad/blob/main/skills/dfm/SKILL.md)，配套 [CNC/turning 审查参考](https://github.com/earthtojake/text-to-cad/blob/main/skills/dfm/references/cnc.md) | 技能声明 MIT，[根许可](https://github.com/earthtojake/text-to-cad/blob/main/LICENSE)可读 | 以实际几何、材料、刀具和夹持为依据；把可达性、刀柄空间、孔深、螺纹与切断区域分开检查 | 借鉴工艺审查方法。其 CNC 部分没有自动测量器，通用供应商设计建议不能充当津上行程、夹持或切削参数 |
| [ReshefElisha/jarvis-onshape-mcp：vision-decompose](https://github.com/ReshefElisha/jarvis-onshape-mcp/blob/main/skills/vision-decompose/SKILL.md) | [MIT 许可](https://github.com/ReshefElisha/jarvis-onshape-mcp/blob/main/LICENSE)可读 | 先总览、再放大局部，记录特征、尺寸来源、相互关系与疑点，最后检查漏项 | 将方法改写为车削特征表。它服务 Onshape 建模，不是 NC 编程；不引入其专用工具、估图尺寸或每步都确认的固定流程 |
| [Eklavya-San/CTQ-extraction：ctq-extraction](https://github.com/Eklavya-San/CTQ-extraction/blob/main/skills/ctq-extraction/SKILL.md) | [README 末尾声明 MIT](https://github.com/Eklavya-San/CTQ-extraction#license)；根目录独立 LICENSE 链接返回 404 | 区分产品检验要求与工艺要求，原样保留公差，单列无法读清的标注 | 借鉴信息保真原则。它不是图纸尺寸真伪验证器；不复制其符号表，不强制用户阅读 JSON，基准和几何公差解释仍要核对图纸采用的标准版本 |

以上均有实际 `SKILL.md`，不是仅以“技能”命名的一般软件。新技能可原创整合这些工作方法并保留来源链接；未复制其代码、表格或大段文字，因此无需把仓库内容整包带入个人技能。

## 明确不直接采用的两个相似结果

- [text-to-cad：gcode](https://github.com/earthtojake/text-to-cad/blob/main/skills/gcode/SKILL.md)：也是 MIT 的实际技能，但任务是 FDM 打印切片；其打印机、耗材与挤出逻辑不适合车床。不能因为名字叫 G-code 就当作车削程序技能。
- [Claude-skills-for-Computational-Designers：digital-fabrication](https://github.com/marcinfinitesimal533/Claude-skills-for-Computational-Designers/blob/main/skills/digital-fabrication/SKILL.md)：[MIT](https://github.com/marcinfinitesimal533/Claude-skills-for-Computational-Designers/blob/main/LICENSE)，内容面向建筑数字制造和铣削。其通用示例把 G90 用作绝对坐标，不能搬到本项目的车床 G90 循环语境；M6/M9 等通用写法也不能覆盖津上手册。

本地组合应为：个人教学与任务组织技能 → 按需调用现有津上专项技能 → 读取对应机器/控制器原文 → 根据当前图纸与现场数据计算和编程。公开技能提供工作方法，不替代机器代码表和现场条件。
