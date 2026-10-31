# mode-full.md：完整流程（套图/Listing 主路径）

参考文件（按需加载，共 8 个）：
- `core/prompt-assembly.md`（Step 4 必读）
- `planning/evidence-rules.md`（Step 2.1）
- `planning/conversion-driver.md`（Step 2.2，驱动力诊断）
- `production/funnel-set.md`（Step 2.2，槽位优先级）
- `production/scenarios/`（Step 4.1 场景路由）
- `compliance/platform-constraints.md`（Step 4.3）
- `production/style-blacklist.md`（Step 4.3）
- `production/campaign-style-lock.md`（Step 3，建 Lock）

---

## Step 1：意图识别（≤1 轮对话）

提取以下信息：
- 产品描述（必须）
- 目标平台 / 市场（必须）
- 参考图路径（有且**无额外卖点** → 直接进 Step 4，跳过 Step 2/3；有参考图**且用户同时提供卖点** → 执行 Step 2.1 证据分级，仍跳过 Step 3）
- 套图张数 / 场景需求（如有）

**国内平台告知**（如果目标平台是淘宝/天猫/京东/拼多多/抖音小店）：

> 检测到目标平台为 [平台名称]。技术预检脚本（白底检测、占比检测、OCR）当前仅覆盖跨境平台（Amazon/TikTok Shop/Shopify/速卖通/Temu），本次任务完成后请人工核对主图规范。

**社媒平台告知**（如果目标平台是 Instagram/Facebook/TikTok 内容侧/YouTube）：

> 检测到目标平台为 [平台名称]，该平台无纯白底 / 产品占比技术预检要求，跳过技术预检，仅执行文案宣称审查；AI 标注合规照常执行。

缺失信息：只追问影响「图的内容」的那一个，其余标假设继续执行。

---

## Step 2：质量护栏（静默执行，不呈现给用户）

### 2.1 证据分级（读 `planning/evidence-rules.md`）

把用户提供的卖点按四种状态分级：

| 状态 | 处理 |
|------|------|
| 已确认 | 保持原意，可进入 Prompt |
| 有依据 | 转利益表达后使用 |
| 待补证 | 改中性表达，删除具体数字 |
| 禁止 | 不进入 Prompt，写入降级记录 |

有卖点被修改或删除时，记录到降级记录，Step 6 交付时输出。

### 2.2 成交驱动力（读 `planning/conversion-driver.md`）

诊断主驱动力（视觉/痛点/参数/信任/情绪）→ 输出驱动力类型 → 映射到 `production/funnel-set.md` 的槽位优先级。

不生成 Storyboard 文档，驱动力结果直接用于 Step 4 的槽位排序。

---

## Step 3：Campaign Style Lock（套图必做）

加载 `production/campaign-style-lock.md`：

- **用户有品牌规范** → 填写 10 字段 Lock
- **无品牌规范** → 读 `assets/default-style-lock.json` + 品类/region 覆盖

→ 输出 Lock 文本，prepend 到每张图 Prompt 开头。

**Lock 持久化**：Step 3 建立的 Lock 文本与 Prompt 一起落盘到工作目录（`campaign-lock-[id].txt`）。用户下次对话说「继续上次的套图」时，读取该文件复用 Lock。

---

## Step 4：Prompt 组装（读 `core/prompt-assembly.md`）

对每张图执行：

**4.1 场景路由**：匹配 `production/scenarios/` 模板关键词，选定场景 JSON。

**4.2 FAB → 5-slot 映射**：按 `core/prompt-assembly.md` 的映射规则组装，冲突优先级：
```
平台强制技术规范 > locked_immutable > style-blacklist > FAB 卖点
```

**4.3 Constraints 槽注入**（四类内容必须全部注入）：
1. 平台技术约束（`compliance/platform-constraints.md` Layer 1）
2. 品类风格冲突（`production/style-blacklist.md` 对应品类行）
3. slop 词过滤（`production/style-blacklist.md` 第二节）
4. 文案宣称边界（待补证替换 + 禁止内容 `do not include` 指令）

**4.4 模型选型**：读场景 JSON 的 `model_hint` 字段（`flare`/`sunburst`），告知用户。场景 JSON 未标 `model_hint` 时默认 `flare`（与 `production/model-routing.md` §五一致：edit 类与质量敏感类模板已在 JSON 标注，未标注场景一律快速模型）。

---

## Step 5：生成 + 预检 + 回修循环

### 5.1 调用 imagegen.sh

```bash
bash scripts/imagegen.sh --prompt "<assembled_prompt>" --mode api
```

### 5.2 技术预检（仅跨境平台）+ 有界回修循环

调用 `scripts/compliance_check.py`，按返回结果执行定向修补：

| 失败原因 | 定向修补策略 | 每种最多轮数 |
|---------|------------|------------|
| `white_bg: fail` | Constraints 强制注入 `pure white background RGB(255,255,255), no gradient, no texture` | 2 轮 |
| `foreground_ratio: fail` | `product_presentation` 改为 `product occupies 90% of frame, fill-frame composition` | 2 轮 |
| `ocr_text: fail` | 删除场景模板 `text_assets` 字段，Constraints 加 `no text, no labels, no watermark` | 2 轮 |

**单图总计 ≤3 轮**（三种失败原因共享该上限，而非各自独立 2 轮）。超限后停止重试，带缺陷交付：当前最佳图 + 具体失败原因 + 人工修改建议。

回修时只改 Constraints 槽和 `product_presentation` 规则，不改 Lock 和 FAB 卖点。

### 5.3 AI 标注合规（Claude 人工判断）

- **A 类**（实拍无人）/ **B 类**（常规修图）→ 无额外操作
- **C 类**（写实 AI 人物）→ 给用户披露清单（平台 toggle + listing 文案 + 保留 C2PA）
- **D 类**（复刻真人）→ 全局规则拦截，拒绝生成，不协商

### 5.4 视觉质量

读 `production/style-blacklist.md` 第四节，执行反 AI 感 8 类特征检查。

---

## Step 6：交付

输出以下内容：

1. 图片文件路径
2. 技术预检结果（pass/fail + violations，仅跨境平台）
3. AI 标注合规提示（C 类时输出）
4. 使用的 Prompt（供用户迭代参考）
5. **宣称调整说明**（仅 Step 2 有降级或拦截时输出）：

```
已调整 N 条宣称以符合证据边界：
- 「原始宣称」→「调整后表达」（原因：[具体原因]）
- 「原始宣称」→ 已删除（原因：[具体原因]）
```
