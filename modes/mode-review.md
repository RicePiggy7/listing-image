# mode-review.md：审查改稿

参考文件：
- `compliance/platform-constraints.md`
- `compliance/copywriting-rules.md`
- `production/style-blacklist.md`
- `core/prompt-assembly.md`（重生成时）

---

## 流程

### Step 1：接收现有图

接收用户提供的图片路径或上传的图片。确认：
- 目标平台（跨境/国内）
- 是否需要重生成，还是只需要书面诊断

**国内平台告知**（如果平台是淘宝/天猫/京东/拼多多/抖音小店）：

> 检测到目标平台为 [平台名称]。技术预检脚本当前仅覆盖跨境平台，审查结果中的技术规范项请人工参照平台最新规则核对。

**社媒平台告知**（如果平台是 Instagram/Facebook/TikTok 内容侧/YouTube）：

> 检测到目标平台为 [平台名称]，该平台无纯白底 / 产品占比技术预检要求，跳过技术预检，仅执行文案宣称审查；AI 标注合规照常执行。

---

### Step 2：找最严重的一个问题

按以下优先级检查，找出**最严重的一个问题**后停止，不输出完整清单：

1. **D 类合规阻断**：图片是否复刻可识别真人 → 若是，拒绝进行后续重生成，仅告知原因
2. **C 类 AI 人物披露**：图片是否包含写实 AI 人物 → 若是，输出 C 类披露清单（平台 toggle + listing 文案 + 保留 C2PA），不阻断后续流程，继续检查其他问题
3. **平台技术硬规范**（对应 `compliance/platform-constraints.md` Layer 1）：
   - 背景是否为纯白 RGB(255,255,255)
   - 产品占比是否 ≥85%
   - 是否包含不允许的文字/Logo
4. **文案宣称问题**（对应 `compliance/copywriting-rules.md`）：
   - 是否有未经证实的具体数字
   - 是否有医疗/功效宣称
   - 是否有保证性表达
5. **视觉质量问题**（对应 `production/style-blacklist.md` 第四节）：
   - 反 AI 感 8 类特征
6. **品类风格冲突**（对应 `production/style-blacklist.md`）

---

### Step 3：给最小修改方案

只针对 Step 2 识别到的那一个问题，给出：

```
问题：[一句话描述]
位置：[图片中的具体位置或宣称文案]
最小修改方案：[具体操作，不扩大改动范围]
```

不提其他问题，不扩大改动。

---

### Step 4：用户确认后重生成

用户确认修改方案后：

1. 读 `core/prompt-assembly.md` 组装修改后的 Prompt
2. 调用 `scripts/imagegen.sh`
3. 跨境平台：调用 `compliance_check.py` 验证修改是否解决了原问题
4. 交付：新图路径 + 验证结果 + 使用的 Prompt
