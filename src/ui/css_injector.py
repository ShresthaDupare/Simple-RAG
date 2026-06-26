"""CSS injector — uses Streamlit Components to inject CSS into the parent document.

st.markdown() and st.html() both have issues with <style> blocks in Streamlit 1.58.0.
This component uses st.components.v1.html() with JavaScript to inject CSS into
the parent document's <head>, which works reliably.
"""

import streamlit.components.v1 as components


def inject_css(css: str) -> None:
    """Inject CSS or HTML link tags into the Streamlit page via a hidden component.

    Args:
        css: CSS string. Can be:
            - A <link> tag (for fonts)
            - A <style> block
            - Raw CSS (auto-wrapped in <style>)
    """
    # Wrap raw CSS in <style> tags if not already an HTML tag
    if not css.strip().startswith("<"):
        css = f"<style>{css}</style>"

    # Use JavaScript to inject into parent document's <head>
    html = f"""
    <div style="display:none;">
    <script>
    (function() {{
        var temp = document.createElement('div');
        temp.innerHTML = {repr(css)};
        while (temp.firstChild) {{
            document.head.appendChild(temp.firstChild);
        }}
    }})();
    </script>
    </div>
    """
    components.html(html, height=0, width=0)
