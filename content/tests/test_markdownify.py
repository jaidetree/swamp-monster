"""django-markdownify renders Work/WorkImage Markdown fields as HTML with the
allowed-tags whitelist enforced (settings.MARKDOWNIFY).
"""

from django.template import Context, Template


def _render(markdown_text):
    template = Template("{% load markdownify %}{{ text|markdownify }}")
    return template.render(Context({"text": markdown_text}))


def test_markdownify_renders_basic_markdown_as_html():
    html = _render("**bold** and _em_ text")
    assert "<strong>bold</strong>" in html
    assert "<em>em</em>" in html


def test_markdownify_renders_a_link():
    html = _render("[site](https://example.com)")
    assert '<a href="https://example.com">site</a>' in html


def test_markdownify_strips_disallowed_tags():
    # <script> is not in WHITELIST_TAGS, so raw/markdown-embedded HTML is
    # stripped rather than rendered.
    html = _render("<script>alert(1)</script>text")
    assert "<script>" not in html
    assert "text" in html


def test_markdownify_strips_disallowed_image_tag():
    # <img> is deliberately absent from WHITELIST_TAGS: Work/WorkImage images
    # are dedicated ImageFields, not Markdown-embedded content.
    html = _render("![alt](https://example.com/x.png)")
    assert "<img" not in html
