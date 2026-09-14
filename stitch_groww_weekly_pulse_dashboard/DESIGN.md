---
name: Weekly Pulse Intelligence
colors:
  surface: '#101419'
  surface-dim: '#101419'
  surface-bright: '#36393f'
  surface-container-lowest: '#0a0e13'
  surface-container-low: '#181c21'
  surface-container: '#1c2025'
  surface-container-high: '#262a30'
  surface-container-highest: '#31353b'
  on-surface: '#e0e2ea'
  on-surface-variant: '#bacac1'
  inverse-surface: '#e0e2ea'
  inverse-on-surface: '#2d3136'
  outline: '#85948c'
  outline-variant: '#3c4a43'
  surface-tint: '#2fe0aa'
  primary: '#44edb7'
  on-primary: '#003828'
  primary-container: '#00d09c'
  on-primary-container: '#00533c'
  inverse-primary: '#006c4f'
  secondary: '#c6bfff'
  on-secondary: '#29009f'
  secondary-container: '#4228c4'
  on-secondary-container: '#b7afff'
  tertiary: '#ffc983'
  on-tertiary: '#452b00'
  tertiary-container: '#f6a724'
  on-tertiary-container: '#654000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#59fdc5'
  primary-fixed-dim: '#2fe0aa'
  on-primary-fixed: '#002116'
  on-primary-fixed-variant: '#00513b'
  secondary-fixed: '#e4dfff'
  secondary-fixed-dim: '#c6bfff'
  on-secondary-fixed: '#170066'
  on-secondary-fixed-variant: '#4025c1'
  tertiary-fixed: '#ffddb4'
  tertiary-fixed-dim: '#ffb955'
  on-tertiary-fixed: '#291800'
  on-tertiary-fixed-variant: '#633f00'
  background: '#101419'
  on-background: '#e0e2ea'
  surface-variant: '#31353b'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.03em
  data-tabular:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: -0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.25rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style
The design system powers an executive-grade, AI-driven review intelligence suite. It prioritizes information density, operational velocity, and razor-sharp clarity. Designed for product directors, quantitative analysts, and engineering leads, the interface transforms thousands of unstructured mobile store reviews into immediate, actionable diagnostics.

The visual style is **High-Density Technical SaaS**:
- Deep, low-noise dark surfaces that reduce eye fatigue during prolonged monitoring.
- High-contrast chromatic signals to immediately differentiate health metrics, positive sentiment, critical bugs, and AI-inferred classifications.
- Crisp boundary definitions via hairline structural borders rather than diffuse drop shadows.
- Utilitarian precision where data cards, charts, tag clouds, and confidence badges coexist within an orderly, frictionless grid.

## Colors
The palette balances an ultra-dark obsidian foundation with surgical semantic indicators:

- **Canvas & Surfaces:**
  - Base Background: `#0B0F14`
  - Elevated Container / Cards: `#12181F`
  - Floating / Dropdown / Modal Surface: `#18202A`
  - Hairline Border / Structural Stroke: `#1E2630`
  - Subtle Hover Border: `#2C3847`

- **Accents & Semantics:**
  - **Primary Mint (`#00D09C`):** Primary interactions, affirmative metrics, positive sentiment clusters, active tabs, and baseline confidence thresholds.
  - **AI Violet (`#7C6BFF`):** Machine intelligence summaries, automated tagging, sentiment drift vectors, and predictive models.
  - **Amber Neutral (`#F5A623`):** Medium priority items, neutral review sentiments, and threshold warnings.
  - **Coral Red (`#FF5C5C`):** Negative feedback spikes, app store rating dips, and critical crash diagnostics.

- **Typography & Content Hierarchy:**
  - Primary / Headings: `#E6EDF3`
  - Secondary / Data Labels: `#8B98A5`
  - Tertiary / Code / Inactive: `#53606F`

## Typography
Inter delivers functional neutrality, horizontal compactness, and unmatched legibility in numeric and technical layouts.

- Enable OpenType feature `cv05` (lowercase l with tail), `cv11` (single-storey a), and `tnum` (tabular numbers) globally across all tables and metric monitors.
- Maintain high contrast between primary analytical values (`#E6EDF3`, semi-bold) and companion meta-descriptors (`#8B98A5`, medium/regular).
- Use uppercase styling exclusively for high-level technical tags, micro-badges, and column headers, paired with `letterSpacing: 0.03em` and `11px` sizing.

## Layout & Spacing
The layout implements a 12-column fluid grid system optimized for dense dashboard configurations and operational split-views:

- **Desktop (>= 1280px):** 12 columns with `1.25rem` (20px) gutters and `2rem` (32px) margins. Standard multi-pane layout: 240px persistent analytical navigation, 6-column central feed for reviews/clusters, 6-column lateral panel for AI synthesis and impact telemetry.
- **Tablet (768px - 1279px):** 8 columns with `1rem` (16px) gutters and `1.5rem` (24px) margins. Lateral panels collapse into tabbed segment views or dismissible slide-outs.
- **Mobile (< 768px):** 4 columns with `0.75rem` (12px) gutters and `1rem` (16px) canvas margins. Stack metric cards vertically; tables shift to swipeable micro-cards.

