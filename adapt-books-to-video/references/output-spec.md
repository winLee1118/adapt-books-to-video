# Output specification

Current scheduling, status, input preparation and audit/submission rules are defined in production-execution.md. In legacy examples, SHOT names may denote generation jobs; preserve filenames and record explicit GEN/SHOT mappings. The detailed prompt fields below belong to the audit, not mandatory equal-length model submissions.

## Contents

1. Project tree
2. IDs and manifest
3. File contracts
4. Asset quantities
5. Delivery gates

## 1. Project tree

Create `<book-slug>-video-kit/`:

All descriptive prompts in every output file must be Chinese, including canonical prompts, negative prompts, storyboard-panel prompts, continuation prompts, and named-model variants. Retain non-Chinese text only when it is a required API/model parameter, asset ID, filename, proper noun, or attributed source quotation; accompany it with Chinese explanation when clarity requires.

```text
<book-slug>-video-kit/
├── 00-brief.md
├── 01-book-map.md
├── 02-research-dossier.md
├── 03-adaptation-plan.md
├── 04-style-bible.md
├── 05-character-bible.md
├── 06-scene-bible.md
├── 07-storyboards.md
├── 08-video-prompts.md
├── 09-model-capabilities.md
├── 10-sources.md
├── 11-quality-report.md
├── 12-continuity-bible.md
├── 13-sound-edit-plan.md
├── 14-screenplay.md
├── 15-reference-asset-map.md
├── 16-realism-qa.md
├── 17-series-bible.md
├── 18-screenplay-qa.md
├── 19-cinematography-transition-plan.md
├── 20-director-design.md
├── 21-shotlist-9col.csv
├── 22-composition-triptychs.md
├── 23-seedance-2x-compiler.md
├── 24-precut-review.md
├── 25-video-result-qa.md
├── active-release.json
├── project-config.json
├── asset-manifest.csv
├── delivery/
│   ├── audio/
│   ├── characters/
│   ├── scenes/
│   ├── shot-anchors/
│   ├── storyboards/
│   └── style-cards/
├── reports/
│   └── retries/
└── process/
    └── cinema-triptychs/
```

`delivery/` holds approved media and submission prompts; root documents are the production package. Internal crops use `process/model-inputs/`, geometry checks use `reports/internal-qa/`, and video inspections use `reports/video-qa/`. `process/cinema-triptychs/` it holds the three required non-delivery `21:9` composition previsualizations for each selected sequence and is never sent to a final image/video model. Do not create folders for per-view character images, scene maps, region guides, or single storyboard panels.

If images cannot be generated, keep the folder and manifest structure and use `PROMPT_ONLY` instead of fake paths.

## 2. IDs and manifest

Use stable IDs. The character, scene, and storyboard IDs each resolve to exactly one delivered file:

- `CHAR-<nn>` character;
- `CHAR-<nn>-PROFILE-CARD` one 16:9 card holding the identity portrait plus front/side/back turnaround;
- `CHAR-<nn>-EXPRESSION-CARD` one 16:9 card holding the story-required expression grid;
- `SCENE-<nn>` location;
- `SCENE-<nn>-MULTIANGLE-CARD` one 16:9 `3×3` fixed-space card, backed by a text-only `SCENE-<nn>-SPATIAL-LOCK`;
- `PROP-<nn>-CARD` one 16:9 form-evidence card, only for a story-identifying prop seen in a medium-close shot or one that already failed a form check;
- `STYLE-COLOR-<nn>` clean color/style reference;
- `SEQ-<nn>` selected narrative sequence;
- `PREVIS-SEQ-<nn>-01` / `02` / `03` three separate non-delivery `21:9` composition-previsualization frames for the sequence;
- `SHOT-<nn>` continuous generation clip;
- `SHOT-<nn>-ANCHOR` clean first frame;
- `SHOT-<nn>-CONTACT` one `3×2` six-panel sheet for that clip.

Retry artifacts use `<id>-retry-<nn>` and live only in `reports/retries`. `PREVIS` artifacts live only in `process/cinema-triptychs/`, are registered as `INTERNAL_PREVIS`, and are never listed as deliverables or video inputs.

`asset-manifest.csv` columns:

