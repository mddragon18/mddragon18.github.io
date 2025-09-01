import os, markdown

POSTS_DIR = "posts"
TEMPLATE = open("templates/base.html").read()

def render(title, content):
    return TEMPLATE.replace("{{ title }}", title).replace("{{ content }}", content)

def main():
    links = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            path = os.path.join(POSTS_DIR, filename)
            with open(path, "r") as f:
                text = f.read()
            html = markdown.markdown(text)
            title = text.strip().splitlines()[0].replace("#", "").strip()
            outname = filename.replace(".md", ".html")
            with open(outname, "w") as f:
                f.write(render(title, html))
            links.append(f'<li><a href="{outname}">{title}</a></li>')

    index_html = "<h1>My Blog</h1><ul>" + "\n".join(links) + "</ul>"
    with open("index.html", "w") as f:
        f.write(render("Home", index_html))

if __name__ == "__main__":
    main()

