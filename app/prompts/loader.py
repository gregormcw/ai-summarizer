from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load_system_prompt() -> str:
    """
    Load a system prompt from the prompts directory.
    Returns:
        str: The content of the prompt file.
    """
    system_prompt_path = PROMPTS_DIR / "base.txt"

    if not system_prompt_path.exists():
        raise FileNotFoundError(
            f"System prompt file 'base.txt' not found in {PROMPTS_DIR}"
        )
    return system_prompt_path.read_text(encoding="utf-8")


def load_prompt(style: str) -> str:
    """
    Load a prompt template based on the specified style.

    Args:
        style (str): The style of the prompt (e.g., "paragraph", "bullet", "tldr").
    Returns:
        str: The content of the prompt template file.
    """
    valid_styles = ["paragraph", "bullet", "tldr"]
    if style not in valid_styles:
        raise ValueError(f"Invalid style '{style}'. Valid styles are {valid_styles}.")

    prompt_path = PROMPTS_DIR / f"{style}.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt template file '{style}.txt' not found in {PROMPTS_DIR}"
        )
    return prompt_path.read_text(encoding="utf-8")


def build_user_prompt(text: str, style: str, max_length: int) -> str:
    """
    Build the user prompt by filling in the template with the provided text and parameters.

    Args:
        text (str): The text to summarize.
        style (str): The style of the summary (e.g., "paragraph", "bullet", "tldr").
        max_length (int): The maximum length of the summary in characters.
    Returns:
        str: Combined instruction and user prompt ready to be sent to the LLM.
    """
    prompt_instruction = load_prompt(style).format(max_length=max_length)
    return prompt_instruction + "\n\nText to summarize:\n" + text
