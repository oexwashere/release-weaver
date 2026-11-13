import argparse
import json
import re
from datetime import date
from urllib.parse import urlparse

GROUPS = {
    "feat": "Features",
    "fix": "Fixes",
    "perf": "Performance",
    "docs": "Documentation",
    "refactor": "Refactoring",
    "test": "Tests",
    "build": "Maintenance",
    "ci": "Maintenance",
    "chore": "Maintenance",
    "style": "Maintenance",
    "revert": "Reverts",
}


def parse(lines):
    entries = []
    unparsed = []
    seen = set()
    for line in lines:
        line = line.strip()
        if not line or line in seen:
            continue
        seen.add(line)
        match = re.fullmatch(
            r"(?:(?P<hash>[a-f0-9]{7,40})\s+)?(?P<type>[a-z]+)(?:\((?P<scope>[^)\r\n]+)\))?(?P<breaking>!)?:\s+(?P<subject>.+)",
            line,
        )
        if not match or match["type"] not in GROUPS:
            unparsed.append(line)
            continue
        item = match.groupdict()
        item["breaking"] = bool(item["breaking"])
        item["group"] = GROUPS[item["type"]]
        entries.append(item)
    return {"entries": entries, "unparsed": unparsed}


def safe(text):
    return re.sub(r"([\\`*_{}\[\]<>])", r"\\\1", text)


def markdown(report, version, release_date, repository=None):
    date.fromisoformat(release_date)
    if repository:
        parsed = urlparse(repository)
        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or any(c in repository for c in "()\r\n")
        ):
            raise ValueError("Repository must be a plain HTTPS URL.")
    lines = [f"# {safe(version)} — {release_date}", ""]
    breaking = [entry for entry in report["entries"] if entry["breaking"]]
    groups = [("Breaking changes", breaking)] + [
        (
            name,
            [e for e in report["entries"] if e["group"] == name and not e["breaking"]],
        )
        for name in dict.fromkeys(GROUPS.values())
    ]
    for name, entries in groups:
        if not entries:
            continue
        lines.extend([f"## {name}", ""])
        for entry in entries:
            text = (f"**{safe(entry['scope'])}:** " if entry["scope"] else "") + safe(
                entry["subject"]
            )
            if entry["hash"]:
                text += (
                    " ("
                    + (
                        f"[{entry['hash'][:7]}]({repository.rstrip('/')}/commit/{entry['hash']})"
                        if repository
                        else entry["hash"][:7]
                    )
                    + ")"
                )
            lines.append("- " + text)
        lines.append("")
    if report["unparsed"]:
        lines.extend(["## Other changes", ""])
        lines.extend("- " + safe(line) for line in report["unparsed"])
        lines.append("")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(
        description="Generate release notes from conventional commit subjects."
    )
    p.add_argument("file")
    p.add_argument("--version", required=True)
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--repository")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        with open(a.file, encoding="utf-8") as f:
            report = parse(f)
        print(
            json.dumps(report, indent=2)
            if a.json
            else markdown(report, a.version, a.date, a.repository)
        )
    except (OSError, ValueError) as e:
        p.exit(2, f"Error: {e}\n")


if __name__ == "__main__":
    main()
