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


def print_tokens():
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server
    metrics = server.parse_token_metrics()

    print("\n📊 Multi-Provider Token & Cost Analytics:")
    print("=" * 60)
    for provider, name in [("claude", "Anthropic Claude"), ("gemini", "Google Gemini"), ("gpt", "OpenAI GPT")]:
        d = metrics.get(provider, {})
        in_t = d.get("input", 0)
        out_t = d.get("output", 0)
        cost = d.get("cost", 0.0)
        krw = round(cost * 1330)
        print(f"🤖 {name}:")
        print(f"   Input Tokens : {in_t:,}")
        print(f"   Output Tokens: {out_t:,}")
        if "cache_read" in d:
            print(f"   Cache Read   : {d.get('cache_read', 0):,}")
        print(f"   Est. Cost    : ${cost:.2f} (₩{krw:,})\n")

    print("📁 Token Consumption by Project:")
    for proj, val in sorted(metrics.get("by_project", {}).items(), key=lambda x: x[1]["total"], reverse=True):
        print(f"   • {proj:25}: {val['total']:,} tokens (Claude: {val['claude']:,} | Gemini: {val['gemini']:,} | GPT: {val['gpt']:,})")
    print("=" * 60 + "\n")


def print_quota():
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server
    metrics = server.parse_token_metrics()
    c = metrics.get("claude", {})
    l5 = c.get("last_5h", {})
    l7 = c.get("last_7d", {})

    print("\n⏳ 5-Hour Rolling & Weekly Quota Rate Limits (Subscription Plans):")
    print("=" * 65)
    print("🤖 Anthropic Claude Plan Utilization:")
    print(f"   • 5-Hour Window : {l5.get('tokens', 0):,} tokens ({l5.get('calls', 0)} calls)")
    print(f"     - Pro Plan Rate Limit  : [{l5.get('pct_pro', 0):>5.1f}%] {'█' * int(l5.get('pct_pro', 0) // 5)}{'░' * (20 - int(l5.get('pct_pro', 0) // 5))}")
    print(f"     - Team Plan Rate Limit : [{l5.get('pct_team', 0):>5.1f}%] {'█' * int(l5.get('pct_team', 0) // 5)}{'░' * (20 - int(l5.get('pct_team', 0) // 5))}")
    print(f"     - 5h Window Rolling Reset in ~{c.get('resets_in_minutes', 165)} minutes\n")

    print(f"   • 7-Day Weekly Window : {l7.get('tokens', 0):,} tokens ({l7.get('calls', 0)} calls)")
    print(f"     - Pro Plan Weekly Cap  : [{l7.get('pct_pro', 0):>5.1f}%] {'█' * int(l7.get('pct_pro', 0) // 5)}{'░' * (20 - int(l7.get('pct_pro', 0) // 5))}")
    print(f"     - Team Plan Weekly Cap : [{l7.get('pct_team', 0):>5.1f}%] {'█' * int(l7.get('pct_team', 0) // 5)}{'░' * (20 - int(l7.get('pct_team', 0) // 5))}")
    print("=" * 65 + "\n")


def toggle_project_archive(name, archive=True):
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server
    cfg = server.load_config()
    archived_set = set(cfg.get("archived_projects", []))
    if archive:
        archived_set.add(name)
        print(f"📦 Project '{name}' is now ARCHIVED (hidden from active list).")
    else:
        archived_set.discard(name)
        print(f"✨ Project '{name}' is now UNARCHIVED (visible in active list).")
    cfg["archived_projects"] = sorted(list(archived_set))
    server.save_config(cfg)


def manage_subagents(action, role=None, project=None, prompt=None, subagent_id=None):
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server

    if action == "list":
        print("\n🤖 Active Subagents Registry:")
        print("=" * 65)
        for s in server.SUBAGENTS_REGISTRY:
            status_symbol = "🟢" if s["state"] == "RUNNING" else ("⚪" if s["state"] == "IDLE" else "🔴")
            print(f"{status_symbol} [{s['id']}] {s['role']:25} | {s['project']:18} | {s['state']}")
            print(f"   Prompt: {s['prompt'][:60]}...")
            print(f"   Tokens: {s['tokens']:,} | Dispatched: {s['dispatched_at']}\n")
        print("=" * 65)
    elif action == "dispatch":
        new_entry = {
            "id": f"subagent-{len(server.SUBAGENTS_REGISTRY) + 101}",
            "role": role or "Custom Specialist",
            "project": project or "General",
            "state": "RUNNING",
            "prompt": prompt or "No prompt provided",
            "tokens": 0,
            "dispatched_at": datetime.now(timezone.utc).isoformat()
        }
        server.SUBAGENTS_REGISTRY.insert(0, new_entry)
        print(f"🚀 Dispatched subagent: {new_entry['id']} ({new_entry['role']}) for project '{new_entry['project']}'")
    elif action == "kill":
        for s in server.SUBAGENTS_REGISTRY:
            if s["id"] == subagent_id:
                s["state"] = "KILLED"
                print(f"🛑 Terminated subagent: {subagent_id}")
                return
        print(f"⚠️ Subagent '{subagent_id}' not found.")


