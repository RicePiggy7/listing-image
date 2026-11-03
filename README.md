# Listing Image — 电商图智能生成

一句话输入产品资料，输出可直接上架的完整视觉方案：主图 + 场景套图 + 执行卡 + 生图 Prompt，覆盖 Amazon/淘宝/TikTok Shop 等跨境和国内平台。

---

## 能帮你做什么

### 场景 1：新品上架出整套图

**你提供**：产品名称 + 3 张产品照 + 核心卖点（可选）

**我输出**：
- 证据账本（哪些卖点能用、哪些要补证）
- 5-7 张主图 + 场景图的完整方案（Storyboard）
- 每张图的执行卡（画面描述 + 图内文案 + 生图 Prompt）
- 实际图片文件（有 API key 时）或 Prompt 包（无 key 时自己生成）

**适合**：上新频繁的卖家、要快速测试市场的新品

---

### 场景 2：图被拒/差评后诊断修复

**你提供**：现有图 + 平台拒信/差评截图

**我输出**：
- 6 维度问题诊断（转化逻辑/视觉层级/证据合规/平台适配/文案画面一致性/风格漂移）
- 最小必要修改方案（只改有问题的地方）
- 修复后的图片或 Prompt

**适合**：主图被 Amazon 拒审、详情页转化率低需要优化

---

### 场景 3：只要策划方案，不要图

**你提供**：产品资料

**我输出**：
- 完整策划方案（证据账本 + 成交驱动力诊断 + Storyboard + 执行卡）
- 可交给设计师或自己用的 Prompt

**适合**：有自己的设计师团队、只需要视觉策划方向

---

## 如何使用

### 方式 1：通过 Claude Code（推荐）

1. 在 Claude Code 里输入：`/listing-image`
2. 根据提示提供产品资料（或直接说「我要上架这款耳机，Amazon」+ 上传产品图）
3. 等待输出，确认方案后开始生图

### 方式 2：命令行调用（技术用户）

配置环境变量后直接调用生图引擎：

```bash
export IMAGE_API_BASE="https://api.openai.com"
export IMAGE_API_KEY="sk-xxx"
export IMAGE_MODEL="gpt-image-2.5-flare"

bash scripts/imagegen.sh --prompt "你的产品描述" --mode api --size 1024x1024
```

无 API key 时用 `--mode manual` 导出 Prompt 包，自行生成。

---

## 输出什么

**策划层（总是输出）**：
- 证据账本表格（卖点 × 来源 × 状态）
- 成交驱动力结论（视觉/痛点/参数/信任/情感/价格，6 选 1）
- Storyboard（每张图的任务、画面、文案）
- 执行卡（5-slot JSON Prompt + Negative Prompt + 证据来源）
- 自审记录（五维 80 分线，不达标必须重写）

**生图层（有 API key 时）**：
- 主图、场景图、卖点信息图等实际图片文件（PNG）
- 每张图的完整 Prompt 记录

---

## 平台覆盖

**跨境**：Amazon / TikTok Shop / Shopify / 速卖通 / Temu / Shopee / Lazada

**国内**：淘宝 / 天猫 / 京东 / 拼多多 / 抖音小店 / 小红书 / 视频号

---

## 不做什么

- ❌ 不生成 listing 文案文档（标题、五点描述）— 只做图和图内文案
- ❌ 不做短视频/直播话术
- ❌ 不自动上架或发布 — 只输出可直接上传的图片文件
- ❌ 不编造资质、数据、功效或平台规则 — 缺资料时标「待确认」

**A+ 内容边界**：可输出 A+ 策划方案和执行卡，但不能直接生成 A+ 模块图片（尺寸不符合生图引擎规则），需人工排版或等渲染层功能。

---

## 技术细节

<details>
<summary>依赖和配置（点击展开）</summary>

**依赖**：需要 `jq`（JSON 处理工具），macOS `brew install jq`，Linux `apt install jq` 或 `yum install jq`。

**生图引擎**：`scripts/imagegen.sh`（支持 OpenAI GPT-Image-2/2.5，provider-agnostic 设计）

**场景模板**：37 个预置场景（白底主图、场景图、卖点信息图、对比图、包装图、UGC 等）

**知识层来源**：策划方法论基于真实电商案例提炼（证据账本、驱动力诊断、23 条关键失败模式护栏）

</details>

<details>
<summary>文件结构（点击展开）</summary>

```
SKILL.md                        # 路由入口（4 信号）+ 开工问卷
modes/
  mode-full.md                  # 端到端主路径（策划 → 确认 → 生图）
  mode-plan.md                  # 纯策划（证据账本 → 驱动力 → 执行卡）
  mode-gen.md                   # 纯生图（场景路由 → imagegen.sh）
  mode-review.md                # 审查/改稿（6 维检查 → 最小修改）
references/                     # 执行卡格式/合规规则/文案质量/平台规则
examples/                       # 真实完整样本（榴莲干 Listing 套图）
production/scenarios/           # 37 个场景模板 JSON
scripts/imagegen.sh             # 生图引擎
```

</details>

---

**快速上手**：在 Claude Code 里输入 `/listing-image` 开始使用，或查看 `examples/durian-worked-example.md` 了解完整输出样本。
