from langchain_core.tools import tool
from playwright.sync_api import sync_playwright
import os

@tool
def get_rendered_html(url: str) -> str:
    """
    Fetch and return the fully rendered HTML of a webpage.

    This function uses Playwright to load a webpage in a headless Chromium
    browser, allowing all JavaScript on the page to execute. Use this for
    dynamic websites that require rendering.

    IMPORTANT RESTRICTIONS:
    - ONLY use this for actual HTML webpages (articles, documentation, dashboards).
    - DO NOT use this for direct file links (URLs ending in .csv, .pdf, .zip, .png).
      Playwright cannot render these and will crash. Use the 'download_file' tool instead.

    Parameters
    ----------
    url : str
        The URL of the webpage to retrieve and render.

    Returns
    -------
    str
        The fully rendered and cleaned HTML content.
    """
    # ... existing code ...
    print("\nFetching and rendering:", url)

    if url.startswith("file://"):
        local_path = url.replace("file://", "", 1)
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading local file: {e}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Load the page (let JS execute)
            page.goto(url, wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(1500)

            # Extract rendered HTML
            content = page.content()

            browser.close()
            return content

    except Exception as e:
        return f"Error fetching/rendering page: {str(e)}"