def create_project(name, template="universal"):
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server
    allowed_root = server.ALLOWED_DEV_ROOT
    target_path = os.path.join(allowed_root, name)
    try:
        safe_target = server.validate_safe_path(target_path, allowed_root)
        if os.path.exists(safe_target):
            print(f"❌ Error: Project '{name}' already exists at {safe_target}")
            return
        os.makedirs(safe_target, exist_ok=True)
        init_harness(safe_target, template)
        # Git init
        import subprocess
        subprocess.run(["git", "-C", safe_target, "init", "-b", "main"], check=True)
        subprocess.run(["git", "-C", safe_target, "add", "."], check=True)
        subprocess.run(["git", "-C", safe_target, "commit", "-m", f"chore: initial commit for {name} with agent harness"], check=True)
        print(f"\n🎉 Successfully created project '{name}' at {safe_target} with '{template}' harness.")
        print(f"👉 Next steps to connect GitHub:\n   cd {safe_target}\n   gh repo create hhhkdev/{name} --private --source=. --push\n")
    except Exception as e:
        print(f"❌ Security/Creation Error: {e}")


def serve_dashboard(port=8765):
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server
    from http.server import HTTPServer
    httpd = HTTPServer(("127.0.0.1", port), server.AgentHubRequestHandler)
    print(f"\n🛡️ Agent Hub Control Center running at: http://127.0.0.1:{port}")
    print(f"🔒 Sandbox Whitelist: {server.ALLOWED_DEV_ROOT}")
    print("Press Ctrl+C to exit.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nAgent Hub stopped.")



def clone_project(url, custom_name=None, template="auto"):
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server
    req = {"url": url, "name": custom_name or "", "template": template}
    # Call internal clone handler logic
    inferred = custom_name or url.rstrip("/").split("/")[-1].replace(".git", "")
    target_path = os.path.join(server.ALLOWED_DEV_ROOT, inferred)
    try:
        safe_target = server.validate_safe_path(target_path, server.ALLOWED_DEV_ROOT)
        if os.path.exists(safe_target):
            print(f"❌ Error: Target directory '{inferred}' already exists.")
            return
        print(f"📥 Cloning '{url}' into '{safe_target}'...")
        import subprocess
        subprocess.run(["git", "clone", url, safe_target], check=True)
        init_harness(safe_target, template if template != "auto" else None)
        print(f"🎉 Successfully cloned and initialized harness at: {safe_target}")
    except Exception as e:
        print(f"❌ Clone Error: {e}")

def launch_desktop():
    app_path = os.path.join(REPO_ROOT, "tools", "Agent Hub.app")
    import subprocess
    if os.path.exists(app_path):
        print("🖥️  Opening standalone 'Agent Hub.app' with custom icon and status bar...")
        subprocess.run(["open", app_path])
    else:
        script_path = os.path.join(REPO_ROOT, "tools", "launch-desktop.sh")
        subprocess.run(["bash", script_path])


def list_ports():
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server
    ports = server.get_active_dev_ports()
    print("\n🔌 Active Listening Ports & Running Projects:")
    print("=" * 70)
    for p in ports:
        status_tag = "🚀 [DEV PROJECT]" if p["is_dev"] else "⚙️  [SYSTEM/BG]"
        print(f"Port :{p['port']:<6} | PID: {p['pid']:<7} | {status_tag} {p['project_name']}")
        print(f"   Cmd: {p['command']} -> {p['cmdline'][:60]}...")
        if p["is_dev"]:
            print(f"   Dir: {p['cwd']}")
        print("-" * 70)
    print()

