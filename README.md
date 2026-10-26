# Argus sandbox agent

A tiny customer-support agent (LangGraph, no LLM, no API key) for trying the **Argus** check on
pull requests.

## Try it

1. Install the **ArgusLabsCI** GitHub App on your org and switch this repo on at
   [app.arguslabs.in](https://app.arguslabs.in) (Setup, step 2).
2. Open a pull request that changes anything. The **Argus** check appears as "Waiting for CI",
   then turns 🟢: every agent run was clean.
3. Open a second pull request that sets `BROKEN = True` in `agent.py`. The tests still pass, but
   `retrieve` now returns no articles and the agent answers with a canned reply. The Argus check
   turns 🔴 (🟠 "warn only" by default) and names `retrieve` as the step that broke, with a fix
   prompt. The bot leaves one comment on the PR.

`.github/workflows/argus.yml` is the whole setup: no secret, no token.

