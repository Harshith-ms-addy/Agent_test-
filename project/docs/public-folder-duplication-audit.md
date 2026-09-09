# Public Folder Code Duplication Audit

**Scope:** `project/public/app.js`, `project/public/index.html`, `project/public/styles.css`

## Summary

The JavaScript is already factored into small helper functions and has no significant duplication. The HTML contains structural repetition that is acceptable for a static page but could be templated if the site grows. The CSS contains several repeated declaration blocks that are good candidates for utility-class consolidation.

## Findings

### 1. CSS: Repeated `backdrop-filter` blur pairs
**Files:** `styles.css`
**Lines:** `.site-header` (138–139), `.visual-stage` (346–347), `.metric-card` (400–401), `.explanation-card` (479–480), `.nav-menu` @mobile (616–617)

The pair `backdrop-filter: blur(...); -webkit-backdrop-filter: blur(...);` is repeated with only the blur radius varying. A reusable `.backdrop-blur` utility (or a `.surface` utility) would remove this duplication and make vendor-prefix handling consistent.

### 2. CSS: Repeated focus-visible outline
**Files:** `styles.css`
**Lines:** `.btn:focus-visible` (86–89), `.nav-link:focus-visible` (232–235), `.brand:focus-visible` (164–168)

`.btn` and `.nav-link` share identical outline declarations; `.brand` is nearly identical with an added `border-radius`. A `.focus-ring` utility class would consolidate this.

### 3. CSS: Repeated "surface" panel styling
**Files:** `styles.css`
**Lines:** `.visual-stage` (336–348), `.metric-card` (389–405), `.explanation-card` (468–481), `.nav-menu` @mobile (607–623)

These components repeat `background`, `border`, `border-radius`, `box-shadow`, and `backdrop-filter`. A `.surface` utility class would capture the shared rules, leaving only position/size modifiers on each component.

### 4. CSS: Identical status-modifier declarations
**Files:** `styles.css`
**Lines:** `.metric-status--stable, .metric-status--normal, .metric-status--low` (432–437)

All three status modifiers currently share the same `color` and `background`. They should either be collapsed into a single base `.metric-status--positive` class, or kept as aliases if semantic names are required.

### 5. HTML: Repeated inline SVG stroke attributes
**Files:** `index.html`
**Lines:** brand SVG paths (19–20)

Both `<path>` elements repeat `stroke="currentColor" stroke-width="2" stroke-linecap="round"`. These can be moved to a CSS `.brand-icon-path` rule to reduce inline repetition.

### 6. HTML: Structural repetition of metric cards
**Files:** `index.html`
**Lines:** 118–140

Five `.metric-card` blocks follow the same markup pattern with only label/value/status changing. If the project later adds dynamic data, these should be generated from a small data array in JavaScript or a template.

### 7. HTML: Structural repetition of waypoint items
**Files:** `index.html`
**Lines:** 147–168

Four `.waypoint-item` blocks follow the same pattern. Like the metric cards, this is a candidate for templating if the data becomes dynamic.

## Consolidation Plan

| # | Finding | Action | Priority | Status |
|---|---------|--------|----------|--------|
| 1 | Focus-visible outline | Combine `.btn:focus-visible` and `.nav-link:focus-visible` rules | High | Done |
| 2 | Backdrop-filter blur pairs | Introduce `.backdrop-blur` / `.surface` utility | Medium | Follow-up |
| 3 | Surface panel styling | Introduce `.surface` utility | Medium | Follow-up |
| 4 | Status modifier duplication | Collapse into shared status class | Medium | Follow-up |
| 5 | Inline SVG stroke attrs | Move to CSS class | Medium | Follow-up |
| 6 | Metric card markup repetition | Templatize via JS/data when dynamic | Low | Follow-up |
| 7 | Waypoint item markup repetition | Templatize via JS/data when dynamic | Low | Follow-up |

## Changes Made in This PR

- `project/docs/public-folder-duplication-audit.md` added.
- `project/public/styles.css`: merged the identical `.btn:focus-visible` and `.nav-link:focus-visible` declaration blocks into a single selector group.

## Next Steps

1. Create follow-up issues/PRs for medium-priority CSS utility-class opportunities (items 2–4) if the project adopts a utility approach.
2. Create follow-up issues for HTML/SVG repetition (items 5–7) when the page becomes dynamic or a build step is introduced.
3. If the project later introduces a framework or templating engine, revisit items 6 and 7 to generate repetitive markup from data.
