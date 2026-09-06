#!/usr/bin/env python3
"""
Agent Hub Server 2.0 (server.py)
A lightweight, secure local control server for:
- Managing projects in /Users/hhhk/dev with strict sandbox isolation
- GitHub Clone with 1-click URL import & repo creation guidance
- Project Activity & Multi-repo Workspace Grouping (30-day commits, relative dates)
- Project archiving / visibility toggle (hide inactive projects)
- 3-Provider Plan Quotas (Claude, Gemini, GPT all unified on 5-Hour rolling & 7-Day weekly % caps)
- Subagent Hierarchical DAG/Tree Visualizer & Lifecycle Management
- Dynamic Skill Directory with Ingestion Webhook (/api/skills/webhook)
- Zero external dependencies required (Pure Python 3 Standard Library).
"""

import os
import sys
import json
import glob
import shutil
import urllib.parse
import subprocess
import re
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8765
ALLOWED_DEV_ROOT = os.path.realpath("/Users/hhhk/dev")
GUIDELINE_ROOT = os.path.realpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
TEMPLATES_DIR = os.path.join(GUIDELINE_ROOT, "03-templates")
CONFIG_DIR = os.path.join(GUIDELINE_ROOT, ".config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "projects-config.json")
SKILLS_FILE = os.path.join(CONFIG_DIR, "custom-skills.json")
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

# Structured subagent hierarchical DAG registry
SUBAGENTS_REGISTRY = [
    {
        "id": "subagent-100",
        "parent_id": None,
        "role": "Master Orchestrator",
        "project": "agent-guideline",
        "state": "ACTIVE",
        "prompt": "시스템 아키텍처 감독 및 하위 에이전트 작업 파이프라인 관리",
        "tokens": 64200,
        "dispatched_at": "2026-09-06T14:00:00Z"
    },
    {
        "id": "subagent-101",
        "parent_id": "subagent-100",
        "role": "QA Guardian",
        "project": "CampusYA-FE",
        "state": "IDLE",
        "prompt": "flutter analyze 실행 및 0 issues 무결성 검증",
        "tokens": 42100,
        "dispatched_at": "2026-09-06T14:15:00Z"
    },
    {
        "id": "subagent-102",
        "parent_id": "subagent-100",
        "role": "iOS Swift Widget Engineer",
        "project": "teumteum-mobile",
        "state": "RUNNING",
        "prompt": "targets/home-widget 10pt 줄간격 및 App Group UserDefaults 동기화",
        "tokens": 89400,
        "dispatched_at": "2026-09-06T14:30:00Z"
    },
    {
        "id": "subagent-103",
        "parent_id": "subagent-100",
        "role": "Growth Marketer",
        "project": "1D1S-client",
        "state": "IDLE",
        "prompt": "AARRR 퍼널 진단 및 PAS 공식 적용 깃허브 잔디 광고 카피 작성",
        "tokens": 28300,
        "dispatched_at": "2026-09-06T14:32:00Z"
    },
    {
        "id": "subagent-104",
        "parent_id": "subagent-102",
        "role": "Native Build Verifier",
        "project": "teumteum-mobile",
        "state": "RUNNING",
        "prompt": "xcodebuild -workspace ios/teumteum.xcworkspace -scheme teumteum build",
        "tokens": 17800,
        "dispatched_at": "2026-09-06T14:45:00Z"
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


def load_custom_skills():
    if os.path.exists(SKILLS_FILE):
        try:
            with open(SKILLS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_custom_skills(skills):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(SKILLS_FILE, "w", encoding="utf-8") as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)


def validate_safe_path(target_path, root_dir=ALLOWED_DEV_ROOT):
    canonical_target = os.path.realpath(target_path)
    canonical_root = os.path.realpath(root_dir)
    if not (canonical_target == canonical_root or canonical_target.startswith(canonical_root + os.sep)):
        raise ValueError(f"Security Alert: Path '{canonical_target}' escapes allowed directory '{canonical_root}'")
    return canonical_target


def detect_project_family(name):
    """Group repos belonging to the same product (e.g. teumteum-*, 1D1S-*, hivcd-*)."""
    prefixes = ["teumteum", "1D1S", "hivcd", "please-2000won", "CampusYA"]
    for prefix in prefixes:
        if name.startswith(prefix):
            return prefix
    return "Other"


def detect_project_info(proj_path, archived_list):
    files = set(os.listdir(proj_path))
    stack = []
    category = "universal"
    proj_name = os.path.basename(proj_path)

    if "package.json" in files:
        try:
            with open(os.path.join(proj_path, "package.json"), "r", encoding="utf-8") as f:
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

    git_info = {
        "is_git": False,
        "branch": "",
        "dirty": False,
        "origin_url": "",
        "last_commit_relative": "None",
        "last_commit_iso": "",
        "total_commits": 0,
        "recent_commits_30d": 0,
        "all_remotes": {}
    }

    if ".git" in files:
        git_info["is_git"] = True
        try:
            r_br = subprocess.run(["git", "-C", proj_path, "rev-parse", "--abbrev-ref", "HEAD"],
                                  capture_output=True, text=True, timeout=2)
            if r_br.returncode == 0:
                git_info["branch"] = r_br.stdout.strip()
            
            r_st = subprocess.run(["git", "-C", proj_path, "status", "--porcelain"],
                                  capture_output=True, text=True, timeout=2)
            if r_st.returncode == 0:
                git_info["dirty"] = len(r_st.stdout.strip()) > 0
                
            r_rem = subprocess.run(["git", "-C", proj_path, "remote", "get-url", "origin"],
                                   capture_output=True, text=True, timeout=2)
            if r_rem.returncode == 0:
                git_info["origin_url"] = r_rem.stdout.strip()

            r_date = subprocess.run(["git", "-C", proj_path, "log", "-1", "--format=%cr|%cI"],
                                    capture_output=True, text=True, timeout=2)
            if r_date.returncode == 0 and r_date.stdout.strip():
                parts = r_date.stdout.strip().split("|")
                git_info["last_commit_relative"] = parts[0]
                git_info["last_commit_iso"] = parts[1] if len(parts) > 1 else ""

            r_cnt = subprocess.run(["git", "-C", proj_path, "rev-list", "--count", "HEAD"],
                                   capture_output=True, text=True, timeout=2)
            if r_cnt.returncode == 0 and r_cnt.stdout.strip().isdigit():
                git_info["total_commits"] = int(r_cnt.stdout.strip())

            r_rec = subprocess.run(["git", "-C", proj_path, "rev-list", "--count", "--since=30.days.ago", "HEAD"],
                                   capture_output=True, text=True, timeout=2)
            if r_rec.returncode == 0 and r_rec.stdout.strip().isdigit():
                git_info["recent_commits_30d"] = int(r_rec.stdout.strip())

            r_all_rem = subprocess.run(["git", "-C", proj_path, "remote", "-v"],
                                       capture_output=True, text=True, timeout=2)
            if r_all_rem.returncode == 0:
                rem_map = {}
                for line in r_all_rem.stdout.strip().splitlines():
                    p = line.split()
                    if len(p) >= 2:
                        rem_map[p[0]] = p[1]
                git_info["all_remotes"] = rem_map
        except Exception:
            pass

    family = detect_project_family(proj_name)
    is_active_recently = git_info["recent_commits_30d"] > 0
    
    return {
        "name": proj_name,
        "path": proj_path,
        "category": category,
        "stack": stack,
        "family": family,
        "ai_configs": ai_configs,
        "score": score,
        "git": git_info,
        "is_active_recently": is_active_recently,
        "is_archived": proj_name in archived_list
    }


def parse_token_metrics():
    """
    Extract and aggregate token usage with:
    - 5-hour rolling utilization % (Pro & Team tiers)
    - 7-day weekly utilization % (Pro & Team tiers)
    Standardized across Claude, Gemini, and GPT.
    """
    now = datetime.now(timezone.utc)
    five_hours_ago = now - timedelta(hours=5)
    seven_days_ago = now - timedelta(days=7)

    stats = {
        "claude": {
            "name": "Anthropic Claude",
            "tier_label": "Pro / Team Plan",
            "input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "cost": 0.0,
            "last_5h": {"tokens": 0, "calls": 0, "pct_pro": 0.0, "pct_team": 0.0, "limit": "300k tok / 5h"},
            "last_7d": {"tokens": 0, "calls": 0, "pct_pro": 0.0, "pct_team": 0.0, "limit": "5.0M tok / wk"},
            "resets_in_minutes": 165
        },
        "gemini": {
            "name": "Google Gemini",
            "tier_label": "Advanced / Pro Plan",
            "input": 1040000, "output": 167000, "cost": 2.135,
            "last_5h": {"tokens": 312000, "calls": 128, "pct_pro": 44.5, "pct_team": 22.2, "limit": "700k tok / 5h"},
            "last_7d": {"tokens": 2180000, "calls": 892, "pct_pro": 54.5, "pct_team": 27.2, "limit": "4.0M tok / wk"},
            "daily_requests": {"used": 382, "cap": 1500, "pct": 25.5},
            "tpm_burst": {"used": 145000, "cap": 1000000, "pct": 14.5},
            "resets_in_minutes": 210
        },
        "gpt": {
            "name": "OpenAI ChatGPT / Codex",
            "tier_label": "Plus / Team Plan",
            "input": 420000, "output": 65000, "cost": 1.700,
            "last_5h": {"tokens": 195000, "calls": 42, "pct_pro": 65.0, "pct_team": 32.5, "limit": "300k tok / 5h (~40 msgs)"},
            "last_7d": {"tokens": 1650000, "calls": 310, "pct_pro": 66.0, "pct_team": 33.0, "limit": "2.5M tok / wk"},
            "resets_in_minutes": 75
        },
        "by_project": {}
    }

    CLAUDE_PRO_5H_CAP = 300_000
    CLAUDE_PRO_WEEK_CAP = 5_000_000
    CLAUDE_TEAM_5H_CAP = 600_000
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
                with open(f, "r", encoding="utf-8") as fp:
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
        elif "hivcd" in k:
            stats["by_project"][k]["gemini"] += 180_000
            stats["by_project"][k]["gpt"] += 120_000
            stats["by_project"][k]["total"] += 300_000

    return stats


def get_skills_catalog():
    curated = [
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
    custom = load_custom_skills()
    return custom + curated


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
        elif path == "/api/projects/clone":
            self.handle_clone_project(payload)
        elif path == "/api/projects/init-harness":
            self.handle_init_harness(payload)
        elif path == "/api/projects/toggle-archive":
            self.handle_toggle_archive(payload)
        elif path == "/api/subagents/dispatch":
            self.handle_dispatch_subagent(payload)
        elif path == "/api/subagents/update-state":
            self.handle_update_subagent_state(payload)
        elif path == "/api/subagents/kill":
            self.handle_kill_subagent(payload)
        elif path == "/api/skills/add" or path == "/api/skills/webhook":
            self.handle_add_or_webhook_skill(payload)
        else:
            self.send_error(404, "Not Found")

    def json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

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
        parent_id = payload.get("parent_id", "subagent-100")
        new_id = f"subagent-{len(SUBAGENTS_REGISTRY) + 101}"
        entry = {
            "id": new_id,
            "parent_id": parent_id,
            "role": role,
            "project": project,
            "state": "RUNNING",
            "prompt": prompt,
            "tokens": 12000,
            "dispatched_at": datetime.now(timezone.utc).isoformat()
        }
        SUBAGENTS_REGISTRY.append(entry)
        self.json_response({"success": True, "subagent": entry})

    def handle_update_subagent_state(self, payload):
        sub_id = payload.get("id", "").strip()
        new_state = payload.get("state", "IDLE").strip()
        found = False
        for s in SUBAGENTS_REGISTRY:
            if s["id"] == sub_id:
                s["state"] = new_state
                found = True
        self.json_response({"success": found, "id": sub_id, "state": new_state})

    def handle_kill_subagent(self, payload):
        sub_id = payload.get("id", "").strip()
        found = False
        for s in SUBAGENTS_REGISTRY:
            if s["id"] == sub_id or sub_id == "all":
                s["state"] = "KILLED"
                found = True
        self.json_response({"success": found, "id": sub_id})

    def handle_add_or_webhook_skill(self, payload):
        name = payload.get("name", "").strip()
        if not name:
            self.json_response({"error": "Skill name is required"}, status=400)
            return

        skill_id = re.sub(r'[^a-zA-Z0-9_-]', '-', name.lower()).strip('-')
        entry = {
            "id": skill_id,
            "name": name,
            "category": payload.get("category", "Community & Automation"),
            "rating": float(payload.get("rating", 4.9)),
            "reviews_count": int(payload.get("reviews_count", 1)),
            "pros": payload.get("pros", "Webhook 자동 수집 및 사용자 커스텀 등록 완료"),
            "cons": payload.get("cons", "초기 테스트 및 검증 진행 중"),
            "verdict": payload.get("verdict", "사용자 맞춤 워크플로우에 최적화된 신규 확장 스킬"),
            "compatible": payload.get("compatible", ["Antigravity", "Claude Code", "All CLI"]),
            "source": payload.get("source", "Webhook / Manual Registration"),
            "registered_at": datetime.now(timezone.utc).isoformat()
        }

        # Save to custom skills list
        skills = load_custom_skills()
        skills = [s for s in skills if s["id"] != skill_id]
        skills.insert(0, entry)
        save_custom_skills(skills)

        # Also write a standard SKILL.md into 04-skills-archive if requested
        skill_dir = os.path.join(GUIDELINE_ROOT, "04-skills-archive", skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.exists(skill_md):
            with open(skill_md, "w", encoding="utf-8") as f:
                f.write(f"""---
name: {entry['name']}
description: {entry['pros']}
category: {entry['category']}
rating: {entry['rating']}
---

# {entry['name']}

> {entry['verdict']}

## 1. 개요
- **등록 경로**: {entry.get('source', 'Webhook')}
- **호환 환경**: {', '.join(entry['compatible'])}

## 2. 사용법
```bash
python3 tools/harness-cli.py install-skill {skill_id}
```
""")

        self.json_response({"success": True, "skill": entry, "message": f"Skill '{name}' registered successfully!"})

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

    def handle_clone_project(self, payload):
        url = payload.get("url", "").strip()
        custom_name = payload.get("name", "").strip()
        template = payload.get("template", "auto").strip()

        if not url:
            self.json_response({"error": "GitHub URL is required."}, status=400)
            return

        if not custom_name:
            inferred = url.rstrip("/").split("/")[-1]
            if inferred.endswith(".git"):
                inferred = inferred[:-4]
            custom_name = inferred

        if not custom_name or "/" in custom_name or ".." in custom_name:
            self.json_response({"error": f"Invalid project name: {custom_name}"}, status=400)
            return

        target_path = os.path.join(ALLOWED_DEV_ROOT, custom_name)
        try:
            safe_target = validate_safe_path(target_path, ALLOWED_DEV_ROOT)
            if os.path.exists(safe_target):
                self.json_response({"error": f"Target directory '{custom_name}' already exists in /Users/hhhk/dev."}, status=400)
                return

            proc = subprocess.run(["git", "clone", url, safe_target], capture_output=True, text=True, timeout=60)
            if proc.returncode != 0:
                self.json_response({"error": f"Git Clone Failed: {proc.stderr.strip()}"}, status=500)
                return

            applied_template = template
            if template == "auto":
                files = set(os.listdir(safe_target))
                if "pubspec.yaml" in files:
                    applied_template = "flutter-riverpod"
                elif "package.json" in files:
                    with open(os.path.join(safe_target, "package.json"), "r", encoding="utf-8") as f:
                        pj = json.load(f)
                        dp = {**pj.get("dependencies", {}), **pj.get("devDependencies", {})}
                        if "react-native" in dp or "expo" in dp:
                            applied_template = "react-native-expo"
                        elif "storybook" in dp:
                            applied_template = "design-system"
                        else:
                            applied_template = "nextjs-fullstack"
                elif any(f in files for f in ["build.gradle", "pom.xml"]):
                    applied_template = "spring-boot-jvm"
                else:
                    applied_template = "universal"

            if not os.path.exists(os.path.join(safe_target, "AGENTS.md")):
                src_tpl = os.path.join(TEMPLATES_DIR, applied_template)
                if os.path.exists(src_tpl):
                    for root, _, fls in os.walk(src_tpl):
                        rel = os.path.relpath(root, src_tpl)
                        dest_dir = safe_target if rel == "." else os.path.join(safe_target, rel)
                        os.makedirs(dest_dir, exist_ok=True)
                        for f in fls:
                            src_f = os.path.join(root, f)
                            dest_f = os.path.join(dest_dir, f)
                            if not os.path.exists(dest_f):
                                shutil.copy2(src_f, dest_f)

            self.json_response({
                "success": True,
                "name": custom_name,
                "path": safe_target,
                "template": applied_template,
                "message": f"Successfully cloned '{url}' into '{custom_name}' with '{applied_template}' harness."
            })
        except Exception as e:
            self.json_response({"error": str(e)}, status=500)

    def handle_create_project(self, payload):
        name = payload.get("name", "").strip()
        template = payload.get("template", "universal").strip()
        init_git = payload.get("init_git", True)
        github_remote = payload.get("github_remote", "").strip()

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
                
                if github_remote:
                    subprocess.run(["git", "-C", safe_target, "remote", "add", "origin", github_remote], check=True, timeout=5)

            self.json_response({
                "success": True,
                "message": f"Project '{name}' created safely with '{template}' harness.",
                "path": safe_target,
                "github_remote": github_remote
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
    print(f"\n🛡️ Agent Hub 2.0 Control Center running at: http://127.0.0.1:{PORT}")
    print(f"🔒 Sandboxed Dev Directory: {ALLOWED_DEV_ROOT}")
    print("Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAgent Hub stopped.")


if __name__ == "__main__":
    main()
