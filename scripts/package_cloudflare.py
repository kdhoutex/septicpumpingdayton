"""Package this static site for Cloudflare Pages without changing the source HTML."""
from pathlib import Path
import argparse, re, zipfile

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
parser.add_argument('--zip',required=True)
args=parser.parse_args()
site=Path(__file__).resolve().parents[1]
dest=Path(args.output).resolve()
if dest == site or site in dest.parents:
 raise SystemExit('Choose an output directory outside the source repository.')
if dest.exists() and any(dest.iterdir()):
 raise SystemExit('Choose a fresh output directory to avoid packaging stale files.')
dest.mkdir(parents=True,exist_ok=True)
ga='''(() => {
  if (!['septicpumpingdayton.com','www.septicpumpingdayton.com'].includes(location.hostname)) return;
  window.dataLayer=window.dataLayer||[];
  window.gtag=function(){window.dataLayer.push(arguments);};
  window.gtag('js',new Date());
  window.gtag('config','G-BJ3C7Q27TE');
  const tag=document.createElement('script'); tag.async=true;
  tag.src='https://www.googletagmanager.com/gtag/js?id=G-BJ3C7Q27TE';
  document.head.appendChild(tag);
})();
'''
for p in site.rglob('*'):
 if not p.is_file(): continue
 rel=p.relative_to(site)
 if '.git' in rel.parts or not (p.suffix=='.html' or rel.parts[0]=='assets' or rel.as_posix() in ['robots.txt','sitemap.xml','design-tokens.json']):continue
 target=dest/rel; target.parent.mkdir(parents=True,exist_ok=True)
 if p.suffix=='.html':
  text=p.read_text(encoding='utf-8')
  text=re.sub(r'<script[^>]+src="https://www.googletagmanager.com/gtag/js[^>]*></script>','',text)
  text=re.sub(r'<script>\s*window.dataLayer.*?</script>','',text,flags=re.S)
  text=re.sub(r'((?:href|value)="[^"\s]*)\.html(?=["#?])',r'\1',text)
  text=text.replace('The website is hosted on GitHub Pages.','The website is hosted on Cloudflare Pages. Its source code is maintained on GitHub.')
  text=text.replace('Provider notices:','Provider notices: <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare privacy</a>,')
  text=text.replace('</head>','<script>if(location.hostname.endsWith(".pages.dev")){document.querySelector(\'meta[name="robots"]\').content="noindex,nofollow";}</script><script src="/assets/analytics.js" defer></script>\n</head>')
  target.write_text(text,encoding='utf-8')
 elif rel.as_posix()=='sitemap.xml':target.write_text(p.read_text(encoding='utf-8').replace('.html</loc>','</loc>'),encoding='utf-8')
 else:target.write_bytes(p.read_bytes())
(dest/'assets/analytics.js').write_text(ga,encoding='utf-8')
(dest/'_headers').write_text('https://septic-dayton-preview.pages.dev/*\n  X-Robots-Tag: noindex, nofollow\n\nhttps://:deployment.septic-dayton-preview.pages.dev/*\n  X-Robots-Tag: noindex, nofollow\n',encoding='utf-8')
thanks=(dest/'thanks.html').read_text(encoding='utf-8')
not_found=re.sub(r'<main id="main">.*?</main>','<main id="main"><div class="wrap page-intro"><h1>Page not found.</h1><p>The address may have changed. <a href="/">Return to the homepage</a> or <a href="/#quote">request a referral</a>.</p></div></main>',thanks,flags=re.S)
not_found=not_found.replace('After your referral request | Septic Pumping Dayton','Page not found | Septic Pumping Dayton')
not_found=re.sub(r'<link rel="canonical"[^>]*>','',not_found)
(dest/'404.html').write_text(not_found,encoding='utf-8')
for p in dest.rglob('*.html'):
 text=p.read_text(encoding='utf-8')
 assert 'src="https://www.googletagmanager.com' not in text,p
 assert len(re.findall(r'<meta[^>]+name="robots"',text))==1,p
 assert not re.search(r'href="/[^"\s]*\.html',text),p
with zipfile.ZipFile(args.zip,'w',zipfile.ZIP_DEFLATED) as z:
 for p in dest.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(dest))
print(f'Cloudflare package ready: {len(list(dest.rglob("*.html")))} HTML files, including a true 404 page.')
