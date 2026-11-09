#!/usr/bin/env python3
"""Build the profile language chart from GitHub's public repository byte totals."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import urllib.request

OWNER = "iisacc-Justmoong"
ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    "C++": "#f34b7d", "Python": "#3572A5", "QML": "#44a51c",
    "CMake": "#DA3434", "Swift": "#F05138", "Objective-C++": "#6866fb",
    "PowerShell": "#012456", "Shell": "#89e051", "TypeScript": "#3178c6",
    "C#": "#178600", "Java": "#b07219", "Rust": "#dea584",
    "Svelte": "#ff3e00", "CSS": "#563d7c", "C": "#555555",
    "JavaScript": "#f1e05a", "HTML": "#e34c26", "Other": "#8b949e",
}


def api(path):
    """Use only GitHub REST; never send the token to a chart hosting service."""
    headers = {"Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28",
               "User-Agent": "iisacc-profile-language-chart"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com/{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def eligible(repositories, owner=OWNER):
    """Count each owned public, non-fork repository ID once, including archives."""
    result = {}
    for repo in repositories:
        full_name = repo["full_name"]
        if (repo["owner"]["login"].lower() != owner.lower()
                or repo["private"] or repo["fork"]
                or full_name.lower() == f"{owner}/{owner}".lower()):
            continue
        result[repo["id"]] = repo
    return sorted(result.values(), key=lambda repo: repo["full_name"].lower())


def collect(owner):
    repositories = []
    page = 1
    while True:
        batch = api(f"users/{owner}/repos?type=owner&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError("Expected a public repository list")
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    records = []
    for repo in eligible(repositories, owner):
        languages = api(f"repos/{repo['full_name']}/languages")
        if (not isinstance(languages, dict)
                or any(type(size) is not int or size < 0 for size in languages.values())):
            raise ValueError(f"Invalid language totals for {repo['full_name']}")
        records.append({
            "id": repo["id"], "name": repo["full_name"],
            "archived": repo["archived"], "default_branch": repo["default_branch"],
            "languages": dict(sorted(languages.items())),
        })
    return snapshot(records, owner)


def snapshot(records, owner=OWNER):
    totals = Counter()
    for repo in records:
        totals.update(repo["languages"])
    totals = dict(sorted(totals.items(), key=lambda item: (-item[1], item[0])))
    if sum(totals.values()) <= 0:
        raise ValueError("No language bytes found; keep the last valid chart")
    return {
        "owner": owner,
        "scope": "Owned public non-fork repositories, including archived repositories; profile repository excluded.",
        "metric": "GitHub Linguist language bytes on each repository's default branch",
        "deduplication": "Each repository ID once; copied code across distinct repositories is not deduplicated.",
        "total_bytes": sum(totals.values()),
        "repository_count": len(records),
        "repositories_with_code": sum(bool(repo["languages"]) for repo in records),
        "languages": totals,
        "repositories": records,
    }


def chart_entries(totals):
    entries = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    if len(entries) > 8:
        entries = entries[:7] + [("Other", sum(size for _, size in entries[7:]))]
    return entries


def render_svg(data, dark=False):
    entries = chart_entries(data["languages"])
    total = data["total_bytes"]
    rows = (len(entries) + 1) // 2
    height = 156 + rows * 30
    bg, fg, muted, border = (("#0d1117", "#f0f6fc", "#9198a1", "#30363d") if dark
                              else ("#ffffff", "#1f2328", "#59636e", "#d1d9e0"))
    labels = [f"{name} {size / total * 100:.1f}%" for name, size in entries]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="648" height="{height}" viewBox="0 0 648 {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Languages in my public repositories</title>',
        f'<desc id="desc">{escape("; ".join(labels))}. By GitHub language bytes; not coding time or proficiency.</desc>',
        f'<rect x="0.5" y="0.5" width="647" height="{height - 1}" rx="12" fill="{bg}" stroke="{border}"/>',
        '<g font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif">',
        f'<text x="32" y="43" fill="{fg}" font-size="24" font-weight="600">Languages</text>',
        f'<text x="32" y="66" fill="{muted}" font-size="13">Public repositories · code size</text>',
        '<defs><clipPath id="bar"><rect x="32" y="86" width="584" height="16" rx="5"/></clipPath></defs>',
        '<g clip-path="url(#bar)">',
    ]
    x = 32.0
    for name, size in entries:
        width = 584 * size / total
        color = COLORS.get(name, "#8b949e")
        parts.append(f'<rect x="{x:.6f}" y="86" width="{width:.6f}" height="16" fill="{color}"/>')
        x += width
    parts.append('</g>')
    for index, (name, size) in enumerate(entries):
        x, y = 32 + (index % 2) * 292, 133 + (index // 2) * 30
        color = COLORS.get(name, "#8b949e")
        parts.append(f'<circle cx="{x + 5}" cy="{y - 5}" r="5" fill="{color}" stroke="{muted}" stroke-width="0.5"/>')
        parts.append(f'<text x="{x + 19}" y="{y}" fill="{fg}" font-size="15" font-weight="600">{escape(name)} <tspan fill="{muted}" font-weight="400">{size / total * 100:.1f}%</tspan></text>')
    date = data["updated_at"][:10]
    parts.append(f'<text x="32" y="{height - 20}" fill="{muted}" font-size="12">{data["repository_count"]} repositories · {len(data["languages"])} languages · updated {date}</text>')
    parts.append('</g></svg>\n')
    return "\n".join(parts)


def save(data, output):
    output.mkdir(parents=True, exist_ok=True)
    target = output / "languages.json"
    previous = json.loads(target.read_text()) if target.exists() else {}
    old_time = previous.pop("updated_at", None)
    # Do not create a daily commit when GitHub's measured data has not changed.
    data["updated_at"] = (old_time if previous == data and old_time else
                          datetime.now(timezone.utc).isoformat(timespec="seconds"))
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    for dark in (False, True):
        theme = "dark" if dark else "light"
        (output / f"languages-{theme}.svg").write_text(render_svg(data, dark))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default=OWNER)
    parser.add_argument("--output", type=Path, default=ROOT / "assets")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", args.owner):
        parser.error("Invalid GitHub username")
    # Complete every API request before touching a committed snapshot.
    data = collect(args.owner)
    save(data, args.output)
    print(f"Updated {data['repository_count']} repositories, {data['total_bytes']} language bytes")


if __name__ == "__main__":
    main()
