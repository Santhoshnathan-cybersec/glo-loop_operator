#!/usr/bin/env python3
"""
glo (Git Loop Operator) — Stealth & Dark Dev Satire Edition
Developed by: Santhosh Nathan (Cybersecurity Researcher)
Instagram: @realhackies
"""

import sys
import os
import time
import json
import random
import subprocess
import argparse
import socket
from pathlib import Path
from typing import List, Tuple
from datetime import datetime, timezone, timedelta
from collections import Counter

import requests
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich import box

console = Console()

# ----------------- CONFIGURATION -----------------
DEFAULT_TOTAL_CYCLES = 5
DEFAULT_SEARCH_PATHS = [
    Path.home() / "github",
    Path.home() / "projects",
    Path.home() / "dev",
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.cwd(),
]

ECONOMY_FILE = Path.home() / ".glo_economy.json"

DARK_DEV_ROASTS = [
    "\"There is no cloud, it's just someone else's computer on fire at 3 AM.\"",
    "\"Pushing untested code directly on Friday afternoon: because suffering builds character.\"",
    "\"My code doesn't have bugs, it just develops unadvertised autonomous features.\"",
    "\"I told management the rewrite would take two weeks. That was four years and three divorces ago.\"",
    "\"Deleted the entire authentication module because it was preventing unauthorized users from giving us money.\"",
    "\"Maximum effort! Pushing straight past code review because QA is a social construct.\" — Deadpool",
    "\"You wanna know how I got these scars? A junior developer force-pushed to main branch without rebasing.\" — The Joker",
    "\"Say 'merge conflict' one more time! I dare you, I double dare you!\" — Pulp Fiction",
    "\"Sell me this pen, or I will drop all database tables in the production schema.\" — Wolf of Wall Street",
    "\"I have a bad feeling about this commit hash...\" — Han Solo",
    "\"I am inevitable. And so is this uncaught NullPointerException.\" — Thanos",
    "\"Stack Overflow was down for 20 minutes and global IT infrastructure regressed to the Bronze Age.\"",
    "\"Replacing 400 lines of microservice architecture with a single unreadable bash one-liner.\"",
    "\"Optimized performance by 90% by removing all error logging and safety assertions.\"",
    "\"The coffee has worn off, the impostor syndrome is permanent, but the green contribution graph is eternal.\""
]

COMMIT_EXCUSES = [
    "fix: deleted the bug by deleting the entire file and blaming git",
    "chore: rewrote critical database connection inside a try-catch-pass block",
    "perf: removed unit tests to dramatically accelerate build times",
    "feat: added artificial latency so we can optimize it next quarter for bonuses",
    "refactor: don't touch this file, it works on dark magic and duct tape",
    "fix: resolved race condition by making all threads sleep indefinitely",
    "docs: updated README to state that the system is broken by design",
    "chore: pretending to write enterprise architecture while staring blankly at terminal",
    "style: re-indented 40,000 lines of legacy code to claim 10x engineering velocity",
    "sec: stored production master keys inside a public markdown table"
]
# -------------------------------------------------


# ----------------- PERSISTENT ECONOMY -----------------
def load_economy() -> dict:
    if not ECONOMY_FILE.exists():
        default_data = {
            "lifetime_commits": 0,
            "lifetime_chow_bucks": 0,
            "total_bail_fines": 0,
            "total_errors": 0,
            "history": []
        }
        save_economy(default_data)
        return default_data
    try:
        with open(ECONOMY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"lifetime_commits": 0, "lifetime_chow_bucks": 0, "total_bail_fines": 0, "total_errors": 0, "history": []}


