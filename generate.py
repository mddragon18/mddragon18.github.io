import os, yaml, markdown, shutil
from datetime import datetime

# Load config
with open("config.yml") as f:
    CONFIG = yaml.safe_load(f)

POSTS_DIR = "posts"
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "site"

def load_template(name):
    return open(os.path.join(TEMPLATES_DIR, name)).read()

def render(template, **kwargs):
    html = template
    for k, v in kwargs.items():
        html = html.replace(f"{{{{ {k} }}}}", str(v))
    return html

def parse_post(path):
    with open(path) as f:
        lines = f.read().split("---", 2)
        meta = yaml.safe_load(lines[1])
        body = lines[2].strip()
    html = markdown.markdown(body, extensions=["fenced_code", "codehilite"])
    return meta, html

def build():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    shutil.copytree("assets", os.path.join(OUTPUT_DIR, "assets"))

    base = load_template("base.html")
    post_tpl = load_template("post.html")

    posts_meta = []
    for fname in sorted(os.listdir(POSTS_DIR), reverse=True):
        if not fname.endswith(".md"): continue
        meta, html = parse_post(os.path.join(POSTS_DIR, fname))
        slug = fname.replace(".md", "")
        outdir = os.path.join(OUTPUT_DIR, "posts", slug)
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "index.html"), "w") as f:
            f.write(render(base,
                title=meta["title"],
                content=render(post_tpl, content=html, **meta),
                **CONFIG
            ))
        posts_meta.append(meta | {"slug": slug})

    # Index
    index_content = "<h1>Blog</h1><ul>"
    for p in posts_meta:
        url = f"/posts/{p['slug']}/"
        index_content += f'<li><a href="{url}">{p["date"]} - {p["title"]}</a></li>'
    index_content += "</ul>"

    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(render(base, title=CONFIG["site_name"], content=index_content, **CONFIG))

if __name__ == "__main__":
    build()
