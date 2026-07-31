class PromptRegistry:
    """
    Manages prompt templates for various AI generation tasks.
    """
    def __init__(self):
        self.templates = {
            "recommendation": "Based on the following architecture context, provide 3 actionable recommendations to improve the system's design, security, or maintainability.\n\nContext:\n{context}",
            "documentation": "Generate a comprehensive Markdown README for the following domain based on its manifest and requirements.\n\nContext:\n{context}",
            "architecture_explanation": "Explain the architecture of this domain in simple terms for a new developer onboarded to the team.\n\nContext:\n{context}"
        }

    def get_prompt(self, template_name: str, context: str) -> str:
        template = self.templates.get(template_name, self.templates["recommendation"])
        return template.format(context=context)
