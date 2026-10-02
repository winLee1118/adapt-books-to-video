---
name: adapt-books-to-video
description: Turn book text or a work title into an evidence-aware Chinese film package with screenplays, researched assets, storyboards, video prompts, and optional prompt-driven BGM planning or generation. Use for adaptations, documentary treatments, script-to-shot production, reference traceability, soundtrack planning, and AI-video realism or continuity repair. Generate any media only when requested and supported.
---

# Adapt Books to Video

把作品转成观众能看懂、能拍摄、能生成、能剪接的故事片或纪录片。采用渐进披露：主入口锁定执行顺序，具体制作方法按阶段读取。

## 跨智能体运行

本技能不依赖本机绝对路径或专有插件。支持 `SKILL.md` 的智能体可直接读取入口并按需读取相对路径资源；不支持自动发现的宿主，可在任务中明确要求读取本目录的 `SKILL.md`。脚本使用 Python 3.10+ 标准库，路径相对于技能目录解析，输出写入用户指定的项目目录。

先检查宿主可用的文件、检索、图片、视频、音频和剪辑工具。仅执行真实可用且已授权的操作；没有生成工具时交付 `PROMPT_ONLY` 包。文档中的工具与模型名称是能力适配目标，不意味着它们随本技能安装。当前模型的接口、限制与版本需使用官方资料或实际入口核验。

## 当前执行合同

- 用户当前明确要求优先于默认值。先读取项目 `active-release.json` 与 `00-brief.md`；没有清单时从实际记录核对并建立，不能凭文件名最高版本号选资产。
- 本入口、[production-execution.md](references/production-execution.md)、[clip-sequencing.md](references/clip-sequencing.md) 是生产调度的现行规则。历史参考页中的“每条必须完整十四节、后镜不得更短”只适用于内部审计覆盖；“一镜到底、逐镜才能规划、整卡必须上传”不再作为通用限制。
- 所有正式图片资产和最终视频保持 `16:9`，单次生成任务 ≤15 秒。时长随内容选择，15 秒不是默认节奏。电影镜头、生成任务与剪辑片段分别记录。
- 每个主要角色交付资料卡和表情卡；每个复用场景交付一张无字九机位卡；每个生成任务交付首帧锚点与一张六格故事板；用户选择结构参考模式时，单幅可改为白描开场构图图，不作为严格首帧。中间裁切、尾帧、测试素材不增加正式图片交付数量。
- 场景先有生产设计拆解、文字空间锁和已验收的无字顶视图，再生成九机位卡。门洞两侧体量、承重点、动线与道具用途必须可解释。
- 每个选定序列保留三张独立 `21:9` PREVIS 中间图；只提取文字导演决定，再在正式 `16:9` 锚点复核。PREVIS 与顶视 QA 图不得上传最终视频模型。
- 所有描述性提示词使用中文；模型名、实际接口字段、资产 ID 和来源原文保留必要字面内容。
- `TEXT / HISTORY / ICONOGRAPHY / INFERENCE / CREATIVE` 分开。考证核验可见主张；演员外貌是 `CASTING_CHOICE`，不从社会、种姓、族群或宗教名称推导。
- `evidence_status`、`generation_status`、`qa_status`、`use_status` 分列。无生成能力不影响证据可通过；缺失图片只阻止依赖真实图片的生成，不阻止标明尚未就绪的文本规划。
- 完整来源链和制作记录保存在审计版；提交版必须自包含地明确资产引用、视觉硬约束、动作时序、运镜、声音与终态，可合并重复说明。不得按字数或小节数评价模型提示词。
- 身份卡锁人；剧情锚点锁本场光线、材质、景深与脸部整合。表演由注意力和触发带动，不安排机械眨眼循环。
- 摄影机运动要有动机、路径和停止条件；固定机位也是有效选择。镜头只需完成其叙事任务，不强制每个反应/空镜都有独立反转。
- 未指定风格时使用 `DEFAULT-GROUNDED-DRAMA` 的可观察参数；已指定神话电影、无对白或其他风格时服从当前项目选择。导演/影片参考只用于提取摄影和叙事方法。
- 模型能力按准确版本和实际 UI/API 核验，不从其他平台迁移控制项。未验证写 `NOT DOCUMENTED`，不可把提示词意图声称为执行保证。
- 生成、上传、导出只在用户已授权范围内执行；无可用生成工具时交付明确的提示词包，不宣称成片通过。
- 背景音乐是按需工作流，不是默认生产步骤。只有用户明确要求“生成/制作/提交 BGM（配乐）”时才可调用音乐生成入口；其余情形仅完成分析、推荐和待发送提示词，状态为 `PROMPT_ONLY`。

