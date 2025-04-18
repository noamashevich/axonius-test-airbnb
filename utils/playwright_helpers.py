def safe_get_text(page, selector: str) -> str:
    try:
        element = page.locator(selector)
        if element.is_visible(timeout=3000):
            return " ".join(element.inner_text().split())
    except:
        pass
    return "Not Available"