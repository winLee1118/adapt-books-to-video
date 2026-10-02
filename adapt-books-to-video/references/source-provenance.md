# 外部方法来源与许可证边界

本 Skill 的整合版本在 2026-08-11 研究了以下公开仓库。新增文字、表格、编码与流程均在本项目中重新组织和撰写；不得把本文件理解为对外部仓库全部内容的再授权。

## 来源

### 2026-08-24 Seedance 2.x 编译流程整合

- `songguoxs/seedance-prompt-skill` — https://github.com/songguoxs/seedance-prompt-skill ：研究多模态引用角色、短时长时间轴、分段衔接和延长工作流，整合为本项目在已批准标准提示词之后的 `SEEDANCE-2X-COMPILER-RECORD`、`@` 素材职责表、时长编译与真实视频续接边界。仓库 README 标注 MIT，但根目录未见独立许可证文件；只吸收高层方法并重新撰写，不逐字复制其 Skill、模板或示例。
- `heloraai/Seedance2.0-Prompt-Optimizer-skill` — https://github.com/heloraai/Seedance2.0-Prompt-Optimizer-skill ：研究 `SCELA`（主体、镜头、效果、光线、声音）作为提交前的完整性检查；许可证为 MIT： https://github.com/heloraai/Seedance2.0-Prompt-Optimizer-skill/blob/main/LICENSE 。不整合其“保留受版权角色核心视觉特征”的相似化规则、IP/品牌规避写法、9:16 默认、未经官方核验的平台限制或任何原始模板/案例。
- 能力边界：每次投放仍以当时的火山引擎/即梦官方 UI 或 API 文档为准。参考入口： https://www.volcengine.com/docs/82379/2222480?lang=zh 、https://api.volcengine.com/api-explorer/?action=CreateContentsGenerationsTasks&groupName=%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90API&serviceCode=ark&version=2024-01-01 。本项目不把第三方仓库的字段、额度、真人肖像限制或视频延长语法当作永久平台事实。
- 边界：不复制仓库的提示词、示例剧情、品牌/IP、画面或版权规避策略。Seedance 编译器只能引用本项目已有、通过证据门禁的最终资产；三张 `21:9` `PREVIS` 和场景顶视 QA 图永远不是模型输入；最终资产与视频维持 `16:9`，每个连续生成片段不超过 15 秒。

### 2026-08-24 Cinema DNA 构图预演整合

- `dacnay816y62-hub/cinema-dna-21x9x3` — https://github.com/dacnay816y62-hub/cinema-dna-21x9x3 ：仅研究关系压力、观众位置、视线流量、色彩命题、反模板化和反 CG/广告/电视剧化的高层构图方法；整合为每个 `SEQ-ID` 三张独立、非交付 `21:9` `PREVIS` 图及文字化 `PREVIS-DECISION`。
- 边界：不复制其 Skill、提示词、三联模板、案例、图片、IP/导演参考或海报系统；仓库根目录当前未见 LICENSE 文件。预演图只用经过本项目证据门禁的资产生成，只回写可观察构图决定，绝不作为最终图像/视频参考或交付资产；最终资产始终保持本项目的 `16:9` 合同。

### 2026-08-23 山音编剧/导演方法整合

- `Shanyin-ai/shanyin-screenwriting-master` — https://github.com/Shanyin-ai/shanyin-screenwriting-master ：仅研究总体篇幅路由、可拍性/对白自检、结构化剧本开发和阶段审阅的高层方法；整合为 `format_route`、`FILMABILITY-PASS` 与可选审阅门。
- `Shanyin-ai/shanyin-director-master` — https://github.com/Shanyin-ai/shanyin-director-master ：仅研究剧本锁定后形成导演意图、节奏组织与九栏分镜导出的高层方法；整合为 `DIRECTOR-DESIGN-CARD`、`SEQ-RHYTHM-CARD` 和可选 `21-shotlist-9col.csv`。
- 边界：本项目未复制两仓库的 `.skill` 原文、提示词、示例剧情、样板角色、风格模板或作者署名内容；新增流程、字段与表述均重新组织和撰写。仓库页面虽标示 MIT，README 还包含署名/不得转售等说明；上述许可证观察为历史记录；本发布包不含外部仓库原文。逐字复用或引入外部材料前，须核验其实际 LICENSE、NOTICE 与作者声明。

### 2026-08-19 摄影机语言与跨视频剪辑调研

以下资料仅用于抽取高层、可观察的摄影与连续性工作流；本 Skill 未复制仓库的提示词、镜头案例、代码或受版权影片的可识别镜头。发布或再分发前仍须检查每个仓库当前的 LICENSE/NOTICE。

