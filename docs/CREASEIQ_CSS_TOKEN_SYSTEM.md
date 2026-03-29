# CreaseIQ CSS Token System

## Goal

This token system separates:
- foundation values
- semantic product roles
- team-skin overrides
- compatibility aliases used by the current dashboard

The system is designed so the product can migrate gradually without breaking existing pages.

## 1. Foundation tokens

Foundation tokens are raw values. They should not be used directly in component CSS unless a semantic token does not exist yet.

### Color foundations

- `--cq-ink-950`
- `--cq-ink-900`
- `--cq-ink-850`
- `--cq-ink-800`
- `--cq-ink-700`
- `--cq-stone-50`
- `--cq-stone-100`
- `--cq-stone-200`
- `--cq-stone-400`
- `--cq-teal-400`
- `--cq-teal-500`
- `--cq-teal-700`
- `--cq-amber-300`
- `--cq-amber-400`
- `--cq-amber-500`
- `--cq-blue-500`
- `--cq-rose-500`

### Typography foundations

- `--cq-font-display`
- `--cq-font-ui`

### Layout foundations

- `--cq-radius-sm`
- `--cq-radius-md`
- `--cq-radius-lg`
- `--cq-radius-xl`
- `--cq-shadow-card`
- `--cq-shadow-accent`
- `--cq-shadow-soft`

## 2. Semantic product tokens

These are the tokens components should prefer.

### Shell tokens

- `--cq-shell-bg`
- `--cq-shell-bg-2`
- `--cq-shell-glow-primary`
- `--cq-shell-glow-secondary`
- `--cq-shell-grid-line`

Use for:
- page background
- sidebar / navigation shells
- ambient glows

### Surface tokens

- `--cq-surface-1`
- `--cq-surface-2`
- `--cq-surface-3`
- `--cq-surface-inverse`

Use for:
- panels
- tiles
- elevated cards
- inverse badges

### Text tokens

- `--cq-text-primary`
- `--cq-text-secondary`
- `--cq-text-inverse`
- `--cq-text-inverse-muted`

Use for:
- headings
- body text
- metadata
- dark-surface copy

### Accent tokens

- `--cq-accent-primary`
- `--cq-accent-primary-strong`
- `--cq-accent-primary-soft`
- `--cq-accent-secondary`
- `--cq-accent-secondary-soft`
- `--cq-accent-tertiary`

Use for:
- CTA buttons
- emphasis pills
- active states
- interactive highlights

### Border tokens

- `--cq-border-soft`
- `--cq-border-strong`
- `--cq-border-accent`
- `--cq-border-highlight`

Use for:
- card borders
- pills
- nav items
- selection states

### Status tokens

- `--cq-status-positive`
- `--cq-status-warning`
- `--cq-status-danger`
- `--cq-status-danger-soft`

Use for:
- positive metrics
- caution states
- risk or alert states

## 3. Team-skin tokens

These are the only tokens a team skin should override.

- `--cq-team-accent-primary`
- `--cq-team-accent-secondary`
- `--cq-team-glow`
- `--cq-team-surface-tint`

### Why only these

This keeps the product architecture stable while letting team mode feel contextual.

### Example usage

Shared product shell:
- `body`
- `sidebar`
- `hero-panel`

Team-aware tinting:
- callout backgrounds
- button gradients
- section glows
- featured-story cards

## 4. Current supported selectors

The shared stylesheet now supports:
- `body[data-team-theme="rr"]`
- `body[data-team-theme="csk"]`
- `body[data-team-theme="mi"]`

These are examples, not the full final team library.

Future team skins should follow the same pattern rather than hardcoding colors across components.

## 5. Compatibility aliases

To avoid rewriting the entire dashboard at once, the current stylesheet maps older variables onto the new semantic system.

Aliases currently provided:
- `--bg`
- `--panel`
- `--panel-strong`
- `--ink`
- `--muted`
- `--accent`
- `--accent-soft`
- `--line`
- `--good`
- `--card-shadow`
- `--radius`
- `--display`
- `--ui`

These should be treated as transition variables. New code should prefer semantic `--cq-*` tokens.

## 6. Usage rules

### Rule 1

Use semantic tokens in component CSS before reaching for foundation tokens.

### Rule 2

Do not put raw team colors into shared modules.

### Rule 3

If a page needs team mode, set the team theme on the page container or body, then let token overrides flow through.

### Rule 4

If a new semantic need appears repeatedly, add a semantic token instead of scattering one-off values.

## 7. Recommended migration path

1. Keep existing pages working through alias mapping.
2. Update new components to use `--cq-*` tokens directly.
3. Refactor team-specific pages so they consume shared semantic tokens with team overrides.
4. Reduce dependence on transition aliases over time.

## 8. Example

Preferred:

```css
.module-card {
  background: var(--cq-surface-1);
  color: var(--cq-text-primary);
  border: 1px solid var(--cq-border-soft);
  border-radius: var(--cq-radius-lg);
}
```

Team-aware CTA:

```css
.cta {
  background: linear-gradient(
    135deg,
    var(--cq-accent-primary-strong),
    var(--cq-team-accent-primary)
  );
  color: var(--cq-text-inverse);
}
```

## 9. Decision summary

CreaseIQ uses:
- a neutral premium shell
- semantic design tokens
- thin team-skin overrides

This is the intended long-term UI architecture for the product.