```text
id,type,purpose,status,file_path,prompt_file,aspect_ratio,target_model,source_text,evidence_ids,evidence_card_id,evidence_gate,production_interpretation,verification_date,production_design_id,action_prop_ids,reference_ids,origin,approved_from,reference_role,frozen_fields,must_not_transfer,upload_order,used_by_script_beats,used_by_shots,continuity_group,style_profile_id,qa_status,failure_code,retry_count,notes
```

Allowed status: `PLANNED`, `PROMPT_ONLY`, `GENERATED`, `REJECTED`, `DEFERRED`. `PREVIS` uses only `GENERATED`, `PROMPT_ONLY` or `DEFERRED`.

## 3. File contracts

### `00-brief.md`

Record scope, edition, audience, `production_track`, `production_form`, `format_route`, episode count/duration where relevant, optional review gates, `composition_previsualization_policy`, format, aspect ratio (`16:9`), total duration, generation duration (beat-driven; maximum 15.0 seconds per job), target models, visual mode, generation availability, content boundaries, assumptions, and open questions. Every final video, reference card, scene view, shot anchor, storyboard and prompt uses `16:9`; only the three non-delivery `PREVIS` images per selected sequence use `21:9`.

### `01-book-map.md`

Map chapters/sections, characters, settings, events, causal changes, motifs, locators, and ambiguity. Include coverage notes showing what was and was not read.

Then include the world inventory for every adapted chapter, built line by line from the primary text per `text-world-inventory.md`:

```text
Locator | Wording in the text | Category | Visual consequence | Label | On screen?
```

Categories are place, attendee, speaker, phenomenon, object, action, time/causality, and scale. Enumerate attendee categories one row each; never collapse them into “a crowd.” Every row is either assigned a screen presentation layer — distinct individual, midground group, distant silhouette, light-and-shadow implication — or marked an explicit omission with a reason.

### `02-research-dossier.md`

Include timeline, setting-versus-composition distinction, evidence matrix, source cards, material-culture notes, iconography, customs, anachronism blacklist, and uncertainty ledger.

Add one `ASSET-EVIDENCE-CARD` for every planned character, scene, prop, top-down plan, multi-angle card and shot anchor, per `asset-evidence-gate.md`. The card gives exact text locator, production interpretation layer, all visible claims with source IDs/limits, uncertainty, `PASS`/`HOLD`/`CONFLICT` evidence result and separate generation/QA/use states and post-generation comparison. No asset prompt may be written before its card is `PASS`.

Add one visual-evidence card per form-locked object, per `visual-evidence.md`:

```text
Object ID and name | Search names (original language / scholarly / English) | Sources with collection IDs, dates, URLs, access dates | Tier |
Period and region | Countable features as exact numbers | Silhouette and proportion | Material and workmanship | Handling |
Form-lock string (Chinese, reusable verbatim) | Negative string (commonly generated wrong forms) | Label | Confidence
```

At least two independent attributable images per object. Retail listings, film stills, game/anime designs, and AI images are tier `D` discovery aids only and never form evidence.

### `03-adaptation-plan.md`

For every candidate scene include score breakdown. For selected scenes include:

```text
Sequence ID and title
Text locator and evidence IDs
Setup → turning action → consequence
Theme and emotional change
Characters, location, props
Duration and clip division
Dialogue/narration strategy
Historical/iconographic risks
Creative changes and justification
Required assets
```

Before making cards, include a dual-track proposal unless `production_track` was explicitly narrowed: `NARRATIVE` and `DOCUMENTARY` each get logline, theme/question, duration, 3–5 sequence plan, evidence/fiction boundary, asset risk, and selection decision. The selected track becomes the sole production authority; if both are requested, use distinct `N-` and `D-` prefixes for beats, assets, and shots.

### `14-screenplay.md`

Follow `screenplay-workflow.md`. Start with the chosen `production_track`, version, text edition, intended duration, and script-to-shot change log.

For `NARRATIVE`, deliver a Chinese standard screenplay with sequence function, `内/外景 地点 — 时段` scene headings, observable action, performable dialogue, source locator, inventions marked `CREATIVE`, sound/voice-over boundary, required assets, and a `SCRIPT-BEAT-ID → SHOT-ID` map.

For `DOCUMENTARY`, deliver an evidence paper edit and standard documentary script. Every segment states center question, claim status, source locator, visual source type, interview/sync, narration, AI reconstruction label/boundary, uncertainty or counterevidence, assets, and `SCRIPT-BEAT-ID → SHOT-ID` map. Generated reconstruction is always labeled `AI_RECONSTRUCTION` and may not be presented as archive, news, or a witnessed event.

