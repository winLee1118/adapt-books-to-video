#!/usr/bin/env python3
"""Create a non-destructive book-to-video project skeleton and timeline."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path


FILES = [
    "00-brief.md",
    "01-book-map.md",
    "02-research-dossier.md",
    "03-adaptation-plan.md",
    "04-style-bible.md",
    "05-character-bible.md",
    "06-scene-bible.md",
    "07-storyboards.md",
    "08-video-prompts.md",
    "09-model-capabilities.md",
    "10-sources.md",
    "11-quality-report.md",
    "12-continuity-bible.md",
    "13-sound-edit-plan.md",
    "14-screenplay.md",
    "15-reference-asset-map.md",
    "16-realism-qa.md",
    "17-series-bible.md",
    "18-screenplay-qa.md",
    "19-cinematography-transition-plan.md",
    "20-director-design.md",
    "21-shotlist-9col.csv",
    "22-composition-triptychs.md",
    "23-seedance-2x-compiler.md",
    "24-precut-review.md",
    "25-video-result-qa.md",
]

DIRS = [
    "delivery/characters",
    "delivery/scenes",
    "delivery/shot-anchors",
    "delivery/storyboards",
    "delivery/style-cards",
    "delivery/audio",
    "process/cinema-triptychs",
    "process/model-inputs",
    "reports/internal-qa",
    "reports/video-qa",
    "reports/retries",
]

MANIFEST_FIELDS = [
    "id",
    "type",
    "purpose",
    "status",
    "file_path",
    "prompt_file",
    "aspect_ratio",
    "target_model",
    "source_text",
    "evidence_ids",
    "evidence_card_id",
    "evidence_gate",
    "production_interpretation",
    "verification_date",
    "production_design_id",
    "action_prop_ids",
    "reference_ids",
    "origin",
    "approved_from",
    "reference_role",
    "frozen_fields",
    "must_not_transfer",
    "upload_order",
    "used_by_script_beats",
    "used_by_shots",
    "continuity_group",
    "style_profile_id",
    "qa_status",
    "failure_code",
    "retry_count",
    "notes",
    "evidence_status",
    "generation_status",
    "qa_status",
    "use_status",
]

SHOTLIST_9COL_FIELDS = [
    "sequence_id",
    "shot_id",
    "time_range",
    "dramatic_job",
    "visual_action_and_blocking",
    "camera_and_composition",
    "sound_and_dialogue",
    "asset_and_continuity_contract",
    "bridge_and_post_responsibility",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\-]+", "-", value, flags=re.UNICODE)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "book"


def timeline(duration: float, panels: int) -> list[dict[str, float | int]]:
    if not math.isfinite(duration):
        raise ValueError("duration must be finite")
    if duration <= 0:
        raise ValueError("duration must be greater than zero")
    if duration > 15.0:
        raise ValueError("duration must not exceed 15 seconds")
    if panels < 6:
        raise ValueError("panels must be at least 6")
    edges = [round(duration * index / panels, 3) for index in range(panels + 1)]
    return [
        {"panel": index + 1, "start": edges[index], "end": edges[index + 1]}
        for index in range(panels)
    ]


def build_config(args: argparse.Namespace, project_name: str) -> dict:
    final_aspect_ratio = "16:9"
    return {
        "book_title": args.book,
        "project_name": project_name,
        "aspect_ratio": final_aspect_ratio,
        "character_card_aspect_ratio": "16:9",
        "scene_and_shot_aspect_ratio": final_aspect_ratio,
        "delivery_policy": "finished-cards-only-no-process-images",
        "delivered_images_per_character": 2,
        "delivered_images_per_scene": 1,
        "delivered_images_per_clip": 2,
        "director_or_classic_film_reference": args.style_reference,
        "style_compilation_mode": args.style_mode,
        "genre": args.genre,
        "production_track": args.production_track,
        "production_form": args.production_form,
        "format_route": args.format_route,
        "episode_count": args.episodes,
        "screenplay_policy": "dual-track-proposal-before-assets; documentary-claims-evidence-bound",
        "dramatic_engine_policy": "source-to-drama; goal-opposition-strategy-turn-choice-cost",
        "short_drama_policy": "golden-3s-hook; payoff-deadline; earned-end-hook; 16:9-action-budget",
        "screenwriting_polish_policy": "filmable-action-and-subtext; reject-explanatory-dialogue-and-unfilmable-interiority; route-by-total-form",
        "director_design_policy": "director-design-card-after-treatment-before-assets; evidence-and-text-bounded; sequence-rhythm-cards",
        "review_gate_policy": "optional-review-at-treatment-script-director-design-and-asset-lock; never-a-mandatory-stepwise-pause",
        "shotlist_export_policy": "optional-nine-column-csv-derived-from-approved-script-beats-and-shots; never-source-of-truth",
        "composition_previsualization_policy": args.composition_previsualization + "; exactly-three-separate-21-9-internal-previs-frames-per-selected-sequence-after-approved-assets; inspect-and-compile-text-decisions-only; never-deliver-or-use-as-final-image-video-input",
        "opening_promise_policy": "one-primary-opening-mode; opening-promise-card-before-first-shot; visible-0-3s-cause-effect; payoff-mapping; first-15-second-handoff; documentary-evidence-boundary",
        "reference_lineage_policy": "audited-lineage; approved-internal-crops; self-contained-submission-reference-map",
        "asset_evidence_policy": "asset-evidence-card-before-prompt; pass-gate-required; text-history-iconography-inference-creative-separated; post-generation-claim-comparison",
        "realism_policy": "light-material-contact-action-time-optics-sound-contract",
        "character_realism_policy": "identity-lock-separated-from-performance-baseline; trigger-smallest-response-selective-development-settle; non-mechanical-blink-gaze-breath",
        "portrait_scene_integration_policy": "profile-card-locks-identity-only; shot-anchor-binds-face-to-scene-light-material-edge-color-and-depth; repair-one-layer-at-a-time",
        "default_visual_baseline": "DEFAULT-GROUNDED-DRAMA when user style is unspecified; grounded-material-realism; practical-natural-light; reaction-contact-editing; motivated-post-transitions",
        "style_overlay_precedence": "history-and-text > explicit-user-constraints > primary-style > genre > defaults",
        "continuity_policy": "frozen-chinese-strings-and-approved-end-frames",
        "scene_spatial_consistency_policy": "text-spatial-lock; mandatory-approved-topdown-geometry-plan-as-intermediate-reference; one-delivered-3x3-nine-station-scene-card; declare-vnn-per-shot",
        "scene_production_design_policy": "production-design-breakdown-before-spatial-lock; evidence-bounded-hero-action-props-or-declared-no-prop-alternative; functional-set-dressing-actor-routes-practical-light-end-state; action-prop-beat-per-clip",
        "camera_motivation_policy": "move-only-on-visible-story-change",
        "cinematography_transition_policy": "one-sequence-camera-language; visible-trigger-path-stop; one-explicit-bridge-per-edge; post-for-unverified-transitions",
        "clip_duration_seconds": args.duration,
        "clip_duration_max_seconds": 15.0,
        "clip_sequencing_policy": "sequence-precut-first; generation-jobs-by-actual-dependencies",
        "workflow_revision": "2026-09-06",
        "active_release_file": "active-release.json",
        "duration_policy": "beat-driven; generation-ceiling-15s; edit-intervals-from-approved-results",
        "production_type": args.production_type,
        "target_model": args.target_model,
        "seedance_2x_compiler_policy": "active-only-for-verified-seedance-target; canonical-prompt-after-evidence-assets-and-contact-sheet; exact-at-reference-map; duration-timeline; actual-video-only-for-native-continuation; 16-9-final; previs-never-input",
        "bgm_workflow_policy": "explicit-request-only; screenplay-director-design-precut-to-bgm-brief-and-prompt; de-named-style-traits; no-generation-without-generate-approved; audio-qa-before-mix",
        "panels_per_clip": args.panels,
        "default_equal_timeline": timeline(args.duration, args.panels) if args.duration is not None else [],
        "note": "Choose duration from story beats; any supplied equal intervals are planning placeholders, not edit cuts.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", required=True, help="Book title")
    parser.add_argument("--output", required=True, type=Path, help="Parent output directory")
    parser.add_argument("--duration", type=float, default=None, help="Optional generation duration; omitted means beat-driven, maximum 15")
    parser.add_argument("--panels", type=int, default=6, help="Storyboard panels per clip, minimum 6")
    parser.add_argument("--aspect-ratio", choices=["16:9"], default="16:9", help="All final videos use 16:9")
    parser.add_argument("--style-reference", default="none", help="Director, classic film, movement, or method used for analysis")
    parser.add_argument(
        "--style-mode",
        choices=["observable-traits", "named-reference-analysis-only"],
        default="observable-traits",
        help="How named style references are compiled into generation prompts",
    )
    parser.add_argument("--genre", default="auto", help="Optional genre/playbook label")
    parser.add_argument("--target-model", default="unselected", help="Requested generation model; verify exact vendor surface before writing an adapter")
    parser.add_argument("--production-type", choices=["UNSELECTED", "DOCUMENTARY", "STORY_FILM", "LIVE_ACTION_CHINESE_MYTHIC_STORY_FILM"], default="UNSELECTED")
    parser.add_argument(
        "--production-track",
        choices=["NARRATIVE", "DOCUMENTARY", "BOTH"],
        default="BOTH",
        help="Screenplay track; BOTH develops both proposals before asset production",
    )
    parser.add_argument(
        "--production-form",
        choices=["FEATURE", "DOCUMENTARY", "AI_SHORT_DRAMA", "MOTION_COMIC", "HYBRID"],
        default="FEATURE",
        help="Controls story rhythm and delivery form; final videos remain 16:9",
    )
    parser.add_argument(
        "--format-route",
        choices=["CONCEPT_SHORT", "SHORT_FILM", "FEATURE", "SERIES"],
        default="FEATURE",
        help="Total-form route; clips remain 16:9 and no more than 15 seconds",
    )
    parser.add_argument(
        "--composition-previsualization",
        choices=["required-if-image-generation-available"],
        default="required-if-image-generation-available",
        help="Creates three non-delivery 21:9 composition frames per selected sequence; final assets remain 16:9",
    )
    parser.add_argument("--episodes", type=int, default=None, help="Optional episode count for serial work")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.panels < 6:
        parser.error("panels must be at least 6")

    project_name = f"{slugify(args.book)}-video-kit"
    project_dir = args.output.resolve() / project_name
    config = build_config(args, project_name)

    if args.dry_run:
        print(json.dumps({"project_dir": str(project_dir), "config": config}, ensure_ascii=False, indent=2))
        return 0

    if project_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing project: {project_dir}")

    project_dir.mkdir(parents=True)
    for directory in DIRS:
        (project_dir / directory).mkdir(parents=True)
    for filename in FILES:
        if filename == "21-shotlist-9col.csv":
            with (project_dir / filename).open("w", newline="", encoding="utf-8-sig") as handle:
                csv.DictWriter(handle, fieldnames=SHOTLIST_9COL_FIELDS).writeheader()
            continue
        heading = filename.removesuffix(".md").split("-", 1)[-1].replace("-", " ").title()
        (project_dir / filename).write_text(f"# {heading}\n", encoding="utf-8")
    (project_dir / "project-config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    release = {
        "schema_version": 2,
        "release_id": "R001",
        "requirements": {"aspect_ratio": "16:9", "max_generation_seconds": 15,
                         "dialogue": "UNSELECTED", "narration": "UNSELECTED", "audio_delivery": "UNSELECTED", "bgm_generation": "NOT_REQUESTED"},
        "documents": {"brief": "00-brief.md", "sound_edit": "13-sound-edit-plan.md", "precut": "24-precut-review.md", "video_qa": "25-video-result-qa.md"},
        "assets": [], "jobs": [], "edit_segments": [], "bridges": [],
    }
    (project_dir / "active-release.json").write_text(
        json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (project_dir / "asset-manifest.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS).writeheader()

    print(project_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
