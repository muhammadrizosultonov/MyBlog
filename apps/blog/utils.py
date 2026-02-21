import markdown


def render_markdown(content: str):
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "toc",
            "tables",
            "md_in_html",
        ],
        extension_configs={
            "toc": {"permalink": True},
        },
        output_format="html5",
    )
    html = md.convert(content or "")
    toc = md.toc
    return html, toc