## 阶段 1：需求与生效版本

读 [production-execution.md](references/production-execution.md)、[output-spec.md](references/output-spec.md)。
锁版本/译本、改编范围、受众、总片长、制作轨道、风格、声画要求、模型入口与交付范围。
从用户当前要求与 `project-config.json` 解析导演风格输入：`director_or_classic_film_reference`（CLI `--style-reference`）、`style_compilation_mode`（`--style-mode`）与 `genre`（`--genre`）。已有项目优先沿用生效风格；当前明确变更则记录影响范围，不重新初始化或静默混用旧风格。具体字段与模式见 [director-style-overlays.md](references/director-style-overlays.md)。
明确选择故事片或纪录片时直接沿用；只有确实未定时才简要给双轨提案，不重复询问已接受的选择。
`production_track` 区分叙事/纪录；`production_form` 区分媒介；`format_route` 区分总篇幅。
真人中式神话故事片另外读取 [production-type-and-mythic-film.md](references/production-type-and-mythic-film.md)，保留 `production_type`、`MYTHIC-WORLD-CARD` 与已选图像传统。
初始化只创建新项目，不改写旧项目内容或批准状态。

## 阶段 2：文本、戏剧与证据

读 [research-and-integrity.md](references/research-and-integrity.md)、[text-world-inventory.md](references/text-world-inventory.md)、[screenplay-workflow.md](references/screenplay-workflow.md)、[dramatic-engine-and-short-drama.md](references/dramatic-engine-and-short-drama.md)。
先定位正文、事件、人物和重要世界元素，再写故事承诺、人物目的、阻力、选择、代价和结果；不能逐段平移小说。
读 [opening-promise-design.md](references/opening-promise-design.md) 和 [screenwriting-directing-overlay.md](references/screenwriting-directing-overlay.md)，通过开场承诺与剧本可拍性检查。无对白项目应靠可见关系和行动建立因果，不把信息偷偷改成旁白。
细致资产考证随已选场次推进，先查核心身份、历史时空和关键物件，不在未选场景上铺满资料卡。
资产生成前读 [asset-evidence-gate.md](references/asset-evidence-gate.md)、[identity-and-setting-evidence.md](references/identity-and-setting-evidence.md)、[visual-evidence.md](references/visual-evidence.md)。
核心历史/宗教形制严格查证；背景按可辨程度与主张风险研究。创作动机、调度和摄影标为创作，不伪装成史实。
纪录片先做证据 paper edit；档案、采访、观察和 AI 重建分别标识，不虚构采访原话或历史现场。

人物驱动场景从剧本阶段开始读 [actor-performance-workflow.md](references/actor-performance-workflow.md)：以PERF-ID贯通角色行动目标、接收与回应、导演台、表情卡、六格故事板、提交提示词和实片表演QA。全景按身体与关系验收，近景才控制面部细节；“克制”不能替代可见表演。

## 阶段 3：导演与整段预剪

读 [directing-and-dramaturgy.md](references/directing-and-dramaturgy.md)、[cinematic-shot-bridging.md](references/cinematic-shot-bridging.md)、[clip-sequencing.md](references/clip-sequencing.md)。
在大量精制资产之前，锁导演设计并完成整段粗镜头表、声音结构和预剪时码。
已指定导演、电影、流派或自定义方法时，先读 [director-style-overlays.md](references/director-style-overlays.md)，在 `04-style-bible.md` 建立一个主 `STYLE-PROFILE` 完整参数合同，再落实到 `20-director-design.md`、镜头表、资产与提交提示词。没有风格输入时读取默认写实基线；风格合同在实片 QA 中复核，不能只记录参考名称。
允许先规划所有镜头，采用已有图片、草图或明确标为临时的占位做动态分镜；无渲染工具则提供时码表并标 `TIMING_REVIEW_ONLY`。
检查观众能否理解行动因果、钩子兑现、信息重复、停顿和镜头间承接。以整段有效为准，之后再精制当前生成任务。
根据模型已验证能力选择 `SINGLE_SHOT` 或 `NATIVE_MULTISHOT`；依赖前片实拍终态的任务才等待前片验收。

