# Prompt specification

Scope: this page defines the internal audit record and visual constraints. Read `production-execution.md` for the current audit/submission split. Only the audit keeps full source/status metadata; model-facing prompts are self-contained, constraint-complete and may merge sections. Clip timing/planning follows `clip-sequencing.md`, including verified multi-shot jobs.

## Contents

1. Shared prompt rules
2. Photoreal character prompts
3. Scene and multi-angle prompts
4. Storyboard image prompts
5. Time-coded video prompts
6. Negative and continuity rules
7. Reference-density and color-card rules
8. Director/classic-film method compilation
9. Prompt repair discipline
10. Worked example of a full clip prompt

## 1. Shared prompt rules

Write all descriptive prompt content in Chinese. This rule applies even when the source work, image model, video model, or official documentation uses another language. Do not provide an English duplicate unless the user explicitly asks for one. Keep only required API/model parameter names, asset IDs, filenames, proper nouns, and verbatim quotations in their original form.

Write prompts in structured Chinese blocks. Put stable facts before action:

```text
资产证据门禁
用途与资产 ID
证据/诠释状态
连续性锚点
主体或标准场景
服装/道具或空间不变量
构图与摄影机
动作与表演
光线/色彩/材质响应
交付物与画幅
排除项/禁止漂移
```

Every character, scene, prop, top-down plan, multi-angle card, anchor, contact sheet and video prompt begins with the `【资产证据门禁】` block from `asset-evidence-gate.md`. It names the `ASSET-EVIDENCE-CARD`, gate result, chosen production interpretation, source IDs/limits and prohibited extrapolations. Only `PASS` permits generation; `HOLD`, `REJECTED` or an unsupported upstream asset makes the prompt `DEFERRED` rather than more imaginative.

Prefer a few compatible, verifiable details per feature. Avoid contradictory lenses, lighting, emotions, actions, or style labels. State exact visible colors/materials and garment construction. “Ancient costume” and “cinematic” are not sufficient.

Use `16:9` for every scene, shot-anchor, storyboard-panel and final-video prompt. `AI_SHORT_DRAMA`/`MOTION_COMIC` do not change the ratio. Keep face references at `4:5` and full-body turnarounds near `2:3` only when they are permitted temporary crops, not shipped assets.

## 2. Photoreal character prompts

### Identity card

Specify:

- role, approximate age, sex/gender presentation only when relevant, ancestry/geographic context with evidence, height/build/proportions, posture;
- face shape, brow, eyes, nose, lips, jaw/chin, ears, skin tone and restrained texture, distinguishing but non-stereotyped marks;
- hairline, texture, length, grooming, facial hair;
- neutral expression plus story-specific expression vocabulary;
- all garment layers from skin outward: silhouette, cut, fiber, weave, weight, dye/color, seams, closures, trim, wear, drape;
- headwear, footwear, jewelry, status marks, and props with historically plausible handling;
- evidence labels and IDs for uncertain choices.

For realistic skin, request fine pores, slight tonal variation, natural lip lines, subtle under-eye texture, believable hairline transitions, and mild facial asymmetry. Do not stack acne, scars, freckles, veins, sweat, wrinkles, and blemishes unless the character/story requires them. Avoid beauty retouching, porcelain skin, waxy highlights, doll symmetry, or glamour posing.

### Three-view turnaround prompt

```text
CHAR-01 三视图源资产。同一名成年角色的三张独立、干净、全身视图：正面、严格 90 度侧面、背面。[逐字重复身份锚点。] 中性解剖站姿，双脚平放且平行，双臂自然垂下并与躯干略微分离，手指清晰可见，没有道具遮挡轮廓；三个视图中的脸部身份、身体比例、发型、服装层次、配饰与鞋履完全一致。符合[时代/地区]史实的服装：[结构与材质]。中性暖灰色无缝背景，均匀柔和交叉布光，眼平机位，等效 85 mm 镜头，近似正交、低畸变的资料照拍摄，中等景深并确保全身清晰，保留自然皮肤与织物纹理。交付物：[优先三张独立图片/带标注审核板]，[画幅]。禁止姿势变化、三分之四侧面、透视拉伸、现代扣件、现代妆容、品牌标识、多余肢体、脚部裁切、服装漂移和装饰性场景。
```

