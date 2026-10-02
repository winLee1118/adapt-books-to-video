#!/usr/bin/env python3
"""Regression tests for the project initializer."""

from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import init_project


class TimelineTests(unittest.TestCase):
    def test_timeline_covers_duration_without_gaps(self) -> None:
        result = init_project.timeline(15.0, 6)
        self.assertEqual(6, len(result))
        self.assertEqual(0.0, result[0]["start"])
        self.assertEqual(15.0, result[-1]["end"])
        for current, following in zip(result, result[1:]):
            self.assertEqual(current["end"], following["start"])

    def test_timeline_rejects_too_few_panels(self) -> None:
        with self.assertRaises(ValueError):
            init_project.timeline(15.0, 5)

    def test_timeline_rejects_over_fifteen_seconds(self) -> None:
        with self.assertRaises(ValueError):
            init_project.timeline(15.1, 6)


class ProjectTests(unittest.TestCase):
    def test_initializer_creates_integrated_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            argv = [
                "init_project.py",
                "--book",
                "测试书",
                "--output",
                temp_dir,
                "--duration",
                "10",
                "--panels",
                "6",
                "--style-reference",
                "黑色电影",
                "--genre",
                "心理剧情",
            ]
            with patch("sys.argv", argv), redirect_stdout(io.StringIO()):
                self.assertEqual(0, init_project.main())

            project = Path(temp_dir) / "测试书-video-kit"
            self.assertTrue((project / "12-continuity-bible.md").is_file())
            self.assertTrue((project / "13-sound-edit-plan.md").is_file())
            self.assertTrue((project / "14-screenplay.md").is_file())
            self.assertTrue((project / "15-reference-asset-map.md").is_file())
            self.assertTrue((project / "16-realism-qa.md").is_file())
            self.assertTrue((project / "17-series-bible.md").is_file())
            self.assertTrue((project / "18-screenplay-qa.md").is_file())
            self.assertTrue((project / "19-cinematography-transition-plan.md").is_file())
            self.assertTrue((project / "20-director-design.md").is_file())
            self.assertTrue((project / "21-shotlist-9col.csv").is_file())
            self.assertTrue((project / "22-composition-triptychs.md").is_file())
            self.assertTrue((project / "23-seedance-2x-compiler.md").is_file())
            self.assertTrue((project / "reports" / "retries").is_dir())
            self.assertTrue((project / "process" / "cinema-triptychs").is_dir())
            self.assertTrue((project / "delivery" / "storyboards").is_dir())

            config = json.loads((project / "project-config.json").read_text(encoding="utf-8"))
            self.assertEqual("黑色电影", config["director_or_classic_film_reference"])
            self.assertEqual("observable-traits", config["style_compilation_mode"])
            self.assertEqual("心理剧情", config["genre"])
            self.assertEqual(15.0, config["clip_duration_max_seconds"])
            self.assertEqual("sequence-precut-first; generation-jobs-by-actual-dependencies", config["clip_sequencing_policy"])
            self.assertEqual(
                "identity-lock-separated-from-performance-baseline; trigger-smallest-response-selective-development-settle; non-mechanical-blink-gaze-breath",
                config["character_realism_policy"],
            )
            self.assertEqual(
                "profile-card-locks-identity-only; shot-anchor-binds-face-to-scene-light-material-edge-color-and-depth; repair-one-layer-at-a-time",
                config["portrait_scene_integration_policy"],
            )
            self.assertEqual(
                "asset-evidence-card-before-prompt; pass-gate-required; text-history-iconography-inference-creative-separated; post-generation-claim-comparison",
                config["asset_evidence_policy"],
            )
            self.assertEqual(
                "DEFAULT-GROUNDED-DRAMA when user style is unspecified; grounded-material-realism; practical-natural-light; reaction-contact-editing; motivated-post-transitions",
                config["default_visual_baseline"],
            )
            self.assertEqual(
                "one-sequence-camera-language; visible-trigger-path-stop; one-explicit-bridge-per-edge; post-for-unverified-transitions",
                config["cinematography_transition_policy"],
            )
            self.assertEqual(
                "text-spatial-lock; mandatory-approved-topdown-geometry-plan-as-intermediate-reference; one-delivered-3x3-nine-station-scene-card; declare-vnn-per-shot",
                config["scene_spatial_consistency_policy"],
            )
            self.assertEqual(
                "production-design-breakdown-before-spatial-lock; evidence-bounded-hero-action-props-or-declared-no-prop-alternative; functional-set-dressing-actor-routes-practical-light-end-state; action-prop-beat-per-clip",
                config["scene_production_design_policy"],
            )
            self.assertEqual(
                "one-primary-opening-mode; opening-promise-card-before-first-shot; visible-0-3s-cause-effect; payoff-mapping; first-15-second-handoff; documentary-evidence-boundary",
                config["opening_promise_policy"],
            )
            self.assertEqual("BOTH", config["production_track"])
            self.assertEqual("FEATURE", config["production_form"])
            self.assertEqual("FEATURE", config["format_route"])
            self.assertEqual(
                "director-design-card-after-treatment-before-assets; evidence-and-text-bounded; sequence-rhythm-cards",
                config["director_design_policy"],
            )
            self.assertEqual(
                "optional-nine-column-csv-derived-from-approved-script-beats-and-shots; never-source-of-truth",
                config["shotlist_export_policy"],
            )
            self.assertEqual(
                "required-if-image-generation-available; exactly-three-separate-21-9-internal-previs-frames-per-selected-sequence-after-approved-assets; inspect-and-compile-text-decisions-only; never-deliver-or-use-as-final-image-video-input",
                config["composition_previsualization_policy"],
            )
            self.assertEqual("16:9", config["aspect_ratio"])
            self.assertEqual("unselected", config["target_model"])
            self.assertEqual(
                "active-only-for-verified-seedance-target; canonical-prompt-after-evidence-assets-and-contact-sheet; exact-at-reference-map; duration-timeline; actual-video-only-for-native-continuation; 16-9-final; previs-never-input",
                config["seedance_2x_compiler_policy"],
            )

            with (project / "asset-manifest.csv").open(encoding="utf-8-sig", newline="") as handle:
                fields = next(csv.reader(handle))
            self.assertIn("style_profile_id", fields)
            self.assertIn("failure_code", fields)
            self.assertIn("retry_count", fields)
            self.assertIn("reference_role", fields)
            self.assertIn("used_by_script_beats", fields)
            self.assertIn("evidence_card_id", fields)
            self.assertIn("evidence_gate", fields)
            self.assertIn("production_interpretation", fields)
            self.assertIn("production_design_id", fields)
            self.assertIn("action_prop_ids", fields)

            with (project / "21-shotlist-9col.csv").open(encoding="utf-8-sig", newline="") as handle:
                shotlist_fields = next(csv.reader(handle))
            self.assertEqual(9, len(shotlist_fields))
            self.assertEqual("sequence_id", shotlist_fields[0])
            self.assertEqual("bridge_and_post_responsibility", shotlist_fields[-1])

    def test_short_drama_keeps_sixteen_by_nine_final_ratio(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            argv = [
                "init_project.py",
                "--book",
                "横幅短剧",
                "--output",
                temp_dir,
                "--production-form",
                "AI_SHORT_DRAMA",
                "--episodes",
                "12",
                "--format-route",
                "SERIES",
            ]
            with patch("sys.argv", argv), redirect_stdout(io.StringIO()):
                self.assertEqual(0, init_project.main())

            project = Path(temp_dir) / "横幅短剧-video-kit"
            config = json.loads((project / "project-config.json").read_text(encoding="utf-8"))
            self.assertEqual("AI_SHORT_DRAMA", config["production_form"])
            self.assertEqual("16:9", config["aspect_ratio"])
            self.assertEqual("16:9", config["character_card_aspect_ratio"])
            self.assertEqual(12, config["episode_count"])
            self.assertEqual("SERIES", config["format_route"])


if __name__ == "__main__":
    unittest.main()
