#!/usr/bin/env python3
"""Run the small, predefined maintenance task scheduled for this repository."""

from datetime import datetime, timezone
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_FILE = ROOT / ".github" / "maintenance" / "schedule.json"
README_FILE = ROOT / "README.md"


def add_section(title, text):
    if not README_FILE.exists():
        print("README.md is not present. Skipping safely.")
        return False

    current = README_FILE.read_text(encoding="utf-8")
    marker = f"## {title}"
    if marker in current:
        print(f"{marker} already exists. No change needed.")
        return False

    updated = current.rstrip() + f"\n\n{marker}\n\n{text}\n"
    README_FILE.write_text(updated, encoding="utf-8")
    return True


def run_task(task_id, description):
    sections = {
        "testing_notes": ("Testing Notes", "Add a short testing note covering the existing Django test command and the role of validation tests."),
        "development_workflow": ("Development Workflow", "Add a short development workflow note covering inspect → change → test → review."),
        "contributing_checklist": ("Contributing Checklist", "Add a small checklist for safe changes to the genomics and proteomics modules."),
        "limitations_notes": ("Limitations Notes", "Add a concise note explaining that automated maintenance only makes predefined, reviewable repository changes."),
        "maintenance_schedule": ("Maintenance Schedule", "Document the scheduled maintenance dates for GenomeZ in this month."),
        "automation_scope": ("Automation Scope", "Document that the workflow stops when there is no meaningful change or a check fails."),
    }

    if task_id == "fix_repo_link":
        if not README_FILE.exists():
            return False
        current = README_FILE.read_text(encoding="utf-8")
        updated = current.replace(
            "https://github.com/heyboiii19/Contact-Book-CLI.git",
            "https://github.com/adityatiwari-git/Contact-Book-CLI.git",
        )
        if updated == current:
            print("Repository URL is already correct. No change needed.")
            return False
        README_FILE.write_text(updated, encoding="utf-8")
        return True

    if task_id in sections:
        title, section_text = sections[task_id]
        return add_section(title, section_text)

    print(f"No implementation exists for task: {task_id}")
    return False


def main():
    schedule = json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
    today = datetime.now(timezone.utc).date().isoformat()
    task = schedule.get(today)

    if not task:
        print(f"No task scheduled for {today}.")
        return 0

    print(f"Scheduled task for {today}: {task['task_id']}")
    changed = run_task(task["task_id"], task["description"])
    print(f"TASK_CHANGED={str(changed).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