Generate the agreed profile card as a whole page first. Inspect identity across its portrait and views; internal single-zone repair and recomposition are allowed. Do not add independent turnaround files to delivery.

### Low-density primary reference

Choose the approved shot anchor first. When a clean character input is needed, derive an internal crop from the approved profile card and record its parent hash and region. Do not add small expression tiles, pose galleries, fabric swatches, prop callouts, decorative typography, long labels, or background scenery. A review board may contain these items, but label it `QA_ONLY` and do not place it first in model inputs.

### Expression prompt

Define observable transitions rather than naming emotion alone:

```text
表情：克制的惊惧逐渐转为坚定。眉毛先轻抬，再轻微向内收紧；上眼睑睁开，视线锁定镜头外一点；下眼睑轻微绷紧；嘴唇在安静吸气时短暂张开，随后轻轻抿合；下颌收紧但不露齿；呼气时双肩逐渐稳定。保持人物身份、年龄、发型、服装、摄影机和光线不变。
```

## 3. Scene and multi-angle prompts

Before any scene image, define `SCENE-xx-SPATIAL-LOCK` once, following `scene-spatial-lock.md`:

```text
标准状态：坐标/参考边；空间边界和开口；每一墙体所属体量、墙厚、每个门窗两侧的可达空间与离画合同；固定的门、窗、道路、祭坛和家具；物体位置与朝向；演员活动区；时间/天气；主光、补光、实景光源及方向；材质与磨损。
空间不变量：必须保持画面世界关系的 4–8 个地标；V01–V09 机位表和每一地标的可见/可遮挡/不应出现矩阵。
```

文字锁通过后，必须生成并验收无字的内部 `SCENE-xx-GEOMETRY-PLAN`：16:9、近似顶视、仅含正确边界/开口/固定物/演员区/光向。它是多机位卡的强制上游中间参考，不交付、不直接作为视频模型参考；文字坐标、标签、箭头和界面全部禁止。它若未生成、被拒绝或为 `PROMPT_ONLY`，场景卡与下游镜头标为 `DEFERRED`。

For every angle repeat the canonical state verbatim, then add:

```text
只改变摄影机。摄影机位 C2 位于[位置/高度]，朝向[方向]，使用[镜头]，[景别]，对焦[主体]；前景为[x]，中景为[y]，背景为[z]，[景深说明]。被遮挡的物体仍保留在标准位置。保持时间、天气、光线方向、物体状态、材质与尺度不变。
```

Use plausible sightlines. A seat, monitor, writing desk, altar, doorway, vehicle, weapon rack, or cooking hearth must face the documented user/action, not rotate toward camera for display. For every visible or crossed doorway, restate the host wall thickness, both connected volumes and the destination after crossing; if one side remains unbuilt/offscreen, prohibit a camera view or actor move that would expose it. Add `禁止穿入薄墙、未建模虚空或无去处门洞` to the scene-specific negatives.

For local details, name the approved `SCENE-xx-MULTIANGLE-CARD` Vnn source region in text and crop from it. Do not generate a marked region-guide image. State “只扩展指定区域；保持 `SCENE-xx-SPATIAL-LOCK` 的相邻地标、材质、光线方向、时间和可见性关系不变”.

## 4. Storyboard image prompts

Read `reference-asset-ledger.md` first. Every anchor prompt, contact-sheet prompt, and panel row begins with the complete `【参考生成资产】` block: asset ID, actual filename/path, status, one role, unique job, frozen fields, must-not-transfer content, upload order, and source chain. Do not refer to a planned image as though it existed.

Write one whole-page prompt for `SHOT-xx-CONTACT` after the current clip's `SHOT-xx-ANCHOR` is approved. Do not write six independent panel-file prompts. Duration in the prompt must be ≤15.0 seconds. For the opening clip, carry `OPENING-PROMISE-ID`, the primary `OPENING-MODE`, viewer question, 0–3s cause/effect and payoff deadline into the contact sheet prompt.