Spacing tokens enforce consistent micro-rhythms: `space-xs` (4px) for inline badge and pill padding, `space-sm` (8px) for input and control element offsets, `space-md` (12px) for item gaps within lists, and `space-xl` (24px) for container boundaries.

## Elevation & Depth
This design system avoids heavy drop shadows, relying instead on **surface tonal stacking** and **crisp 1px low-contrast outlines**:

1. **Level 0 (Canvas):** Base viewport `#0B0F14`.
2. **Level 1 (Card & Module Layer):** `#12181F` bounded by a 1px solid stroke of `#1E2630`. No box shadow is applied under default states.
3. **Level 2 (Hover & Active States):** Surface maintains `#12181F`, stroke escalates to `#2C3847`, with an ambient stroke highlight glow on interactive edges (`0 0 0 1px #00D09C` for selected filters or cards).
4. **Level 3 (Overlays, Flyouts & Tooltips):** Surface `#18202A`, stroke `#2C3847`, backed by an ambient shadow `0 8px 24px -4px rgba(0, 0, 0, 0.6)`.
5. **AI Accentuation:** Feature areas managed by automated intelligence models feature a hairline accent: a top border gradient of `linear-gradient(90deg, #7C6BFF 0%, transparent 60%)`.

## Shapes
A unified radius structure matches technical precision with modern enterprise aesthetics:

- **Containers & Analytics Cards:** Fixed `12px` border radius (`rounded-lg` token variant) to frame data sets cleanly without visual crowding.
- **Inputs, Nested Panels, and Filter Bars:** `8px` (`rounded`) for compact visual containment.
- **Chips, Pill Tags, and AI Badges:** `9999px` (fully rounded pill) to create distinct separation between categorical meta-items and geometric data cards.
- **Stroke Width:** Universally locked at `1px` to preserve density and legibility across all display scales.

## Components

### Buttons
- **Primary:** Background `#00D09C`, text `#0B0F14` (Inter 13px, weight 600), border-radius 8px. Hover shifts background to `#00B887`. Active compresses slightly (`transform: scale(0.98)`).
- **Secondary / Outline:** Background `transparent`, text `#E6EDF3`, border `1px solid #1E2630`. Hover applies surface `#18202A` and border `#2C3847`.
- **AI Action Variant:** Background `rgba(124, 107, 255, 0.12)`, text `#7C6BFF`, border `1px solid rgba(124, 107, 255, 0.35)`. Hover raises background to `rgba(124, 107, 255, 0.2)`.

### Chips & Badges
- **Status / Sentiment Pills:** Inline flex, height 22px, padding 0 8px, border-radius 9999px, font size 11px, weight 600.
  - Positive: Background `rgba(0, 208, 156, 0.1)`, text `#00D09C`, border `1px solid rgba(0, 208, 156, 0.25)`.
  - Neutral: Background `rgba(245, 166, 35, 0.1)`, text `#F5A623`, border `1px solid rgba(245, 166, 35, 0.25)`.
  - Negative: Background `rgba(255, 92, 92, 0.1)`, text `#FF5C5C`, border `1px solid rgba(255, 92, 92, 0.25)`.
- **AI Intelligence Badge:** Background `rgba(124, 107, 255, 0.1)`, text `#7C6BFF`, border `1px solid rgba(124, 107, 255, 0.3)`. Accompanied by a leading 12px spark icon.

### Form Inputs & Search
- **Search & Filter Bars:** Height 36px, background `#0B0F14`, border `1px solid #1E2630`, text `#E6EDF3`, placeholder `#8B98A5`, border-radius 8px, padding `0 12px`.
- **Focus State:** Border color `#00D09C`, outline none, subtle ring `0 0 0 1px #00D09C`.

### Cards & Data Containers
- **Metric & Insight Cards:** Surface `#12181F`, border `1px solid #1E2630`, border-radius 12px, padding 16px. Header row displays title in `#8B98A5` (12px) with trend badge top-right. Metric value in `#E6EDF3` (22px bold).

### Sleek Progress & Ratio Indicators
- **Track:** Height 4px, background `#1E2630`, border-radius 2px, overflow hidden.
- **Fill:** Solid fill color mapped to state (`#00D09C`, `#7C6BFF`, `#F5A623`, or `#FF5C5C`), with smooth transitions (`width 300ms cubic-bezier(0.4, 0, 0.2, 1)`).

### Review Table & Data Feeds
- **Row:** Height 48px, border-bottom `1px solid #1E2630`, text `#E6EDF3`. Hover state changes background to `rgba(255, 255, 255, 0.02)`.
- **Confidence Scoring:** Monospaced tabular indicator paired with a 32px mini progress meter in the row metadata.