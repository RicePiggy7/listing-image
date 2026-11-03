# 纯策划模式

只交付可直接执行的视觉方案，不调用生图。沿用用户已提供的平台、市场、产品资料和产出范围，缺失信息列入稿外待确认清单。

## Step 1：建立证据账本

读取 `planning/evidence-rules.md`，逐条标注卖点：已确认 / 有依据 / 待补证 / 禁止。用户口述、视觉观察和推测分别记录，不当作检测或资质证明；降级表达同样需要事实支持。

输出证据账本：

| 卖点/宣称 | 来源类型及文件/图号/URL | SKU/市场/条件/日期 | 状态 | 最终表达或处理 | 待确认事项 |
|---|---|---|---|---|---|

仅将已确认和有依据的内容用于最终文案及 Prompt；待补证内容删除或改为已有资料支持的中性表达，禁止内容排除并记录原因。

## Step 2：判断成交驱动力

读取 `planning/conversion-driver.md`，从以下六类中选择 **1 个主驱动力，最多 1 个辅驱动力**，说明选择依据和视觉重点：

- 视觉/质感
- 痛点/效率
- 理性/参数
- 信任/证据
- 情绪/身份
- 价格/组合/促销

原参考文件只有五类，本步骤补充第六类：**价格/组合/促销**。触发条件为用户提到活动价、套装、赠品、满减或限时；视觉重点为到手内容、单件或组合价、优惠条件、活动时间。价格和促销条件须有来源，缺失时不编造。

## Step 3：输出 Storyboard + 执行卡

1. 读取 `production/campaign-style-lock.md`，先确定视觉风格；套图建立或复用 Campaign Style Lock，单图确定本张风格。每条 Prompt 完整包含适用的风格约束。
2. 读取 `references/platform-playbooks.md` 的对应平台段落、`references/copy-quality-rules.md` 和 `references/compliance-rules.md`，分别核对文案与合规。平台策略建议不作为现行硬规则；具体要求优先核验官方最新来源，记录来源及核验日期。
3. 读取 `references/output-contracts.md`，按其中格式输出 Storyboard，再为每张图提供一张完整执行卡，保留任务、画面、图内文案、最终文字层、排版、证据来源和禁止项。Storyboard 张数按信息量和需求确定。同时读取 `production/style-blacklist.md`，将品类禁忌风格和 slop 词注入每张执行卡的 Negative Prompt。格式与详略基准见 `examples/durian-worked-example.md`。
4. 每卡提供可单独使用的 **5-slot JSON Prompt**，键名为 `scene`、`subject`、`important_details`、`use_case`、`constraints`；另列 **Negative Prompt**。写全产品身份、已确认结构/材质、光线、构图、文字留白与风格约束，不使用"同上"。待确认内容仅列在稿外，不进入最终文字层或可执行 Prompt。

### 5-slot 组装规则

- **FAB 映射**：Feature → `subject`；Advantage → `important_details` 前置；Benefit → `important_details` 后置；认证类 Evidence → `constraints` 的 verification note；工艺/产地类 → `important_details` 末尾（工艺与产地关键词必须保留，如 handcrafted、hand-woven、Vietnam，不得省略或改写）。
- **待补证卖点**：降级为中性表达（删数字/倍数，改方向性描述），并在 `constraints` 逐字写入对应标准 do-not-include 短语。
- **禁止状态**：相关内容不得出现在任何槽位；`constraints` 必须逐字使用标准短语。健康/医疗功效宣称必须同时包含 do not include treatment claims 与 do not include medical benefit。
- **`constraints` 四类必填**：① 平台技术约束（如 pure white background RGB(255,255,255)、product occupies ≥85% of frame）；② 品类禁用风格用 no + 关键词逐项列出（Electronics 品类必写 no vintage, no retro）；③ slop 禁用词用 do not use + 词列表；④ 宣称边界用上述 do-not-include 标准短语。
- **冲突优先级**：平台强制技术规范 > locked_immutable > style-blacklist > FAB 卖点。被平台规范覆盖的 locked 颜色/背景值不得残留在任何槽位（包括 `scene` 与 `use_case`）；覆盖时 `constraints` 只写目标值（如 pure white background RGB(255,255,255)），不得以「不要 X」式反向指令复述被覆盖值——图像模型对否定措辞易泄漏被禁属性。
- **`subject` 槽是产品结构事实**：忠实转写商品资料给出的结构细节，不得改写。

端到端模式在 Storyboard 后按 `mode-full.md` 判断是否需要确认，再继续执行卡；纯策划模式连续完成本步骤。

交付前按以下五维逐张自审，本模式以此表替代输出模板中的旧评分维度。分数以必要条件为锚点：必要条件有任一条不满足，该维度封顶 79 分，必须重写，最多 2 轮。缺证无法完成的内容只列为阻断项，不标成最终稿。尚未生图的项目只审查方案，不声称成图已验收。

### 自审记录

| 维度 | 分数 | 依据（一句话，写明满足了哪些必要条件） | 重写了什么 |
|---|---|---|---|
| 证据与合规 |  | 每条宣称可追溯、无待补证写成事实、无占位符 |  |
| 转化逻辑 |  | 每张图独立决策任务、Top 3 购买理由清楚、商品名称已解决、文案通过质量自检 |  |
| 视觉层级 |  | 第一视觉落点明确、文字不超规格上限、产品主体占比合理 |  |
| 一致性 |  | 按 Style Lock 执行、产品身份与参考图一致、同套图字体和语气一致 |  |
| 可执行性 |  | Prompt 自包含（结构/材质/光线/构图/留白/禁止项）、每卡有文字渲染方式和文案规格自检 |  |

- 重写轮次：0 / 1 / 2
- 未达标项：无（或写明维度、原因、需要的资料）

交付前对照 `production/craft.md`「关键失败模式」逐条检查；发现问题就地修正，不跳过。

最终交付：证据账本、驱动力结论、视觉风格、Storyboard、逐图执行卡与完整 Prompt、《自审记录》及稿外待确认/阻断清单。
