# Plan 版本与变更日志

本文件汇总 **每个 Plan 阶段已交付的能力** 与 **冻结后的修复/迭代记录**，并按 **版本日期** 归档，条目习惯对齐 [Keep a Changelog](https://keepachangelog.com/) 的 **Added / Changed / Fixed**，便于扫读与发版说明。  
主 Plan 全文由 Cursor 管理，本地路径通常为：`~/.cursor/plans/ai_recruitment_agent_mvp_6f1c943a.plan.md`（M1–M9 范围与验收以该文件为准）。

## 维护约定

- 每完成一个可验收的 Plan 段落、或发布一次值得记录的版本，在下方 **追加** 新的一节（日期格式 `YYYY-MM-DD`）；版本索引表同步增一行。
- 每一节建议包含三类（可缺省）：**Added**（新能力）、**Changed**（行为或体验调整）、**Fixed**（缺陷）。历史包袱（如 Post-Plan P1/P2）可在小节标题或列表中保留原编号便于对主 Plan §15 映射。
- 可选：在 Git 上打 **语义化标签**（如 `v0.1.0`），并在索引表「标签」列填写，便于 `git diff v0.1.0..v0.2.0`。
- 若仅镜像主 Plan 某一节，在条目中写明对应章节（如 §15）。
- **文档末尾的「当前能力快照」** 仅在发布新节时更新为「截至最新版本」的 In scope / Out of scope，供下一次扩展快速对齐。

### 新版本模板（复制后填空）

```markdown
## YYYY-MM-DD — 简短标题

**标签**：（可选）`v0.x.y`  
**关联主 Plan**：（可选）章节或里程碑 ID

### Added
- …

### Changed
- …

### Fixed
- …
```

---

## 版本索引

| 版本日期   | 标签（可选） | 说明 |
|------------|--------------|------|
| 2026-05-12 | —            | MVP（主 Plan M1–M9）基线 + Post-Plan 联调修复（P1）与前端升级（P2）；日志体例改为 Added/Changed/Fixed |

---

## 2026-05-12 — MVP 基线与 Post-Plan 迭代

**标签**：（建议首次发版时打 `v0.1.0`）  
**关联主 Plan**：M1–M9 交付范围；Post-Plan 变更对应主 Plan §15 镜像约定。

### Added

- **主 Plan（M1–M9）— 对外能力与基线实现**（细节与验收以主 Plan 为准）  
  - **后端**：FastAPI；简历 PDF 上传与解析（`pdfplumber`）；LangGraph 招聘流程编排；岗位匹配与状态持久化（如 `aiosqlite`）；SSE 事件流。  
  - **API**：`POST /applications/upload`；`GET /applications/{id}`、`GET /applications/{id}/events`、`GET /applications/{id}/result`；`POST /applications/{id}/select-job`、`POST /applications/{id}/reupload`、`POST /applications/{id}/cancel`；`GET /jobs`。  
  - **前端（基线）**：简历上传、SSE 订阅、岗位列表与选择、缺失信息提示、流程状态展示、终止态/错误态。  
  - **演示**：`scripts/demo.sh` 与 `demo-fixtures/`（success / match_failed / missing_required 等场景）。
- **P2.1** `StatusTimeline.tsx`：四步可视化步骤条（Resume Uploaded → Parsing Resume → Matching Jobs → Result/Action），图标状态（完成 / 进行中 / 失败 / 待机）与可读状态文案；覆盖实际 status（含 `match_failed_terminated`，修正 `no_qualified_jobs_terminated` key）。
- **P2.4** `MissingInfoAlert.tsx`：卡片式缺失字段展示、重传次数说明、内嵌隐藏 `<input type="file">` 调用真实 `POST /applications/{id}/reupload`。
- **P2.5** `Application.tsx`：`match_failed_terminated` / `user_cancelled_terminated` 全屏结果页；`system_error` 内联提示与 Try again；上传 loading、全局 API 错误 banner；SSE 触发快照刷新（`qualifiedJobs` / `missingFields`）。
- **P1.5** `scripts/gen_demo_pdfs.py`：用 `reportlab` 生成可解析 demo PDF（`resume_success.pdf`、`resume_match_failed.pdf`、`resume_missing_required.pdf`）。

### Changed

- **P2.2** `JobList.tsx`：提交中 "Processing…"、防重复点击（disabled）、卡片式样式。
- **P2.3** `ResumeUpload.tsx`：`disabled`、重置 input 避免同文件无法二次选择。

### Fixed

- **P1.1** CORS：`backend/main.py` 增加 `CORSMiddleware`，允许 `http://localhost:5173` 与 `http://127.0.0.1:5173`。
- **P1.2** `graph.py`：选岗后继续执行时不再从空 `pdf_bytes` 重跑 `pdf_parse_node`；在 `waiting_job_selection` 且已选岗时直达 `interview_invitation_node`。
- **P1.3** `resume_extract.py` mock：`name` 行切割与 `lower` 一致，避免 `IndexError`。
- **P1.4** `resume_extract.py` mock：邮箱用正则检测全文；平面/设计类关键词触发 skill 以走 `MATCH_FAILED` 演示路径。

---

## 当前能力快照（截至 2026-05-12）

本节供 **下一次迭代** 快速对齐「已实现 vs 准备扩展」；发新版本后改为最新日期。

### In scope（已实现）

- 用户上传简历 PDF → 解析 → 岗位匹配 →（可选）选岗、缺字段重传、取消 → SSE 展示进度与终态（含匹配失败、用户取消、系统错误等前端呈现）。
- 本地演示脚本与三份可被 `pdfplumber` 解析的 demo 简历。
- 开发环境下前后端联调 CORS（localhost / 127.0.0.1:5173）。

### Out of scope（本快照未承诺）

- 生产级认证、多租户、真实邮件/日历邀约发送、持久化迁移策略、非本地 CORS/部署配置（除非后续版本写入本日志 **Added**）。
- 主 Plan 中若仍有未实现条目，以 Cursor 主 Plan 文件为准；此处仅概括仓库当前产品行为。
