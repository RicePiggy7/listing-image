# E-Commerce Visual

给跨境电商卖家提供端到端出图能力，出图质量达到专业电商设计师水准。

> ⚠️ **数据隐私提示**
> API 模式会把产品图和参考图上传到你配置的端点（`IMAGE_API_BASE`）。请只使用你有权上传的素材，并先确认端点的数据保留与隐私条款。
> 如对数据敏感，使用 manual 模式（`--mode manual`）导出 prompt 包，不上传任何内容。

---

## 快速上手

在 Claude Code 里直接描述你的产品和目标平台，Skill 会自动路由到正确的模式：

- **套图 / Listing 任务** → 完整 6 步流程（主路径）
- **单张快速出图** → 跳过策划层，直接生成
- **审查现有图** → 找最严重的一个问题 + 最小修改方案
- **批量/动图/换品/换色/抠图** → 编辑型或生成型批量流程

---

## 文件结构

```
ecommerce-visual/
├── SKILL.md                        # 入口路由（≤80 行）
├── modes/
│   ├── mode-full.md                # 完整流程：套图/Listing
│   ├── mode-single.md              # 单张出图
│   ├── mode-review.md              # 审查改稿
│   └── mode-bulk.md                # 批量/进阶能力
├── core/
│   └── prompt-assembly.md          # FAB→5-slot 映射规则 + 完整示例
├── planning/
│   ├── conversion-driver.md        # 成交驱动力诊断
│   └── evidence-rules.md           # 证据账本规则（精简版）
├── production/                     # 场景模板与生产方法论
│   ├── scenarios/                  # 39 个场景模板 JSON
│   ├── craft.md
│   ├── model-routing.md
│   ├── motion-gif.md
│   ├── style-blacklist.md
│   ├── funnel-set.md
│   └── campaign-style-lock.md
├── compliance/
│   ├── platform-constraints.md     # 跨境图片技术规范 + AI 标注
│   └── copywriting-rules.md        # 文案宣称审查（精简版）
├── scripts/
│   ├── imagegen.sh                 # 出图脚本（api / manual 双通道）
│   └── compliance_check.py         # 主图技术预检（白底 / 占比 / OCR）
├── assets/
│   └── default-style-lock.json     # 默认风格锁（10 字段 + 品类覆盖）
└── evals/
    ├── trigger-evals.json          # Step 0 路由 golden cases（18 条）
    └── fab-mapping-evals.json      # FAB→5-slot 映射 golden cases（5 条）
```

---

## 设计原则

**策划层后置，不暴露给用户**：证据账本、成交驱动力、FAB 过滤在 Prompt 组装时自动执行，不是用户需要经历的步骤。

**合规先分流**：Step 0 路由时就判断平台（跨境/国内/社媒），三套合规路径从此分开，不在生成后才补。

**生产层即拿即用**：`production/`、`scripts/`、`assets/` 是稳定的生产资产——39 个场景模板、出图脚本、技术预检、风格锁均已就绪。本套件的增量是把证据账本和 FAB 转化逻辑注入 Prompt 组装步骤，形成从策划到出图的完整链路。

**全局合规红线（所有路径均强制）**：D 类拦截（复刻真人）+ 三不红线（不剥离 C2PA、不教唆规避 AI 标注、不造假实拍）。

---

## 成功指标

| 指标 | 目标值 |
|------|--------|
| Amazon 主图预检一次通过率 | ≥85% |
| 套图任务零追问完成率 | ≥70% |
| 单次调用加载参考文件数 | mode-single ≤3，mode-full ≤6 |
| FAB→5-slot evals 通过率 | 100% |

---

## 范围边界（Out of Scope）

- 视频剪辑、短视频脚本
- 广告投放策略
- 图片压缩、格式转换
- 纯 SEO/关键词研究
- 发布到平台（只到素材交付）
- 复刻可识别真人（D 类，主动拦截）
- 国内平台图片技术预检（Step 1 已告知，需人工核对）
- edit 类模板的 `ref_roles` / `text_assets` preserve 注入未实现；编辑型任务的产品保真依赖 prompt 措辞，非自动保障
