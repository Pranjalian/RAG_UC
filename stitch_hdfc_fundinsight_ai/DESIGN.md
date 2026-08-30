---
name: Cognitive Wealth
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#bccabb'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#869486'
  outline-variant: '#3d4a3e'
  surface-tint: '#4de082'
  primary: '#6bfb9a'
  on-primary: '#003919'
  primary-container: '#4ade80'
  on-primary-container: '#005e2d'
  inverse-primary: '#006d36'
  secondary: '#adc6ff'
  on-secondary: '#002e6a'
  secondary-container: '#0566d9'
  on-secondary-container: '#e6ecff'
  tertiary: '#d8e0fa'
  on-tertiary: '#283044'
  tertiary-container: '#bcc4de'
  on-tertiary-container: '#495166'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6dfe9c'
  primary-fixed-dim: '#4de082'
  on-primary-fixed: '#00210c'
  on-primary-fixed-variant: '#005227'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#dae2fd'
  tertiary-fixed-dim: '#bec6e0'
  on-tertiary-fixed: '#131b2e'
  on-tertiary-fixed-variant: '#3f465c'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-mono:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: -0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style
The design system is engineered to project a synthesis of institutional reliability and forward-looking intelligence. It caters to sophisticated investors who value data-driven clarity over traditional financial jargon. 

The aesthetic is **Dark-Mode Glassmorphism**, utilizing deep atmospheric layering to create a sense of infinite digital space. The interface should feel like a high-end command center—precise, calm, and illuminated by subtle data-driven "energy" from the neon accents. High-transparency surfaces and background blurs are used to signify the AI's "fluid" processing power, while sharp typography ensures the factual nature of the mutual fund data remains the focus.

## Colors
This design system utilizes a deep-space palette to reduce eye strain and emphasize glowing data visualizations.

- **Primary (#4ade80):** A soft neon green used exclusively for growth indicators, primary call-to-actions, and "active" AI states.
- **Secondary (#3b82f6):** A vibrant blue used for informational highlights, secondary interactive elements, and stability indicators.
- **Background (#0f172a):** A deep slate-navy that serves as the foundation for all glass effects.
- **Surface:** Derived from the background with varying opacities (e.g., `rgba(15, 23, 42, 0.6)`) to create the glass effect.
- **Accents:** Subtle radial gradients combining the primary and secondary colors should be used sparingly as background "glows" to suggest AI presence.

## Typography
The typography strategy balances the approachable, geometric curves of **Outfit** for headings with the high-legibility, functional nature of **Inter** for data and body text. 

- Use **Outfit** for all display and headline roles to reinforce a futuristic, "tech-first" brand image.
- Use **Inter** for all fund performance metrics, AI-generated insights, and navigational labels.
- Financial figures should use the `data-mono` style to ensure numbers align vertically in tables and lists, aiding quick comparison of fund returns.

## Layout & Spacing
The layout follows a **Fluid Grid** model with generous internal padding to maintain the "airy" feel of the glassmorphic style. 

- **Desktop:** 12-column grid with 24px gutters. Content is centered within a 1280px max-width container.
- **Mobile:** 4-column grid with 16px margins. 
- **Rhythm:** All spacing (margins, padding, gaps) must be multiples of the 8px base unit. 
- AI-driven insights should be presented in "floating" modules that span the full width of the container on mobile, or 4-8 columns on desktop, to differentiate them from standard fund listings.

## Elevation & Depth
Depth is created through **Glassmorphism** and light, not shadows.

- **Background:** The base `#0f172a` layer.
- **Glass Panels:** Semi-transparent surfaces (`opacity: 60-80%`) with a `backdrop-filter: blur(12px)`. 
- **Borders:** Instead of heavy shadows, use 1px solid borders with a linear gradient (top-left to bottom-right). The gradient should go from white (at 10-20% opacity) to completely transparent.
- **Glowing States:** Elements that require high focus (like the AI's current suggestion) should have a soft, 20px outer glow using the primary or secondary color at 15% opacity.

## Shapes
This design system employs a "Rounded" language to soften the technical nature of the AI.

- **Standard Elements:** Use `0.5rem` (8px) for buttons, input fields, and small cards.
- **Container Elements:** Use `1rem` (16px) for main content cards and modals to create a distinct grouping.
- **Pill Elements:** Use `100px` (full round) for status chips (e.g., "High Growth," "Low Risk") and the primary AI chat trigger.

## Components
- **Buttons:** Primary buttons use a solid `#4ade80` fill with dark text. Secondary buttons use a glass background with a subtle `#3b82f6` border.
- **Input Fields:** Semi-transparent dark fills with a 1px border that glows blue (#3b82f6) when focused. Labels should always sit above the field in the `label-sm` style.
- **Glass Cards:** The core component. Must feature a `backdrop-filter: blur(16px)` and a subtle gradient border. Used for fund summaries and AI-generated portfolio advice.
- **Charts & Sparklines:** Use the primary green for positive growth and secondary blue for baseline or comparative indices. Avoid red unless indicating critical errors; use neutral grays for negative performance to maintain the "calm" brand tone.
- **AI Chat Interface:** A persistent, semi-transparent panel that slides from the right or bottom, utilizing the most intense glass blur and a soft green ambient glow at the header.
- **Chips:** Small, pill-shaped indicators with low-opacity fills of the accent colors (e.g., 10% green fill with 100% green text).