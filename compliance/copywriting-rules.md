# 文案合规规则（精简版）

本文件只保留影响 Constraints 槽注入的内容。完整的宣称分析框架见 `planning/evidence-rules.md`。

---

## 1. 宣称类型与 Constraints 槽注入规则

| 宣称类型 | Constraints 槽注入方式 |
|---------|----------------------|
| 性能/效果（无来源的精确数字） | `do not include specific performance figures without verified source` |
| 认证/资质（SKU 适用性未确认） | `do not include [认证名称] badge or label` |
| 比较宣称（无统一口径竞品数据） | `do not include direct competitor comparisons` |
| 健康/医疗功效 | `do not include health claims, treatment claims, or medical benefit statements` |
| 绝对化保证（最好/100%/永久） | `do not include superlatives or guarantee language` |
| 价格/稀缺（与实际条件不符） | `do not include pricing claims or scarcity indicators` |

---

## 2. 高风险直接拦截（不进入 Prompt，写入降级记录）

以下宣称直接进入「禁止」状态，不做降级替换，直接拦截：

- 治疗/康复/修复某疾病或症状
- 保证性效果（「100% 有效」「永久保证」「零风险」）
- 虚构认证或奖项
- 虚构销量/评价/排名数据
- 把普通食品写成具有预防或治疗疾病的功效

---

## 3. 待补证宣称的标准替换模式

| 原始宣称类型 | 替换为 |
|------------|--------|
| 具体 dB/% 降噪数据（无第三方认证） | 「有效降噪」/ `effective noise cancellation` |
| 续航比竞品长 N 小时（无来源） | 「续航优秀」/ `long battery life` |
| 3 倍耐用（无测试来源） | 「耐用设计」/ `durable construction` + 材质描述 |
| 提升免疫力（普通食品） | 删除，或改为配料/营养信息描述 |
| 全网最低价（未实时核验） | 删除价格相关宣称 |

---

## 4. AI 标注合规（Constraints 槽注入）

C 类图（写实 AI 人物）的 Constraints 槽中不需要额外注入文案限制，但交付时需要提供披露清单：
- 平台 AIGC 标注 toggle 位置
- Listing 文案合规说明
- 保留 C2PA 元数据提示

---

## 5. 平台规则时效性提示

以下内容通常需要实时核验，本文件按保守原则执行：
- 图片是否允许文字、徽章、人物、场景道具
- 类目资质与禁售规则
- 促销、对比、功效、评价相关限制

无法实时核验时，在交付说明中注明：
> 平台规则未实时核验，以下结果按保守原则执行，上线前请以平台最新官方规则复核。