For narrative adaptations, start with a `SOURCE-TO-DRAMA` table from `dramatic-engine-and-short-drama.md`; each scene carries its engine card: POV, goal, opposition, strategy, value start/end, turn trigger, choice, cost, and exit question. Every story-film, documentary, short-drama or motion-comic opening/return segment has an `OPENING-PROMISE-CARD` from `opening-promise-design.md`: `OPENING-PROMISE-ID`, one primary `OPENING-MODE`, audience question, first visible fact, 0–3s cause/effect, payoff mapping, source/creative boundary and first-shot handoff. `AI_SHORT_DRAMA`/`MOTION_COMIC` episodes additionally carry `HOOK-ID`, 0–3s visual hook, promise/payoff deadline, value turn, end-hook consequence, `16:9` read order, and dialogue/AI-action constraints.

### `17-series-bible.md`

Record the selected dramatic lenses, premise, central dramatic question, story/season promise, protagonist desire versus need, opponent system, stakes, irreversible costs, relationship arcs, phase/act map, and ending promise. For episodic work, add a map with `EP-ID`, A/B line function, inherited hook, opening 0–3s hook, payoff or transformation, turning choice, emotional end state, end-hook consequence, and next-episode obligation. Keep `HOOK-ID` and `SCRIPT-BEAT-ID` stable through rewrites.

### `18-screenplay-qa.md`

Run the gates in `dramatic-engine-and-short-drama.md` before asset creation. Report whether every source unit was adapted rather than transcribed; scene goal/opposition/strategy/turn/choice/cost; hook promise/payoff; reversal causality; dialogue subtext; series/episode continuity; and final-form/AI feasibility. Log F21–F27 evidence, one changed variable, and the re-review result.

### `19-cinematography-transition-plan.md`

Follow `cinematic-shot-bridging.md`. For each `SEQ-ID`, record its dramatic question, one de-named camera language, axis/set map, first-eye landing point, camera energy, light policy and sound motif. For every `SHOT → SHOT` edge, record:

```text
FROM-SHOT | TO-SHOT | previous approved end-frame asset | shared vector | exactly one bridge |
incoming 0.0s information | audio bridge/source/timing | next required first frame | model/post responsibility | QA
```

`shared vector` must be a concrete action, composition, eyeline/axis, light/environment or sound fact present at both ends. A sequence may choose a static camera language; do not prescribe movement merely to make it look cinematic. A movement must state a visible trigger, path, stop and resulting new information. Mark unverified cuts, dissolves, wipes and J/L bridges `后期制作`.

### `20-director-design.md`

Before character, scene, or shot assets, write one `DIRECTOR-DESIGN-CARD` for the selected production track. It must state the intended audience experience, controlling POV, central dramatic/evidence question, emotional and rhythm curve, visual/sound motif, `16:9` composition policy, camera and performance policy, production/action limits, and evidence/style conflicts with their resolutions. Add one compact `SEQ-RHYTHM-CARD` per sequence: sequence purpose, start/end value, pressure escalation, reveal/decision point, rest/aftermath, and handoff. This file cannot introduce a historical claim, prop, costume, architecture, character fact, or model ability that is absent from its upstream evidence/asset record.

### `21-shotlist-9col.csv`

Optional export only. It has exactly these nine columns:

```text
sequence_id,shot_id,time_range,dramatic_job,visual_action_and_blocking,camera_and_composition,sound_and_dialogue,asset_and_continuity_contract,bridge_and_post_responsibility
```

Every row must cite an existing `SCRIPT-BEAT-ID`/`SHOT-ID`, duration ≤15.0 seconds, approved reference assets, and the exact incoming/outgoing state. It is a compact human production view; the source of truth remains `14-screenplay.md`, `07-storyboards.md`, `08-video-prompts.md`, and the reference asset map.

### `22-composition-triptychs.md`

For each selected `SEQ-ID`, write the three `PREVIS-SEQ-xx-01`/`02`/`03` contracts and prompts from `cinema-composition-overlay.md`, their upstream asset/evidence IDs, generated/PROMPT_ONLY result, inspection findings and one `PREVIS-DECISION-SEQ-xx`. The decision records only adopted viewing-position, composition-pressure, eye-flow, color-thesis, camera-position/optical and anti-template fields. It must explicitly state that no `PREVIS` file is a delivery asset or an input to a final image/video prompt.

