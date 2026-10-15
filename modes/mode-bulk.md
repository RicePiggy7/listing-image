# mode-bulk.md：批量/进阶能力

批量任务分两类，策划层适用范围不同。

---

## 批量任务分类

### 编辑型批量（跳过所有策划步骤，包括 FAB）

适用场景：
- 换色 / 换背景（`edit-recolor.json` / `edit-bg-swap.json`）
- 透明抠图（`transparent-cutout.json`）
- 批量翻译文案（`bulk-translate.json`）
- 换季视觉（`edit-seasonal.json`）
- 本地化编辑（`edit-localization.json` / `edit-mask.json`）

逻辑：输入是已有图片 + 编辑指令，不涉及新产品卖点，FAB 过滤没有意义。直接走**场景路由 → Prompt 组装 → imagegen.sh**，跳过 Step 2/3。

Style Lock 处理：
- 原图是套图的一部分 → 复用已有 Lock（从 `campaign-lock-[id].txt` 读取）
- 单图编辑 → 不需要 Lock

---

### 生成型批量（可选 FAB 过滤）

适用场景：
- 爆款换品（`bulk-product-swap.json`）：保留现有套图版式，只换产品
- 产品动图（`motion-gif.json`）：生成 16 格帧图
- 批量社媒图：同一产品，多个平台不同尺寸/风格

逻辑：涉及新产品或新场景。

- 用户**提供了新卖点** → 走 Step 2 证据分级过滤（`planning/evidence-rules.md`）
- 用户**只提供产品描述，无卖点** → 跳过 Step 2，直接场景路由

Style Lock 处理：
- 动图任务（`motion-gif.json`）→ **必须有 Lock**（16 格帧图要保持视觉一致性），无 Lock 时新建
- 换品任务 → 复用原套图的 Lock
- 批量社媒图 → 新建或复用，取决于是否有已有套图

---

## 执行流程（两类共用）

### Step 1：意图识别 + 任务分类

确认：
- 任务类型（编辑型 / 生成型）
- 输入图片路径（编辑型必须）
- 目标平台（决定合规路径）
- 批量数量 / 尺寸需求

**国内平台告知**（如果平台是淘宝/天猫/京东/拼多多/抖音小店）：

> 检测到目标平台为 [平台名称]。技术预检脚本当前仅覆盖跨境平台，批量完成后请人工核对平台主图规范。

**社媒平台告知**（如果平台是 Instagram/Facebook/TikTok 内容侧/YouTube）：

> 检测到目标平台为 [平台名称]，该平台无纯白底 / 产品占比技术预检要求，跳过技术预检，仅执行文案宣称审查；AI 标注合规照常执行。

---

### Step 2：场景路由

根据任务类型匹配 `production/scenarios/` 模板：

| 任务 | 场景模板 |
|------|---------|
| 换色/换背景 | `edit-recolor.json` / `edit-bg-swap.json` |
| 透明抠图 | `transparent-cutout.json` |
| 批量翻译 | `bulk-translate.json` |
| 换季 | `edit-seasonal.json` |
| 本地化 | `edit-localization.json` |
| 换品 | `bulk-product-swap.json` |
| 动图 | `motion-gif.json`（读 `production/motion-gif.md`） |
| 社媒图 | `social-media.json` |

---

### Step 3：Prompt 组装（读 `core/prompt-assembly.md`）

- 编辑型：基于编辑指令组装，无 FAB 映射
- 生成型（有卖点）：走完整 FAB → 5-slot 映射
- 生成型（无卖点）：只填 `subject` + `scene`，`important_details` 留空或填产品基本描述

动图特殊处理：读 `production/motion-gif.md`，为 16 格帧图逐帧组装 Prompt，Lock 注入每帧。

---

### Step 4：批量生成 + 预检

循环调用 `scripts/imagegen.sh`（每次最多 `--count 4`，批量任务按需循环；脚本本身无原生批量模式）。

技术预检（仅跨境平台）：每张图独立运行 `compliance_check.py`，有界回修（单图总计 ≤3 轮）。

AI 标注合规：C 类、D 类全局规则同样适用于批量任务，不因批量而放宽。

---

### Step 5：交付

1. 批量图片路径列表
2. 每张图的技术预检结果摘要
3. 失败图片的具体原因和人工修改建议（如有）
4. 宣称调整说明（生成型批量有卖点过滤时输出）
