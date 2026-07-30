<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Trellis Workflow Enhancer：将 Trellis 工作流、经核验的 Matt 与 Waza 能力转为由用户选择的可选增强项。">
</p>

[English](./README.md)

# Trellis Workflow Enhancer

一个用于增强既有 Trellis 工作流的可选 skill，不会把流程控制权交给另一套框架。它先盘点目标仓库，核验本地已安装及上游最新的 Matt Pocock 和 Waza skill 能力，再给出增强前后的对比表。用户未选择前，不会修改任何内容。

## 首次运行产出

首次运行只做分析，会提供：

- 来自 Trellis 配置、工作流、规范、任务和真实校验命令的证据；
- 本地与上游 skill 的当前证据，不会静默更新任一 skill；
- 包含收益、成本、风险、前置条件和精确影响文件的增强对比；
- 与每个建议并列的 `N0`「不变更」选项。

## 增强前后

| 增强前 | 选择增强后 |
| --- | --- |
| 通用建议可能忽略仓库实际结构 | 根据真实 Trellis 解析器和模块根目录明确包与规范范围 |
| 产品或领域决策不清晰时，规划深度不足 | 通过已核验的深度决策路径澄清，并将结论写回 Trellis 任务产物 |
| 测试、诊断和手工检查混在一起 | 命名明确的反馈闭环；只在真实测试接缝使用 TDD，修复前先复现问题 |
| 所有改动承担相同的审查成本 | 仅对已定义的高风险改动进行独立审查 |
| 视觉工作可能脱离工程计划 | Waza 的视觉探索将状态和验收条件回写到 `design.md` |
| 因 skill 流行度决定是否集成 | 由观察到的缺口、明确的取舍和用户选择的 ID 决定 |

## 工作方式

1. **盘点**：读取目标仓库的 Trellis 文件、任务状态、规范、代码结构和可执行校验入口。
2. **核验**：检查已安装的 Matt/Waza skill，并在只读模式下与官方上游来源比对。
3. **对比**：展示紧凑的 `ID | 增强前 | 可选增强后 | 收益 | 成本` 表格，其中包含 `N0` 不变更选项。
4. **选择**：等待用户选择具体 ID、组合或不变更。
5. **应用**：仅实施被选中的项目级集成，并使用仓库实际工具验证。

Trellis 始终负责任务生命周期、包范围、规范加载与验收证据。不会把 Matt 或 Waza 的内容复制进项目，也不会将它们视作竞争性的任务管理系统。

## 安装

```bash
npx skills@latest add lei1024/trellis-workflow-enhancer
```

## 使用

```text
使用 $trellis-workflow-enhancer 检查这个仓库的 Trellis 工作流，
对照最新已核验的 Matt 和 Waza skill，先展示可选增强项，再修改任何文件。
```

## 可选组合

| ID | 组合 | 常见触发条件 |
| --- | --- | --- |
| S1 | 范围与规范 | 多根代码库、陈旧模板或归属不清 |
| D1 | 决策与知识 | 产品规则、领域术语、UX 状态或模块归属不清 |
| F1 | 反馈与诊断 | 行为变更、缺乏信心、缺陷或性能回归 |
| R1 | 独立审查 | 共享模块、鉴权、迁移、公开契约或高风险 UI 路径 |
| V1 | 视觉迭代 | UI 行为、信息层级、响应式状态或依赖截图验证的改动 |
| H1 | 工作流健康度 | 非简单仓库需要一次只读的可维护性审计 |
| N0 | 不变更 | 现有 Trellis 工作流已经适配该仓库 |

目录与对比模板刻意保持通用。skill 会移除没有得到目标仓库和上游能力证据支持的行，而不是向每个仓库强行套用全部组合。

## 安全边界

- 未得到明确的选项选择前，绝不修改目标仓库。
- 未核验上游来源前，绝不把本地已安装 skill 称为最新版本。
- 绝不自动安装或更新 Matt、Waza、Trellis、全局设置或 hook。
- 不会因增强建议而修改 `.gitignore`、暂存、提交、推送、归档任务或改写历史。
- 不会臆造测试命令；缺少测试或手工验证时会明确说明。
- 不会在对比报告或持久化的本地文档中暴露密钥、私有 URL、用户数据或内部基础设施信息。

## 上游来源

skill 以官方 [Matt Pocock skills 仓库](https://github.com/mattpocock/skills) 和 [Waza 仓库](https://github.com/tw93/Waza) 作为只读上游来源。由于两个目录都会独立变化，skill 会在每次分析时核验名称和版本。

## 仓库结构

```text
trellis-workflow-enhancer/
├── SKILL.md
├── README.zh-CN.md
├── agents/openai.yaml
├── assets/readme/hero.svg
└── references/
    ├── comparison-template.md
    └── integration-catalog.md
```

## 许可证

[MIT](./LICENSE)
