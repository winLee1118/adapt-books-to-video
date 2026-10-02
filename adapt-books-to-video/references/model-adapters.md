# Model adapters

## Contents

1. Verification rule
2. Canonical-to-model adaptation
3. Capability-first prompt shapes
4. Cross-model compiler contract
5. Seedream image family
6. Seedance family
7. MiniMax/Hailuo family
8. Unknown or unavailable model

## 1. Verification rule

Model names, features, limits, and APIs change. On every run involving a named model:

1. Search official product, developer, API, or release documentation.
2. Record exact model name, URL, publication/update date when visible, and access date.
3. Check accepted inputs, image/video/audio reference behavior, duration choices, aspect/resolution, audio support, continuation/editing, reference counts, and prompt/API fields.
4. Write `NOT DOCUMENTED` instead of guessing.
5. If the requested label is not found in official sources, mark it `UNVERIFIED REQUESTED NAME`. Do not silently treat `Seedance 2.5` as `Seedance 2.0`, or `MiniMax H3` as `MiniMax-Hailuo-2.3`.

Use primary/official technical sources. UI behavior can differ from API behavior; name the surface verified.

## 2. Canonical-to-model adaptation

Never discard the canonical prompt. Adapt only:

- supported duration and segmentation;
- prompt density/ordering and language;
- input reference notation and upload order;
- audio/dialogue instructions when natively supported;
- supported continuation/editing/multi-shot workflow;
- real API/UI parameters documented by the vendor.

Keep the evidence gate in the audit and enforce it before submission. Compile its allowed visible claims, interpretation and prohibited extrapolations into the model prompt; source IDs and review dates need not be submitted. Read production-execution.md for constraint_map and the audit/submission split.

Write the canonical prompt and every named-model adapter in Chinese. Translate descriptive examples from official documentation into Chinese instead of copying their English prose. Preserve only literal UI/API field names, reference tokens, model names, asset IDs, and required syntax in their original form, then explain their role in Chinese.

Do not change identity, history, wardrobe, geometry, action causality, expressions, or visual continuity to fit a model. Split a complex shot instead.

## 3. Capability-first prompt shapes

Classify the verified target surface before writing vendor-specific syntax:

| Shape | Verified input surface | Write this | Avoid this |
|---|---|---|---|
| `P1-ANCHOR-MOTION` | One approved image/first frame plus motion text | Describe only temporal change, camera path, performance, physics, audio status and end state | Re-describing the whole image in conflicting words |
| `P2-FULL-DESCRIPTION` | Text-to-video or weak/no image conditioning | Repeat identity, wardrobe, scene geometry, format, camera, timed action and exclusions | Assuming the model remembers another clip |
| `P3-KEYFRAME-EVOLUTION` | Verified first/last frame or keyframe sequence | Freeze start/end states and describe the physical transition between them | Demanding impossible teleportation between incompatible frames |
| `P4-NATIVE-MULTISHOT` | Officially documented multi-shot/timeline input | Use explicit shot boundaries, cut logic, sound bridges and cross-shot state | Packing unrelated scenes into one prompt because the model accepts long text |

Choose by capability, not by vendor reputation. If official documentation does not verify a control surface, do not select its shape. Complex identity- or geography-sensitive action should default to one approved anchor per clip even when multi-shot is available.

## 4. Cross-model compiler contract

For every requested model, produce a short compiler record:

```text
目标名称与核验状态
采用的提示词形态：P1/P2/P3/P4
资产证据门禁：证据卡 ID、PASS、生产解释层、不得推导项
输入素材顺序及每项唯一职责
从标准提示词保留的硬约束
因能力限制而拆分/后期处理的内容
厂商专用语法与来源
中文模型提示词
负向约束的实际放置位置；不存在专用字段时写 NOT DOCUMENTED
输出后的检查重点与失败编码
```

跨模型转换只允许改变表达结构、时长分段、引用格式和已验证控制项。不得自行改变导演参数、历史事实、人物表演弧、空间地标或镜头叙事功能。

如果两个模型对负向提示、声音或多镜头的处理不同，分别生成完整版本，不使用“同上”。所有描述性内容保持中文。

同一章内每个提交提示词都须自包含，按约束覆盖而不是长度相同验收。后续镜头不得因为“承接上一镜”而省略参考素材、景别、运镜、环境、对白或负向约束；续接关系通过逐字重述上一镜批准终态来表达。

## 5. Seedream image family

Verify the exact image-model name and product surface before use. As checked on 2026-08-07, the official Dreamina/CapCut page names `Seedream 5.0 Pro` and describes reference-guided image generation/editing, structured character design sheets, storyboards/video first frames, multilingual text, and 2K-oriented production output. Official source: `https://dreamina.capcut.com/seedream/seedream-5-0-pro`.

Do not inherit unsupported claims from tutorials or third-party pages. In particular, do not claim 4K output, a fixed maximum reference count, layer export, regional brush controls, or model-to-video consistency unless the exact official surface documents them. Record absent values as `NOT DOCUMENTED`.

For book-to-video assets, use this conservative order:

```text
角色资料/表情成品卡 → 文字 `SCENE-xx-SPATIAL-LOCK` → 无字内部顶视 `SCENE-xx-GEOMETRY-PLAN`（必经并验收） → 同一空间的 `SCENE-xx-MULTIANGLE-CARD` 九机位卡 → 指定 Vnn 区域临时裁切 → 独立色卡 → 镜头首帧
```

