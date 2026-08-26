# PieseAutoHar.ro - Detalii Extrase

## Info General
- Nume: Auto Har
- Titlu: Piese Auto din Dezmembrari Suceava | Auto Har
- URL: https://pieseautohar.ro
- Tip: React SPA pe GitHub Pages

## SEO
- Meta desc: "Piese auto din dezmembrari Suceava - Auto Har. Piese originale second-hand, import Europa, garantie si livrare rapida."
- Keywords: piese auto dezmembrari Suceava, piese auto second hand Suceava
- OG locale: ro_RO

## Design System (din CSS)

### Culori HSL
| Rol | HSL | HEX |
|-----|-----|-----|
| Background | 220 15% 10% | #14161b |
| Foreground | 0 0% 98% | #fafafa |
| Primary | 0 72% 51% | #d92b2b |
| Accent (Mint) | 168 76% 42% | #1abc9c |
| Card | 220 14% 14% | #181a20 |
| Muted | 220 12% 22% | #2a2d35 |
| Border | 220 12% 20% | #26292f |

### Gradient-uri
- primary: linear-gradient(135deg, #d92b2b, #b32424)
- mint: linear-gradient(135deg, #1abc9c, #16a085)
- dark: linear-gradient(180deg, #14161b, #0c0d10)
- card: linear-gradient(145deg, #1a1c22, #14161b)
- glass: linear-gradient(135deg, rgba(26,28,34,0.8), rgba(20,22,27,0.6))

### Fonturi
- Principal: Outfit, system-ui, sans-serif
- Titluri: Space Grotesk, sans-serif
- Mono: SFMono-Regular, Menlo, Monaco

### Efecte
- Card glass: backdrop-filter: blur(20px)
- Shadow card: 0 20px 50px rgba(0,0,0,0.5)
- Glow rosu: 0 0 40px rgba(217,43,43,0.25)
- Glow mint: 0 0 40px rgba(26,188,156,0.3)
- Border radius: 0.75rem
- Container max: 1400px

## Arhitectura Tehnica
- Framework: React + Vite
- Styling: Tailwind CSS
- UI Lib: shadcn/ui (Radix UI)
- Charts: Recharts
- Routing: custom SPA handler pt GitHub Pages

## Tracking
- Google Analytics: G-806DL60HS1
- Google Ads: AW-17863968839
- Cookie consent banner GDPR (bottom)
- Tracking se incarca doar dupa accept cookies

## Componente Identificate
- Hero overlay (gradient: #16181d80 -> #16181dd9 -> #16181d)
- Card glass, gradient card
- Sidebar colapsabil
- Navigation menu viewport
- Dialog/Modal cu animatii slide
- Toast/Snackbar cu swipe
- Tabel intunecat cu hover
- Skeleton loading (pulse)
- Input, badge, button variants
- Accordion

## Layout Breakpoints
- sm: 640px (2 coloane)
- md: 768px (4 coloane produse, navbar desktop)
- lg: 1024px (3-4 coloane)

## Animatii CSS
- float: translateY(0) -> (-8px), 4s infinite
- pulse-glow: glow pulsant mint, 2s infinite
- accordion-up/down
- slide-in/out pentru sidebar, dialog, toast

## Note
Site-ul este o aplicatie React SPA - continutul dinamic (produse, pagini, text renderizat) se incarca prin JavaScript si nu a putut fi extras static. Informatiile de mai sus provin din meta tag-uri, CSS si structura HTML initiala.