### `23-seedance-2x-compiler.md`

Create this file when Seedance/即梦 is a requested target; otherwise state `NOT REQUESTED` and leave the generic adapter authoritative. For each `SHOT-ID`, record one `SEEDANCE-2X-COMPILER-RECORD` from `seedance-2x-workflow.md`: exact verified model and UI/API surface, official capability-source URL/access date, selected mode, submitted aspect ratio `16:9`, requested duration, canonical prompt source, `@` upload sequence with one role and exclusion per asset, paste-ready Chinese submission prompt, timecode plan, expected final state, continuation/transition operator action, and QA result.

Only approved, real final assets, their registered/inspected clean crops and an actual prior approved video may appear in the upload map. `PREVIS`, geometry plans, review boards, non-existent future assets, and a previous clip described only in text are invalid inputs. Any unverified model name, token syntax, reference limit, duration mode, native audio, continuation/editing feature, or transition is marked `NOT DOCUMENTED`/`后期制作`, never guessed.

### `04-style-bible.md`

Define medium, realism, camera/lens family, depth-of-field logic, lighting, exposure, palette, texture, environmental behavior, supernatural rules, aspect-ratio composition, and global exclusions.

If a director, classic film, movement, or genre is requested, add one `STYLE-PROFILE-xx` with the analysis reference, use boundary, narrative bias, lens set, shot-size bias, `16:9` composition, allowed/avoided moves, motion budget, light, palette, texture, editing, sound, performance, and style-specific negatives. Include a de-named Chinese generation block and one neutral-versus-overlay comparison. State all conflicts resolved in favor of history or text. If no visual style is supplied, record `DEFAULT-GROUNDED-DRAMA` from `default-grounded-drama-baseline.md`, its scope and exclusions, then compile it to visible parameters rather than treating it as a named-style prompt.

### `05-character-bible.md`

For each character include `ASSET-EVIDENCE-CARD` ID and `PASS` result, selected production interpretation, identity and evidence, observable facial/body traits, age, expression range, grooming, wardrobe layers and construction, materials/colors/wear, accessories, footwear, props, `PERFORMANCE_BASELINE` (gaze, posture, breath, hand-rest habit, pressure micro-action and avoided habit), per-shot `FACE_INTEGRATION_LOCK` (scene light, face shadow topology, material separation, edge color/depth), performance rules, continuity anchors, negative rules, generated-file links, and QA. Keep `IDENTITY_LOCK` separate from variable performance state and from scene-specific portrait light. Do not convert a textual social category or later devotional image into historical physical facts.

Write exactly two prompts per principal character, each producing one whole-page card in a single generation:

1. `CHAR-<nn>-PROFILE-CARD` — 16:9. Left 36%–42%: heading `角色资料卡` and one large head-and-shoulders identity portrait whose face fills over half the zone height. Right 58%–64%: heading `三视图` and three equal-height full-body views in front, strict 90-degree side, and back order, feet uncropped. One shared warm-neutral page background, one shared light direction, no other text.
2. `CHAR-<nn>-EXPRESSION-CARD` — 16:9. Header line `表情参考 | EXPRESSION REFERENCE`, then a `3×2` grid of six head-and-shoulders close-ups, each in a thin rounded frame with a two-line centered caption: short Chinese expression name above, all-caps English name below. Drop to `2×2` only when the delivery resolution cannot keep a single face inspectable.

Both cards are deliverables and source assets; model inputs may be approved internal crops. Do not write prompts for standalone face, turnaround, single-expression, garment, prop, or low-density two-zone files, and do not deliver them.

Avoid moralized physiognomy. Do not encode virtue or villainy as ethnicity, disability, skin color, or facial “defect.”

### `06-scene-bible.md`

For each scene include:

- `ASSET-EVIDENCE-CARD` ID, `PASS` gate, production interpretation and visible-claim/limit table;
- historical/evidence basis;
- `SCENE-<nn>-PRODUCTION-DESIGN-BREAKDOWN`: narrative task/evidence question, immediate goal, obstacle/threshold, entry/exit, hero/action prop or declared no-prop alternative, functional set-dressing clusters, practical-light story role, environment pressure and inspectable end state;
- canonical state and coordinate system, described in text only;
- `SCENE-<nn>-SPATIAL-LOCK`: boundary/opening topology, reference wall/axis, fixed-landmark and visibility tables, actor zones, V01–V09 station table and prohibitions;
- named primary landmark chosen for cross-shot recognizability;
- fixed landmark table with position, orientation, dimensions/relative scale, material, and state;
- time, weather, practical/natural light sources and directions;
- actor zones and the nine camera stations used by the default delivery card;
- continuity exclusions and angle-to-shot map;
- generated-file link and geometry QA.