```text
SHOT-03-CONTACT，本镜 15.0 秒，3×2 宫格。以已批准的 SHOT-03-ANCHOR 作为构图与空间几何的唯一控制参考；CHAR-02-PROFILE-CARD 只控制人物身份。六格保留同一锁定布景和一条连续摄影机语言，呈现已批准 `ACTION-PROP-BEAT` 的准备、压力、可见变化、余波与终态；至少三格可检查人物—物件/空间关系的变化。每格安全角落放小型中文时间码，不遮挡脸、手、道具或主地标。无大标题带、无界面、无字幕。画幅 16:9。
```

Plan the full sequence first. Only actual dependent submissions wait for this task's approved inputs or real end state; independent shot plans may proceed.

## 5. Time-coded video prompts

Each internal audit covers the applicable fields below. Submission prompts may merge repeated facts and omit administrative metadata; preserve every hard visual/audio constraint through constraint_map. Repeat needed continuity facts instead of relying on “承接上镜，其余不变”. Read `cinematic-shot-bridging.md` before choosing a camera move or bridge.

```text
【镜头标识】
镜头 ID | SCRIPT-BEAT-ID | EP-ID/HOOK-ID（如适用） | 用途一句话 | 精确时长（≤15.0 秒） | 本章绝对时段 | 文本定位

若为故事片、纪录片、短剧或漫剧的开场/回归段，紧接着写 `【开场承诺】`：`OPENING-PROMISE-ID`、主/辅 `OPENING-MODE`、观众问题、首帧可见事实与首眼落点、0.0–3.0 秒因果、首次变化、兑现期限、首段终态和下一镜必须承接的方向。纪录片另写来源与 `AI_RECONSTRUCTION`/CREATIVE 边界；禁止标题卡、背景说明、无关风景、未发生的伪危机或尚未可见的“悬念”。

【资产证据门禁】
资产/镜头：……；证据卡：AEC-……；门禁：PASS；核验日期：YYYY-MM-DD。
生产解释层：叙事世界 / 指定历史时空 / 指定图像学传统（仅取实际选择）。
可见主张与来源：TEXT……；HISTORY……；ICONOGRAPHY……；INFERENCE/CREATIVE……。
不得推导：文本或后世图像不支持的年龄、脸型、服装、建筑、地域、时代、宗教属性或其他可见细节。
只允许生成：证据卡列出的可见主张；生成后逐项比对：……。

【参考生成资产】
逐条写在提示词正文内；每条含资产 ID、实际文件名/路径、状态、唯一职责、冻结字段、不得迁移内容、上传顺序与来源链：
1. [COMPOSITION_ANCHOR] SHOT-xx-ANCHOR（文件名；状态：GENERATED）——只锁定首帧构图、机位、焦段、人物屏幕位置、地标位置与光向。不得迁移：字幕、边框、未点名人物、页面排版。上传顺序：1；来源链：SCENE-xx-MULTIANGLE-CARD → SHOT-xx-ANCHOR。
2. [IDENTITY] CHAR-xx-PROFILE-CARD（文件名；状态：GENERATED）——只锁定人物身份、面部、身体比例与服装层次；注明允许裁切区。不得迁移：背景、版式、标题文字与并排构图。上传顺序：2；来源链：TEXT/EVIDENCE → CHAR-xx-PROFILE-CARD。
3. [PERFORMANCE] CHAR-xx-EXPRESSION-CARD（文件名；状态：GENERATED）——参考本镜指定格的可见表情状态，注明格号及适用时段；入态到该状态允许自然过渡。不得迁移：网格、边框与中英文标签。上传顺序：3；来源链：CHAR-xx-PROFILE-CARD → CHAR-xx-EXPRESSION-CARD。
4. [SCENE_GEOMETRY] SCENE-xx-MULTIANGLE-CARD（文件名；状态：GENERATED）——只核验空间几何与地标关系，注明依据 Vnn、主地标和两项固定关系。不得迁移：宫格分割线与九格拼接形式。上传顺序：4；来源链：TEXT/EVIDENCE → SCENE-xx-SPATIAL-LOCK → SCENE-xx-MULTIANGLE-CARD。
5. [PROP_FORM] PROP-xx-CARD（文件名，如有；状态：GENERATED）——只锁定道具形制与可数特征。不得迁移：分区版式与标签。上传顺序：5；来源链：EVID-xx → PROP-xx-CARD。
6. [END_STATE] 上一镜批准终帧（文件名，如有；状态：GENERATED）——只锁定姿态、物体状态、视线和空间状态；后续镜头优先级高于旧锚点。
禁止从任何参考图复制其页面底色、标题、标签、分格线、未点名元素或不属于声明职责的内容。无图像参考时明确写“无图像参考，依据 TEXT/EVIDENCE 生成”。

【固定事实】
人物身份串（逐字复制冻结串）。服装层次与材质。道具形制串（含可数特征的确切数字）。
4–8 个固定地标及其屏幕方位。每个将被看见或跨越的门洞的墙厚、两侧体量、通过后的抵达状态与离画限制。时间、季节、天气。主光方向与色温。

【道具戏剧合同】
逐件写：标签（TEXT/HISTORY/ICONOGRAPHY/INFERENCE/CREATIVE）、持有人、叙事目标、初态、准备、接触／受力、可见变化、材料／声音余波、终态。若为 `CREATIVE`，明确“无地域、无时代断言的非历史行动载体”，并写不得伪装成的历史物件；没有通过此合同的物件不得入画。

【格式】
画幅；分辨率目标；时长；帧率（仅在已核实支持时写）。

【景别与摄影机】
景别（大远景/远景/全景/中景/中近景/近景/特写，写明取哪一种）；镜头焦段；机位高度与角度；
被摄主体在画面中的占比与位置；对焦目标；景深与焦外程度。

【运镜】
起幅与落幅机位；运动类型（固定/推/拉/摇/移/升降/跟随）；幅度与速度；缓动方式；
触发事件与停止条件。没有可见叙事变化时写“全程固定机位，无推拉摇移”，不得留空。

【环境与氛围】
处所与空间性质；云、雾、烟、尘、水汽的分布与流速；空气透视与层次；
背景群体的呈现层级；环境材质与光的相互作用；不得出现的地域或时代元素。

【分时段节拍】
每一段必须同时写出：景别、运镜、动作阶段、表情与视线、环境响应、声音或对白，以及人物—英雄道具/行动支撑物（或已声明的无道具空间压力）的可检查状态。整段先给 `ACTION-PROP-BEAT`：目标/初态 → 准备 → 压力 → 可见变化 → 余波 → 终态；按本镜的实际叙事任务设置可见变化；反应/细节镜不强制三个动作或独立反转。
0.00–[a] 秒——……
[a]–[b] 秒——……
……
[n]–[总时长] 秒——稳定进入可续接的明确终帧。

【对白与声音】
有对白时逐字写出台词、说话者、语气、语速与口型幅度，并注明是原文引用还是改写；
宗教或受版权文本不得伪造原话。无对白时写“无对白”，并给出旁白、环境声、拟音、音乐或有意静默。
模型未核实原生音频时，整段标“后期制作”。

【表演】
先写 `PERFORMANCE_BASELINE`：镜头开始时的注视对象、眼睑张力、呼吸、肩颈、双手和重心；再写触发物及秒数、最先出现的最小反应、仅 1–2 个区域的后续发展或抑制、身体/道具对应和稳定终态。眨眼、视线与呼吸必须由注意力和触发驱动，禁止精确周期循环或多人同步。仅描述在本镜景别下真正可见的面部区域；细则见 `character-realism-distillation.md`。

【负向约束】
禁止身份变形、年龄变化、服装变化、多余手指/肢体、道具形制改变、地标漂移、群演复制、
机位跳变、焦段变化、焦点搜索、曝光闪烁、时间/天气变化、穿入薄墙、未建模虚空或无去处门洞、现代物品、错误地域元素、
文字/字幕/水印以及未经要求的剪切；禁止瓷娃娃皮肤、统一油亮高光、泛化磨皮、脸部独立曝光、无来源双侧轮廓光、剪纸边缘和从角色资料卡迁移的中性棚拍光。逐字写入本片的专用否定串。

【真实感物理合同】
可见主光和实景光源及其方向、软硬、遮挡；皮肤、布料、硬质物、地面在受光/接触后的不同反应；
动作按准备→受力/接触→惯性/余波展开，写清支撑点、重心、手指、脚底和道具位置；
人物微动作、环境慢变量和禁止突变；焦段感、焦点平面、允许的机位移动及其物理/叙事触发；
同期声、环境声、拟音、静默各自的空间来源。未核验模型原生音频时标“后期制作”。
近景人物另写 `FACE_INTEGRATION_LOCK`：当前场景主光/环境补光/色温，眉下—鼻翼—下唇—下颌—颈部的遮挡阴影逻辑，皮肤/头发/织物的不同反射，以及人物边缘与背景的色温和景深关系；身份卡只锁脸与服装，不迁移其棚拍光和背景。

【跨视频承接与转场】
入镜：写明“段落首镜，无前镜”或上一镜 `SHOT-ID`、批准终帧真实文件名，并逐字重述人物姿态/视线、道具、地标、主光、动作轴、摄影机能量和正在延续的环境/声音状态。
接入方式：非首镜从 `HARD_CUT_ON_ACTION`、`MATCH_ACTION`、`MATCH_COMPOSITION`、`MATCH_EYELINE`、`MATCH_SOUND`、`J_CUT`、`L_CUT`、`OCCLUSION_WIPE`、`DISSOLVE_TIME_OR_MENTAL_SHIFT`、`BLACK_FIELD_PUNCTUATION`、`MOTIVATED_RUSH_TRANSITION` 中恰选一种；写出共享向量和本镜 0.0 秒新增的信息。段落首镜明确“无前镜”，不得虚构入场转场。
声音桥：写明声源、进入/延续秒数、退出方式；原生音频未核实则标“后期制作”。
出口/交棒：写明下一个 `SHOT-ID` 或“段落末镜”，当前可剪切动作/静止点、下一镜必须保留的首帧状态和剪辑责任。未核实切换/叠化/擦拭/多镜功能时标“后期制作”。

【终帧状态】
人物姿态、表情、视线、道具位置、光线与地标状态，供下一镜逐字抄写为起始状态。
```

