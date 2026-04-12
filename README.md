# 🚀 Launchpad — CI/CD Deployment Pipeline

> Push code to GitHub. It's live in 2 minutes. No manual steps.

![CI](https://img.shields.io/github/actions/workflow/status/gaus13/launchpad/ci.yml?label=CI&logo=github)
![CD](https://img.shields.io/github/actions/workflow/status/gaus13/launchpad/cd.yml?label=CD&logo=github)
![Docker](https://img.shields.io/badge/Docker-containerised-2496ED?logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-reverse--proxy-009639?logo=nginx)

---

## What It Does

A self-hosted push-to-deploy pipeline that mirrors how Heroku and Render work internally. Every `git push` to `main` automatically builds, tests, and deploys the app to a live cloud server.

```
git push → CI (build + test) → CD (push image + SSH deploy) → Live on server
```

**Live at:** http://139.59.63.52/health

---

## Stack

| Layer | Tech |
|---|---|
| App | FastAPI (Python) |
| Containerisation | Docker |
| Image Registry | Docker Hub |
| CI/CD | GitHub Actions (separate pipelines) |
| Cloud Server | DigitalOcean Droplet — Ubuntu 24.04 |
| Reverse Proxy | Nginx (port 80 → 8000) |
| Secrets | GitHub Secrets — zero hardcoded credentials |

---

## Pipeline

**CI** — triggers on every push and PR to `main`
- Builds Docker image tagged with commit SHA
- Spins up container and runs live health check
- Blocks CD if this fails — broken code never ships

**CD** — triggers only when CI passes
- Pushes image to Docker Hub with `:latest` and `:sha` tags
- SSHs into Droplet, pulls new image, replaces running container

---

## Key Decisions Worth Noting

- **Separate CI and CD files** — CI runs on every PR, CD only deploys on `main` success
- **SHA-tagged images** — every build is traceable and rollback-ready
- **`|| true` on docker stop** — first deploy doesn't fail if no container exists yet
- **Nginx as reverse proxy** — app never exposes raw port to the internet
- **`--restart unless-stopped`** — container survives server reboots automatically

---

## Run Locally

```bash
git clone https://github.com/gaus13/launchpad.git
cd launchpad
docker build -t launchpad .
docker run -d -p 8000:8000 --name launchpad launchpad
curl http://localhost:8000/health
```

---

## Endpoints

| Endpoint | Response |
|---|---|
| `/` | App status |
| `/health` | `{"status": "high sir"}` |
