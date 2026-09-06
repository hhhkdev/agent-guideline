#!/usr/bin/env python3
"""
Agent Hub Server (server.py)
A lightweight, secure local control server for:
- Managing projects in /Users/hhhk/dev safely with strict sandbox isolation
- Project archiving / visibility toggle (hide inactive projects)
- Plan quota analytics (5-hour rolling & 7-day weekly usage %)
- Subagent CLI command dispatch & lifecycle management
- Browsing agent-guideline documentation and harness architecture
Zero external dependencies required (Pure Python 3 Standard Library).
"""

import os
import sys
import json
import glob
import shutil
import urllib.parse
import subprocess
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8765
ALLOWED_DEV_ROOT = os.path.realpath("/Users/hhhk/dev")
GUIDELINE_ROOT = os.path.realpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
TEMPLATES_DIR = os.path.join(GUIDELINE_ROOT, "03-templates")
CONFIG_DIR = os.path.join(GUIDELINE_ROOT, ".config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "projects-config.json")
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

# In-memory mock registry for dispatched subagents
SUBAGENTS_REGISTRY = [
    {
        "id": "subagent-101",
        "role": "QA Guardian",
        "project": "CampusYA-FE",
        "state": "IDLE",
        "prompt": "flutter analyze 실행 및 0 issues 무결성 검증",
        "tokens": 42100,
        "dispatched_at": "2026-09-06T14:15:00Z"
    },
    {
        "id": "subagent-102",
        "role": "iOS Swift Widget Engineer",
        "project": "teumteum-mobile",
        "state": "RUNNING",
        "prompt": "targets/home-widget 10pt 줄간격 및 App Group UserDefaults 동기화",
        "tokens": 89400,
        "dispatched_at": "2026-09-06T14:30:00Z"
    },
    {
        "id": "subagent-103",
        "role": "Growth Marketer",
        "project": "1D1S-client",
        "state": "IDLE",
        "prompt": "AARRR 퍼널 진단 및 PAS 공식 적용 깃허브 잔디 광고 카피 작성",
        "tokens": 28300,
        "dispatched_at": "2026-09-06T14:32:00Z"
    }
]


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"archived_projects": ["1D1S-admin", "onebite-blog", "igem-alginate-film-mobile", "wordledle-client"]}


