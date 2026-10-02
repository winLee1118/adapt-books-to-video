# 生效版本与制作执行合同

## 1. 生效入口

每个制作项目以 `active-release.json` 固定当前生效要求和文件；`00-brief.md` 解释创作意图。新用户要求先记录，再更新受影响任务。不要以文件名数字、修改时间或旧 QA 的 PASS 自动推定当前资产有效。

清单 schema_version 为 2，基本结构如下（示意，不代表素材已经存在）：

```json
{
  "schema_version": 2,
  "release_id": "R001",
  "requirements": {"aspect_ratio": "16:9", "max_generation_seconds": 15, "dialogue": "UNSELECTED", "narration": "UNSELECTED", "audio_delivery": "UNSELECTED", "bgm_generation": "NOT_REQUESTED"},
  "documents": {"sound_edit": "13-sound-edit-plan.md"},
  "assets": [],
  "jobs": [],
  "edit_segments": [],
  "bridges": []
}
```

- `documents`：用途 → 当前项目内相对路径，例如 screenplay、director_design、capabilities、precut、video_qa；只写真实文件，未创建时不登记。档案旧稿仍可保留。
- `assets` 每项：`id, path, sha256, origin, evidence_status, generation_status, qa_status, use_status, role`；文件未生成时 path/sha256 为 null。裁切另写 `parent_id, parent_sha256, crop_xywh`（父图像素坐标）以及区域说明。
- `jobs` 每项：`id, mode, duration_seconds, model, surface, capability_record, prompt_path, prompt_sha256, input_ids, depends_on, status, shots, expected_end_state, actual_end_state, result_asset_id, review_path`。shots 每项为 `id, start, end, purpose`，时码覆盖生成任务，不要求等分。
- APPROVED 任务另写 `actual_duration_seconds`，必须来自实际视频元数据。`edit_segments`：`job_id, in, out, timeline_start`，采用已验收片段的实际区间，不用请求时长推定素材边界。
- `bridges`：`from_job, to_job, method, status, review_path`；记录画面主桥接和可叠加的声音桥，复核实际拼接。
- `requirements.bgm_generation` 只可为 `NOT_REQUESTED`、`ANALYZE_ONLY`、`PROMPT_ONLY`、`GENERATE_APPROVED`、`GENERATED`、`QA_PASS` 或 `QA_FAIL`。它记录背景音乐工作流的真实状态，不触发生成。真实 BGM 作为 `assets` 中 `role=BGM` 的音频文件登记；其提示词、时长、审听与混音结论写入 `13-sound-edit-plan.md`。

状态相互独立：

| 字段 | 允许值 | 含义 |
|---|---|---|
| evidence_status | PASS / HOLD / CONFLICT | 可见主张与生产解释是否成立 |
| generation_status | PLANNED / PROMPT_ONLY / GENERATED | 文件是否实际产生；用户提供文件经登记也用 GENERATED，origin 保留 USER_SUPPLIED |
| qa_status | PENDING / PASS / FAIL | 是否已检查对应媒体，不由证据状态推出 |
| use_status | ACTIVE / SUPERSEDED / BLOCKED | 当前版本是否允许使用 |
| job status | PLANNED / READY / SUBMITTED / GENERATED / APPROVED / REJECTED | 任务执行阶段 |

READY 之前必须核对输入为证据通过、文件存在、QA 通过且 ACTIVE。视频 APPROVED 另外要求实际结果文件、审查记录、实际终态；文本计划不得填成实际终态。版本变化时标记受影响下游需复核，保留旧记录，不静默更新已提交任务的输入哈希。

历史项目迁移先建候选清单，对照人工最新说明确认文件和要求。`PASS / PROMPT_ONLY` 拆为 evidence_status=PASS、generation_status=PROMPT_ONLY、qa_status=PENDING。不能为通过检查而捏造哈希、资产批准或补填视频终态。

## 2. 单位分层

