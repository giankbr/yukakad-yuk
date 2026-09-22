# Wedding templates

Three invitation designs are available in the dashboard template picker:

| ID | Preview | Direction |
| --- | --- | --- |
| `alyra` | `/invitation/demo?template=alyra` | Ivory editorial, oversized Gilda Display names, overlapping photo |
| `weddings` | `/invitation/demo?template=weddings` | Close recreation of the one-page Webflow template: top bar, italic Instrument Serif hero, paired square photos, slider, timeline, RSVP, tabs, FAQ (`WeddingsOnePage`) |
| `veloria` | `/invitation/demo?template=veloria` | Taupe and olive, Newsreader/Carattere, asymmetric photographic layout |

Visual references: https://alyra-wedding.webflow.io/, https://weddings-one-page-template.webflow.io/, https://veloria-template.webflow.io/. Layouts are implemented in React/CSS, not imported Webflow source. Veloria borrows the agency site’s taupe/olive palette, arched photography collage, numbered stats, and dark olive bands — adapted into invitation sections rather than planner commerce pages. Demo photos use the existing Unsplash sample images; real invitations use their uploaded gallery. Fonts are loaded from Google Fonts with serif fallbacks.

The selected `template_id` is returned by the public invitation API. These three IDs render through `WeddingTemplate`; existing IDs retain the previous renderer. PostgreSQL migration 014 adds catalog entries without removing existing templates. Restart the backend to apply migrations. Preview RSVP is a local simulation and never posts a real response.

Verification:

```sh
cd backend
go test ./...
cd ../frontend
npx tsc --noEmit
npm run lint
# Start the frontend at port 3001, then:
node scripts/check-wedding-templates.mjs
```

Set `PREVIEW_ORIGIN` to another local origin and `CHROME_BIN` to your Chrome executable if needed. `UPDATE_PREVIEWS=1` regenerates the catalog screenshots. The browser check validates all three previews at 1440px and 390px, images, horizontal overflow, and demo RSVP, and saves full-page screenshots in a temporary folder.
