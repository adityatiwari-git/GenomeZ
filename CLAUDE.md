# GenomeZ Daily Development Agent

## Purpose

This repository may be maintained by an automated Claude Code workflow that works on explicitly scheduled development tasks.

The agent must make real, explainable improvements to GenomeZ. It must never modify code merely to create activity.

## Non-negotiable rules

1. Read the scheduled task before making changes.
2. Inspect the relevant existing code, tests, README, and recent git history before editing.
3. Prefer the smallest useful change that genuinely addresses the task.
4. Preserve existing behavior unless the task explicitly requires a behavior change.
5. Do not create placeholder features, cosmetic-only changes, empty commits, or changes whose only purpose is contribution activity.
6. Never expose, create, modify, or commit secrets, API keys, tokens, credentials, or local environment files.
7. Do not change deployment configuration, dependencies, authentication behavior, or unrelated files unless the scheduled task requires it.
8. Add or update tests when a behavior change warrants them.
9. Run the most relevant available tests/checks after editing.
10. Inspect the final git diff and remove unrelated changes.
11. If the scheduled task does not justify a meaningful improvement, make no changes and do not create a pull request.
12. Never merge a pull request automatically.

## Quality bar

Before opening a PR, ask:

> Would I be comfortable explaining this exact change to a professor or recruiter as a real improvement I made to GenomeZ?

If the answer is no, discard the change.

## Pull request requirements

When a meaningful change is completed:
- use a concise, task-specific branch/PR title;
- explain what changed and why;
- mention tests/checks that were run;
- do not mention automated daily activity, contribution graphs, green squares, this chat, or token usage;
- leave the PR for human review and merging.

## Testing

GenomeZ is a Django application. Prefer the project's existing test suite and use the repository's documented commands. Do not install unrelated packages just to make a test pass.
