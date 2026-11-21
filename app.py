
import streamlit as st

from scraper.multi_page_scraper import scrape_website
from ai.content_generator import generate_brochure_content
from pdf.pdf_generator import create_pdf


st.set_page_config(
    page_title="AI Company Brochure Generator",
    page_icon="📘",
    layout="wide"
)


st.title("📘 AI Company Brochure Generator")

st.write(
    "Enter a public company website URL to generate a professional brochure."
)

st.info(
    "Use only public website pages that you are permitted to access. "
    "This application does not bypass logins, paywalls or CAPTCHAs."
)


url = st.text_input(
    "Company Website URL",
    placeholder="https://example.com"
)


if st.button(
    "Generate Brochure",
    type="primary",
    disabled=not url.strip()
):

    try:

        # Step 1: Scrape website
        with st.spinner("Scraping website pages and finding company logo..."):

            pages = scrape_website(url.strip())

        if not pages:

            st.error("No useful website pages were found.")
            st.stop()

        st.success(
            f"Successfully collected {len(pages)} pages."
        )

        # Step 2: Get company logo
        logo_data = pages[0].get("logo_data", "")

        if logo_data:

            st.success("Company logo detected successfully.")

        else:

            st.info(
                "Company logo was not found. "
                "A default logo mark will be used."
            )

        # Step 3: Generate brochure content
        with st.spinner("Generating brochure using Ollama..."):

            brochure_text = generate_brochure_content(pages)

        st.subheader("Brochure Preview")

        st.markdown(brochure_text)

        # Step 4: Get company name
        company_name = pages[0].get(
            "title",
            "Company Profile"
        )

        # Step 5: Generate PDF with logo
        with st.spinner("Creating professional PDF..."):

            pdf_bytes = create_pdf(
                brochure_text,
                company_name,
                logo_data
            )

        st.success("Brochure PDF created successfully!")

        # Step 6: Download PDF
        st.download_button(
            label="Download Company Brochure PDF",
            data=pdf_bytes,
            file_name="company_brochure.pdf",
            mime="application/pdf"
        )

    except Exception as error:

        st.error(f"Error: {error}")

        st.caption(
            "Check whether Ollama is running, the model is installed, "
            "and the website is accessible."
        )
