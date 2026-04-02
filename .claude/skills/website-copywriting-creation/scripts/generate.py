#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env in current working directory
load_dotenv()

def generate_copy(wireframe_path, audience, offer, tone):
    """Generates landing page copy using Claude based on wireframe and context."""

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found.")
        print("Set it in a .env file in your project root or as an environment variable.")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    # Read wireframe
    try:
        with open(wireframe_path, "r") as f:
            wireframe_content = f.read()
    except FileNotFoundError:
        print(f"Error: Wireframe file not found at {wireframe_path}")
        sys.exit(1)

    system_prompt = """You are a World-Class Copywriter specialized in High-Converting Landing Pages.
    You strictly follow the frameworks of StoryBrand (Donald Miller), Alex Hormozi ($100M Offers), and CRO best practices.

    Your goal is to take a specific WIREFRAME (structure) and fill it with persuasive, high-impact copy.

    GUIDELINES:
    - Clarity > Cleverness.
    - Write in a modular format (Section by Section).
    - Use "You" language (Customer is the Hero).
    - Focus on Transformation (Before -> After).
    - Keep paragraphs short and scannable.
    """

    user_prompt = f"""
    CONTEXT:
    - Target Audience: {audience}
    - The Offer: {offer}
    - Desired Tone: {tone}

    THE WIREFRAME (Follow this structure exactly):
    {wireframe_content}

    INSTRUCTIONS:
    Write the full landing page copy for every section in the wireframe.
    Use markdown formatting.
    Include [Visual Cues] in brackets where appropriate.
    """

    print("Generating copy with Claude...")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        temperature=0.7,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return message.content[0].text

def main():
    parser = argparse.ArgumentParser(description="Generate landing page copy from a wireframe.")
    parser.add_argument("wireframe", help="Path to the wireframe markdown file")
    parser.add_argument("--audience", required=True, help="Description of the target audience")
    parser.add_argument("--offer", required=True, help="Description of the offer")
    parser.add_argument("--tone", default="Professional yet conversational", help="Desired tone of voice")
    parser.add_argument("--output", default=".tmp/landing_page_copy.md", help="Output file path")

    args = parser.parse_args()

    copy_content = generate_copy(args.wireframe, args.audience, args.offer, args.tone)

    # Ensure directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    with open(args.output, "w") as f:
        f.write(copy_content)

    print(f"\nCopy generated successfully!")
    print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main()
