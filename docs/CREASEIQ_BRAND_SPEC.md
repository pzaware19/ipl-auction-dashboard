# CreaseIQ Brand Spec

## Purpose

CreaseIQ is the platform brand for the product layer that sits above any one IPL team.

It should feel like:
- a cricket intelligence console
- a front-office strategy platform
- a premium analyst workspace

It should not feel like:
- a franchise fan site
- a themed microsite for one team
- a broadcast graphic package masquerading as a product

The product architecture is:
- `CreaseIQ` = master shell and design system
- team workspaces such as RR = contextual skin layered on top of the shell

This distinction is deliberate. It allows the platform to scale across teams without losing coherence or looking like a renamed franchise dashboard.

## Brand Positioning

### Core idea

CreaseIQ turns IPL ball-by-ball analysis into decision intelligence.

### Product promise

CreaseIQ helps analysts, scouting teams, and strategy staff move from raw cricket data to actionable decisions across:
- player evaluation
- matchup planning
- auction strategy
- salary value analysis
- squad construction
- match-by-match preparation

### Tone

The product should sound:
- precise
- composed
- premium
- analytical
- confident without being noisy

Avoid copy that sounds:
- fan-led
- overly promotional
- meme-heavy
- franchise dependent

## Visual Identity

### Brand mood

CreaseIQ should look like a modern intelligence product with cricket-native context.

The visual language should communicate:
- trust
- clarity
- technical rigor
- competitive edge

### Design principles

1. Neutral platform first
CreaseIQ should always read as the core system before any team tint is applied.

2. High-contrast analytical surfaces
Dense information should still feel deliberate and readable.

3. Premium restraint
Use bold accents sparingly. Most surfaces should be calm enough for data-heavy workflows.

4. Team skins are overlays, not redesigns
Team mode should change emphasis and tinting, not component architecture.

5. Sports-native, not sports-cliche
The product can feel cricket-aware without relying on literal bats, balls, pitch icons, or loud franchise aesthetics everywhere.

## Brand Palette

### CreaseIQ master palette

- `Graphite 950` `#081014`
- `Graphite 900` `#0F1720`
- `Slate 850` `#182230`
- `Slate 800` `#1E2C3C`
- `Slate 700` `#314658`
- `Mist 50` `#F5F7F8`
- `Mist 100` `#EAF0F2`
- `Mist 200` `#D6E0E5`
- `Mist 400` `#9FB0BB`
- `Signal Teal 400` `#2DD4BF`
- `Signal Teal 500` `#16B6A5`
- `Signal Teal 700` `#0D7C75`
- `Signal Amber 300` `#F5C96A`
- `Signal Amber 400` `#F5B840`
- `Signal Amber 500` `#DD9D20`
- `Signal Blue 500` `#4D8CFF`
- `Alert Rose 500` `#E85D75`

### Color roles

- Graphites and slates are the structural shell.
- Mists are the readable dashboard surfaces.
- Teal is the primary product accent.
- Amber is the secondary decision highlight.
- Blue is a tertiary analytic accent.
- Rose is reserved for risk, alerts, and team-specific overlays when needed.

## Typography

### Display font role

Use a condensed, assertive system stack for:
- hero titles
- module headers
- scoreline-like emphasis

Current stack:
- `"Trebuchet MS", "Avenir Next Condensed", "Arial Narrow", sans-serif`

### UI font role

Use a cleaner UI stack for:
- body copy
- tables
- controls
- descriptions

Current stack:
- `"Avenir Next", "Segoe UI", sans-serif`

### Type behavior

- Headers may be uppercase when the module benefits from a scorecard or control-room feel.
- Body text should remain sentence case and readable.
- Tight tracking is appropriate for display headers, but not for body copy.

## Layout and Surfaces

### Surface hierarchy

- `shell background`: dark graphite
- `inverse/navigation surfaces`: dark slate
- `primary content surfaces`: light mist panels
- `secondary content surfaces`: softer mist layers
- `accent surfaces`: teal or amber soft fills used sparingly

### Shape language

CreaseIQ uses rounded but disciplined geometry.

- small radius: controls, pills
- medium radius: tiles, callout cards
- large radius: hero panels and high-importance modules

Avoid extremely sharp or novelty geometry. The system should feel polished rather than aggressive.

## Motion and Feedback

Motion should reinforce state changes, not decorate the product.

Recommended motion style:
- short hover lifts
- subtle shadow increases
- restrained glow on focus/selection

Avoid:
- long easing curves
- playful bounce
- excessive shimmer or pulsing outside live-state indicators

## Team Skin Strategy

### Rule

CreaseIQ owns the shell. Teams only tint it.

### What team skins may change

- accent colors
- glow colors
- hero tint overlays
- badge highlights
- selected state emphasis

### What team skins should not change

- typography system
- panel architecture
- spacing scale
- control structure
- information density
- navigation model

### Example

RR can use pink and blue overlays inside an RR workspace, but the product should still feel recognizably CreaseIQ underneath.

## Product-Layer Guidance

### Main platform surfaces

These should default to the CreaseIQ neutral palette:
- `index.html`
- shared navigation shells
- public or cross-team analytics modules
- research and valuation modules

### Team workspace surfaces

These may use team skins:
- RR hub
- match-day team views
- team-specific planning surfaces

## Copy Guidance

Preferred language:
- decision intelligence
- strategy layer
- active core
- matchup edge
- valuation
- phase profile
- squad architecture

Avoid overusing:
- magic
- genius
- game changer
- fan-first slogans

## Implementation Rule

All future UI work should use semantic tokens first.

Do not hardcode franchise colors directly into shared product surfaces.

If a page is team-specific:
1. keep CreaseIQ semantic structure intact
2. override team accent tokens only
3. avoid introducing one-off layout behavior for a single team

## Short Brand Summary

CreaseIQ is a premium cricket decision-intelligence platform.

Its brand should feel:
- neutral
- strategic
- credible
- scalable across teams

The platform shell is CreaseIQ.
Team identity is a skin, not the brand.
