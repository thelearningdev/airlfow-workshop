# Slides — Claude Guide

## Structure

`slides.md` is a thin container: global Slidev frontmatter + `src:` imports + shared `<style>` block.
All slide content lives in `pages/`.

| File | Content |
|---|---|
| `pages/intro.md` | Setup, BookOps story, Business Problem, Workshop Arc, Final Pipeline |
| `pages/module-0.md` | Apache Airflow 101, Hello World DAG, Exercise 0, Architecture, Reflections checklist |
| `pages/data-engineering.md` | What Is DE, What Is a Pipeline, What Is Orchestration |
| `pages/module-1.md` | Data Ingestion — TaskFlow, dynamic mapping, Exercise 1 |
| `pages/module-2.md` | Retry Safety — Idempotency, Exercise 2, Pipeline Checkpoint |
| `pages/module-3.md` | Enrichment & Data Quality — validation, quarantine, Exercise 3 |
| `pages/module-4.md` | History & Time — SCD Type 2, Backfill, Exercise 4 |
| `pages/outro.md` | Summary cards, Explore Next, Thank You, Appendix |

## Layouts in use

- `title-slide` — dark full-bleed, white text; section titles and exercise intros
- `blue-title-slide` — blue full-bleed; "After Exercise N" and summary slides
- `blue-sidebar` — main content layout; uses `::header::` and `::content::` slots, optional `::footer::`
- `none` — raw HTML, used for the split-screen Airflow/DE and Technology/Business slides

## Custom CSS classes (defined in `slides.md` `<style>`)

| Class | Purpose |
|---|---|
| `.concept-shell` / `.concept-step` | Stepped narrative cards (business moment → question → wrong instinct → principle → implication) |
| `.concept-step.warning` / `.success` / `.action` | Colour variants for concept steps |
| `.balanced-cols` | Two-column grid |
| `.panel` + `.pain` / `.reality` / `.action` / `.caution` / `.takeaway` | Coloured panel cards |
| `.timeline-grid` / `.timeline-card` | Module arc grid |
| `.check-list` | Bulleted list with filled blue ✓ circle — use `<ul class="check-list"><li>…</li></ul>` |
| `.exercise-why` | Purple italic callout box explaining why an exercise matters |
| `.caption` | Small italic footnote |
| `.summary-grid` / `.summary-card` | 2×2 glass cards on dark backgrounds |
| `.big-idea` / `.subtle-line` / `.section-note` / `.hero-kicker` | Title-slide typography helpers |

## Conventions

- Animations use `v-click` (single reveal) or `<v-clicks>` (list reveal). Checklist slides have no animations.
- Exercise slides follow the pattern: `exercise-why` callout → numbered `<v-clicks>` list → `::footer::` with starter file path.
- "After Exercise N" slides use `blue-title-slide` layout with `.big-idea` + `.subtle-line`.
- Pipeline Checkpoint slides use a mermaid `flowchart LR` diagram + `.caption`.
