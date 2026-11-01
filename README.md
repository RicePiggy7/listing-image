# Listing Image

![hero](assets/hero.png)

跨境电商 Listing 套图生成工具。输入产品信息，自动完成策划分析、Prompt 组装和合规检查，调用图片接口输出可直接使用的电商图片素材。

---

## 功能概览

**套图生成**：从产品信息出发，生成完整 listing 套图——主图、场景图、细节图、对比图。适合亚马逊、Shopify 等跨境平台上新。

**单张出图**：描述具体需求直接生成，不走完整套图流程。适合补图、测试风格、快速验证。

**审查改稿**：上传现有图片，找出最严重的问题并给出最小修改方案。

**批量编辑**：换背景、换颜色、换产品、抠图、GIF 动图等批量任务。

---

## 工作原理

### 策划层自动执行

用户只需描述产品，工具在内部完成成交驱动力分析、证据账本整理、FAB 过滤和 5-slot Prompt 组装，不需要手动经历这些步骤。相关规则定义在 `core/prompt-assembly.md` 和 `planning/`。

### 合规提前分流

任务开始时就判断目标平台（跨境 / 国内 / 社媒），三条合规路径从此独立处理。图片技术规范和 AI 标注要求在 `compliance/platform-constraints.md`，文案宣称审查规则在 `compliance/copywriting-rules.md`。

### 全局合规红线

所有路径强制执行：D 类拦截（复刻可识别真人）、不剥离 C2PA 元数据、不教唆规避 AI 标注要求、不造假实拍。

### 39 个场景模板

`production/scenarios/` 内置 39 个场景模板 JSON，覆盖主图、场景图、细节、对比、GIF、A+ 模块、直播图、节日活动等类型，开箱即用。

---

## 输出通道

**API 模式（默认）**：产品图和参考图上传到 `IMAGE_API_BASE` 配置的端点，直接返回生成结果。使用前确认端点的数据保留和隐私条款，只上传有权使用的素材。

**Manual 模式（`--mode manual`）**：导出完整 prompt 包，不上传任何内容。适合数据敏感场景，或在其他工具里手动生成。

---

## 文件结构

```
listing-image/
├── SKILL.md                        # 入口路由（≤80 行）
├── modes/
│   ├── mode-full.md                # 完整流程：套图 / Listing
│   ├── mode-single.md              # 单张出图
│   ├── mode-review.md              # 审查改稿
│   └── mode-bulk.md                # 批量 / 进阶能力
├── core/
│   └── prompt-assembly.md          # FAB→5-slot 映射规则 + 完整示例
├── planning/
│   ├── conversion-driver.md        # 成交驱动力诊断
│   └── evidence-rules.md           # 证据账本规则
├── production/
│   ├── scenarios/                  # 39 个场景模板 JSON
│   ├── craft.md
│   ├── model-routing.md
│   ├── motion-gif.md
│   ├── style-blacklist.md
│   ├── funnel-set.md
│   └── campaign-style-lock.md
├── compliance/
│   ├── platform-constraints.md     # 跨境图片技术规范 + AI 标注
│   └── copywriting-rules.md        # 文案宣称审查
├── scripts/
│   ├── imagegen.sh                 # 出图脚本（api / manual 双通道）
│   └── compliance_check.py         # 主图技术预检（白底 / 占比 / OCR）
├── assets/
│   └── default-style-lock.json     # 默认风格锁（10 字段 + 品类覆盖）
└── evals/
    ├── trigger-evals.json          # Step 0 路由 golden cases（18 条）
    └── fab-mapping-evals.json      # FAB→5-slot 映射 golden cases（6 条）
```

---

## 质量基线

| 指标 | 目标值 |
|------|--------|
| Amazon 主图预检一次通过率 | ≥85% |
| 套图任务零追问完成率 | ≥70% |
| 单次调用加载参考文件数 | mode-single ≤5，mode-full ≤10 |
| FAB→5-slot evals 通过率 | 100% |

---

## 不覆盖的范围

- 视频剪辑、短视频脚本
- 广告投放策略
- 图片压缩、格式转换
- 纯 SEO / 关键词研究
- 发布到平台（只到素材交付）
- 复刻可识别真人（D 类，主动拦截）
- 国内平台图片技术预检（Step 1 有提示，需人工核对）
- edit 类模板的 `ref_roles` / `text_assets` preserve 注入未实现；有参考图时 mode-full 会自动走 img2img/edits 通道并强制提取材质结构特征，但形态保真仍依赖端点能力，交付前需人工比对