### Uniformity rules

- Every audit covers applicable fields. Submission length depends on action and input complexity, never on matching the first clip's word count.
- Continuation is expressed by restating the previous clip's approved end state inside `【固定事实】`, `【分时段节拍】`, and `【跨视频承接与转场】`, not by referring the reader elsewhere.
- Keep the full lineage in the audit/upload manifest. The submission body identifies actual references and their duties, essential locks and exclusions; validate that they match the manifest.
- Each beat states shot size, camera movement, action, expression, environment, audio, and a checkable person–prop or person–space state. A beat missing any is incomplete.
- Each `SEQ` names one de-named camera language; every move has a visible trigger, path, stop, and newly visible narrative information. Fixed camera is mandatory when no such change exists.
- Each edge has exactly one primary bridge, at least one shared action/composition/eyeline/light/environment/sound vector, and an explicit model-versus-post-production boundary.

### Timing rules

- Cover the full clip once, without gaps or overlaps.
- Use one dominant action per beat. Include anticipation, execution, reaction, and settle when relevant.
- Describe camera movement quantitatively enough to visualize, but do not invent a model control parameter.
- Use rack focus only between two named planes and include its timing.
- Use a cut only if the target model supports/plausibly follows multi-shot prompts and the shot plan explicitly calls for it. Otherwise split into clips.
- For a continuation, use the prior approved final frame as the primary reference and start from its exact pose, gaze, camera, light, and object states.
- Unless multi-shot cuts/transitions are officially verified for the target, generate only the continuous single shot and perform cuts, J/L bridges, dissolves and wipes in post-production.

