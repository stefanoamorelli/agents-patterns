import os


def get_anthropic_model():
    """Get Anthropic Claude model using API key from environment."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found in environment. "
            "Make sure it's exported in your shell or .env file"
        )

    from strands.models.anthropic import AnthropicModel
    return AnthropicModel(
        model_id="claude-3-5-sonnet-20241022",
        max_tokens=8192,
    )


def get_default_model():
    """Get the default model (Anthropic Claude)."""
    return get_anthropic_model()