def save_economy(data: dict):
    with open(ECONOMY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def record_push_reward(commits_count: int):
    data = load_economy()
    data["lifetime_commits"] += commits_count
    data["lifetime_chow_bucks"] += (commits_count * 100)
    save_economy(data)


def record_error_penalty():
    data = load_economy()
    data["total_errors"] += 1
    data["total_bail_fines"] += 500
    save_economy(data)


def display_economy_card(session_commits: int, session_errors: int):
    data = load_economy()
    net_wealth = data["lifetime_chow_bucks"] - data["total_bail_fines"]
    wealth_color = "green" if net_wealth >= 0 else "red"

    table = Table(title="[bold gold1]🎰 Mr. Chow's Underground Bailout Ledger 🎰[/bold gold1]", box=box.ROUNDED)
    table.add_column("Financial Metric", style="cyan")
    table.add_column("Session Stats", style="bold white")
    table.add_column("Lifetime Historical Ledger", style="bold yellow")

    table.add_row("Pushes / Commits", f"+{session_commits} commits", f"{data['lifetime_commits']} Total Lifetime Commits")
    table.add_row("Chow Bucks Earned ($100/commit)", f"+${session_commits * 100}", f"${data['lifetime_chow_bucks']} Gross Earned")
    table.add_row("Bail Money Fines ($500/error)", f"-${session_errors * 500}", f"-${data['total_bail_fines']} Paid to Bail Bonds")
    table.add_row("Net Standing", f"${(session_commits * 100) - (session_errors * 500)}", f"[{wealth_color}]${net_wealth} Net Balance[/{wealth_color}]")

    console.print(table)
# ------------------------------------------------------


def render_punch_sequence():
    """Kinetic punch impact animation."""
    punch_stages = [
        "[bold yellow]👊 (Winding up kinetic hook...)[/bold yellow]",
        "[bold yellow]👊💨 ════════════ (Propelling through network stack...)[/bold yellow]",
        "[bold red]💥 [BOOM! BATCH PACKET INJECTED DIRECTLY INTO REMOTE GIT BUFFER] 💥[/bold red]"
    ]
    for stage in punch_stages:
        console.print(f"  {stage}")
        time.sleep(0.18)
    time.sleep(0.08)


def run_git(args: List[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True
    )


def check_for_rate_limit(output: str) -> bool:
    """Detects HTTP 429 or GitHub rate limiting abuse detection in stderr."""
    triggers = ["429", "too many requests", "abuse detection", "rate limit exceeded", "temporarily blocked"]
    return any(t in output.lower() for t in triggers)


def diagnose_git_error(err: subprocess.CalledProcessError) -> Tuple[str, str]:
    out = (err.stderr or "").strip() or (err.stdout or "").strip() or "Unknown error."
    cmd_str = " ".join(err.cmd)

    if check_for_rate_limit(out):
        cat = "🚨 CRITICAL RATE LIMIT (HTTP 429 DETECTED)"
        tip = "GitHub flagged automated traffic. The fail-safe has initiated an emergency shutdown."
    elif "nothing to commit" in out:
        cat = "Clean Working Tree"
        tip = "No byte changes detected. Working tree clean."
    elif "Author identity unknown" in out or "tell me who you are" in out:
        cat = "Missing Identity"
        tip = "Run `git config --global user.name` and `user.email`."
    elif "Permission denied" in out or "Authentication failed" in out:
        cat = "Authentication Rejection"
        tip = "GitHub rejected your Personal Access Token or SSH key."
    elif "src refspec" in out or "does not match any" in out:
        cat = "Branch Reference Mismatch"
        tip = "Target branch does not exist on local repository."
    elif "remote: Repository not found" in out:
        cat = "Repository Not Found"
        tip = "Check remote configuration with `git remote -v`."
    elif "rejected because the remote contains work" in out or "non-fast-forward" in out:
        cat = "Remote Divergence"
        tip = "Rebase required: `git pull --rebase origin <branch>`."
    else:
        cat = "Subprocess Execution Failure"
        tip = "Inspect arguments, write permissions, and connectivity."

    return cat, f"Failed Command: `{cmd_str}`\nDetails: {out}\nRecommendation: {tip}"


def get_current_branch(repo_path: Path) -> str:
    try:
        return run_git(["branch", "--show-current"], cwd=repo_path).stdout.strip() or "main"
    except Exception:
        return "main"


def ensure_git_identity(repo_path: Path):
    try:
        run_git(["config", "user.name"], cwd=repo_path)
    except Exception:
        run_git(["config", "user.name", "Santhosh Nathan"], cwd=repo_path)
    try:
        run_git(["config", "user.email"], cwd=repo_path)
    except Exception:
        run_git(["config", "user.email", "santhosh@cybersec.local"], cwd=repo_path)


def discover_git_repos(search_paths: List[Path]) -> List[Path]:
    repos = set()
    for root in search_paths:
        if not root.exists():
            continue
        if (root / ".git").is_dir():
            repos.add(root.resolve())
            continue
        try:
            for item in root.iterdir():
                if item.is_dir() and (item / ".git").is_dir():
                    repos.add(item.resolve())
        except (PermissionError, OSError):
            continue
    return sorted(list(repos))


def display_header():
    console.clear()
    banner = """
    ██████╗ ██╗      ██████╗ 
   ██╔════╝ ██║     ██╔═══██╗
   ██║  ███╗██║     ██║   ██║
   ██║   ██║██║     ██║   ██║
   ╚██████╔╝███████╗╚██████╔╝
    ╚═════╝ ╚══════╝ ╚═════╝ 
    """
    console.print(Panel(
        f"[bold cyan]{banner}[/bold cyan]\n"
        f"[bold gold1]⚡ GLO // Stealth Anti-Detection & Dark Satire Telemetry Suite ⚡[/bold gold1]\n"
        f"[bold white]Architect:[/bold white] [bold green]Santhosh Nathan[/bold green] | [bold magenta]Cybersecurity Researcher[/bold magenta] | [dim]@realhackies[/dim]",
        border_style="cyan",
        box=box.DOUBLE
    ))


def perform_doh_resolution(domain: str = "github.com") -> Tuple[str, str, float]:
    doh_providers = [
        ("Cloudflare-DoH", "https://cloudflare-dns.com/dns-query"),
        ("Google-DoH", "https://dns.google/resolve")
    ]
    provider_name, url = random.choice(doh_providers)
    t0 = time.time()
    resolved_ip = "140.82.121.4"
    try:
        resp = requests.get(
            url,
            params={"name": domain, "type": "A"},
            headers={"accept": "application/dns-json"},
            timeout=2.0
        )
        if resp.status_code == 200:
            data = resp.json()
            answers = data.get("Answer", [])
            for ans in answers:
                if ans.get("type") == 1:
                    resolved_ip = ans.get("data")
                    break
    except Exception:
        try:
            resolved_ip = socket.gethostbyname(domain)
        except Exception:
            pass

    latency = round((time.time() - t0) * 1000, 2)
    return provider_name, resolved_ip, latency


def generate_mutated_payload(cycle_num: int, sub_commit: int) -> Tuple[str, str, str]:
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
    commit_msg = random.choice(COMMIT_EXCUSES)
    entropy_hex = os.urandom(8).hex()

    templates = [
        (
            f"core/telemetry_eval_{cycle_num}_{sub_commit}.py",
            f'''# Automated Telemetry Module {cycle_num}.{sub_commit}
# Entropy Tag: {entropy_hex} | Timestamp: {now_iso}
# Directive: "{commit_msg}"

import hashlib

def verify_block_integrity():
    raw_stream = b"{entropy_hex}_payload_block_{cycle_num}"
    digest = hashlib.sha256(raw_stream).hexdigest()
    return f"Block signature verified: {{digest[:16]}}"

if __name__ == "__main__":
    print(verify_block_integrity())
''',
            commit_msg
        ),
        (
            f"docs/CHANGELOG_v{cycle_num}.md",
            f'''# Telemetry Changelog v{cycle_num}.{sub_commit}
* **Timestamp**: `{now_iso}`
* **Entropy Checksum**: `{entropy_hex}`
* **Applied Mutation**: `{commit_msg}`
* **Status**: Reconciled upstream sync.
''',
            f"docs(audit): update telemetry changelog block {cycle_num}.{sub_commit}"
        ),
        (
            f"configs/telemetry_spec_{cycle_num}.json",
            json.dumps({
                "cycle": cycle_num,
                "sub_commit": sub_commit,
                "entropy": entropy_hex,
                "timestamp": now_iso,
                "status": "synchronized"
            }, indent=2),
            f"chore(config): synchronize spec metrics {cycle_num}.{sub_commit}"
        )
    ]

    choice = templates[(cycle_num + sub_commit) % len(templates)]
    return choice[0], choice[1], choice[2]


def select_repository() -> Tuple[Path, str]:
    with console.status("[bold green]Scanning filesystem for target Git repos, Boss...[/bold green]", spinner="dots"):
        repos = discover_git_repos(DEFAULT_SEARCH_PATHS)
        time.sleep(0.3)

    table = Table(title="[bold yellow]📁 Target Repositories Detected[/bold yellow]", box=box.ROUNDED)
    table.add_column("#", justify="center", style="cyan", no_wrap=True)
    table.add_column("Target Stash", style="bold white")
    table.add_column("Location on Disk", style="dim")

    for idx, repo in enumerate(repos, 1):
        table.add_row(str(idx), repo.name, str(repo))

    custom_idx = len(repos) + 1
    table.add_row(str(custom_idx), "[italic yellow]+ Enter custom repo path manually[/italic yellow]", "")
    console.print(table)

    selected_repo = None
    while True:
        choice = Prompt.ask(f"[bold green]Which repository are we deploying to, Boss? (1-{custom_idx})[/bold green]", default="1")
        if choice.isdigit() and 1 <= int(choice) <= len(repos):
            selected_repo = repos[int(choice) - 1]
            break
        elif choice.isdigit() and int(choice) == custom_idx:
            manual_path = Prompt.ask("[bold green]Enter absolute path to repository[/bold green]")
            p = Path(manual_path).expanduser().resolve()
            if (p / ".git").is_dir():
                selected_repo = p
                break
            console.print("[bold red]❌ Error: Not a valid Git repository (.git not found).[/bold red]")
        else:
            console.print("[bold red]Please select a valid option from the table.[/bold red]")

    ensure_git_identity(selected_repo)
    active_branch = get_current_branch(selected_repo)
    return selected_repo, active_branch


def render_osi_live_pipeline(repo_name: str, branch: str, cycle_num: int, batched_count: int):
    doh_prov, edge_ip, doh_lat = perform_doh_resolution("github.com")

    osi_layers = [
        ("🌐 L7 APPLICATION", f"DoH ({doh_prov}) -> {edge_ip} ({doh_lat}ms)", f"[bold cyan]HTTP/2 POST ({batched_count} batched commits)[/bold cyan]", "📦 PDU: Refspec Stream (0x7F 0x45)"),
        ("🔐 L6 PRESENTATION", "Zlib Delta Packfile Compression & TLS 1.3 Ciphers", "[bold yellow]AES-256-GCM [TAG 0x9B4F][/bold yellow]", "🔒 Payload: Encrypted"),
        ("🤝 L5 SESSION", "Persistent Duplex Socket Handshake via Edge ASN AS36459", "[bold blue]RPC_SOCKET_OPEN[/bold blue]", "📡 State: Synchronized"),
        ("⚡ L4 TRANSPORT", "TCP 3-Way Handshake (SYN ➜ SYN-ACK ➜ ACK)", "[bold magenta]PORT 443 [ACK 0x7E3B][/bold magenta]", "🔢 Seq: 4182937 | Win: 65535"),
        ("🧭 L3 NETWORK", f"IPv4 Datagram Encapsulation & WAN Routing -> {edge_ip}", "[bold red]IP_FORWARDED [TTL: 64][/bold red]", "🗺️ Hops: 8 Gateways"),
        ("🔗 L2 DATA LINK", "Ethernet II Framing & FCS 32-Bit CRC Validation", "[bold green]ETHERNET_FRAME_VALID[/bold green]", "🛡️ MAC: C0:FF:EE:89:12:34"),
        ("💡 L1 PHYSICAL", "Modulating Raw Optical Photon Bitstream Across Fiber WAN", "[bold white on red] BITS FIRING (1.4 Gbps) [/bold white on red]", "⚡ [01000111 01101001 01110100]")
    ]

    console.print("\n" + "═" * 78)
    console.print(f"[bold cyan]⚡ LIVE OSI / TCP-IP BATCH TRANSMISSION // CYCLE #{cycle_num} ({batched_count} COMMITS BATCHED)[/bold cyan]")
    console.print("═" * 78)

    for layer_name, action, status_badge, packet_meta in osi_layers:
        with console.status(f"[bold white]{layer_name}[/bold white]: Processing packet stream...", spinner="dots12"):
            time.sleep(0.30)
        console.print(f"  [bold yellow]{layer_name:<20}[/bold yellow] ➔ {status_badge}")
        console.print(f"    [dim]↳ {action} | {packet_meta}[/dim]")
        time.sleep(0.08)

    console.print("\n[bold green]📡 Remote Ingestion & Lock Confirmation:[/bold green]")
    with console.status("[bold cyan]Remote daemon unpacking batch objects & validating tree hashes...[/bold cyan]", spinner="aesthetic"):
        time.sleep(0.4)

    console.print(f"  [bold green]✔ [200 OK ACCEPTED][/bold green] Remote refs updated on [bold white]origin/{branch}[/bold white]!")
    
    roast_quote = random.choice(DARK_DEV_ROASTS)
    console.print(Panel(
        f"[bold gold1]🎬 Pop-Culture & Dark Dev Satire:[/bold gold1]\n"
        f"[italic magenta]{roast_quote}[/italic magenta]",
        box=box.ROUNDED,
        border_style="magenta"
    ))


def execute_batched_cycle(repo_path: Path, branch: str, cycle_num: int) -> int:
    batch_size = random.randint(2, 4)
    console.print(f"\n[bold green]➜ Initiating Cycle #{cycle_num}: Generating batch of {batch_size} local commits...[/bold green]\n")

    for sub in range(1, batch_size + 1):
        rel_path, content, commit_msg = generate_mutated_payload(cycle_num, sub)
        target_file = repo_path / rel_path
        target_file.parent.mkdir(parents=True, exist_ok=True)

        with console.status(f"[bold yellow]📦 Mutating & Staging ({sub}/{batch_size}) Boss...[/bold yellow] ({rel_path})", spinner="point"):
            target_file.write_text(content)
            if rel_path.endswith(".py"):
                subprocess.run([sys.executable, str(target_file)], capture_output=True, text=True)
            run_git(["add", rel_path], cwd=repo_path)
            time.sleep(0.25)

        with console.status(f"[bold magenta]✍️ Signing local commit #{sub} Boss...[/bold magenta]", spinner="dots2"):
            run_git(["commit", "-m", commit_msg], cwd=repo_path)
            time.sleep(0.25)

        console.print(f"  [bold green]✔[/bold green] [{sub}/{batch_size}] Committed locally: [cyan]\"{commit_msg}\"[/cyan] [dim]({rel_path})[/dim]")

    render_punch_sequence()

    with console.status(f"[bold red]🚀 Flushing socket buffer to origin/{branch}...[/bold red]", spinner="aesthetic"):
        push_res = run_git(["push", "origin", branch], cwd=repo_path)
        if check_for_rate_limit(push_res.stderr or push_res.stdout):
            raise subprocess.CalledProcessError(429, ["git", "push"], output=push_res.stdout, stderr=push_res.stderr)
        time.sleep(0.4)

    render_osi_live_pipeline(repo_path.name, branch, cycle_num, batch_size)
    record_push_reward(batch_size)
    console.print(f"  [bold gold1]💰 Reward Credited:[/bold gold1] [bold green]+${batch_size * 100} Chow Bucks[/bold green] ({batch_size} commits pushed)\n")
    return batch_size


def countdown_timer(base_seconds: int, next_cycle: int):
    jitter = random.randint(-5, 8)
    total_seconds = max(15, base_seconds + jitter)

    mins, secs = divmod(total_seconds, 60)
    time_display = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
    jitter_text = f"+{jitter}s" if jitter >= 0 else f"{jitter}s"

    with Progress(
        SpinnerColumn(spinner_name="clock"),
        TextColumn(f"[bold yellow]Stealth Cooldown: Waiting {time_display} before Cycle #{next_cycle}... ({jitter_text} WAF Jitter)[/bold yellow]"),
        BarColumn(bar_width=35, style="blue", complete_style="cyan"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Sleeping it off", total=total_seconds)
        for _ in range(total_seconds):
            time.sleep(1)
            progress.update(task, advance=1)
    console.print()


def render_contribution_heatmap(time_range_choice: str = None):
    display_header()
    repos = discover_git_repos(DEFAULT_SEARCH_PATHS)
    if not repos:
        console.print("[bold red]No Git repositories found to analyze.[/bold red]")
        return

    table = Table(title="[bold yellow]📁 Select Repository for Stats Analysis[/bold yellow]", box=box.ROUNDED)
    table.add_column("#", justify="center", style="cyan", no_wrap=True)
    table.add_column("Repository Target", style="bold white")
    table.add_column("Path", style="dim")
    for idx, r in enumerate(repos, 1):
        table.add_row(str(idx), r.name, str(r))
    console.print(table)

    repo_idx = Prompt.ask(f"[bold green]Choose repository (1-{len(repos)})[/bold green]", default="1")
    target_repo = repos[int(repo_idx) - 1] if repo_idx.isdigit() and 1 <= int(repo_idx) <= len(repos) else repos[0]

    ranges = {
        "1": ("Last 3 Months", 90, 13),
        "2": ("Last 6 Months", 180, 26),
        "3": ("Full Year (12 Months)", 365, 52),
        "4": ("All-Time Historical Reckoning", 9999, 52)
    }

    if not time_range_choice:
        console.print("\n[bold cyan]📅 Select Heatmap & Stats Timeframe:[/bold cyan]")
        console.print("  [bold yellow]1[/bold yellow] -> Last 3 Months (Quick Sprint)")
        console.print("  [bold yellow]2[/bold yellow] -> Last 6 Months (Mid-Year Grind)")
        console.print("  [bold yellow]3[/bold yellow] -> Full 1 Year (Annual History)")
        console.print("  [bold yellow]4[/bold yellow] -> All-Time (Lifetime Reckoning)")
        time_range_choice = Prompt.ask("[bold green]Select timeframe (1-4)[/bold green]", default="1")

    label, total_days, num_weeks = ranges.get(time_range_choice, ranges["1"])

    try:
        res = run_git(["log", "--pretty=format:%ad", "--date=short"], cwd=target_repo)
        raw_dates = res.stdout.strip().splitlines() if res.stdout.strip() else []
    except Exception:
        raw_dates = []

    date_counts = Counter(raw_dates)
    total_commits = len(raw_dates)
    today = datetime.now().date()
    filtered_commits = sum(count for d_str, count in date_counts.items() if datetime.strptime(d_str, "%Y-%m-%d").date() >= (today - timedelta(days=total_days)))

    display_weeks = min(num_weeks, 26)
    heatmap_table = Table(title=f"[bold green]📊 Commit Heatmap ({label}) — {target_repo.name}[/bold green]", box=box.ROUNDED)
    heatmap_table.add_column("Day", style="bold cyan", justify="center")
    
    for w in range(display_weeks, 0, -1):
        heatmap_table.add_column(f"W-{w}", justify="center")

    levels = ["[dim]·[/dim]", "[green]░[/green]", "[green]▒[/green]", "[bold green]▓[/bold green]", "[bold green]█[/bold green]"]
    days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for day_idx in range(7):
        row = [days_labels[day_idx]]
        for w in range(display_weeks - 1, -1, -1):
            target_day = today - timedelta(weeks=w, days=(today.weekday() - day_idx))
            c = date_counts.get(target_day.strftime("%Y-%m-%d"), 0)
            lvl = 0 if c == 0 else (1 if c <= 2 else (2 if c <= 5 else (3 if c <= 10 else 4)))
            row.append(f"{levels[lvl]}")
        heatmap_table.add_row(*row)

    console.print(heatmap_table)

    stats_panel = Panel(
        f"[bold gold1]Repository:[/bold gold1] [bold white]{target_repo.name}[/bold white]   |   "
        f"[bold gold1]Timeframe Selected:[/bold gold1] [bold cyan]{label}[/bold cyan]\n"
        f"[bold green]Commits in Period:[/bold green] [bold white]{filtered_commits}[/bold white]   |   "
        f"[bold green]All-Time Lifetime Commits:[/bold green] [bold white]{total_commits}[/bold white]\n"
        f"[bold magenta]Recruiter Deception Score:[/bold magenta] [bold white]99.8% (Senior 10x Architect)[/bold white]   |   "
        f"[bold magenta]Actual Braincells Used:[/bold magenta] [bold white]0.001%[/bold white]\n\n"
        f"[italic dim]\"We found Doug, but he's sunburnt on the roof with 400 unmerged pull requests.\"[/italic dim]",
        title="[bold gold1]🎰 The Wolfpack Ledger & Performance Stats[/bold gold1]",
        border_style="gold1",
        box=box.DOUBLE
    )
    console.print(stats_panel)
    display_economy_card(0, 0)


def display_milestone_banner(current_push: int, total_pushes: int):
    next_milestone = current_push + 5
    banner = f"""
  ╔═════════════════════════════════════════════════════════════════════════╗
  ║  🔥 BINGO! {current_push} CYCLES COMPLETED — PRODUCTION HAS NOT MELTED DOWN! 🔥 ║
  ║  Next Target Milestone: Cycle #{next_milestone:<38} ║
  ╚═════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(f"[bold gold1]{banner}[/bold gold1]", border_style="gold1", box=box.HEAVY))


def main():
    parser = argparse.ArgumentParser(description="glo (Git Loop Operator) - Anti-Detection & Dark Satire Suite")
    parser.add_argument("--stats", "-s", action="store_true", help="Display commit heatmap & persistent bailout economy")
    parser.add_argument("--range", "-r", type=str, choices=["1", "2", "3", "4"], help="Direct timeframe (1=3M, 2=6M, 3=1Y, 4=All)")
    args = parser.parse_args()

    if args.stats:
        render_contribution_heatmap(args.range)
        return

    display_header()
    repo_path, branch = select_repository()

    console.print(Panel(
        f"[bold green]Target Repository:[/bold green] [bold white]{repo_path.name}[/bold white]\n"
        f"[bold green]Working Directory:[/bold green] [dim]{repo_path}[/dim]\n"
        f"[bold green]Active Branch:[/bold green] [cyan]{branch}[/cyan] (Auto-detected)\n"
        f"[bold green]Lead Researcher:[/bold green] [magenta]Santhosh Nathan (Cybersecurity Researcher)[/magenta]",
        title="[bold yellow]Stealth Pipeline Armed[/bold yellow]",
        box=box.ROUNDED
    ))

    with console.status(f"[bold cyan]Checking upstream sync on origin/{branch}...[/bold cyan]", spinner="arc"):
        try:
            run_git(["pull", "--rebase", "origin", branch], cwd=repo_path)
        except Exception:
            pass

    total_cycles = IntPrompt.ask(
        "[bold cyan]How many batched push cycles are we deploying, Boss?[/bold cyan]",
        default=DEFAULT_TOTAL_CYCLES
    )

    if total_cycles <= 0:
        console.print("[bold red]Session aborted: Count must be > 0.[/bold red]")
        sys.exit(0)

    session_start_time = time.time()
    total_session_commits = 0
    session_errors = 0

    for current_cycle in range(1, total_cycles + 1):
        try:
            pushed_count = execute_batched_cycle(repo_path, branch, current_cycle)
            total_session_commits += pushed_count

            console.print("═" * 78)
            console.print(f"[bold green]✔ CYCLE #{current_cycle} OF {total_cycles} COMPLETE (+{pushed_count} COMMITS SYNCED)![/bold green]")
            console.print("═" * 78 + "\n")

            if current_cycle % 5 == 0:
                display_milestone_banner(current_cycle, total_cycles)

            if current_cycle < total_cycles:
                base_cooldown = current_cycle * 60
                countdown_timer(base_cooldown, current_cycle + 1)

        except subprocess.CalledProcessError as err:
            session_errors += 1
            record_error_penalty()
            cat, details = diagnose_git_error(err)
            console.print(Panel(
                f"[bold red]Category:[/bold red] {cat}\n"
                f"[bold red]Fine Incurred:[/bold red] -$500 Bail Money to Mr. Chow\n\n{details}",
                title="[bold red]🚨 Critical Execution Fault / Lockout[/bold red]",
                border_style="red",
                box=box.HEAVY
            ))
            break
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Operation halted by Boss. Exiting safely.[/bold yellow]")
            break

    duration = round(time.time() - session_start_time, 1)
    mins, secs = divmod(int(duration), 60)
    summary = Table(title="[bold green]📊 Execution Summary[/bold green]", box=box.ROUNDED)
    summary.add_column("Telemetry Metric", style="cyan")
    summary.add_column("Reported Value", style="bold white")
    summary.add_row("Lead Researcher", "Santhosh Nathan")
    summary.add_row("Target Repo", repo_path.name)
    summary.add_row("Branch Deployed", branch)
    summary.add_row("Total Commits Deployed", str(total_session_commits))
    summary.add_row("Cycles Executed", str(current_cycle))
    summary.add_row("Duration", f"{mins}m {secs}s")
    console.print(summary)
    console.print()
    display_economy_card(total_session_commits, session_errors)
    console.print(f"\n[bold cyan]All automated push cycles completed flawlessly. Rest up, Boss! 🚀[/bold cyan]\n")


if __name__ == "__main__":
    main()