## 6. Negative and continuity rules

Keep negatives specific to likely failure modes:

- **Historical:** modern zippers, elastic cuffs, machine-perfect seams, synthetic shine, modern glass, electric fixtures, contemporary makeup, generic fantasy armor, mixed dynasties/regions.
- **Human:** face drift, beautification, plastic skin, dead eyes, incorrect gaze, inconsistent age, floating hair, fused fingers, hand/prop intersection.
- **Wardrobe:** missing underlayers, changed collar/closure, mirrored accessories, altered wear/dye, cloth behaving like rubber.
- **Scene:** moving doors/windows/furniture, changing object count/orientation, impossible sightline, inconsistent sun direction, unexplained weather/time change.
- **Camera:** lens breathing, accidental zoom, rolling horizon, focus hunting, teleporting camera, unrequested speed ramp or cut.
- **Religious/iconographic:** unrelated symbols, mixed traditions without intent, sensationalized suffering, modern occult motifs, incorrect ritual gesture.

Repeat the compact continuity-anchor block verbatim across related prompts. Repeating it is required even when it feels redundant; only decorative adjectives may vary. Trimming the anchor block, the reference list, the shot size, the camera line, the environment line, the dialogue line, or the negatives out of a later clip is a defect.

## 7. Reference-density and color-card rules