当用户要求配乐分析、推荐、提示词或生成时，再读 [background-music-workflow.md](references/background-music-workflow.md)。从当前生效的剧本、导演台、分镜与预剪中编译 `BGM-BRIEF` 和提示词；不可把音乐生成作为阶段 3 或阶段 6 的默认动作。

## 阶段 4：资产与构图

读 [reference-asset-strategy.md](references/reference-asset-strategy.md)、[reference-asset-ledger.md](references/reference-asset-ledger.md)、[scene-spatial-lock.md](references/scene-spatial-lock.md)、[cinematic-scene-production-design.md](references/cinematic-scene-production-design.md)。
按选定剧本生成角色、道具、场景顶视和九机位卡，逐张检查再批准。资料卡优先整页生成，修复可使用内部单区素材并合回，不增加交付卡数。
真人表演还读 [realism-distillation.md](references/realism-distillation.md)、[performance-and-microexpressions.md](references/performance-and-microexpressions.md)、[character-realism-distillation.md](references/character-realism-distillation.md)。
风格未定读 [default-grounded-drama-baseline.md](references/default-grounded-drama-baseline.md)；明确导演/电影参考才读 [director-style-overlays.md](references/director-style-overlays.md)。
依 [cinema-composition-overlay.md](references/cinema-composition-overlay.md) 完成三张 PREVIS；在最终 16:9 首帧复核人物关系、视线、空间和道具，没有通过则调整正式构图。
模型上传素材可从批准卡无损裁切，登记父图版本、范围、职责、排除项和哈希；先核验裁切未破坏身份或必要几何。六格板默认仅作 QA；用户选择线稿/白描上传时，读 [structural-storyboard-reference.md](references/structural-storyboard-reference.md)，按已核验的分镜与主体图组合能力编译普通图参考，区分结构、身份、材质职责。

## 阶段 5：Seedance 或其他模型提交

读 [prompt-spec.md](references/prompt-spec.md)、[model-adapters.md](references/model-adapters.md)。
先写完整审计记录，再编译自包含的提交提示词；保留完整资产映射供操作者核对，在模型正文内明确每个实际引用的职责与必要冻结事实。
Seedance/即梦目标必须读 [seedance-2x-workflow.md](references/seedance-2x-workflow.md)，生成 `23-seedance-2x-compiler.md`、可复制提示词与当前上传清单。
提交前核验生效版本、真实文件、引用槽、动作负荷、时码、原生/后期边界。不把“无对白”误写为“无环境声”；最终要求静音时在导出验收中检查音轨。
真实延长必须有支持该操作的准确界面和已验收前片；计划终态不得冒充已生成终帧。

## 阶段 6：成片、剪辑与反馈

读 [video-result-qa.md](references/video-result-qa.md)、[continuity-and-failure-repair.md](references/continuity-and-failure-repair.md)。
对每个候选视频检查规格和全时段动作，记录实际镜头数、关键事件、身份/道具/空间漂移、可用区间和实际终态。
检查前段末一秒与后段首一秒及实际剪接预览；通过后更新生效清单、剪辑时码与总 QA。不同任务使用不同文件版本是允许的，必须由清单明确固定。
不以静态故事板或提示词 QA 代替视频 QA。未播放/未审查的结果只标待审；结构验证器不能批准画面质量。
失败先定位资产、调度、动作负荷、参考冲突、模型能力或剪辑问题；选择一个主要根因修复，记录同条件试片结果。重复同一失败三次后换可解释方案，不盲目重抽。

已请求并实际生成 BGM 时，按 `background-music-workflow.md` 审查可用时长、无意人声、循环/剪点、对白遮蔽与音量自动化，再登记到 `13-sound-edit-plan.md`、生效清单和 `delivery/audio/`。没有真实音频、未听审或未获生成请求时，不得声称配乐已完成。

## 工具与交付

- [scripts/init_project.py](scripts/init_project.py)：创建新项目和待填写的版本清单，默认时长由节拍决定。
- [scripts/validate_release.py](scripts/validate_release.py)：只读校验生效清单、引用文件/哈希、任务时码、依赖和状态，不替代视觉验收。
- [output-spec.md](references/output-spec.md)：交付卡形态、现有文档及新增生效/预剪/视频 QA 合同。
- [source-provenance.md](references/source-provenance.md)：再分发前查许可证与署名。

返回实际交付路径、当前生效版本、生成/待生成状态、视频和跨片段验收结果、未完成项。只有已产生并审查的影片才能称为通过；本 Skill 优化本身不等于任何旧影片已改善。
