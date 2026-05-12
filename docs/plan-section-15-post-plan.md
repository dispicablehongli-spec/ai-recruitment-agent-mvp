# §15 Post-Plan 修改记录（与 Cursor 主 Plan 同步）

完整主 Plan 由 Cursor 管理，路径通常为：

`~/.cursor/plans/ai_recruitment_agent_mvp_6f1c943a.plan.md`

为便于在 **GitHub / 克隆后的仓库** 内查看「Plan 冻结之后」的变更，本节在此镜像；与上述文件中的 **§15** 内容一致。

---

## 15. Post-Plan 修改记录（Plan 冻结后的实际变更）

> 以下变更在 M1-M9 主 plan 冻结并交付后产生，记录于此保持文档与代码同步。

### P1 — 首次联调修复（2026-05-12）

#### P1.1 CORS 缺失（阻断前端所有请求）

- **问题**：前端 `localhost:5173` 向后端 `localhost:8000` 发请求被浏览器跨域拦截，上传无任何响应。
- **修复**：`backend/main.py` 加入 `CORSMiddleware`，允许源 `http://localhost:5173` 及 `http://127.0.0.1:5173`。

#### P1.2 `graph.py` — 选岗后重走 PDF 解析导致 `system_error`

- **问题**：`apply_job_selection` 设置 `selected_job_id` 后调用 `run_until_interrupt_or_end`，但函数未区分「首次上传」与「继续执行」，每次都从 `pdf_parse_node` 重新解析。而 `pdf_bytes` 在落库时已被清空（`""`），解析失败 → `error_node` → `system_error`。
- **修复**：在 `run_until_interrupt_or_end` 入口增加判断：`status == "waiting_job_selection" and selected_job_id` 已设 → 直接跳至 `interview_invitation_node`，跳过 PDF 重解析。

#### P1.3 `resume_extract.py` mock — `name` 提取 IndexError

- **问题**：`_mock_resume` 用 `"name:" in lower`（小写）判断，但用 `text.split("name:")` 原始大小写切割。若用户 PDF 含 `"Name:"` 则检查通过但切割失败，`[1]` 抛 `IndexError` → `system_error`。
- **修复**：统一对 `lower` 操作，并加 `len(parts) > 1` 保护。

#### P1.4 `resume_extract.py` mock — email / match_failed 检测逻辑不符合实际 PDF 内容

- **问题**：mock 仅检查字面量 `"missing_email"` / `"match_failed"` 是否在文本中，实际 PDF 中不含这两个字符串，导致：
  - `resume_missing_required.pdf`（Jordan Kim，无 email）被识别为有 email → 进入匹配而非缺字段分支
  - `resume_match_failed.pdf`（Marco Rivera，平面设计师）被识别为有软件技能 → 可能匹配成功
- **修复**：
  - email：改为正则 `r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"` 检测 PDF 全文是否含邮箱地址
  - match_failed：检测 `"graphic design" / "illustrat" / "figma" / "procreate" / "adobe illustrator"` 等关键词 → 强制输出 `["painting"]` 技能触发无匹配

#### P1.5 demo PDF 重生成（真实 reportlab PDF）

- **问题**：原 `demo-fixtures/resumes/` 下的三份 PDF 是文字 stub（带 PDF 头但无可解析内容），`pdfplumber` 提取不到有效文本。
- **修复**：新增 `scripts/gen_demo_pdfs.py`，用 `reportlab` 生成含完整段落、真实格式的 PDF：
  - `resume_success.pdf`：Alice Chen，Python/FastAPI/LangGraph 6 年后端工程师，触发成功路径
  - `resume_match_failed.pdf`：Marco Rivera，8 年平面设计师，触发 `MATCH_FAILED`
  - `resume_missing_required.pdf`：Jordan Kim，前端开发，故意省略 email，触发缺字段分支

### P2 — 前端 UI 全面升级（2026-05-12）

#### P2.1 `StatusTimeline.tsx` — 重写为可视化步骤流程图

- **原始**：仅裸输出 SSE 事件原始字符串列表，无任何可读性。
- **重写**：四步步骤条（Resume Uploaded → Parsing Resume → Matching Jobs → Result/Action），每步含图标状态（绿色 ✓ / 蓝色脉冲动画 / 红色 ✕ / 灰色待机），底部显示当前状态的人类可读描述。覆盖所有实际 status 枚举值（新增 `match_failed_terminated`，修正错误 key `no_qualified_jobs_terminated`）。

#### P2.2 `JobList.tsx` — 加载状态 + 防重复点击

- **升级**：点击岗位按钮后显示 "Processing…"，其余按钮 disabled，避免重复提交。样式升级为 border card 风格。

#### P2.3 `ResumeUpload.tsx` — disabled 状态 + 样式升级

- **升级**：支持 `disabled` prop（上传进行中时按钮灰显），重置 input 值防止同文件二次触发失效。

#### P2.4 `MissingInfoAlert.tsx` — 友好提示卡片 + 内嵌重传文件选择

- **原始**：三行文字 + 两个无样式按钮，`onReupload` 为空函数。
- **重写**：📋 图标卡片，橙色列表显示缺失字段（字段名翻译为人类可读标签），说明重传次数限制，"Re-upload Resume" 按钮内嵌隐藏 `<input type="file">`，直接触发文件选择并调用真实 `/reupload` 接口。

#### P2.5 `Application.tsx` — 完整状态机 + 错误处理 + 结果页

- **新增**：
  - `match_failed_terminated` 全屏结果页：🔍 图标 + 自然语言解释 + 三条操作建议 + 重新上传按钮
  - `user_cancelled_terminated` 全屏结果页：👋 图标 + 已撤回提示 + 重新开始按钮
  - `system_error` 内联提示：说明为临时问题 + "Try again" 链接
  - 上传 loading 状态：按钮灰显 + 旋转动画
  - 全局错误展示：API 失败时红色 error banner
  - `reupload` 函数：连接真实 `/applications/{id}/reupload` 接口
  - SSE 驱动状态更新：每次收到 SSE 事件自动重新拉取快照，`qualifiedJobs` / `missingFields` 实时刷新
