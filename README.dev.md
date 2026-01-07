Development setup
-----------------

This file documents how to spin up the development environment using Docker Compose,
run tests locally, and what secrets/env vars are required.

1) Copy example env file

```powershell
copy config\env.example config\.env
```

Edit `config/.env` and set any required secrets (see list below).

2) Start dev environment (build + live-reload)

```powershell
docker compose -f docker-compose.dev.yml up --build
```

The API will be available at `http://localhost:8000` and Swagger UI at `/docs`.

3) Run tests locally

```powershell
python -m pip install -r config/requirements.txt
pytest -q
```

Required / recommended env vars (examples):
- `SECRET_KEY` (JWT signing key)
- `MONGODB_URL` (e.g. `mongodb://mongo:27017` for local compose)
- `MONGODB_DB_NAME` (default `doc_intelligence`)
- `REDIS_URL` (e.g. `redis://redis:6379/0`)
- `CHROMA_API_KEY`, `CHROMA_TENANT`, `CHROMA_DATABASE` (if using Chroma Cloud)
- `OPENAI_API_KEY`, `GEMINI_API_KEY`, etc. for LLMs when testing integrations

CI / GitHub Actions:
- A basic workflow is included at `.github/workflows/ci.yml` that runs tests and builds a Docker image.
- To publish images to GitHub Container Registry or Docker Hub, update the workflow and add registry secrets (`GHCR_TOKEN`, `DOCKER_USERNAME`, `DOCKER_PASSWORD`).

If you want me to enable image publishing in CI, tell me which registry you prefer and I will add the steps.

Security & next steps (must do now)
- If you have shared any tokens publicly (chat, comments, etc.), rotate/revoke them immediately. Do not paste tokens in chat.

Setting repository secrets for CI and GHCR
1) Install `gh` (GitHub CLI) and login: `gh auth login`
2) Run the helper script to set secrets interactively (PowerShell):

```powershell
pwsh .\scripts\set_github_secrets.ps1 -Interactive
```

Or set individual secrets via `gh`:

```powershell
gh secret set SECRET_KEY --body "<your-secret>"
gh secret set MONGODB_URL --body "<your-mongo-url>"
gh secret set REDIS_CLOUD_PASSWORD --body "<your-redis-password>"
# etc.
```

Publishing images to GHCR
- The CI workflow uses `GITHUB_TOKEN` and `packages: write` permission to push the built image to GHCR as:
	`ghcr.io/<owner>/doc-summarizer-agent:latest` (and a commit-specific tag)
- If you prefer using a PAT, create a token with `write:packages` and `read:packages` and add it to repo secrets (e.g. `GHCR_PAT`). Update the workflow to use that secret.

Removing secrets from the repo history (optional, destructive)
- If `config/.env` (or other files with secrets) was already committed, you'll need to rewrite git history to remove them. Recommended tools: `git filter-repo` or BFG Repo-Cleaner.
- This rewrites history and requires coordination. Example (do NOT run without understanding):

```bash
# using git filter-repo (recommended):
git filter-repo --path config/.env --invert-paths
# or using BFG:
bfg --delete-files config/.env
# After rewriting, force-push and coordinate with collaborators:
git push --force
```

If you want me to prepare a safe PR with the history-rewrite commands and step-by-step guidance, say so — I will not perform destructive history changes without your explicit approval.