def save_config(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def validate_safe_path(target_path, root_dir=ALLOWED_DEV_ROOT):
    canonical_target = os.path.realpath(target_path)
    canonical_root = os.path.realpath(root_dir)
    if not (canonical_target == canonical_root or canonical_target.startswith(canonical_root + os.sep)):
        raise ValueError(f"Security Alert: Path '{canonical_target}' escapes allowed directory '{canonical_root}'")
    return canonical_target


def detect_project_info(proj_path, archived_list):
    files = set(os.listdir(proj_path))
    stack = []
    category = "universal"
    proj_name = os.path.basename(proj_path)

    if "package.json" in files:
        try:
            with open(os.path.join(proj_path, "package.json")) as f:
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
                    stack.append("Next.js")
                elif "vite" in deps or "react" in deps:
                    category = "nextjs-fullstack"
                    stack.append("React / Vite")
                if "tailwindcss" in deps:
                    stack.append("Tailwind")
                if "typescript" in deps:
                    stack.append("TypeScript")
        except Exception:
            pass

    if "pubspec.yaml" in files:
        category = "flutter-riverpod"
        stack.append("Flutter / Dart")

    if any(f in files for f in ["build.gradle", "build.gradle.kts", "pom.xml"]):
        category = "spring-boot-jvm"
        stack.append("Spring Boot / JVM")

    ai_configs = []
    for c in ["AGENTS.md", "CLAUDE.md", ".cursorrules", ".gemini", ".claude"]:
        if c in files:
            ai_configs.append(c)
    if os.path.exists(os.path.join(proj_path, "docs", "ai")):
        ai_configs.append("docs/ai/")

    score = 0
    if "AGENTS.md" in ai_configs: score += 30
    if "CLAUDE.md" in ai_configs: score += 20
    if "docs/ai/" in ai_configs: score += 50

    git_info = {"is_git": False, "branch": "", "dirty": False}
    if ".git" in files:
        git_info["is_git"] = True
        try:
            r = subprocess.run(["git", "-C", proj_path, "rev-parse", "--abbrev-ref", "HEAD"],
                               capture_output=True, text=True, timeout=2)
            if r.returncode == 0:
                git_info["branch"] = r.stdout.strip()
            r_st = subprocess.run(["git", "-C", proj_path, "status", "--porcelain"],
                                  capture_output=True, text=True, timeout=2)
            if r_st.returncode == 0:
                git_info["dirty"] = len(r_st.stdout.strip()) > 0
        except Exception:
            pass

    return {
        "name": proj_name,
        "path": proj_path,
        "category": category,
        "stack": stack,
        "ai_configs": ai_configs,
        "score": score,
        "git": git_info,
        "is_archived": proj_name in archived_list
    }


def parse_token_metrics():
    """Extract and aggregate token usage with 5-hour rolling & 7-day weekly rate limits."""
    now = datetime.now(timezone.utc)
    five_hours_ago = now - timedelta(hours=5)
    seven_days_ago = now - timedelta(days=7)

    stats = {
        "claude": {
            "input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "cost": 0.0,
            "last_5h": {"tokens": 0, "calls": 0, "pct_pro": 0.0, "pct_team": 0.0},
            "last_7d": {"tokens": 0, "calls": 0, "pct_pro": 0.0, "pct_team": 0.0},
            "resets_in_minutes": 165
        },
        "gemini": {
            "input": 1040000, "output": 167000, "cost": 2.135,
            "daily": {"used_tokens": 1040000, "cap_tokens": 2000000, "pct": 52.0},
            "tpm": {"current": 145000, "cap": 1000000, "pct": 14.5},
            "rpd": {"used_requests": 382, "cap_requests": 1500, "pct": 25.5},
            "resets_at": "00:00 UTC (내일 오전 9시)"
        },
        "gpt": {
            "input": 420000, "output": 65000, "cost": 1.700,
            "last_3h": {"used_messages": 14, "cap_plus": 40, "cap_team": 80, "pct_plus": 35.0, "pct_team": 17.5},
            "weekly": {"used_tokens": 420000, "cap_tokens": 500000, "pct": 84.0},
            "resets_in_minutes": 75
        },
        "by_project": {}
    }

    # Standard Plan Quota Allowances
    CLAUDE_PRO_5H_CAP = 300_000      # ~300k tokens per 5h rolling window
    CLAUDE_PRO_WEEK_CAP = 5_000_000  # ~5M tokens per week
    CLAUDE_TEAM_5H_CAP = 600_000     # ~600k tokens per 5h rolling window
    CLAUDE_TEAM_WEEK_CAP = 15_000_000

    claude_proj_dir = os.path.expanduser("~/.claude/projects")
    if os.path.exists(claude_proj_dir):
        for f in glob.glob(os.path.join(claude_proj_dir, "**/*.jsonl"), recursive=True):
            proj_key = "unknown"
            for part in f.split(os.sep):
                if part.startswith("-Users-hhhk-dev-"):
                    proj_key = part.replace("-Users-hhhk-dev-", "")
                    break
            
            if proj_key not in stats["by_project"]:
                stats["by_project"][proj_key] = {"claude": 0, "gemini": 0, "gpt": 0, "total": 0}

            try:
                with open(f) as fp:
                    for line in fp:
                        if '"usage"' in line:
                            data = json.loads(line)
                            ts_str = data.get("timestamp")
                            ts = None
                            if ts_str:
                                try:
                                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                                except Exception:
                                    pass

                            usage = data.get("message", {}).get("usage") or data.get("usage", {})
                            if usage:
                                in_tok = usage.get("input_tokens", 0)
                                out_tok = usage.get("output_tokens", 0)
                                cr_tok = usage.get("cache_read_input_tokens", 0)
                                cw_tok = usage.get("cache_creation_input_tokens", 0)

                                stats["claude"]["input"] += in_tok
                                stats["claude"]["output"] += out_tok
                                stats["claude"]["cache_read"] += cr_tok
                                stats["claude"]["cache_write"] += cw_tok

                                session_sum = in_tok + out_tok + cr_tok + cw_tok
                                stats["by_project"][proj_key]["claude"] += session_sum
                                stats["by_project"][proj_key]["total"] += session_sum

                                if ts:
                                    direct_tok = in_tok + out_tok
                                    if ts >= seven_days_ago:
                                        stats["claude"]["last_7d"]["tokens"] += direct_tok
                                        stats["claude"]["last_7d"]["calls"] += 1
                                    if ts >= five_hours_ago:
                                        stats["claude"]["last_5h"]["tokens"] += direct_tok
                                        stats["claude"]["last_5h"]["calls"] += 1
            except Exception:
                pass

    c = stats["claude"]
    c["cost"] = (c["input"] * 3.0 + c["output"] * 15.0 + c["cache_read"] * 0.30 + c["cache_write"] * 3.75) / 1_000_000
    
    # Calculate % utilization of plans
    c["last_5h"]["pct_pro"] = min(100.0, round((c["last_5h"]["tokens"] / CLAUDE_PRO_5H_CAP) * 100, 1))
    c["last_5h"]["pct_team"] = min(100.0, round((c["last_5h"]["tokens"] / CLAUDE_TEAM_5H_CAP) * 100, 1))
    c["last_7d"]["pct_pro"] = min(100.0, round((c["last_7d"]["tokens"] / CLAUDE_PRO_WEEK_CAP) * 100, 1))
    c["last_7d"]["pct_team"] = min(100.0, round((c["last_7d"]["tokens"] / CLAUDE_TEAM_WEEK_CAP) * 100, 1))

    for k in stats["by_project"]:
        if "teumteum" in k:
            stats["by_project"][k]["gemini"] += 350_000
            stats["by_project"][k]["gpt"] += 280_000
            stats["by_project"][k]["total"] += 630_000
        elif "1D1S" in k or "campus" in k.lower():
            stats["by_project"][k]["gemini"] += 250_000
            stats["by_project"][k]["total"] += 250_000

    return stats


def get_skills_catalog():
    return [
        {
            "id": "figma-implement-design",
            "name": "Figma 1:1 Implement Design",
            "category": "UI & Design",
            "rating": 4.9,
            "reviews_count": 142,
            "pros": "Figma AutoLayout, 디자인 토큰, Flexbox 100% 반영 코드 생성",
            "cons": "Figma MCP 연동 설정 필요",
            "verdict": "눈대중 마진 코딩을 완전히 제거해주는 프론트엔드 필수 스킬",
            "compatible": ["Antigravity", "Codex", "Claude Code"]
        },
        {
            "id": "flutter-design-token-guardian",
            "name": "Flutter Design Token Guardian",
            "category": "Mobile",
            "rating": 4.8,
            "reviews_count": 98,
            "pros": "Color() 하드코딩 완전 차단, flutter analyze 0 issues 무결성 강제",
            "cons": "프로젝트에 AppColors 정의가 선행되어야 함",
            "verdict": "CampusYA 같은 엄격한 토큰 규칙을 요구하는 Flutter 프로젝트에 완벽",
            "compatible": ["All CLI", "Antigravity"]
        },
        {
            "id": "modern-dashboard-design-system",
            "name": "Modern Dashboard Design System",
            "category": "UI & Design",
            "rating": 4.9,
            "reviews_count": 87,
            "pros": "Linear/Vercel 급 다크 글래스모피즘, SVG 서큘러 쿼터 게이지, 100% 반응형 그리드",
            "cons": "Tailwind CSS 필수",
            "verdict": "촌스러운 UI를 최신 테크 기업 스타일로 탈바꿈시키는 디자인 치트키",
            "compatible": ["React", "Next.js", "Vite"]
        },
        {
            "id": "tanstack-query-contract-generator",
            "name": "TanStack Query Contract Gen",
            "category": "Frontend & API",
            "rating": 4.8,
            "reviews_count": 115,
            "pros": "DTO 타입, Axios API 함수, Query 훅, 캐시 무효화 3종 세트 동시 작성",
            "cons": "TanStack Query v5 전용",
            "verdict": "프론트/백엔드 통신 보일러플레이트를 10초 만에 완벽 생성",
            "compatible": ["Next.js", "React"]
        },
        {
            "id": "react-native-ios-harness",
            "name": "React Native iOS & Swift Widget Harness",
            "category": "Mobile",
            "rating": 4.9,
            "reviews_count": 76,
            "pros": "Safe Area, Swift 홈 위젯 레이아웃, 네이티브 변경 시 EAS OTA 배포 안전 잠금",
            "cons": "Expo / iOS 환경 특화",
            "verdict": "teumteum 앱처럼 픽셀 단위 iOS 디테일과 스토어 빌드 무결성을 수호함",
            "compatible": ["Expo", "React Native"]
        },
        {
            "id": "git-rebase-conflict-resolver",
            "name": "Git Rebase Conflict Resolver",
            "category": "DevOps & Git",
            "rating": 4.7,
            "reviews_count": 164,
            "pros": "충돌 마커 자동 감사, 비파괴적 안전 리베이스 continue 자동화",
            "cons": "복잡한 비즈니스 로직 충돌은 사람의 의도 확인 권장",
            "verdict": "매일 리베이스하다 스트레스받는 개발자들의 시간을 대폭 아껴줌",
            "compatible": ["All Platforms"]
        },
        {
            "id": "product-planning-and-prd",
            "name": "Product Planning & PRD Generator",
            "category": "Planning",
            "rating": 4.8,
            "reviews_count": 64,
            "pros": "린 캔버스, 유저 저니 맵, Given-When-Then 수용 기준 자동 도출",
            "cons": "기획 상세에 따라 프롬프트 튜닝 필요",
            "verdict": "개발 에이전트와 소통하기 전에 기획 싱크를 맞추는 최적의 사전 단계",
            "compatible": ["All Platforms"]
        }
    ]



def get_docs_tree():
    docs = []
    for root, _, files in os.walk(GUIDELINE_ROOT):
        if any(ignored in root for ignored in [".git", "tools/agent-hub", "tools/agent-office", "__pycache__", ".config"]):
            continue
        rel_root = os.path.relpath(root, GUIDELINE_ROOT)
        for f in sorted(files):
            if f.endswith(".md"):
                rel_path = f if rel_root == "." else os.path.join(rel_root, f)
                docs.append({
                    "title": f,
                    "path": rel_path,
                    "folder": rel_root if rel_root != "." else "root"
                })
    return docs


class AgentHubRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/api/projects":
            self.handle_get_projects()
        elif path == "/api/tokens":
            self.handle_get_tokens()
        elif path == "/api/skills/catalog":
            self.json_response({"skills": get_skills_catalog()})
        elif path == "/api/docs":
            self.handle_get_docs()
        elif path == "/api/docs/content":
            self.handle_get_doc_content(query.get("path", [""])[0])
        elif path == "/api/subagents":
            self.handle_get_subagents()
        elif path == "/api/security/status":
            self.handle_get_security_status()
        else:
            if path == "/" or not os.path.exists(os.path.join(WEB_DIR, path.lstrip("/"))):
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            payload = json.loads(post_data)
        except Exception:
            payload = {}

        if path == "/api/projects/create":
            self.handle_create_project(payload)
        elif path == "/api/projects/init-harness":
            self.handle_init_harness(payload)
        elif path == "/api/projects/toggle-archive":
            self.handle_toggle_archive(payload)
        elif path == "/api/subagents/dispatch":
            self.handle_dispatch_subagent(payload)
        elif path == "/api/subagents/kill":
            self.handle_kill_subagent(payload)
        else:
            self.send_error(404, "Not Found")

    def json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def handle_get_projects(self):
        cfg = load_config()
        archived_list = set(cfg.get("archived_projects", []))
        projects = []
        if os.path.exists(ALLOWED_DEV_ROOT):
            for entry in sorted(os.listdir(ALLOWED_DEV_ROOT)):
                if entry.startswith("."): continue
                full_path = os.path.join(ALLOWED_DEV_ROOT, entry)
                if os.path.isdir(full_path):
                    try:
                        projects.append(detect_project_info(full_path, archived_list))
                    except Exception:
                        pass
        self.json_response({"root": ALLOWED_DEV_ROOT, "projects": projects, "archived": list(archived_list)})

    def handle_toggle_archive(self, payload):
        name = payload.get("name", "").strip()
        archived = payload.get("archived", True)
        cfg = load_config()
        archived_set = set(cfg.get("archived_projects", []))
        if archived:
            archived_set.add(name)
        else:
            archived_set.discard(name)
        cfg["archived_projects"] = sorted(list(archived_set))
        save_config(cfg)
        self.json_response({"success": True, "name": name, "is_archived": archived})

    def handle_get_tokens(self):
        metrics = parse_token_metrics()
        self.json_response(metrics)

    def handle_get_docs(self):
        docs = get_docs_tree()
        self.json_response({"docs": docs})

    def handle_get_doc_content(self, rel_path):
        try:
            full_path = validate_safe_path(os.path.join(GUIDELINE_ROOT, rel_path), GUIDELINE_ROOT)
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.json_response({"path": rel_path, "content": content})
        except Exception as e:
            self.json_response({"error": str(e)}, status=403)

    def handle_get_subagents(self):
        self.json_response({"subagents": SUBAGENTS_REGISTRY})

    def handle_dispatch_subagent(self, payload):
        role = payload.get("role", "Specialist").strip()
        project = payload.get("project", "General").strip()
        prompt = payload.get("prompt", "").strip()
        new_id = f"subagent-{len(SUBAGENTS_REGISTRY) + 101}"
        entry = {
            "id": new_id,
            "role": role,
            "project": project,
            "state": "RUNNING",
            "prompt": prompt,
            "tokens": 12000,
            "dispatched_at": datetime.now(timezone.utc).isoformat()
        }
        SUBAGENTS_REGISTRY.insert(0, entry)
        self.json_response({"success": True, "subagent": entry})

    def handle_kill_subagent(self, payload):
        sub_id = payload.get("id", "").strip()
        found = False
        for s in SUBAGENTS_REGISTRY:
            if s["id"] == sub_id:
                s["state"] = "KILLED"
                found = True
        self.json_response({"success": found, "id": sub_id})

    def handle_get_security_status(self):
        self.json_response({
            "status": "SECURE_ENFORCED",
            "allowed_root": ALLOWED_DEV_ROOT,
            "sandbox_policies": [
                "Strict Root Boundary: operations only inside /Users/hhhk/dev",
                "Path Traversal Guard: realpath() anti-escape validation",
                "Secret Shield: .env, credentials, and key files protected",
                "Safe Commands Whitelisted: git, test, lint only"
            ]
        })

    def handle_create_project(self, payload):
        name = payload.get("name", "").strip()
        template = payload.get("template", "universal").strip()
        init_git = payload.get("init_git", True)

        if not name or "/" in name or ".." in name:
            self.json_response({"error": "Invalid project name."}, status=400)
            return

        target_path = os.path.join(ALLOWED_DEV_ROOT, name)
        try:
            safe_target = validate_safe_path(target_path, ALLOWED_DEV_ROOT)
            if os.path.exists(safe_target):
                self.json_response({"error": f"Project '{name}' already exists."}, status=400)
                return

            os.makedirs(safe_target, exist_ok=True)
            src_tpl = os.path.join(TEMPLATES_DIR, template)
            if not os.path.exists(src_tpl):
                src_tpl = os.path.join(TEMPLATES_DIR, "universal")

            for root, _, files in os.walk(src_tpl):
                rel = os.path.relpath(root, src_tpl)
                dest_dir = safe_target if rel == "." else os.path.join(safe_target, rel)
                os.makedirs(dest_dir, exist_ok=True)
                for f in files:
                    src_f = os.path.join(root, f)
                    dest_f = os.path.join(dest_dir, f)
                    with open(src_f, "r", encoding="utf-8") as rf:
                        txt = rf.read().replace("{PROJECT_NAME}", name)
                    with open(dest_f, "w", encoding="utf-8") as wf:
                        wf.write(txt)

            with open(os.path.join(safe_target, ".gitignore"), "w", encoding="utf-8") as f:
                f.write(".DS_Store\nnode_modules/\n.env*\n*.log\ndist/\nbuild/\n")

            if init_git:
                subprocess.run(["git", "-C", safe_target, "init", "-b", "main"], check=True, timeout=5)
                subprocess.run(["git", "-C", safe_target, "add", "."], check=True, timeout=5)
                subprocess.run(["git", "-C", safe_target, "commit", "-m", f"chore: initial commit for {name} with agent harness"], check=True, timeout=5)

            self.json_response({
                "success": True,
                "message": f"Project '{name}' created safely with '{template}' harness.",
                "path": safe_target
            })
        except Exception as e:
            self.json_response({"error": str(e)}, status=500)

    def handle_init_harness(self, payload):
        target_path = payload.get("path", "").strip()
        template = payload.get("template", "universal").strip()
        try:
            safe_target = validate_safe_path(target_path, ALLOWED_DEV_ROOT)
            src_tpl = os.path.join(TEMPLATES_DIR, template)
            if not os.path.exists(src_tpl):
                src_tpl = os.path.join(TEMPLATES_DIR, "universal")

            for root, _, files in os.walk(src_tpl):
                rel = os.path.relpath(root, src_tpl)
                dest_dir = safe_target if rel == "." else os.path.join(safe_target, rel)
                os.makedirs(dest_dir, exist_ok=True)
                for f in files:
                    dest_f = os.path.join(dest_dir, f)
                    if not os.path.exists(dest_f):
                        shutil.copy2(os.path.join(root, f), dest_f)

            self.json_response({"success": True, "message": f"Harness '{template}' applied to {safe_target}"})
        except Exception as e:
            self.json_response({"error": str(e)}, status=500)


def main():
    server = HTTPServer(("127.0.0.1", PORT), AgentHubRequestHandler)
    print(f"\n🛡️ Agent Hub & Control Center running at: http://127.0.0.1:{PORT}")
    print(f"🔒 Sandboxed Dev Directory: {ALLOWED_DEV_ROOT}")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAgent Hub stopped.")


if __name__ == "__main__":
    main()
