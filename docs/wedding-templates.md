# Wedding templates

Three invitation designs are available in the dashboard template picker:

| ID | Preview | Direction |
| --- | --- | --- |
| `alyra` | `/invitation/demo?template=alyra` | Ivory editorial, oversized Gilda Display names, overlapping photo |
| `weddings` | `/invitation/demo?template=weddings` | Cream and white, Instrument Serif, paired portraits and timeline |
| `veloria` | `/invitation/demo?template=veloria` | Taupe and olive, Newsreader/Carattere, asymmetric photographic layout |

Visual references: https://alyra-wedding.webflow.io/, https://weddings-one-page-template.webflow.io/, https://veloria-template.webflow.io/. Layouts are implemented in React/CSS, not imported Webflow source. Demo photos use the existing Unsplash sample images; real invitations use their uploaded gallery. Fonts are loaded from Google Fonts with serif fallbacks.

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
