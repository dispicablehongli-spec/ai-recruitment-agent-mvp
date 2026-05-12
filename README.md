# AI Recruitment Agent MVP

## Product plan (§15 同步)

主 Plan 由 Cursor 保存在 `~/.cursor/plans/ai_recruitment_agent_mvp_6f1c943a.plan.md`。  
**Plan 冻结后的变更（第 15 节）** 在仓库内可见：**[docs/plan-section-15-post-plan.md](docs/plan-section-15-post-plan.md)**。

## Prerequisites
- Python 3.11+
- Node.js 18+

## Environment
Create `.env` in project root:

```env
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

## Run backend

```bash
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

## Run frontend

```bash
cd frontend
npm run dev
```

## Demo scenarios

```bash
bash scripts/demo.sh success
bash scripts/demo.sh match_failed
bash scripts/demo.sh missing_required
```

## API summary
- `POST /applications/upload`
- `GET /applications/{id}`
- `GET /applications/{id}/events`
- `POST /applications/{id}/select-job`
- `POST /applications/{id}/reupload`
- `POST /applications/{id}/cancel`
- `GET /applications/{id}/result`
- `GET /jobs`
