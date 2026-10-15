# Working Together and site-wide layout audit | 15 October 2026

The existing `terms.html` route now presents **Working Together**. Project Policies remains the small section/navigation label. All eight approved policies, both tables, the full introduction and the closing enquiry text are preserved in `content/working-together.json`.

## Policy page

- Editorial reading measure, full-length paragraphs and numbered sections; no fixed-height policy cards.
- Desktop sticky contents navigation with current-section indication. At 1050px and below it returns to normal flow, protecting tablet reading space.
- Native keyboard-accessible mobile accordions at 600px and below. All text remains open without JavaScript; anchor navigation opens its destination. Direct hash links work.
- Anchor offsets account for a sticky/fixed header if one is present. The current site header is in normal flow.
- Semantic payment and licensing tables with captions and row/column headers. Both tables wrap within the mobile viewport.
- Request a Quote uses `contact.html?type=project`, retaining the current enquiry process.

## Shared causes and corrections

1. Absolute cover ornaments occupied the same visual area as cover titles. `layout-safeguards.css` isolates their stacking, makes ornaments ignore pointer input, and gives cover lettering the matching opaque background. The artwork remains around the text.
2. Shared action rows and section headings did not consistently reserve independent space for wrapped links and their underlines. Action alignment, wrapping, underline padding and action-to-section spacing now keep rules in normal flow, outside text and controls.
3. The generic `.resource-body article+article` margin also applied inside resource/sample grids, offsetting adjacent cards. It is reset specifically inside those grids. Resource-card headings now use measured responsive type instead of the generic large heading size.
4. The generic table minimum width was 620px, including inside narrow sample cards. Sample tables now use a fixed column layout with wrapping and appropriate cell padding. Other intentionally scrollable comparison tables remain contained within their own scroll area.
5. Shared grid/flex children, footer disclosures, buttons and forms now have scoped wrapping, natural height, line-height, focus and touch-target safeguards. Existing colors, animation behavior, images and editorial dividers are retained.

## Verification

- 66 root HTML routes discovered; no other HTML routes exist in this checkout.
- 64 public routes reviewed in Chromium at **375, 390, 430, 768, 820, 1024, 1280, 1440 and 1920px**, height 1000px.
- **576 route/viewport checks and full-page screenshots**, including initial and expanded disclosure/review states. Border/text geometry, clipping, page overflow and runtime errors checked. No unresolved findings in the final matrix.
- Screenshots inspected across every public route at mobile and desktop widths, with larger targeted reviews of policy tables, typography, sample cards, actions and tablet navigation.
- **450 additional layout-state checks**: all package categories and all three markets at all nine widths; work filters; FAQ search/expanded states; filled/focused contact form. All 24 service-detail pages additionally checked with every market selected at 375, 820 and 1440px.
- Policy accordions tested with Enter and Space; all nine widths tested for section links, deep links, active navigation, responsive navigation position and quote handoff.
- Existing package-to-enquiry handoff and all four enquiry routing/success states passed with mocked submissions. No real messages sent.
- BellaBelles five-slide carousel navigation and all three original videos passed playback and seeking checks. Rhode prototype and strategy-PDF actions retained.
- 149 unique internal file/fragment destinations checked; no missing local files or fragment targets.
- All 22 root JavaScript files passed `node --check`. This is a static site with no package/build manifest or separate application build command.
- `assets/`, `packages.json`, `catalogue.js`, and `rate-model.js` are unchanged from the pre-task commit. No package records, rates, CV facts, downloads or approved project media were rewritten.
- Owner routes `enquiries.html` and `feedback-review.html` retain their verified redirects to the existing authenticated host. Its private interface was not accessed or visually audited.

Browser automation uses Chromium viewport emulation. Physical iPad/iPhone devices and Safari were not available; these are not claimed as device/Safari tests. Geometry checks complement screenshot inspection and interaction checks; they are not a guarantee for every possible browser/font/user-content combination.

## Repeating the checks

Install `scripts/requirements-validation.txt` and the Playwright Chromium browser. Serve the repository root with `python3 -m http.server 8000`, then run `python scripts/audit_layout.py --base-url http://localhost:8000/ --output /tmp/portfolio-layout-audit`. Screenshot files are review artifacts outside the repository. The policy source can be rebuilt with `python scripts/build_policies.py`.

## Route-by-route coverage

Every public route below passed the nine-width matrix in both initial and expanded states. Other than the policy body and footer label, page copy and project content are unchanged; shared styles and cache references were updated.

| Route | Scope | Result |
| --- | --- | --- |
| `404.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `approach.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `availability.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `brief.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `build-brief.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `calculator.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `case-advertising-research.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `case-beetle-club.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `case-bellabelles-egypt.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `case-moving-truck.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `case-rhode.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `case-substack.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `case-the-sae-talk.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `case-thy-academia.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `checklist.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `collaborate.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `compare.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `confirmation.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `contact.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `cv.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `experience.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `faq.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `feedback.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `guide.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `index.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `journey.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `privacy.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `recruiters.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `samples.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-1.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-10.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-11.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-12.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-13.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-14.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-15.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-16.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-17.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-18.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-19.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-2.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-20.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-21.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-22.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-23.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-24.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-3.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-4.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-5.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-6.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-7.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-8.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `service-9.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `services.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `start.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `terms.html` | Approved policy content and responsive page redesign | All nine widths passed |
| `transformations.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `website-business.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `website-landing.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `website-portfolio.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `website-shop.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `websites.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `work.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |
| `writing.html` | Shared typography, borders, spacing and interaction-state audit | All nine widths passed |

| Owner redirect | Result |
| --- | --- |
| `enquiries.html` | Existing authenticated-host redirect verified; private interface not audited |
| `feedback-review.html` | Existing authenticated-host redirect verified; private interface not audited |
