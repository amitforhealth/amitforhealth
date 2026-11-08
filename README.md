# AmitForHealth

Source of amitforhealth.in, Amit Kumar's personal site.

- `posts/` — one Markdown file per essay (title, slug, dek, date, section at the top)
- `assets/style.css` — the design
- `build.py` — turns the posts into the website (`python3 build.py`, needs `pip install markdown pyyaml`)
- `site/` — the finished website that Cloudflare Pages publishes

**To add an essay:** add a file to `posts/`, list its slug under the right section at the top of `build.py`, run `python3 build.py`, commit and push. Cloudflare republishes in about a minute.

Cloudflare Pages settings: framework preset **None**, build command **empty**, build output directory **site**.
