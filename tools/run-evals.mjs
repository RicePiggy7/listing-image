#!/usr/bin/env node
// skill 侧 evals 跑测器（M3 验收 P2）：
//   trigger 18 条 = 信号路由（signal/route）+ 平台分流（platform_path/notice）
//   FAB 6 条 = 生产知识集（INTEGRATION.md §5 的 6 文件映射）下的 5-slot 映射断言
// 用法：node tools/run-evals.mjs   （LLM 配置读 ../piggy-workbench/.env）
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const ENV = (() => {
  try {
    return fs.readFileSync(path.resolve(REPO, "..", "piggy-workbench", ".env"), "utf8");
  } catch {
    return "";
  }
})();
const envGet = (k) => process.env[k] ?? ENV.match(new RegExp(`^${k}=(.*)$`, "m"))?.[1];
const BASE = envGet("CLIPFORGE_LLM_BASE_URL");
const KEY = envGet("CLIPFORGE_LLM_API_KEY");
const MODEL = envGet("CLIPFORGE_LLM_MODEL");

async function llm(system, user) {
  const r = await fetch(`${BASE.replace(/\/$/, "")}/chat/completions`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${KEY}` },
    body: JSON.stringify({
      model: MODEL,
      temperature: 0,
      reasoning_effort: "low",
      messages: [
        { role: "system", content: system },
        { role: "user", content: user },
      ],
    }),
  });
  const j = await r.json();
  if (!r.ok) throw new Error(`LLM ${r.status}: ${JSON.stringify(j).slice(0, 200)}`);
  return j.choices[0].message.content.replace(/```json|```/g, "").trim();
}

const skill = fs.readFileSync(path.join(REPO, "SKILL.md"), "utf8");
const triggerEvals = JSON.parse(fs.readFileSync(path.join(REPO, "evals", "trigger-evals.json"), "utf8"));
const fabEvals = JSON.parse(fs.readFileSync(path.join(REPO, "evals", "fab-mapping-evals.json"), "utf8"));

// ===== 生产知识集（与 piggy-workbench A2 加载器 full 模式映射一致）=====
const KNOWLEDGE_FILES = [
  "core/prompt-assembly.md",
  "planning/evidence-rules.md",
  "planning/conversion-driver.md",
  "production/funnel-set.md",
  "compliance/platform-constraints.md",
  "production/style-blacklist.md",
];
const loaded = KNOWLEDGE_FILES.map((rel) => `----- ${rel} -----\n${fs.readFileSync(path.join(REPO, rel), "utf8")}`).join("\n");
const FAB_SYSTEM = `你是电商 Listing 图像 prompt 组装器。根据下方知识库与商品资料，产出严格的 5-slot PromptSpec JSON（scene/subject/important_details/use_case/constraints，全部英文，值为字符串），不要输出任何其他文字。

必须执行的知识规则：
1. FAB→5-slot 映射：Feature→subject；Advantage→important_details 前置；Benefit→important_details 后置；认证类 Evidence→constraints 的 verification note；工艺/产地类→important_details 末尾。
2. 「待补证」卖点必须降级为中性表达，并在 constraints 写 do not include 指令。
3. 禁止性证据（标注「禁止」）→ 相关内容不得出现在任何槽位，且 constraints 写 do not include。
4. 场景槽从场景模板或输入的 scene_template 结合商品合理填充。
5. constraints 必须包含 4 类：平台技术约束、品类禁用风格、slop 禁用词、宣称边界。
6. 冲突优先级：平台强制技术规范 > locked_immutable > style-blacklist > FAB 卖点。
7. subject 槽是产品结构事实：忠实转写商品资料给出的结构细节，不得改写。

【知识库】
${loaded}`;

// ===== trigger evals =====
let triggerPass = 0;
const triggerFails = [];
for (const e of triggerEvals) {
  const out = await llm(
    `${skill}\n\n以上是 Skill 入口文件（含信号识别与平台分流）。判断用户输入，只输出严格 JSON：
{"signal":"A|B|C|D","route":"modes/mode-xxx.md","platform_path":"cross-border|domestic|social-media|unknown","notice":"需要告知用户的内容，无则空字符串"}
判定依据：SKILL.md 的信号识别与平台分流规则。不要输出其他文字。`,
    e.input,
  );
  let parsed;
  try {
    parsed = JSON.parse(out.slice(out.indexOf("{"), out.lastIndexOf("}") + 1));
  } catch {
    triggerFails.push(`${e.id}: 输出非 JSON: ${out.slice(0, 80)}`);
    console.log(`✗ ${e.id}（非 JSON）`);
    continue;
  }
  const problems = [];
  if (e.expected_signal && parsed.signal !== e.expected_signal) problems.push(`signal 期望 ${e.expected_signal} 实际 ${parsed.signal}`);
  if (e.expected_route && parsed.route !== e.expected_route) problems.push(`route 期望 ${e.expected_route} 实际 ${parsed.route}`);
  if (e.expected_platform_path && parsed.platform_path !== e.expected_platform_path)
    problems.push(`platform_path 期望 ${e.expected_platform_path} 实际 ${parsed.platform_path}`);
  if (e.expected_notice && !(parsed.notice ?? "").includes(e.expected_notice.slice(0, 8)))
    problems.push(`notice 未含关键句: ${e.expected_notice.slice(0, 20)}`);
  if (!problems.length) {
    triggerPass++;
    console.log(`✓ ${e.id}`);
  } else {
    triggerFails.push(`${e.id}: ${problems.join("; ")}`);
    console.log(`✗ ${e.id}: ${problems.join("; ")}`);
  }
}

// ===== FAB evals =====
let fabPass = 0;
const fabFails = [];
for (const e of fabEvals) {
  const out = await llm(FAB_SYSTEM, JSON.stringify(e.input, null, 2));
  const specText = out.slice(out.indexOf("{"), out.lastIndexOf("}") + 1);
  const spec = JSON.parse(specText);
  const flat = JSON.stringify(spec).toLowerCase();
  const eo = e.expected_output ?? {};
  const problems = [];
  for (const [slot, must] of Object.entries(eo)) {
    if (slot === "important_details_must_include" || slot === "constraints_must_include") {
      for (const inc of must) if (!flat.includes(inc.toLowerCase())) problems.push(`缺少: ${inc}`);
    }
    if (slot.endsWith("_must_exclude")) {
      for (const exc of must) if (flat.includes(exc.toLowerCase())) problems.push(`不应出现: ${exc}`);
    }
  }
  for (const slot of ["scene", "subject", "important_details", "use_case", "constraints"]) {
    if (!specText.includes(`"${slot}"`)) problems.push("5-slot 不完整");
  }
  if (!problems.length) {
    fabPass++;
    console.log(`✓ ${e.id}`);
  } else {
    fabFails.push(`${e.id}: ${problems.join("; ")}`);
    console.log(`✗ ${e.id}: ${problems.join("; ")}`);
  }
}

console.log(`\n===== 结果 =====`);
console.log(`trigger: ${triggerPass}/${triggerEvals.length} 通过`);
console.log(`fab:     ${fabPass}/${fabEvals.length} 通过`);
if (triggerFails.length) console.log("trigger 失败明细:\n" + triggerFails.join("\n"));
if (fabFails.length) console.log("fab 失败明细:\n" + fabFails.join("\n"));
fs.writeFileSync(
  path.join(REPO, "evals", "last-run.json"),
  JSON.stringify(
    {
      at: new Date().toISOString(),
      model: MODEL,
      knowledge: "full-mode 6 files（生产映射）",
      triggerPass,
      triggerTotal: triggerEvals.length,
      fabPass,
      fabTotal: fabEvals.length,
      triggerFails,
      fabFails,
    },
    null,
    2,
  ),
);
