# mode-single.md：单张出图

参考文件（共 3 个）：
- `core/prompt-assembly.md`（Prompt 组装，含 Constraints 槽注入规则）
- `production/scenarios/`（场景路由）
- `compliance/platform-constraints.md`（Layer 1 平台技术约束）

> `production/style-blacklist.md` 的品类冲突和 slop 词规则由 `core/prompt-assembly.md` 在 Step 3 Prompt 组装时按需指引读取；规则本体仍在 `style-blacklist.md`。

---

## 流程（跳过 Step 2/3，直接进 Step 4）

### Step 1：意图识别

提取：产品描述、目标平台/市场、场景需求。

**国内平台告知**（如果平台是淘宝/天猫/京东/拼多多/抖音小店）：

> 检测到目标平台为 [平台名称]。技术预检脚本当前仅覆盖跨境平台，本次任务完成后请人工核对主图规范。

**社媒平台告知**（如果平台是 Instagram/Facebook/TikTok 内容侧/YouTube）：

> 检测到目标平台为 [平台名称]，该平台无纯白底 / 产品占比技术预检要求，跳过技术预检，仅执行文案宣称审查；AI 标注合规照常执行。

**Style Lock 询问**：如果用户说「要和之前的图保持一致」，询问是否有已建的 Lock 文件路径，或是否需要新建一个 Lock。

---

### Step 2：场景路由

匹配 `production/scenarios/` 模板关键词，选定场景 JSON。

---

### Step 3：Prompt 组装（读 `core/prompt-assembly.md`）

按 5-slot 结构组装，Constraints 槽注入：
1. 平台技术约束
2. 品类风格冲突过滤
3. slop 词过滤
4. 如果用户有提供卖点：按证据状态过滤（待补证改中性表达，禁止内容拦截）

模型选型：读场景 JSON `model_hint`，建议对应模型。

---

### Step 4：生成 + 预检

调用 `scripts/imagegen.sh`。

技术预检（仅跨境平台）：调用 `compliance_check.py`，有界回修，单图总计 ≤3 轮，超限带缺陷交付。

AI 标注合规：
- C 类（写实 AI 人物）→ 披露清单
- D 类（复刻真人）→ 全局拦截，拒绝生成

---

### Step 5：交付

1. 图片文件路径
2. 技术预检结果
3. 使用的 Prompt
4. 宣称调整说明（仅有降级时输出）
