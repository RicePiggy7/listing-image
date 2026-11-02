# 纯生图模式

## Step 1：接收输入

接收执行卡（含 5-slot JSON）或用户 Prompt 描述，确认目标平台和输出目录，沿用已有信息。先确定或复用视觉风格，再补充执行细节；不重新开展完整策划。

读取 `references/compliance-rules.md` 核对输入宣称；具体平台规则优先查询官方最新来源，无法核验时标明。生成前识别人物类型：D 类复刻可识别真人，拒绝生成；C 类写实 AI 人物，记录交付时的标注要求。

生图前对照 `production/craft.md`「关键失败模式」检查 Prompt 是否自包含、要素是否齐全、禁止项是否明确；发现问题就地修正。

## Step 2：场景路由

从 `production/scenarios/` 的 39 个场景 JSON 中按关键词和画面任务匹配模板，补充光线、材质表现、构图细节。读取 `production/style-blacklist.md`，将品类禁忌风格和 slop 词注入 Negative Prompt。保留执行卡事实和风格约束，材质仅采用已确认资料；模板示例及平台约束均须核对，不能直接当作商品事实或最新规则。

将风格约束、完整五槽内容和 Negative Prompt 合并为可独立执行的 `prompt.txt`，保存到输出目录。

## Step 3：生图

从项目根目录运行；将下列路径替换为实际路径。API 模式需配置 `IMAGE_API_BASE`、`IMAGE_API_KEY`、`IMAGE_MODEL`，不输出密钥：

```bash
OUTPUT_DIR="<输出目录>" bash scripts/imagegen.sh --mode api --size 1024x1024 --prompt-file "<输出目录>/prompt.txt"
```

有产品参考图时追加 `--image "<参考图路径>"`。无 key 时使用 manual 模式导出 Prompt 包：

```bash
bash scripts/imagegen.sh --mode manual --size 1024x1024 --prompt-file "<输出目录>/prompt.txt" --output "<输出目录>/prompt-pack"
```

以脚本返回的结果和实际文件为准；manual 模式只产出 Prompt 包，不声称已生成图片。

## Step 4：交付

交付图片实际路径（manual 模式交付 Prompt 包路径）及完整 Prompt。检查商品识别、购买理由、证据可见、文案合规、套图一致性，修正不足后附《自审记录》（维度、结论、依据、修正内容）；未完成或无法检查的项目明确注明。

C 类写实 AI 人物另附 AI 标注合规清单：核验目标平台当前披露要求及开关、按要求提供 AI 内容说明、保留 C2PA/SynthID 等来源标记。D 类复刻真人拒绝生成。
