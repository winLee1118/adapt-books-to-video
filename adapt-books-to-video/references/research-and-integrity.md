# Research and integrity

## Contents

1. Source-text protocol
2. Historical research protocol
3. Evidence tiers and claim labels
4. Religious and culturally sensitive works
5. Citation and uncertainty format
6. Per-asset evidence gate
7. Research completion gate

## 1. Source-text protocol

Identify the exact source before adapting:

- title and alternate title;
- author, compiler, attributed speaker, or tradition;
- original language and date range;
- edition, recension, canon, chapter/section system, translator, publisher, and publication year;
- supplied file/URL or lawful public source;
- whether the source is complete, abridged, translated, annotated, or modernized.

Use canonical locators rather than page numbers alone when editions vary. Store short quotations only when necessary and legally permissible; otherwise paraphrase with a locator. Never conflate commentary with the source text.

For scriptures or transmitted texts, distinguish:

- narrative setting;
- likely composition/redaction period;
- translation/transmission period;
- period represented by later iconography;
- production interpretation selected for the video.

## 2. Historical research protocol

Research the visible world, not just headline dates. Use a matrix with these rows:

| Domain | Questions to resolve |
|---|---|
| Chronology | Exact/approximate date, political context, calendar/season |
| Geography | Region, terrain, settlement type, distances, climate |
| People | Population, identity terms, age/status roles, grooming |
| Clothing | Silhouette, layers, closures, fibers, weave, dyes, footwear, wear |
| Built world | Plan, materials, roof/floor/walls, thresholds, furniture |
| Objects | Tools, vessels, books/writing, weapons, currency, lamps |
| Customs | Greetings, posture, hospitality, mourning, worship, taboo |
| Labor | Who performs which work, technique, tool handling |
| Food | Ingredients, vessels, preparation, meal etiquette |
| Light/sound | Available illumination, street/house ambience, ritual sound |
| Iconography | Attributes, mudras/gestures, halos, thrones, colors, symbols |

Search in the work's language and relevant scholarly languages when possible. Prefer object-level evidence from museum collections, excavation reports, catalogues, architectural surveys, textile studies, art-historical corpora, and contemporaneous depictions.

Text descriptions alone cannot fix an object's form. For any object that will be legible on screen, search for images and follow `visual-evidence.md` before writing a prompt. Combine the object's original-language, scholarly, and English names with the target period and region, because an unqualified search returns modern reproductions and fantasy designs. Record countable features as exact numbers rather than vague quantities.

## 3. Evidence tiers and claim labels

Use these source tiers:

- **A — Primary/contemporaneous:** the work itself, inscriptions, excavated objects, dated images, contemporaneous records.
- **B — Authoritative secondary:** peer-reviewed scholarship, academic books, museum/university research, critical editions.
- **C — Reputable synthesis:** encyclopedias and institutional educational material.
- **D — Discovery only:** blogs, retailer costumes, fan wikis, social posts, unsourced reconstructions. Use only to find better sources.

Apply one label to each production decision:

- `TEXT`: directly stated or unambiguously implied by the selected edition.
- `HISTORY`: supported by external evidence about the relevant period/place.
- `ICONOGRAPHY`: follows a documented visual tradition, which may postdate the story setting.
- `INFERENCE`: plausible synthesis where direct evidence is absent.
- `CREATIVE`: intentional adaptation choice for clarity, pacing, or aesthetics.

Never upgrade an inference by repeating it. For photoreal reconstructions, avoid false precision: if dye, hairstyle, skin tone, architecture, or ritual gesture is uncertain, select a plausible range and record it.

## 4. Religious and culturally sensitive works

- Identify the tradition, canonical status, major recensions/translations, and whether depictions differ by region or sect.
- Do not collapse deity, bodhisattva, saint, monk, historical person, allegorical figure, and ordinary human into one ontology.
- Separate devotional iconography from archaeological reconstruction. A halo, lotus, crown, mudra, guardian, hell realm, miracle, or divine scale may be `ICONOGRAPHY`, not `HISTORY`.
- Do not add eroticization, horror spectacle, comic distortion, or modern occult symbols unless the user explicitly requests an interpretive style and it remains appropriate.
- Preserve doctrinally important relationships and avoid invented quotations. Paraphrase teachings carefully and cite the section.
- If a scene includes punishment, death, caste/class, ethnicity, gender roles, disability, or collective trauma, describe only what the adaptation needs and avoid demeaning physiognomic stereotypes.
- Where living communities disagree, state the chosen tradition or show alternatives.

For religious or mythological works, verify the selected Chinese edition/translation, narrative setting, translation history, and later East Asian iconographic conventions separately. Do not assume a single historical costume layer can represent all four.

## 5. Citation and uncertainty format

Create `sources.md` entries as:

```text
[S-001] Tier A | Author/institution | Title/object | Date | Stable URL or bibliographic data | Accessed YYYY-MM-DD | Supports: garment closure and textile fiber.
```

Create evidence cards as:

```text
Decision: C-01 outer robe construction
Label: HISTORY + INFERENCE
Claim: ...
Evidence: S-003, S-007
Confidence: high / medium / low
Visual consequence: ...
Rejected alternatives: ...
```

Create the uncertainty ledger with columns:

```text
ID | Question | Competing readings | Evidence | Selected production choice | Label | Confidence | Visual risk
```

Every web-derived factual claim must have a nearby citation in the research dossier. Record access dates because model documentation and online collections change.

## 6. Per-asset evidence gate

Read `asset-evidence-gate.md` before generating any asset. Research is not “complete” merely because a project has a bibliography: each character, scene, prop, top-down plan, multi-angle card and shot anchor needs an `ASSET-EVIDENCE-CARD` with a `PASS`/`HOLD`/`PROMPT_ONLY` result.

For every visible claim, state whether the source supports it as `TEXT`, `HISTORY`, `ICONOGRAPHY`, `INFERENCE`, or `CREATIVE`, and state what the same source does **not** support. A social identity named in a text is not evidence for a specific physical type, clothing, hairstyle, ethnicity, architecture or historical date. A later devotional artwork is not evidence for the historical world of a narrative unless it is explicitly used only as `ICONOGRAPHY`.

An asset can pass only when its selected production interpretation is stated and all prominent visible features are either independently supported or deliberately bounded. If the evidence leaves the period, region, material culture or iconographic layer unresolved, mark the asset `HOLD` and its dependent assets `DEFERRED`; do not ask the model to guess.

## 7. Research completion gate

Do not start final asset generation until:

- the exact source edition is identified or explicitly marked unresolved;
- the adapted chapter has a line-by-line world inventory with attendee categories enumerated individually;
- every legible object has image-based form evidence, exact countable features, a form-lock string, and a negative string, or is labeled `INFERENCE`;
- the story setting and text-composition/transmission periods are separated;
- every visible costume/architecture/ritual choice has a source or a labeled inference;
- the anachronism blacklist covers garments, materials, objects, architecture, light, grooming, symbols, and behavior;
- sacred/supernatural visuals have a declared iconographic system;
- major source conflicts appear in the uncertainty ledger.
- every planned asset has an `ASSET-EVIDENCE-CARD`, a `PASS` gate, a source/limit table and a required post-generation evidence comparison; unsupported assets remain `HOLD` or `DEFERRED`.
