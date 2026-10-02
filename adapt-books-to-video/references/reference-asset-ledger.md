# 参考生成资产台账与提示词标注

## 1. 一图一职、一镜可追溯

所有送入图像或视频模型的参考图片必须先登记为资产；每张图只能有一个首要职责。每个生成资产还必须先关联一张 `ASSET-EVIDENCE-CARD` 和 `EVIDENCE-GATE: PASS`。不要把未批准的草图、带大量文字的审核页、拼贴灵感板或无来源网络图直接塞入生成模型，也不要用提示词补全证据卡未允许的细节。

在 `15-reference-asset-map.md` 和 `asset-manifest.csv` 为每个资产补充下列字段：

```text
asset_id | filename/path | type | status | origin | source/evidence locator |
evidence_card_id | evidence_gate | production_interpretation | verification_date |
approved_from | reference_role | frozen_fields | allowed_crop/zone |
must_not_transfer | used_by_script_beats | used_by_shots | qa_owner | qa_result
```

`origin` 只能为 `GENERATED`、`USER_SUPPLIED`、`LICENSED_OR_ARCHIVAL`、`TEMPORARY_CROP`、`INTERNAL_QA`、`INTERNAL_PREVIS` 或 `PROMPT_ONLY`。`approved_from` 要列出生成该资产时使用的上游资产 ID；没有上游参考时写 `TEXT_ONLY`。`TEMPORARY_CROP` 记录父图与裁切区域，不作为交付物。`INTERNAL_QA` 用于每个 recurring scene 必经的 `SCENE-xx-GEOMETRY-PLAN` 顶视中间参考，必须标明“不交付、不得直接作为视频模型参考”；其 QA 未通过则下游 `SCENE-xx-MULTIANGLE-CARD` 与镜头不得启动。`INTERNAL_PREVIS` 仅用于每个 `SEQ-ID` 的三张 `21:9` 构图预演图，必须标明“不交付、不得作为最终图像或视频模型参考”；它只能输出文字化的导演决定，不得取代任何正式资产或门禁。

## 2. 参考角色词典

- `COMPOSITION_ANCHOR`：只锁定首帧构图、机位、焦段感、屏幕方向与固定地标。
- `IDENTITY`：只锁定人物脸部、体型、发型、服装层次；不得迁移资料卡的中性棚拍背景、光向、高光形状或景深。
- `PERFORMANCE`：只锁定指定表情、视线、`PERFORMANCE_BASELINE` 与可见动作幅度；不得从表情卡迁移网格/标签或光线，不能以它改写身份锁。
- `SCENE_GEOMETRY`：只锁定场景结构、地标关系、时间和主光方向。
- `GEOMETRY_QA`：只核验 `SCENE-xx-SPATIAL-LOCK` 的俯视拓扑；不得迁移文字、标签、构图、人物、风格或当作视频输入。
- `PREVISUALIZATION_ONLY`：只供人工/模型文字化检查观看位置、构图压力、视线流量、色彩命题和反模板化风险；不得作为最终图像、故事板或视频模型输入，也不得将其可识别画面直接复刻进最终资产。
- `PROP_FORM`：只锁定可数形制、材料、持握方式和朝向。
- `COLOR_MATERIAL`：只锁定色彩、反差、颗粒、皮肤/布料/金属等材料响应。
- `EVIDENCE_ONLY`：只用于事实核验；除非记录为可用视觉来源，不得转抄其构图或人物。
- `END_STATE`：只锁定上一镜批准终帧中的姿态、物体状态、视线和空间状态。
- `EVIDENCE_GATE`：不是图像输入；只声明本资产可生成的证据边界、解释层和核验结果。任何非 `PASS` 资产不得继续。

如果同一图片被要求承担互相冲突的角色，拆为不同的裁切或新锚点；不要让模型自行权衡。

## 3. 审计版完整引用块与提交映射

每个资产/视频审计版使用完整块，分镜格可引用该审计块 ID。模型提交版自包含地写实际文件/槽位、职责、冻结项和排除项，来源链/哈希留在上传清单。没有图时明确写 `无图像参考，依据 TEXT/EVIDENCE 生成`：

```text
【参考生成资产】
1. [COMPOSITION_ANCHOR] SHOT-03-ANCHOR.png（资产 ID：SHOT-03-ANCHOR；状态：GENERATED）
   用途：只锁定 0 秒构图、50mm 视角、人物左右位置、镜头高度和四处地标。
   冻结字段：……；不得迁移：字幕、边框、未点名人物、页面排版。
   上传顺序：1；来源链：SCENE-01-MULTIANGLE-CARD → SHOT-03-ANCHOR。
2. [IDENTITY] CHAR-01-PROFILE-CARD.png（资产 ID：CHAR-01-PROFILE-CARD；状态：GENERATED）
   用途：只锁定主角面部、发型、身体比例及服装层次；裁切：左侧肖像区。
   冻结字段：……；不得迁移：标题、三视图网格、背景色。
```

每条都必须有：资产 ID、实际文件名/路径、状态、角色、唯一用途、冻结字段、不得转移的内容、上传顺序、来源链。提示词开头另附 `ASSET-EVIDENCE-CARD`、门禁状态、生产解释层和不得推导项。参考资产不存在、证据门禁不是 `PASS` 或未通过质检时不能写成已生成，改为 `PROMPT_ONLY`/`DEFERRED` 并停止依赖它。

## 4. 生成顺序与资产依赖图

按最小充分集建立依赖：证据/文本 → 角色、场景、道具、色彩卡 → `INTERNAL_PREVIS`（只读出文字决定，不回传图片）→ 当前镜锚点 → 当前镜宫格 → 视频。下一镜优先把上一镜批准终帧标为 `END_STATE`，而不是重复引用所有上游图片。

在 `15-reference-asset-map.md` 以表格列出每个 `SCRIPT-BEAT-ID` 与 `SHOT-ID` 的输入资产、角色、上传顺序、输出资产及 QA 状态。场景引用另写 `SCENE-xx-SPATIAL-LOCK` 与依据 Vnn；一个引用有缺失、状态为 `REJECTED`、来源链循环或 Vnn 不存在时，该镜标 `DEFERRED`。

## 5. QA

验收每一镜时逐项检查：

1. 资产文件真实存在且状态正确；
2. 每张参考图只有一个声明职责；
3. 首帧、身份、空间、道具、色彩和终帧职责没有冲突；
4. 提示词明确禁止复制卡片文字、网格、边框、未点名元素和任何 `PREVIS` 图像；
5. 输出画面实际保持所声明的冻结字段；
6. `asset-manifest.csv`、剧本 beat、分镜表、提示词引用块与资产图互相可反查。

把“未标参考图”“资产 ID/文件名不一致”“将证据图误当风格图”“引用已拒绝资产”“未写不得转移项”都记录为 `F15`。先修台账，再重新生成受影响资产。

## 6. 当前状态与输入派生

状态按 production-execution.md 分列，origin 不等于 generation_status。从批准卡无损裁切时保存到 process/model-inputs/，登记父图 ID/哈希、crop_xywh、输出哈希和 QA；只允许完整保留任务所需特征的区域。默认不上传六格板，仅在准确模型的已核验故事板模式才启用。下一任务只有在需要连续生成时优先使用实际批准尾帧，不能把计划终态或故事板末格当实际尾帧。
