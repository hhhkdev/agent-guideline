#!/usr/bin/env python3
"""
Agent Harness CLI (harness-cli.py)
A developer utility to inspect projects, evaluate AI-readiness,
and automatically scaffold customized AGENTS.md and docs/ai/ harnesses.
"""

import os
import sys
import json
import shutil
import argparse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(REPO_ROOT, "03-templates")
SKILLS_DIR = os.path.join(REPO_ROOT, "04-skills-archive")


def detect_stack(project_path):
    files = set(os.listdir(project_path))
    stack = []
    category = "unknown"

    # Check package.json
    if "package.json" in files:
        try:
            with open(os.path.join(project_path, "package.json")) as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                
                if "react-native" in deps or "expo" in deps:
                    category = "react-native-expo"
                    stack.append("React Native / Expo")
                elif "storybook" in deps:
                    category = "design-system"
                    stack.append("Storybook Design System")
                elif "next" in deps:
                    category = "nextjs-fullstack"
                    stack.append("Next.js App Router")
                elif "vite" in deps or "react" in deps:
                    category = "nextjs-fullstack"  # similar frontend template
                    stack.append("React / Vite")
                
                if "tailwindcss" in deps:
                    stack.append("Tailwind CSS")
                if "typescript" in deps:
                    stack.append("TypeScript")
        except Exception:
            pass

    # Check Flutter
    if "pubspec.yaml" in files:
        category = "flutter-riverpod"
        stack.append("Flutter / Dart")

    # Check Spring Boot / JVM
    if any(f in files for f in ["build.gradle", "build.gradle.kts", "pom.xml"]):
        category = "spring-boot-jvm"
        stack.append("Spring Boot / JVM")

    # Check existing AI configs
    ai_configs = []
    for candidate in ["AGENTS.md", "CLAUDE.md", ".cursorrules", ".gemini", ".claude"]:
        if candidate in files:
            ai_configs.append(candidate)
    if os.path.exists(os.path.join(project_path, "docs", "ai")):
        ai_configs.append("docs/ai/")

    return category, stack, ai_configs


def scan_directory(target_path):
    print(f"\n🔍 Scanning project at: {target_path}\n" + "=" * 60)
    category, stack, ai_configs = detect_stack(target_path)
    
    print(f"📦 Detected Category : {category}")
    print(f"🛠️  Tech Stack        : {', '.join(stack) if stack else 'Unknown'}")
    print(f"🤖 Existing AI Setup : {', '.join(ai_configs) if ai_configs else 'None'}")
    
    # Readiness score
    score = 0
    if "AGENTS.md" in ai_configs:
        score += 30
    if "CLAUDE.md" in ai_configs:
        score += 20
    if "docs/ai/" in ai_configs:
        score += 50

    print(f"📊 AI Readiness Score: {score}/100")
    if score == 100:
        print("🎉 Excellent! Fully equipped with harness & modular docs.")
    elif score >= 50:
        print("⚡ Good foundation. Consider upgrading to modular docs/ai/ structure.")
    else:
        print("⚠️  Needs setup. Run `python3 harness-cli.py init <path>` to install harness.")
    print("=" * 60 + "\n")


def init_harness(target_path, template_name=None, dry_run=False):
    detected_cat, stack, _ = detect_stack(target_path)
    template = template_name or detected_cat

    src_template_dir = os.path.join(TEMPLATES_DIR, template)
    if not os.path.exists(src_template_dir):
        print(f"⚠️ Template '{template}' not found. Falling back to 'universal'.")
        src_template_dir = os.path.join(TEMPLATES_DIR, "universal")

    print(f"🚀 Initializing harness for: {target_path}")
    print(f"📁 Selected Template: {os.path.basename(src_template_dir)}")

    for root, dirs, files in os.walk(src_template_dir):
        rel_path = os.path.relpath(root, src_template_dir)
        dest_dir = target_path if rel_path == "." else os.path.join(target_path, rel_path)

        if not os.path.exists(dest_dir):
            if not dry_run:
                os.makedirs(dest_dir, exist_ok=True)
            print(f"  [CREATE DIR]  {dest_dir}")

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            action = "OVERWRITE" if os.path.exists(dest_file) else "CREATE"
            print(f"  [{action} FILE] {dest_file}")
            if not dry_run:
                shutil.copy2(src_file, dest_file)

    print("\n✅ Harness initialized successfully!")


def list_skills():
    print(f"\n📦 Archived Skills in {SKILLS_DIR}:\n" + "=" * 60)
    for skill_name in sorted(os.listdir(SKILLS_DIR)):
        skill_path = os.path.join(SKILLS_DIR, skill_name)
        if os.path.isdir(skill_path) and not skill_name.startswith("."):
            skill_file = os.path.join(skill_path, "SKILL.md")
            desc = ""
            if os.path.exists(skill_file):
                with open(skill_file) as f:
                    for line in f:
                        if line.startswith("description:"):
                            desc = line.replace("description:", "").strip()
                            break
            print(f"🔹 {skill_name}")
            if desc:
                print(f"   {desc[:100]}...")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Agent Harness Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    scan_p = subparsers.add_parser("scan", help="Scan and evaluate a project")
    scan_p.add_argument("path", help="Path to project directory")

    init_p = subparsers.add_parser("init", help="Initialize harness in project")
    init_p.add_argument("path", help="Path to project directory")
    init_p.add_argument("--template", help="Specific template to apply", default=None)
    init_p.add_argument("--dry-run", action="store_true", help="Simulate without writing")

    subparsers.add_parser("list-skills", help="List archived skills")

    args = parser.parse_args()

    if args.command == "scan":
        scan_directory(os.path.abspath(args.path))
    elif args.command == "init":
        init_harness(os.path.abspath(args.path), args.template, args.dry_run)
    elif args.command == "list-skills":
        list_skills()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
