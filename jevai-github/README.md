# Jev.ai — jevai.it.com

English, static multi-page directory.

## Included

- 46 preserved original source URLs, grouped into 10 categories.
- Search, category filtering, A–Z sorting, empty-state reset and URL filter state.
- Homepage, What, Why, How, full English field guide, TypeSafe resources and privacy.
- Original purple/green J jester emblem.
- Per-page titles, descriptions, canonical links, JSON-LD, sitemap and robots.
- Google Analytics G-6B7H863MFF, loaded after visitor consent.
- A browser-dependent optional WebMCP filter tool; unsupported browsers continue normally.

## Build and preview

Requires Python 3.9+; Node is used only for JavaScript checks.

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check dist/assets/site.js
node scripts/check-interactions.cjs
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Use an HTTP server rather than opening the files directly: links are root-relative.

`content/projects.json` stores all translated project entries. `content/*.md` stores page copy. `scripts/build.py` generates the static HTML. CSS, JS and the logo live in `dist/assets/` and are authored assets; do not delete that folder before building.

## Remaining inputs

The source article references 17 unavailable media files: three still images, seven videos and seven video posters. See `content/media-manifest.json`. The delivered Markdown contained relative paths, not the files or their origin. No missing-image elements are rendered. Original media requires the source article URL or local asset directory before the site can be considered complete.

The English guide is an editorial translation/adaptation of the supplied article, not a claim that this site ran its experiments. Vendor reports, source-author measurements and illustrative calculations are labeled. Resource links distinguish TypeSafe official pages, community projects, integration providers and independent authors.

The domain is configured in metadata but has not been connected or deployed. Analytics delivery has not been verified in the GA dashboard. All 46 supplied external URLs are preserved; their projects have not been individually installed or audited.

## Validation

Static document checks and a lightweight DOM-fixture JavaScript interaction check pass. These do not substitute for visual QA in a real browser. WebMCP registration and execution in a supported browser have not been validated.

## Deployment

Use `dist/` as the public root on your static hosting provider. The included `vercel.json` sets this output directory for Vercel. Keep source content and scripts outside the public root. Connect and verify jevai.it.com separately. The root 404.html is supplied for hosts that support custom missing-page responses.

## September 23 content update

The long guide has been replaced by focused overview, setup, examples, question types, confidence, performance, demos, use cases, limitations and rollout pages. `/guide/` redirects to `/what-is-jev/` on Cloudflare Pages. Two supplied screenshots are included; remaining original media is pending. Navigation uses Official TypeSafe resources and no separate official-site header button.