Apply these adapter rules:

- preserve the finished-card contract: the scene delivery asset is one 3×3 multi-angle card, backed by a text spatial lock; do not produce a second delivery map or a set of standalone direction images;
- an internal unlabeled geometry plan is only upstream QA and never a direct video input; the video-facing `SCENE_GEOMETRY` reference is the approved multi-angle card with its declared Vnn;
- for an edit, name the input image and state precisely what may change and what must remain fixed;
- derive every scene-card Vnn from the approved `SCENE-xx-SPATIAL-LOCK`, then repeat “只改变摄影机”；
- keep region guides and labeled color-card review versions out of final frame generation;
- keep all descriptive prompts in Chinese and preserve only literal UI/model names in their official form.

## 6. Seedance family

Read [seedance-2x-workflow.md](seedance-2x-workflow.md) for the required Seedance 2.x compiler record, reference-role map, timing compiler, continuation boundary, SCELA check and rejection rules. It supplements this section; it does not weaken the canonical prompt, evidence gate, 16:9 delivery contract, or ≤15-second clip limit.

Use the exact verified Seedance version. If the requested label (for example `Seedance 2.5`) is not found in official sources, keep it marked `UNVERIFIED REQUESTED NAME`, write the full adapter anyway, and require the operator to confirm duration, reference count, audio, and multi-shot support before submitting. Never fabricate API fields, bracket tokens, or capability claims to make the prompt look vendor-specific.

Seedance-family prompts are written as dense continuous Chinese natural language rather than key-value lists. The model follows explicit shot-language vocabulary, so state 景别 and 运镜 in words it can act on, and preserve applicable visual/audio constraints from `prompt-spec.md`; merge repetitions and omit audit-only metadata in the submission variant, with constraint_map documenting coverage.

Recommended paragraph order:

```text
参考素材与各自职责 → 景别与机位 → 固定人物与场景事实 → 运镜及其触发/停止 →
环境、云雾与光线 → 按时间顺序的动作与表演节拍 → 对白与声音 → 禁止漂移规则 → 真实感物理合同 → 跨视频承接与转场 → 终帧状态
```

Write the reference mapping inside the prompt body, naming each asset and its single job, and stating what must not be copied from it:

```text
以 SHOT-01-ANCHOR.png 为锁定首帧，控制构图、机位、焦段、人物屏幕位置与光向；
CHAR-02-PROFILE-CARD.png 只控制该人物的面部身份、身体比例与三层僧衣层次，不取其页面底色、标题文字与并排版式；
PROP-01-CARD.png 只控制锡杖形制，杖头左右各三枚圆环、共六环，不取其分区版式；
SCENE-01-MULTIANGLE-CARD.png 仅用于核验 V03 的地标关系，不取其九格分割线或其他站位构图。
禁止从上述任何参考图复制标题、标签、分格线或未点名的元素。
```

For a verified multimodal version that documents slot tokens, map every uploaded asset explicitly, for example:

```text
@Image 1 控制首帧构图与场景几何；@Image 2 只控制角色 A 的脸部与服装；@Video 1 只提供摄影机节奏；@Audio 1 只提供时间节奏与环境声。禁止从次要参考素材复制无关内容。
```

Shot-size and camera vocabulary must be explicit in every clip, for example 「广中景，50mm，眼平机位，人物占画高约三分之二，全程固定机位，无推拉摇移」 or 「中近景，65mm，略低机位，缓慢推近约百分之三，由抬眼触发，至肩线入画停止」. A clip that omits 景别 or 运镜 is incomplete even if the action is described.

Dialogue and ambience are written in the same prompt: quote the line verbatim with speaker, tone, pace, and mouth-movement scale, or state 「无对白」 plus the intended narration, ambience, foley, and silence. Mark audio 「后期制作」 whenever native audio is unverified.

Every generation job receives its own self-contained adapter; length may vary. Do not shorten `SHOT-02` and `SHOT-03` into continuation notes; restate the frozen identity, wardrobe, prop-form, landmark, and light strings verbatim in each one. Also state the prior approved end-state, exactly one bridge from `cinematic-shot-bridging.md`, the shared vector, the required next first frame, and whether the transition/audio bridge is post-production.

Use native multi-shot generation only when verified and when transitions are intentional. For consistency-sensitive work, prefer one clip/shot anchor at a time, then continue from an approved final frame.

## 7. MiniMax/Hailuo family

Use the exact official API/UI model name. Official MiniMax documentation may expose text-to-video, image-to-video, subject-reference, first/last frame, or other modes depending on model and surface. Confirm which mode exists before specifying it.

Recommended prompt order:

```text
主体与动作 → 环境 → 运镜与景别 → 表情与物理响应 → 光线/风格 → 禁止漂移约束
```

If a first-frame image is supported, make the clean shot anchor the first-frame input and write movement as a temporal evolution from that exact frame. If duration is restricted to discrete choices, divide the canonical sequence accordingly and recalculate all beat ranges.

Never invent bracket syntax, camera tokens, negative-prompt fields, subject-reference counts, or end-frame controls. Use only currently documented UI/API syntax.

## 8. Unknown or unavailable model

Deliver:

1. 保持不变的中文标准提示词；
2. a capability table marking unknown fields;
3. 不含厂商专用语法的保守中文自然语言适配版；
4. a note asking the operator to map duration, references, and audio after confirming the real model surface.

If a nearest verified model is useful, provide it as a separate, clearly labeled fallback. Never imply equivalence.