- `SCENE/SEQ`：场次或叙事序列，负责人物目的、证据问题与整体转折。
- `SHOT`：电影中的一个镜头，负责可见信息、反应、选择、空间或余波。
- `GEN`：一次模型生成任务，≤15 秒，含一个或多个 SHOT；多镜头必须有准确模型/界面能力依据。
- `EDIT`：从实际视频截取的可用区间，允许短于生成时长。

旧 `SHOT-xx` 图片与 ID 不批量重命名；在清单中映射至 GEN 和电影 SHOT。新增项目仍按每个 GEN 两张交付图：首帧与六格板，内部电影镜头不自动增加交付图片数量。六格是抽样状态而非六次剪切。

时长随节拍确定。插入、反应、空间建立无需独立完成整套戏剧弧；场次层面必须有变化。若所需剪辑片段短于模型最小时长，生成合法长度并记录采用区间，不拉长最终剪辑节奏。首三秒要求作用于开场/回归段，不机械重复于每个任务。

## 3. 全段预剪与依赖

先写整个选定序列的粗镜头表、声音结构、桥接和时间预算，再精制资产。`24-precut-review.md` 记录每镜的新信息、入/出点、预期画面、声音、桥接和高风险动作。可用临时图/草图预览节奏，标明不作模型参考；没有实际预览则写 TIMING_REVIEW_ONLY。

预剪检查：无说明能否读懂目标与结果；开场承诺能否兑现；是否重复；人物反应是否有空间；无对白需求是否真的靠动作成立；每次切镜是否有新信息。纪录片按问题/证据推进，不能强塞虚构对抗。

通过后处理当前 GEN。只对依赖真实终态的任务串行等待；独立镜头可先设计或准备。生成后以实际时长、切点和可用区间回写预剪与 13/19 号计划。预剪通过不等于所有精细资产已通过。

## 4. 资产输入与构图

正式交付卡数量、16:9、场景先顶视再九机位以及三张 21:9 PREVIS 均不变。内部 `process/model-inputs/` 可保存从已批准卡提取的干净裁切；`reports/internal-qa/` 保存顶视和检查图；`reports/video-qa/` 保存抽帧与片段检查。

整卡与裁切按可见细节密度、模型支持和实际试片选择。裁切必须保留所需身份/道具/几何信息，记录父版本与裁切区域，检查文字和边框。裁切不能恢复原图没有的细节。首帧充分时不重复塞入所有角色、表情和场景卡。

PREVIS 只转成文字导演决定。正式16:9锚点须重新检查：画面边缘是否丢人物/关键物、眼线是否成立、空间比例和主要信息是否清楚；记录在 22 号文件，不把21:9预演裁切后上传。

## 5. 审计版与提交版

审计版保留证据卡、完整资产台账、脚本版本、生产解释、摄影/表演/真实感、预期终态和来源边界。提交版给模型，只保留会改变可见输出的已批准约束和实际输入引用。

用 `constraint_map` 记录“审计约束 → 提交语句或输入职责”。允许合并重复光线、身份和物理描述，允许不同任务长度不同；禁止遗漏核心动作、人物身份、关键形制、空间关系、声音要求或改编边界。来源编号和审核日期不需要读给模型，但其结论必须转成正确可见内容。

正文要自包含：哪个文件/槽位控制哪个人物或空间、本任务何时发生什么、如何拍、怎么结束、哪些内容不迁移。完整路径、哈希、来源等放上传清单便于操作，不用“见上镜”代替本镜必要事实。指令只要求当前任务内容，不让模型执行后期剪辑备注。

若模型不支持某能力，明确改变任务包装或后期方案；不能为缩短提示词改变导演意图。对同一试片比较原版与简洁版时固定资产和生成设置，分别记录动作完成率、漂移、可用秒数及成本，不能凭字数宣称质量提升。

## 6. 更新 Skill 的发布纪律

工作区是开发源；全局目录是运行副本。同步前比较差异，合并全局独有的有效功能，再对实际变更文件做备份、复制和哈希比对。不要镜像删除目标目录、覆盖未合并改动或改写业务项目的生效清单。
