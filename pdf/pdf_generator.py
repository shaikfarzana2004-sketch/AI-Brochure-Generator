
from pathlib import Path
from html import escape

from markdown import markdown
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_PATH = ROOT / "brochure" / "template.html"
CSS_PATH = ROOT / "brochure" / "style.css"


HEADER_TEMPLATE = """
<div style="
    width: 100%;
    margin: 0 18mm;
    padding-bottom: 5px;
    border-bottom: 1px solid #dce5eb;
    font-family: Arial, sans-serif;
    font-size: 8px;
    color: #748398;
">
    AI COMPANY BROCHURE GENERATOR
</div>
"""


FOOTER_TEMPLATE = """
<div style="
    width: 100%;
    margin: 0 18mm;
    padding-top: 5px;
    border-top: 1px solid #dce5eb;
    display: flex;
    justify-content: space-between;
    font-family: Arial, sans-serif;
    font-size: 8px;
    color: #748398;
">
    <span>Company Profile</span>

    <span>
        Page <span class="pageNumber"></span>
        of <span class="totalPages"></span>
    </span>
</div>
"""


def build_html(
    brochure_text,
    company_name="Company Profile",
    company_logo_data=""
):

    # Check template file
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(
            f"Template not found: {TEMPLATE_PATH}"
        )

    # Check CSS file
    if not CSS_PATH.exists():
        raise FileNotFoundError(
            f"CSS file not found: {CSS_PATH}"
        )

    # Read HTML template
    template = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    # Read CSS
    css = CSS_PATH.read_text(
        encoding="utf-8"
    )

    # Convert Markdown into HTML
    body = markdown(
        brochure_text,
        extensions=[
            "extra",
            "sane_lists",
            "nl2br",
            "tables"
        ]
    )

    # Prepare company name safely
    safe_name = escape(
        (company_name or "Company Profile")[:100]
    )

    # Prepare logo HTML
    if (
        company_logo_data
        and company_logo_data.startswith("data:image/")
        and ";base64," in company_logo_data
    ):

        safe_logo = escape(
            company_logo_data,
            quote=True
        )

        logo_html = (
            f'<img class="company-logo" '
            f'src="{safe_logo}" '
            f'alt="Company logo">'
        )

    else:

        logo_html = (
            '<div class="logo-fallback">PROFILE</div>'
        )

    # Replace HTML placeholders
    html_document = template.replace(
        "COMPANY_NAME_PLACEHOLDER",
        safe_name
    )

    html_document = html_document.replace(
        "COMPANY_LOGO_PLACEHOLDER",
        logo_html
    )

    html_document = html_document.replace(
        "/* CSS_CONTENT_PLACEHOLDER */",
        css
    )

    html_document = html_document.replace(
        "BROCHURE_HTML_PLACEHOLDER",
        body
    )

    # Validate placeholders
    placeholders = [
        "COMPANY_NAME_PLACEHOLDER",
        "COMPANY_LOGO_PLACEHOLDER",
        "CSS_CONTENT_PLACEHOLDER",
        "BROCHURE_HTML_PLACEHOLDER"
    ]

    for placeholder in placeholders:

        if placeholder in html_document:

            raise ValueError(
                f"Template placeholder not replaced: {placeholder}"
            )

    # Validate brochure content
    if len(body.strip()) < 100:

        raise ValueError(
            "Brochure content is too short to create a PDF."
        )

    return html_document


def create_pdf(
    brochure_text,
    company_name="Company Profile",
    company_logo_data=""
):

    # Build complete HTML
    html_document = build_html(
        brochure_text,
        company_name,
        company_logo_data
    )

    # Generate PDF using Playwright
    with sync_playwright() as p:

        browser = p.chromium.launch()

        try:

            page = browser.new_page()

            page.set_content(
                html_document,
                wait_until="networkidle"
            )

            pdf_data = page.pdf(
                format="A4",
                print_background=True,

                display_header_footer=True,

                header_template=HEADER_TEMPLATE,
                footer_template=FOOTER_TEMPLATE,

                margin={
                    "top": "24mm",
                    "right": "18mm",
                    "bottom": "22mm",
                    "left": "18mm"
                }
            )

            return pdf_data

        finally:

            browser.close()
