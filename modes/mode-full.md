# 端到端模式

1. 执行 `modes/mode-plan.md` Step 1–3：建立证据账本，确定成交驱动力，锁定视觉风格，输出 Storyboard 和逐图执行卡。
2. 在 Step 3 的 **Storyboard 输出后、展开执行卡前**停一次，等待用户确认。用户已说「直接做」或资料充分时跳过；资料充分指商品身份、目标平台、产出范围、关键卖点依据及视觉方向足以执行。已有信息沿用，不重复询问。
3. 完成执行卡及策划自审后，将执行卡、5-slot JSON Prompt、Negative Prompt、风格约束和证据边界传入 `modes/mode-gen.md`，执行 Step 1–4；不重复策划。
4. 合并交付策划方案、图片实际路径与完整 Prompt，并附《自审记录》。无 key 时交付方案和 manual Prompt 包，明确尚未生成图片。
