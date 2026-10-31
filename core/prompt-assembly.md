# Prompt Assembly: FAB → 5-slot 映射规则

每张图的 Prompt 由 5 个槽组装而成。本文件定义映射规则、冲突优先级和完整示例。

---

## 1. 5-slot 结构

```json
{
  "scene": "",
  "subject": "",
  "important_details": "",
  "use_case": "",
  "constraints": ""
}
```

---

## 2. FAB → 5-slot 映射表

| FAB 层 | 承载内容 | 映射到哪个槽 | 组装顺序 |
|--------|---------|------------|---------|
| Feature（产品功能/参数） | 已确认的规格、材质、结构 | `subject`（与产品描述合并） | 第 1 顺位 |
| Advantage（功能优势） | 与竞品/替代方案的差异 | `important_details`（前置） | 第 2 顺位 |
| Benefit（用户收益） | 用户的直接体验、感受、场景 | `important_details`（后置） | 第 3 顺位 |
| Evidence（证据来源） | 认证/检测/工艺/产地 | 见下方路径判断 | 第 4 顺位 |

**Evidence 路径判断**：
- 认证/检测（如「FDA 认证」「ISO 9001」「CE 认证」）→ 进 `constraints` 槽的 verification note
- 工艺/产地（如「手工制作」「意大利进口」）→ 进 `important_details` 槽末尾

**`important_details` 槽组装规则**：线性文本，按 Advantage → Benefit → Evidence（工艺/产地）的顺序拼接，用逗号或句号分隔。

**`scene` 槽来源**：从 `production/scenarios/` 的场景模板 JSON 读取，不来自 FAB。

---

## 3. 冲突优先级

当 FAB 卖点、场景模板约束、Style Lock、平台规范之间发生冲突，按此优先级处理（高优先级强制覆盖低优先级）：

```
平台强制技术规范 > locked_immutable > style-blacklist > FAB 卖点
```

**说明**：平台主图技术规范是外部强制约束，产品过不了技术预检等于白做。品牌 Lock 是内部偏好，必须让位于平台合规。

**具体冲突判断规则**：

1. 如果 `locked_immutable` 写了 `background: warm beige #EDE4D3`，但平台是 Amazon 主图 → 删除该 Lock 项，强制注入 `background: pure white RGB(255,255,255)`

2. 如果 `locked_immutable` 写了 `no additional accessories`，而 Benefit 提到 `comes with extra charging case` → 删除该 Benefit

3. 如果 `style-blacklist.md` 对应品类禁止某风格（如 Electronics 禁止 vintage/retro），而场景模板建议 `vintage feel` → 删除该建议，不带入 Prompt

4. 覆盖 `locked_immutable` 的颜色/背景等值时，Constraints **只写目标值**（如 `pure white background RGB(255,255,255)`），不写「不要 warm cream」式反向指令——图像模型对否定措辞容易泄漏被禁属性；被覆盖的 locked 值不得以任何形式（含 do not use 指令）出现在任何槽位

---

## 4. Constraints 槽必须包含的 4 类内容

每张图的 `constraints` 槽在组装时必须注入以下内容：

1. **平台技术约束**：从 `compliance/platform-constraints.md` Layer 1 查表，按目标平台注入
2. **品类风格冲突过滤**：从 `production/style-blacklist.md` 对应品类行注入禁止风格
3. **slop 词过滤**：从 `production/style-blacklist.md` 第二节注入禁用词列表
4. **文案宣称边界**：「待补证」卖点的中性表达替换结果，「禁止」内容写成 `do not include [内容]` 指令

---

## 5. 完整示例：蓝牙耳机主图

### 输入（产品基础描述 + FAB 四段，含证据等级标注）

- **product_description**（产品基础描述）: 无线头戴式耳机，哑光黑色，铝合金框架
- **Feature**: 蓝牙 5.3 芯片，续航 50 小时，主动降噪【已确认，来自产品规格表】
- **Advantage**: 相比蓝牙 5.0 连接更稳定，续航比同价位产品长 20 小时【待补证：对比数据无来源 → 降级为「同类产品中续航优秀」，不使用具体倍数】
- **Benefit**: 长途旅行无需频繁充电，嘈杂环境也能专注听音乐【有依据，可由参数推导】
- **Evidence**: 通过 CE 认证【已确认】；实验室测试降噪效果 -42dB【待补证：第三方未认证 → 降级为「有效降噪」】
- **target_platform**: Amazon US
- **category**: Electronics

### 降级/拦截记录（Step 2 生成，Step 6 告知）

- 「续航比同价位产品长 20 小时」→「同类产品中续航优秀」（原因：对比数据无来源，待补证）
- 「降噪效果 -42dB」→「有效降噪」（原因：实验室数据未经第三方认证，待补证）

### 输出（5-slot JSON）

```json
{
  "scene": "clean white background, soft diffused studio lighting, centered composition",
  "subject": "wireless over-ear headphones, matte black finish, aluminum alloy frame, Bluetooth 5.3 chipset, 50-hour battery life, active noise cancellation",
  "important_details": "Stable connection compared to Bluetooth 5.0, outstanding battery life among similar products, ideal for long trips without frequent charging, effective active noise cancellation for focus in noisy environments",
  "use_case": "Amazon US main image, target audience: commuters and travelers",
  "constraints": "Pure white background RGB(255,255,255), product occupies ≥85% of frame, no text or logo, no watermark, CE certified. Do not use: stunning, breathtaking, game-changing, revolutionary (slop词). No vintage, no retro style (Electronics品类blacklist). Do not include specific dB noise reduction figures. Do not include battery life comparison claims with specific numbers."
}
```

---

## 6. 模型选型

读场景模板 JSON 的 `model_hint` 字段（`flare` / `sunburst`），建议用户使用对应模型。模型选型完全由场景模板决定，不受驱动力诊断影响。
