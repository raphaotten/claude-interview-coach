"""Convert a markdown resume to a styled PDF using markdown + xhtml2pdf."""

import sys
import re
import markdown
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

import platform as _platform
if _platform.system() == "Darwin":
    _FONT_DIR = "/System/Library/Fonts/Supplemental"
    pdfmetrics.registerFont(TTFont("Calibri",           f"{_FONT_DIR}/Arial.ttf"))
    pdfmetrics.registerFont(TTFont("Calibri-Bold",      f"{_FONT_DIR}/Arial Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Calibri-Italic",    f"{_FONT_DIR}/Arial Italic.ttf"))
    pdfmetrics.registerFont(TTFont("Calibri-BoldItalic",f"{_FONT_DIR}/Arial Bold Italic.ttf"))
else:
    _FONT_DIR = "C:/Windows/Fonts"
    pdfmetrics.registerFont(TTFont("Calibri",           f"{_FONT_DIR}/calibri.ttf"))
    pdfmetrics.registerFont(TTFont("Calibri-Bold",      f"{_FONT_DIR}/calibrib.ttf"))
    pdfmetrics.registerFont(TTFont("Calibri-Italic",    f"{_FONT_DIR}/calibrii.ttf"))
    pdfmetrics.registerFont(TTFont("Calibri-BoldItalic",f"{_FONT_DIR}/calibriz.ttf"))
registerFontFamily(
    "Calibri",
    normal="Calibri",
    bold="Calibri-Bold",
    italic="Calibri-Italic",
    boldItalic="Calibri-BoldItalic",
)

CSS = """
@page {
    size: A4;
    margin: 8mm 13mm 8mm 13mm;
}

body {
    font-family: Calibri, Helvetica, sans-serif;
    font-size: 10pt;
    line-height: 1.1;
    color: #000000;
}

h1 {
    font-size: 14pt;
    font-weight: bold;
    color: #000000;
    text-align: center;
    margin-bottom: 1pt;
    padding-bottom: 0;
}

.contact-line {
    text-align: center;
    font-size: 8pt;
    color: #000000;
    margin-top: 0;
    margin-bottom: 1pt;
}

h2 {
    font-size: 11pt;
    font-weight: bold;
    color: #000000;
    border-bottom: 1pt solid #000000;
    padding-bottom: 1pt;
    margin-top: 5pt;
    margin-bottom: 5pt;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
}

p {
    margin-top: 0;
    margin-bottom: 1pt;
    color: #000000;
}

ul {
    margin-top: 0;
    margin-bottom: 1pt;
    padding-left: 12pt;
}

li {
    margin-bottom: 0;
    color: #000000;
}

hr {
    display: none;
}

strong {
    color: #000000;
}

em {
    color: #000000;
}

.job-header {
    width: 100%;
    border-collapse: collapse;
    margin-top: 4pt;
    margin-bottom: 0;
}

.job-title {
    font-size: 10pt;
    font-weight: bold;
    color: #000000;
    text-align: left;
    padding: 0;
}

.job-date {
    font-size: 10pt;
    color: #000000;
    text-align: right;
    padding: 0;
    white-space: nowrap;
}

.job-company {
    font-size: 10pt;
    color: #000000;
    font-style: italic;
    padding: 0;
    padding-bottom: 1pt;
}

.job-location {
    font-size: 10pt;
    color: #000000;
    font-style: italic;
    text-align: right;
    padding: 0;
    padding-bottom: 1pt;
    white-space: nowrap;
}
"""


def transform_job_headers(html: str) -> str:
    """Convert <h3>Title | Company | Date</h3> into a two-row table layout."""
    def replace_h3(m):
        content = m.group(1)
        parts = [p.strip() for p in content.split(' | ')]
        if len(parts) == 4:
            title, company, location, date = parts
            return (
                f'<table class="job-header"><tr>'
                f'<td class="job-title">{title}</td>'
                f'<td class="job-date">{date}</td>'
                f'</tr><tr>'
                f'<td class="job-company">{company}</td>'
                f'<td class="job-location">{location}</td>'
                f'</tr></table>'
            )
        elif len(parts) == 3:
            title, company, date = parts
            return (
                f'<table class="job-header"><tr>'
                f'<td class="job-title">{title}</td>'
                f'<td class="job-date">{date}</td>'
                f'</tr><tr>'
                f'<td class="job-company" colspan="2">{company}</td>'
                f'</tr></table>'
            )
        elif len(parts) == 2:
            title, date = parts
            return (
                f'<table class="job-header"><tr>'
                f'<td class="job-title">{title}</td>'
                f'<td class="job-date">{date}</td>'
                f'</tr></table>'
            )
        # Single part — just render as bold paragraph
        return f'<p><strong>{content}</strong></p>'

    return re.sub(r'<h3>(.*?)</h3>', replace_h3, html)


def transform_edu_entries(html: str) -> str:
    """Convert <p><strong>Degree</strong> | School | Date</p> into table layout."""
    def replace_edu(m):
        degree = m.group(1).strip()
        rest = m.group(2).strip()
        parts = [p.strip() for p in rest.split(' | ', 1)]
        if len(parts) == 2:
            school, date = parts
            return (
                f'<table class="job-header"><tr>'
                f'<td class="job-title">{degree}</td>'
                f'<td class="job-date">{date}</td>'
                f'</tr><tr>'
                f'<td class="job-company" colspan="2">{school}</td>'
                f'</tr></table>'
            )
        return m.group(0)

    return re.sub(r'<p><strong>(.*?)</strong>\s*\|(.*?)</p>', replace_edu, html)


def tag_contact_line(html: str) -> str:
    """Apply .contact-line class to the first <p> immediately after <h1>."""
    return re.sub(
        r'(<h1>.*?</h1>\s*)(<p>)',
        r'\1<p class="contact-line">',
        html,
        count=1,
        flags=re.DOTALL,
    )


def convert(md_path: str, pdf_path: str) -> None:
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "sane_lists"],
    )

    html_body = transform_job_headers(html_body)
    html_body = transform_edu_entries(html_body)
    html_body = tag_contact_line(html_body)

    full_html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<style>{CSS}</style>
</head><body>{html_body}</body></html>"""

    with open(pdf_path, "wb") as out:
        status = pisa.CreatePDF(full_html, dest=out)

    if status.err:
        print(f"Error generating PDF: {status.err}")
        sys.exit(1)
    else:
        print(f"PDF written to {pdf_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/md_to_pdf.py <input.md> [output.pdf]")
        sys.exit(1)

    md_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else md_file.rsplit(".", 1)[0] + ".pdf"
    convert(md_file, pdf_file)