After `SCENE-<nn>-SPATIAL-LOCK` passes, write one prompt per scene producing `SCENE-<nn>-MULTIANGLE-CARD` in a single generation: 16:9, a `3×3` grid of nine edge-to-edge views of the same location, 2–6 px dividers, no page margin, and zero text of any kind. The cells are V01 entrance/primary-landmark, V02 left relationship wide, V03/V04 action A/reverse, V05/V06 action B/reverse, V07 relational wide, V08 threshold and V09 safe insert/opposite-side. The primary landmark must be recognizable in at least six cells; each cell preserves two other declared visible relations; time, weather, materials and light direction stay identical; fixed objects may be occluded but must not move, duplicate, mirror, rotate without cause or change material.

The card is the deliverable and the model input. An unlabeled 16:9 `SCENE-<nn>-GEOMETRY-PLAN` is mandatory after the production-design breakdown and text spatial lock and before the card: generate, inspect and approve it as the card's intermediate topology reference. It must carry the approved hero/action-prop positions, actor routes, meaningful empty zones and practical-light relation without labels. It remains a non-delivery, non-video-input QA artifact and cannot replace the card; a rejected/missing/`PROMPT_ONLY` plan blocks the card and downstream shots. Do not produce annotated maps, standalone masters, standalone directional views, region guides, or annotated detail images. When a shot needs a local insert, describe the region in text and crop it from the approved Vnn card cell.

### `07-storyboards.md`

Begin each shot with its purpose, exact duration (≤15.0 seconds), chapter-absolute time range, source locator, shot anchor, references, continuity contract, `ACTION-PROP-BEAT`, inspectable end state, and transition. The beat states target/hero-prop initial state (or stated no-prop pressure), preparation, obstacle, visible change, aftermath and terminal prop/space state. Opening/return clips also list `OPENING-PROMISE-ID`, main mode, viewer question, 0–3s visible cause/effect, payoff deadline and next-shot handoff. Plan the entire sequence before refining jobs by their actual dependencies. Then include a panel table:

```text
Panel | Time | Shot/lens/angle | Focus & depth | Camera movement (trigger/path/stop) | Blocking/action | Expression/performance | Light/color | Audio | Incoming bridge / outgoing handoff | Continuity/no-drift | Asset/prompt
```

Use six sampled rows per generation job, with each row's cinematic SHOT-ID. Time ranges must cover `[0, duration]` exactly with no gap or overlap. Duration must not exceed 15.0 seconds.

Also record per panel: `SCRIPT-BEAT-ID`, `EP-ID`/`HOOK-ID` when applicable, dramatic beat, shot job (`改变情绪`/`推进行动`/`增加压力`), environmental pressure, body micro-action, motif/sound anchor, first eye landing point, movement trigger/path/stop, screen direction, incoming shared vector, exactly one cut/transition method, outgoing first-frame contract, post-production responsibility, and reference asset IDs. For a short-drama/motion-comic opening, explicitly audit the 0–3s visual hook, payoff deadline, `16:9` read order and subtitle/post-production boundary. A panel is an audit state and does not require an actual edit.

The panel table is a document artifact. The image deliverables for each clip are exactly two files: a clean unlabeled `SHOT-<nn>-ANCHOR` and one `SHOT-<nn>-CONTACT` `3×2` sheet generated as a whole page. The six cells retain one locked set and continuous camera language, while at least three show a checkable person–prop or person–space state change; a motivated move or full-body blocking is permitted. Verified NATIVE_MULTISHOT jobs may include explicit cuts; keep each internal shot's geometry and cross-cut continuity inspectable. Do not deliver individual panel files.

### `08-video-prompts.md`

Every job gets an internal audit covering the canonical fields in `prompt-spec.md`, in this order:

