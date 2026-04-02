#!/usr/bin/env python3
import argparse
import sys
import os

# Template metadata
TEMPLATES = {
    "1": {
        "name": "Short Warm Offer Page",
        "file": "1_short_warm.md",
        "best_for": "Email/retargeting, warm traffic, low-friction offers"
    },
    "2": {
        "name": "Direct-to-Product Ecom",
        "file": "2_ecom_product.md",
        "best_for": "Cold ads, single product campaigns"
    },
    "3": {
        "name": "Long-Form Sales Page",
        "file": "3_long_form_sales.md",
        "best_for": "High-ticket, complex offers, cold traffic"
    },
    "4": {
        "name": "Lead-Gen Services",
        "file": "4_leadgen_services.md",
        "best_for": "Services, medical, B2B, form fills"
    },
    "5": {
        "name": "Pre-Sell Advertorial",
        "file": "5_advertorial.md",
        "best_for": "Education before sale, overcoming skepticism"
    }
}

def get_script_dir():
    """Get the directory where this script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def load_template(template_key):
    """Load a template file from resources/templates/"""
    script_dir = get_script_dir()
    template_path = os.path.join(
        script_dir, 
        "..", 
        "resources", 
        "templates", 
        TEMPLATES[template_key]["file"]
    )
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    with open(template_path, "r") as f:
        return f.read()

def interactive_template_selection():
    """Present template options and get user selection."""
    print("\n=== Select Landing Page Template ===\n")
    
    for key, info in TEMPLATES.items():
        print(f"{key}. {info['name']}")
        print(f"   Best for: {info['best_for']}\n")
    
    while True:
        choice = input("Select template (1-5): ").strip()
        if choice in TEMPLATES:
            return choice
        print("Invalid selection. Please choose 1-5.")

def generate_wireframe_from_template(goal, template_content):
    """Insert goal into template and return formatted wireframe."""
    # Simple replacement - template already has structure
    wireframe = f"# Wireframe: {goal}\n\n"
    wireframe += template_content
    return wireframe

def main():
    parser = argparse.ArgumentParser(description="Generate a landing page wireframe using proven templates.")
    parser.add_argument("--goal", help="Goal of the page (e.g., 'NSS Membership Sales')")
    parser.add_argument("--template", choices=["1", "2", "3", "4", "5"], help="Template to use (1-5)")
    parser.add_argument("--output", default=".tmp/wireframe.md", help="Output file path")
    parser.add_argument("--list", action="store_true", help="List available templates and exit")

    args = parser.parse_args()
    
    # List templates and exit
    if args.list:
        print("\nAvailable Templates:\n")
        for key, info in TEMPLATES.items():
            print(f"{key}. {info['name']}")
            print(f"   File: {info['file']}")
            print(f"   Best for: {info['best_for']}\n")
        return
    
    # Get template selection
    if args.template:
        template_key = args.template
    else:
        template_key = interactive_template_selection()
    
    # Get goal
    if args.goal:
        goal = args.goal
    else:
        goal = input("\nWhat is the goal of this page? (e.g., 'Sell NSS Membership'): ").strip()
        if not goal:
            goal = "Landing Page"
    
    # Load template
    print(f"\nGenerating wireframe using '{TEMPLATES[template_key]['name']}'...")
    template_content = load_template(template_key)
    
    # Generate wireframe
    wireframe = generate_wireframe_from_template(goal, template_content)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Write to file
    with open(args.output, "w") as f:
        f.write(wireframe)
        
    print(f"✅ Wireframe saved to: {args.output}")
    print(f"📄 Template: {TEMPLATES[template_key]['name']}")

if __name__ == "__main__":
    main()
