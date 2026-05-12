# AI Recruitment Agent MVP

## 产品与流程

这是一个 **AI 招聘代理 MVP**：候选人上传 **简历 PDF**，后端解析并与开放岗位匹配，**LangGraph** 编排流程；前端通过 **SSE** 展示进度，支持 **选岗**、**缺失信息补传** 与 **撤回申请**。

**典型流程**：上传 → 解析与匹配 →（必要时）补传 →（有岗时）选岗 → 成功邀约或匹配失败 / 取消 / 错误等终态。

## 最近更新

（仅保留面向读者的摘要；**完整变更与边界**见 **[docs/plan-version-log.md](docs/plan-version-log.md)**。）

- **2026-05-12**：MVP 主流程与 API、Post-Plan 联调与前端升级；文档与版本日志体例整理；**`scripts/dev.sh`** 一键起后端+前端（可选 `--open`）及 README 一键开发说明。

## 环境与运行

### Prerequisites
- Python 3.11+
- Node.js 18+

### Environment
Create `.env` in project root:

```env
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### 本地一键开发（推荐）

在项目根目录执行（后端后台跑，前端前台；**Ctrl+C** 会一并结束后端）：

```bash
bash scripts/dev.sh
```

macOS 下启动并用系统浏览器打开前端：

```bash
bash scripts/dev.sh --open
```

### 分别启动（可选）

**后端**

```bash
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

**前端**

```bash
cd frontend
npm run dev
```

### Demo scenarios

```bash
bash scripts/demo.sh success
bash scripts/demo.sh match_failed
bash scripts/demo.sh missing_required
```

## API

- `POST /applications/upload`
- `GET /applications/{id}`
- `GET /applications/{id}/events`
- `POST /applications/{id}/select-job`
- `POST /applications/{id}/reupload`
- `POST /applications/{id}/cancel`
- `GET /applications/{id}/result`
- `GET /jobs`