def kill_port_cli(port=None, pid=None):
    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools", "agent-hub"))
    import server
    success, msg = server.terminate_process_on_port(port=port, pid=pid)
    if success:
        print(f"✓ {msg}")
    else:
        print(f"❌ Failed to terminate: {msg}")

def launch_menubar():
    bin_path = os.path.join(REPO_ROOT, "tools", "status-bar", "agent-hub-menubar")
    import subprocess
    print("⚡ Starting Agent Hub Status Bar monitor in background...")
    subprocess.Popen([bin_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✓ Status Bar icon running! Check your macOS top menu bar for ⚡ C:% G:% O:%")

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
    subparsers.add_parser("tokens", help="Show token metrics across Claude, Gemini, GPT")
    subparsers.add_parser("quota", help="Show 5-hour rolling and 7-day plan quota utilization percentage")

    arch_p = subparsers.add_parser("archive", help="Archive a project to hide from active list")
    arch_p.add_argument("name", help="Project name")

    unarch_p = subparsers.add_parser("unarchive", help="Unarchive a project to show in active list")
    unarch_p.add_argument("name", help="Project name")

    sub_p = subparsers.add_parser("subagent", help="Manage and inspect subagents via CLI")
    sub_sub = sub_p.add_subparsers(dest="sub_action")
    sub_sub.add_parser("list", help="List active subagents")
    disp_p = sub_sub.add_parser("dispatch", help="Dispatch a new subagent")
    disp_p.add_argument("--role", required=True, help="Role name")
    disp_p.add_argument("--project", default="General", help="Project name")
    disp_p.add_argument("--prompt", required=True, help="Task prompt")
    kill_p = sub_sub.add_parser("kill", help="Kill a subagent")
    kill_p.add_argument("id", help="Subagent ID (e.g. subagent-101)")

    create_p = subparsers.add_parser("create-project", help="Create a new sandboxed project")
    create_p.add_argument("name", help="Project name (under /Users/hhhk/dev)")
    create_p.add_argument("--template", help="Harness template (nextjs-fullstack, react-native-expo, flutter-riverpod, spring-boot-jvm, design-system, universal)", default="universal")

    ports_p = subparsers.add_parser("ports", help="List active ports and running projects")
    
    kill_port_p = subparsers.add_parser("kill-port", help="Kill process running on specific port")
    kill_port_p.add_argument("port", type=int, help="Port number to kill (e.g. 3000)")

    subparsers.add_parser("menubar", help="Launch macOS menu bar status monitor")

    clone_p = subparsers.add_parser("clone", help="Clone GitHub repo and auto-inject harness")
    clone_p.add_argument("url", help="GitHub repo URL")
    clone_p.add_argument("--name", help="Custom folder name", default=None)
    clone_p.add_argument("--template", help="Harness template", default="auto")

    start_p = subparsers.add_parser("start", help="All-in-one: launch server, menubar monitor, and desktop app window")
    desktop_p = subparsers.add_parser("desktop", help="Launch Agent Hub as standalone macOS desktop app")

    serve_p = subparsers.add_parser("serve", help="Launch the Agent Hub Web Control Center")
    serve_p.add_argument("--port", type=int, default=8765, help="Port to listen on")

    args = parser.parse_args()

    if args.command == "scan":
        scan_directory(os.path.abspath(args.path))
    elif args.command == "init":
        init_harness(os.path.abspath(args.path), args.template, args.dry_run)
    elif args.command == "list-skills":
        list_skills()
    elif args.command == "tokens":
        print_tokens()
    elif args.command == "quota":
        print_quota()
    elif args.command == "archive":
        toggle_project_archive(args.name, archive=True)
    elif args.command == "unarchive":
        toggle_project_archive(args.name, archive=False)
    elif args.command == "subagent":
        if args.sub_action == "list":
            manage_subagents("list")
        elif args.sub_action == "dispatch":
            manage_subagents("dispatch", role=args.role, project=args.project, prompt=args.prompt)
        elif args.sub_action == "kill":
            manage_subagents("kill", subagent_id=args.id)
        else:
            sub_p.print_help()
    elif args.command == "create-project":
        create_project(args.name, args.template)
    elif args.command == "ports":
        list_ports()
    elif args.command == "kill-port":
        kill_port_cli(port=args.port)
    elif args.command == "menubar":
        launch_menubar()
    elif args.command == "clone":
        clone_project(args.url, args.name, args.template)
    elif args.command == "start" or args.command == "desktop":
        launch_desktop()
    elif args.command == "serve":
        serve_dashboard(args.port)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