- `wuwangzhang1216/DirectorSKILL` — https://github.com/wuwangzhang1216/DirectorSKILL ：分镜前的调度、镜头/焦段心理、光线、180 度轴、视线、连续性状态与质检；借鉴为镜头的“触发—路径—停止”和跨镜几何合同。
- `0xhughs/director-skills` — https://github.com/0xhughs/director-skills ：创作意图、电影化执行与模型适配的分层；借鉴为 `SEQ` 摄影语言卡与模型/后期边界。
- `LinHao-city/StoryMind` — https://github.com/LinHao-city/StoryMind ：先完成镜头表，再为每镜定义景别、运动、光线和角色精确描述；借鉴为先规划镜头链再写生成提示词。
- `Krenlis/director-craft-framework` — https://github.com/Krenlis/director-craft-framework ：将摄影参数绑定到可见身体、光线、运动与环境反馈；借鉴为不以设备名或“电影感”替代可见结果。
- American Society of Cinematographers, *Shot Craft* — https://theasc.com/articles/shot-craft-the-cinematographers-reel ：摄影机移动应被动机化并扩展叙事；借鉴为“无可见新信息则固定机位”的验收规则。
- StudioBinder, *Camera Movement Guide* — https://www.studiobinder.com/camera-shots/camera-movements/ ：摄影机运动须服务叙事；借鉴为按叙事功能选择移动而非堆叠术语。
- StudioBinder, *Complex Master Shot* — https://www.studiobinder.com/blog/directing-technique-complex-master-shot/ ：通过人物调度、前景/背景与位置关系显现权力变化；借鉴为优先调度/构图而非无理由移动摄影机。

### 2026-08-18 剧本与短剧方法调研

以下仓库只提供高层工作流与格式研究。未复制具体提示词、样例剧情、角色、台词、素材或代码；再分发前必须重新检查各仓库 LICENSE/NOTICE。

- `worldwonderer/drama-skills` — https://github.com/worldwonderer/drama-skills ：分离开发、剧本、资产、分镜、视频提示词与独立审稿责任；借鉴为“先锁创作决定，再编译资产”的流程边界。
- `ChrisChen667788/wind-comic` — https://github.com/ChrisChen667788/wind-comic ：短剧首镜钩子、反转密度、悬念检测、角色身份锚点和后期字幕边界；借鉴为可审查的短剧质量门。
- `0xsline/short-drama` — https://github.com/0xsline/short-drama ：分集目录、开篇规则、节奏曲线与集尾钩子；借鉴为集级承诺—兑现—新钩子台账。
- `story-apps/starc` — https://github.com/story-apps/starc ：多剧本、研究资料、人物和场景状态在同一项目下管理；借鉴为 `17-series-bible.md` 与稳定 ID 的项目结构。
- `teriflix/scrite` — https://github.com/teriflix/scrite ：自定义故事节拍、人物/地点报告与剧本格式；借鉴为结构透镜可选择、而非单一固定模板。

### `smixs/visual-skills`

- 地址：https://github.com/smixs/visual-skills
- 许可证：CC BY 4.0；改编需署名。
- 借鉴范围：场景先于形容词、镜头必须承担叙事工作、摄影机运动需要动机、空间可读性与环境压力。
- 署名：Serge Shima — https://github.com/smixs/visual-skills

### `cclank/lanshu-awesome-ai-video-kit`

- 地址：https://github.com/cclank/lanshu-awesome-ai-video-kit
- 许可证：MIT（以仓库当前许可证为准）。
- 借鉴范围：模型能力核验、跨模型提示词转换、时间轴、参考素材任务分工与失败检查。

### `jnMetaCode/ai-shortfilm-prompts`

- 地址：https://github.com/jnMetaCode/ai-shortfilm-prompts
- 许可证：作者自有方法/模板为 MIT；仓库内标明属于 Mx-Shell 的原始提示词和材料保留原权利。
- 借鉴范围：分阶段构造短片提示词、类型片路由和输出前自检。
- 排除范围：没有复制或整合 Mx-Shell 的受限原始提示词、文档摘录或具体案例文本。

### `woodfantasy/Seedance2.0-ShotDesign-Skills`

- 地址：https://github.com/woodfantasy/Seedance2.0-ShotDesign-Skills
- 许可证：MIT-0（以仓库当前许可证为准）。
- 借鉴范围：导演/视觉风格参数化、七区微表情观察、时间戳表演弧、摄影与表演冲突检查。

### `wuwangzhang1216/DirectorSKILL`

- 地址：https://github.com/wuwangzhang1216/DirectorSKILL
- 许可证：MIT（以仓库当前许可证为准）。
- 借鉴范围：单一风格覆盖层、连续性状态、关键帧优先、失败编码与最低成本修复。

## 使用规则

- 外部许可证可能变化；发布或再分发前重新检查仓库的 LICENSE 和 NOTICE。
- 不复制具体导演作品中的镜头、角色、对白、剧情或美术设计；只迁移高层方法与可观察参数。
- 最终模型提示词优先使用去专名参数，不以导演名、电影名或 IP 名称作为唯一风格控制。
- 保留本文件和 `smixs/visual-skills` 的署名信息，除非彻底移除其可识别的改编内容。