1. 镜头标识：ID、`SCRIPT-BEAT-ID`、`EP-ID`/`HOOK-ID`/`OPENING-PROMISE-ID`（如适用）、用途、精确时长（≤15.0 秒）、章内绝对时段、文本定位；开场/回归段另写主开场模式、观众问题、0–3 秒可见因果、兑现期限和纪录片来源边界；
2. 参考素材：写在提示词正文内，逐条给资产 ID、文件名、唯一职责，以及不得从该图取用的内容；
3. 固定事实：身份串、服装、道具形制串（含确切数字）、4–8 个地标、时间与主光方向；
4. 格式：画幅、分辨率目标、时长；
5. 景别与摄影机：景别名称、焦段、机位高度与角度、主体占比、对焦目标、景深；
6. 运镜：起落幅、运动类型、幅度速度缓动、触发与停止条件；固定机位时明确写出；
7. 环境与氛围：处所、云雾烟尘的分布与流速、空气透视、背景群体层级、禁止的地域元素；
8. 分时段节拍：每段同时含景别、运镜、动作、表情视线、环境响应、声音或对白，以及人物—关键物/空间关系的可检查状态；
9. 对白与声音：逐字台词、说话者、语气语速口型，或明确写“无对白”并给旁白与环境声；
10. 表演：眨眼、呼吸、重心、手部张力、视线转移；
11. 负向约束：通用禁漂移串加本片专用否定串；
12. 真实感物理合同：可见光源与材质响应、接触/支撑/重心、准备—受力—余波、环境时间层、摄影限制和声源；近景另写 `FACE_INTEGRATION_LOCK`，使脸部阴影、材质、边缘色温和景深服从当前场景，而不迁移资料卡棚拍光；
13. 跨视频承接与转场：上一镜批准终帧、恰一种接入方式、共享向量、声音桥、出口/下一镜首帧合同和模型/后期责任。
14. 终帧状态：供下一镜逐字抄写。

The `参考素材` section is the complete `【参考生成资产】` block from `reference-asset-ledger.md`: each item must give its asset ID, actual filename/path, status, one role, unique job, frozen fields, “must not transfer” details, upload order, and source chain. Repeat this block in anchor, contact-sheet, storyboard-panel, and video prompts.

Then add one named-model adapter per requested model, plus continuation instructions that restate the prior clip's approved final frame verbatim.

Later submissions are independently complete, with length proportional to the job. Compressing `SHOT-02` or `SHOT-03` into a continuation note, or omitting references, shot size, camera movement, environment, dialogue, or negatives because they were stated earlier, is a delivery failure.

Prepend a compiler record for each model: verified surface, selected `P1`–`P4` prompt shape, reference roles, preserved hard constraints, capability-driven splits/post work, official syntax source, and likely failure codes.

### `09-model-capabilities.md`

Use:

```text
Requested name | Verification status | Exact official name | Official source | Checked date | Inputs | Duration | Resolution/aspect | Audio | Reference limits | Prompt/control notes | Fallback decision
```

Do not guess missing cells. Write `NOT DOCUMENTED`.

### `10-sources.md`

List text editions, historical sources, collection objects, official model documentation, and access dates. Keep claim support clear.

### `11-quality-report.md`

Report generated/prompt-only/rejected counts, screenplay-track/evidence integrity, source-to-drama and opening-promise/payoff coverage, reference-lineage coverage, historical uncertainties, anachronism audit, character continuity, scene geometry, filmable production design, storyboard timing/action-prop state changes, camera-language and bridge-chain review, model verification, dramaturgy, physical realism, `PERFORMANCE_BASELINE`/trigger/response and `FACE_INTEGRATION_LOCK` review, visual inspection findings, failed assets, and remaining risks. For each failure include `F01`–`F63`, observed evidence, probable cause, one changed variable, retry result, and escalation decision.

### `12-continuity-bible.md`

Store only frozen strings and auditable state:

- character identity, hair, wardrobe layers, props, injuries/wetness/dirt;
- scene coordinate and landmark strings, time/weather/light state;
- screen direction, eyeline, camera height, lens feel and palette;
- each shot's start state, approved end state and final-frame asset;
- declared state transitions such as time jump, costume change, door opening, object transfer or weather change.

Copy frozen Chinese strings verbatim into prompts. Do not paraphrase them per shot.

### `13-sound-edit-plan.md`

For every sequence include:

```text
Time | Shot/source clip | In/out state | Cut/transition reason | Eye-trace/screen direction |
Dialogue/voice-over | Ambience | Foley | Music | Silence | J/L-cut or sound bridge |
Continuity risk | Required pickup/repair
```

Separate sound that a verified model can generate from sound requiring post-production. Protect the sequence's motif and intentional silence. Do not invent copyrighted dialogue, lyrics, score cues, or unlicensed recordings.

