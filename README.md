# Septic Pumping Dayton

Source for the independent Dayton, Texas referral website. Operator availability is unconfirmed. Do not add reviews, office locations, dispatch promises, or provider credentials without supporting evidence.

## Cloudflare Pages deployment

The `septic-dayton-preview` Pages project uses Direct Upload. A Git push does not deploy this Pages project.

From this repository, using Python 3, build into a fresh output directory outside the repository:

```text
python scripts/package_cloudflare.py --output ../cloudflare-build --zip ../cloudflare-upload.zip
```

Upload the resulting ZIP as a production deployment in the existing Pages project. Do not upload the repository directory or an old preview ZIP. The package contains 16 HTML files, including a true 404 page, plus assets and crawler configuration.

The packager converts internal links, canonical URLs, the form return URL, and sitemap entries to extensionless paths. Cloudflare redirects the original `.html` URLs to those paths. It loads Google Analytics only on the apex and www production hostnames. The pages.dev hosts receive noindex metadata and hostname-specific X-Robots-Tag rules. These rules must never apply to the live domain.

Before calling a deployment complete, verify the custom domains are Active, HTTPS works, the homepage and service pages load, original `.html` links redirect correctly, the live domain has index/follow metadata, pages.dev remains noindex, the sitemap uses clean URLs, and form return navigation works. Verify actual test receipt in the private inbox before claiming end-to-end delivery. Keep setup tests out of customer counts.

## Continuity

The repository root retains its prior GitHub Pages-compatible HTML as a migration fallback. Do not remove the old CNAME or GitHub hosting until the new domain and workflow are verified. Current hosting state belongs in the private operating record, not assumptions based on a successful build or push.

The original Muse site folder and launch ZIP are historical copies. Do not deploy them over this source. Preserve the approved navy, white, and light blue palette in `design-tokens.json`.

Keep homeowner contact information, consent records, request tracking, operator discussions, and revenue evidence out of this public repository. The private Google Sheet is a manual tracker; form emails do not append automatically.
