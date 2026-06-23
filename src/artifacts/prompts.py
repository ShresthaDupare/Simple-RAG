"""Artifact prompts — templates for each artifact type."""

SYSTEM_PROMPT = "You are a study assistant. Follow the instructions precisely and format output in clean Markdown."

ARTIFACT_PROMPTS: dict[str, str] = {
    "summary": (
        "Create a comprehensive summary of the following document.\n"
        "Include:\n"
        "- Main topic and purpose\n"
        "- Key concepts (with brief explanations)\n"
        "- Important facts, formulas, or definitions\n"
        "- Section-by-section breakdown if applicable\n"
        "Format in clean Markdown with headers and bullet points.\n\n"
        "Document: {content}"
    ),
    "glossary": (
        "Extract all key terms and their definitions from the following document.\n"
        "Format as a Markdown table:\n"
        "| Term | Definition |\n"
        "|------|------------|\n"
        "Include only technical/important terms. Be concise but accurate.\n\n"
        "Document: {content}"
    ),
    "compare": (
        "Based on the following documents about {topic}, create comparison tables that highlight:\n"
        "- Similarities and differences between concepts\n"
        "- Pros and cons where applicable\n"
        "- Key distinguishing features\n"
        "Format as clean Markdown tables.\n\n"
        "Documents:\n{content}"
    ),
    "explain": (
        "Provide a detailed, step-by-step explanation of {topic} based on the following material.\n"
        "Include:\n"
        "- Clear sequential steps\n"
        "- Examples where possible\n"
        "- Common misconceptions to avoid\n"
        "Format in clean Markdown.\n\n"
        "Context:\n{content}"
    ),
}

ARTIFACT_TYPE_LABELS: dict[str, str] = {
    "summary": "Summary",
    "glossary": "Glossary",
    "compare": "Comparison",
    "explain": "Explanation",
}