When BGM analysis, prompt preparation, or generation is explicitly requested, add one `BGM-BRIEF` and one `BGM-GENERATION-RECORD` for each affected sequence using `background-music-workflow.md`. The record contains its source document versions, `STYLE-TRAIT-CARD`, prompt path/hash, requested and actual duration, tool/model, trigger status, resulting `BGM-ID`, audio QA and mixing decisions. `PROMPT_ONLY` is a valid final status; do not create a music file merely because this document exists.

### `15-reference-asset-map.md`

Use the table contract in `reference-asset-ledger.md`. For each `SCRIPT-BEAT-ID` and `SHOT-ID`, map upstream reference assets (with role and upload order) to the generated output asset and QA result. No missing filename/status, rejected reference, cyclic chain, or role conflict is allowed.

### `16-realism-qa.md`

For every approved shot, record the physical realism contract and its inspection result: source light/material response, contact/support/weight, action phases and inertia, slow/fast time layers, optics/focus/camera, and acoustic space. Log `F16`–`F20` repairs with one changed variable.

## 4. Asset quantities

Exact delivered image count unless the brief narrows it:

- one style bible;
- each principal character: exactly 2 images — 1 `PROFILE-CARD` + 1 `EXPRESSION-CARD`;
- each recurring scene: exactly 1 image — 1 `MULTIANGLE-CARD`;
- each qualifying form-locked prop: at most 1 image — 1 `PROP-<nn>-CARD`, only when the gate in `visual-evidence.md` is met;
- each production look: at most 1 clean color/style card, only when color matching matters;
- each continuous clip: exactly 2 images — 1 `SHOT-<nn>-ANCHOR` + 1 `SHOT-<nn>-CONTACT`;
- each selected sequence: exactly 3 separate non-delivery `21:9` `PREVIS-SEQ-<nn>-01`/`02`/`03` images when image generation is available; otherwise exactly 3 `PROMPT_ONLY` records. They live only in `process/cinema-triptychs/`, are excluded from all delivery counts and may never be used as image/video-model inputs;
- one manifest row for every delivered asset, including prompt-only assets.
- one frozen continuity record per recurring character, location and prop, plus one start/end-state record per clip;
- one sound/edit timeline per selected sequence, even when all audio is marked for post-production.

A two-character, one-scene, three-clip package therefore still delivers 4 + 1 + 6 = 11 images; a selected sequence adds exactly three non-delivery `21:9` `PREVIS` files only. Any other file beyond this contract must be a declared additional character/scene/clip or a retry artifact in `reports/retries`. Secondary characters who never appear in a close shot get a text card only, no image.

Generate a large cast in tiers. Principal characters receive the full set; supporting characters receive only what their visible shots require; crowds receive archetype sheets and variation rules.

## 5. Delivery gates

