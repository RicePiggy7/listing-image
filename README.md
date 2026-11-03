# Listing Image

跨境电商 Listing 图端到端生成工具。输入产品资料，输出可直接执行的视觉策划方案和/或图片文件。

---

## 快速开始

配置三个环境变量后即可调用生图：

```bash
export IMAGE_API_BASE="https://api.openai.com"
export IMAGE_API_KEY="sk-xxx"
export IMAGE_MODEL="gpt-image-2.5-flare"
```

无 API key 时用 `--mode manual` 导出 Prompt 包，自行生图。

---

## 工作流

skill 根据用户输入自动选择路径，用户无需指定 mode：

| 信号 | 触发条件 | 路径 |
|---|---|---|
| A | 有执行卡/Prompt，或说「生图」「出图」 | `modes/mode-gen.md` |
| B | 说「策划」「执行卡」「Storyboard」，或只要方案 | `modes/mode-plan.md` |
| C | 有产品资料且要图 / 端到端 / 未分类 | `modes/mode-full.md` |
| D | 有现成图/稿，说「检查」「被拒」「改稿」 | `modes/mode-review.md` |

---

## 文件结构

```
SKILL.md                        # 路由入口 + 开工问卷 + 运行原则
modes/
  mode-full.md                  # 端到端主路径（策划 → 确认 → 生图）
  mode-plan.md                  # 纯策划（证据账本 → 驱动力 → 执行卡）
  mode-gen.md                   # 纯生图（场景路由 → imagegen.sh）
  mode-review.md                # 审查/改稿（六维检查 → 最小修改）
planning/
  evidence-rules.md             # 证据分级规则（已确认/有依据/待补证/禁止）
  conversion-driver.md          # 六类成交驱动力诊断
production/
  scenarios/                    # 39 个场景模板 JSON
  campaign-style-lock.md        # 套图视觉风格锁定协议
  craft.md                      # 生图工艺清单 + 关键失败模式护栏
  funnel-set.md                 # 漏斗槽位定义
  style-blacklist.md            # 品类风格禁忌 + slop 词过滤
  model-routing.md              # 模型选型建议
  motion-gif.md                 # GIF 动图规格
references/                     # 来自 feichanggege/ecommerce-visual-copywriting-skill（MIT）
  output-contracts.md           # 执行卡格式合约
  compliance-rules.md           # 广告法文案规则
  copy-quality-rules.md         # 文案质量自检
  platform-playbooks.md         # 多平台规则参考
  source-notes.md               # 法规/平台规则核验来源（按需加载）
examples/                       # 真实样本（来自 feichanggege）
  README.md
  durian-worked-example.md
scripts/
  imagegen.sh                   # 生图引擎（provider-agnostic，支持 api/manual 双模式）
assets/
  default-style-lock.json       # 无品牌规范时的风格 fallback
```

---

## 平台覆盖

跨境：Amazon / TikTok Shop / Shopify / 速卖通 / Temu / Shopee / Lazada

国内：淘宝 / 天猫 / 京东 / 拼多多 / 抖音小店 / 小红书 / 视频号

---

## 边界

- 不生成 listing 文案文档（标题、五点描述）
- 不做短视频/直播口播话术
- 不自动上架或发布
- 不编造资质、数据、功效或平台规则

