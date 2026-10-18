# UI/UX Design System & Style Guide
## Centurion University of Technology and Management (CUTM)

---

### 1. Brand Identity & Visual Language

The visual design system of Centurion University of Technology and Management reflects institutional prestige, academic rigor, and technological innovation. It blends royal navy tones with warm educational gold accents and clean, readable typography.

---

### 2. Color Palette

| Token Name | Hex Code | Swatch | Intended Usage |
| :--- | :--- | :---: | :--- |
| `--navy` | `#102b4e` | 🟦 | Primary brand header, footer, page titles, cards |
| `--blue` | `#1458a6` | 🔷 | Interactive primary buttons, links, active navigation |
| `--gold` | `#d4af37` | 🟨 | Emblem border, highlighted badges, merit accolades |
| `--gold-light`| `#f7c567` | 🟡 | Gradient overlays, star icons, accent borders |
| `--ink` | `#17283d` | ⬛ | Body typography, high-contrast headings |
| `--muted` | `#64748b` | 🔘 | Secondary descriptions, timestamps, table subtitles |
| `--line` | `#e3e9f0` | ⚪ | Structural dividers, card borders, form input borders |
| `--pale` | `#f4f7fb` | ⬜ | Page canvas background, alternating section backgrounds |
| `--green` | `#10b981` | 🟩 | High merit probability, live sync indicator, WhatsApp |
| `--amber` | `#f59e0b` | 🟧 | Moderate chance, pending status, warning alerts |
| `--red` | `#ef4444` | 🟥 | Error feedback, low merit indicator, delete actions |

---

### 3. Typography

#### Primary Display Font: **Manrope**
- **Weights:** 700 (Bold), 800 (Extra Bold)
- **Usage:** Main hero headers, page titles, university branding, numerical KPI statistics.
- **Characteristics:** Geometric, authoritative, premium institutional appeal.

#### Primary Body Font: **DM Sans**
- **Weights:** 400 (Regular), 500 (Medium), 600 (Semi-Bold), 700 (Bold)
- **Usage:** Paragraphs, form labels, table cells, descriptions, navigation links.
- **Characteristics:** Highly legible across desktop and mobile screens.

---

### 4. Component Standards

#### 4.1 University Logo & Circular Emblem
- **Dimensions:** 50px × 50px (Header Navigation), 52px × 52px (Login Card), 38px × 38px (Admin Header).
- **Styling:**
  ```css
  border-radius: 50%;
  object-fit: contain;
  background: #ffffff;
  border: 1.5px solid rgba(212, 175, 55, 0.5);
  box-shadow: 0 4px 12px rgba(16, 43, 78, 0.12);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  ```
- **Interactivity:** Scales smoothly to `1.06` on hover.

#### 4.2 Topline Notice Banner
- High-visibility banner pinned to the top of all public pages.
- Contains the admission alert pill, helpline telephone link (`1800-123-CUTM`), official email, and quick-access portal link: `🔐 Login / Register`.

#### 4.3 Buttons & Actions
- **Primary Action (`.button`):** Solid `--blue` background, bold white text, subtle hover lift (`translateY(-1px)`).
- **Secondary Action (`.button.secondary`):** Muted slate `#eaf0f7`, `--navy` text.
- **Success Action (`.button.success`):** Soft green `#ecfdf5`, `#065f46` text, ideal for CSV exports and WhatsApp outreach.
- **Outline Action (`.btn-outline`):** Transparent background with golden or white borders.

#### 4.4 Status Badges
- **Reference ID Badge:** Monospace font, slate container (`#f1f5f9`), bold dark blue text.
- **Status Pills:**
  - `New`: Yellow pill (`#fef3c7`, text `#b45309`)
  - `Contacted`: Indigo pill (`#e0e7ff`, text `#4338ca`)
  - `Verified`: Green pill (`#dcfce7`, text `#15803d`)
  - `Confirmed`: Blue pill (`#dbeafe`, text `#1d4ed8`)
  - `Rejected`: Red pill (`#fee2e2`, text `#b91c1c`)

#### 4.5 Live Alert Toast
- Positioned fixed at `top: 22px; right: 22px; z-index: 99999;`.
- Dark navy background `#0f172a` with glowing green accent stripe `#22c55e`.
- Slide-in transition from the right (`@keyframes slideIn`).

---

### 5. Responsive Design Breakpoints

| Breakpoint | Target Devices | Layout Adjustments |
| :--- | :--- | :--- |
| `< 520px` | Mobile (Smartphones) | Single-column form grid, stacked header actions, full-width buttons |
| `520px – 768px` | Small Tablets | 2-column event forms, collapsed hamburger navigation menu |
| `768px – 1024px` | Large Tablets & Laptops | Responsive multi-column layout, visible navigation links |
| `> 1024px` | Desktop Displays | Full multi-column grid, max content container `1200px` |