- No asset is orphaned: each maps to a shot or declared reusable purpose.
- No shot is under-specified: purpose, ≤15s duration, six-panel table, anchor, contact sheet, references, light, audio status, and inspectable end state exist.
- No generation job exceeds 15.0 seconds; only submissions with missing actual dependencies remain DEFERRED. Full-sequence plans may precede generation.
- No generated image is accepted without visual inspection.
- The delivered image count matches section 4 exactly; no process image ships.
- Each selected sequence has exactly three separately generated or `PROMPT_ONLY` `21:9` `PREVIS` records and one inspected `PREVIS-DECISION`; no `PREVIS` file is in `delivery/`, appears in a final prompt reference ledger, or is uploaded to a video model.
- Every card obeys its layout contract: profile card has two headings only, expression card has one header line plus per-cell bilingual captions, scene card has zero text.
- Every face inside a card is inspectable at delivery resolution; no face is reduced to a thumbnail.
- Identity holds across the profile card portrait, its three turnaround views, and all expression cells.
- Every planned asset has a traceable `ASSET-EVIDENCE-CARD`, `PASS` gate, selected production interpretation and post-generation comparison; no `HOLD`, `REJECTED` or unsupported `INFERENCE` asset enters a card, prompt or shot.
- Each recurring scene has an approved text `SPATIAL-LOCK`; the scene card's primary landmark appears in at least six of nine cells with one light direction, and every Vnn remains consistent with its landmark visibility table.
- Retry artifacts stay in `reports/retries` and never appear in `delivery/`.
- Every visible element of a scene card traces to a world-inventory row or carries a `CREATIVE` label; no textually prominent attendee, phenomenon, or place silently disappears.
- Every form-locked object has two independent attributable images, exact counts, a form-lock string, and a negative string, and its countable features were counted against the delivered image.
- No historical assertion lacks a citation or an inference label.
- No named model receives invented capabilities.
- Every internal audit covers applicable canonical fields, with the complete prompt-embedded reference asset block, 景别, 运镜, environment/cloud behavior, dialogue-or-`无对白`, negatives, physical realism contract, cross-video bridge, and end state written inside the prompt body.
- Every beat line states shot size, camera movement, action, expression, environment response, and audio.
- Submission constraint_map covers all hard requirements without relying on earlier prompts. Different word counts are acceptable.
- `19-cinematography-transition-plan.md` gives every `SHOT → SHOT` edge one de-named sequence camera language, a move trigger/path/stop when applicable, at least one shared vector, exactly one primary bridge, and a model-versus-post-production boundary.
- `20-director-design.md` is locked before asset creation and contains no fact outside approved text/evidence/creative labels; its sequence rhythm cards agree with the selected screenplay track.
- When requested, every `21-shotlist-9col.csv` row is an export of an approved `SCRIPT-BEAT-ID`/`SHOT-ID`, preserves the ≤15-second limit, and names its assets, state and bridge; it never becomes a substitute source of truth.
- The selected screenplay track is complete and maps every script beat to shots; story-film inventions and documentary reconstructions/claims are visibly labeled.
- Every asset, beat, storyboard and prompt is traceable through the reference asset map; source light, contact physics, motion follow-through, stable optics, and sound space pass the realism QA.
- Each visible principal performance records baseline → trigger → smallest reaction → selective development/suppression → stable end state; identity fields never change to simulate emotion, and blink/gaze/breath behavior is non-mechanical and compatible with the shot size.
- Every close-shot face uses the current scene's light and depth: profile/expression cards lock identity/performance only; `SHOT-xx-ANCHOR` verifies face shadow topology, material separation, edge color and exposure against the scene before video generation.
- Narrative source units are transformed through `SOURCE-TO-DRAMA`; every scene has goal, opposition, strategy, value turn, choice and cost, not a prose transcription.
- `AI_SHORT_DRAMA`/`MOTION_COMIC` episodes pass the 0–3s hook, promise/payoff, earned end-hook, `16:9` readability, and generative action-budget gates in `18-screenplay-qa.md`.
- If the user supplied no style, every prompt uses the de-named `DEFAULT-GROUNDED-DRAMA` parameters while preserving text/evidence and user-constraint priority; black field, occlusion, sound bridge and motivated-rush effects name their reason, shared vector and post-production boundary.

## 6. Current execution files

`active-release.json` follows production-execution.md; it is the current version/file authority, separate from the archival asset-manifest.csv. New manifest CSVs also have evidence_status, generation_status, qa_status and use_status columns; old status remains a legacy field, not approval.

`24-precut-review.md` records the whole-sequence rough shot/sound timeline, timing review or actually viewed animatic, story comprehension, opening payoff, repetition and repair. Mark placeholders as temporary, never approved model inputs.

`25-video-result-qa.md` follows video-result-qa.md and records real video metadata, full-view coverage, observed actions/cuts, defects, usable ranges, actual end state and bridge preview results. The overall quality report identifies the active release and pending post work.

Run `python scripts/validate_release.py <project>/active-release.json` before submitting active jobs. It reads only and reports structural errors; it cannot approve images, movie quality, official capability claims or inferred events. An empty new project is a scaffold, not submission-ready.

## 7. Optional per-video dashboard

Only when the user explicitly requests dashboard generation or refresh, read [dashboard-workflow.md](dashboard-workflow.md). Do not create dashboard files during ordinary initialization, production, QA or delivery.

On request, create `dashboard-map.json` with explicit scene/episode/video numbering and file/excerpt ownership, then generate `reports/boards/index.html`, one HTML page per video unit, and `dashboard-generated.json`. Display script breakdown, script detail, director notes/blocking, assets, storyboards, prompts, sound/edit records, QA and other files. Shared documents and the complete workflow file inventory remain accessible and visibly distinct from per-video content. Missing or unmapped material is labeled; a dashboard cannot approve it. The optional pages do not alter official image counts or become model inputs. Output is a local snapshot, not an automatically hosted website.