- Give every model input exactly one declared job. Prefer a minimum sufficient set over attaching every available asset.
- For character-led shots, normally use the approved shot anchor plus `CHAR-xx-PROFILE-CARD`; add `CHAR-xx-EXPRESSION-CARD` only when the shot visibly needs a named expression.
- For environment-led shots, normally use `SCENE-xx-MULTIANGLE-CARD` plus one color/style card; do not attach process images.
- Generate `STYLE-COLOR-xx` as a separate clean card with five to eight large swatches and no scene collage. Record hexadecimal colors, dominant/secondary/accent roles, saturation, contrast, color temperature, highlight roll-off, shadow hue, grain, and key material response in the adjacent Chinese prompt text.
- If labels are required for human review, place them in a separate review version. Use the clean unlabeled swatch card for generation to reduce unwanted text transfer.
- Treat “reference card works best,” “color restoration is high,” or similar claims as `INFERENCE` until tested with the exact target model, input mode, and resolution.

## 8. Director/classic-film method compilation

Keep the named director, film, or movement in `04-style-bible.md` as analysis context. Compile the actual generation prompt from observable parameters in this order:

```text
叙事倾向与本镜头工作
构图/画面层次
焦段、机位、景深和观众第一落点
允许的运镜、触发事件、路径和停止条件
光源、方向、硬软、光比和曝光
主辅色、黑位、高光、颗粒和材料响应
剪辑节奏、停顿、声音与表演强度
16:9 横幅构图与观众第一落点
历史与文本优先约束
风格专属排除项
```

禁止只写“某导演风格”“像某经典电影”后让模型自行猜测。禁止复刻可识别镜头、角色造型、台词、场景或专属道具。模型可能限制姓名/IP 时，最终提示词完全去专名。

用户未指定风格时，读取 `default-grounded-drama-baseline.md`，在 `04-style-bible.md` 记录 `DEFAULT-GROUNDED-DRAMA`，再把其可见的前景—人物—空间层次、实景/自然光、低至中饱和材料本色、反应/接触剪辑和受动机转场写进相应提示词段落。不得把该 ID、视频名或“同款风格”写入模型提示词；历史/文本/证据和用户明确风格优先。

## 9. Prompt repair discipline

生成失败后先分配 `F01`–`F63`，再针对根因修改。一次重试只改变一个主要变量：开场承诺/兑现映射、证据门禁/生产解释层、生产设计/道具用途、提示词约束、参考素材、空间锁/站位、静态锚点、角色基线/触发、肖像—场景整合、镜头时长/动作负荷、物理合同、剧本节拍、镜头方案或桥接方式。

不要通过添加“高质量、完美、电影感”等词修复身份、手、空间、光向、表情或历史错误。源锚点错误时先修图；单镜动作过多时拆镜；同类失败三次时停止盲目重抽并升级到重新规划。

## 表演编译可追踪性

按 [actor-performance-workflow.md](actor-performance-workflow.md) 保留performance_constraint_map：PERF-ID→故事板格→实际参考格/时段→提交语句→实片验收点。正文写原行动、刺激、可见接收/回应、终态及必要语气。表情卡控制指定阶段的状态，不冻结整条眉眼与口部。删除毫米级表情量化、固定眨眼周期与不可见细节；不把完整七区表机械复制到提交版。
