#!/usr/bin/env bash
set -euo pipefail

SCENARIO=${1:-}
if [[ -z "$SCENARIO" ]]; then
  echo "Usage: bash scripts/demo.sh <success|match_failed|missing_required>"
  exit 1
fi

case "$SCENARIO" in
  success) PDF="demo-fixtures/resumes/resume_success.pdf" ;;
  match_failed) PDF="demo-fixtures/resumes/resume_match_failed.pdf" ;;
  missing_required) PDF="demo-fixtures/resumes/resume_missing_required.pdf" ;;
  *) echo "Unknown scenario: $SCENARIO"; exit 1 ;;
esac

echo "[1/3] Starting backend on :8000"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/vibe_backend.log 2>&1 &
BACKEND_PID=$!
sleep 2

echo "[2/3] Uploading fixture: $PDF"
APP_ID=$(curl -s -X POST -F "file=@$PDF" http://localhost:8000/applications/upload | python -c "import sys, json; print(json.load(sys.stdin)['application_id'])")
echo "application_id=$APP_ID"

echo "[3/3] Next steps"
echo "- Open frontend and follow status for app: $APP_ID"
if [[ "$SCENARIO" == "success" ]]; then
  echo "- call POST /applications/$APP_ID/select-job with a qualified job id"
elif [[ "$SCENARIO" == "missing_required" ]]; then
  echo "- call POST /applications/$APP_ID/reupload with resume_success.pdf"
else
  echo "- verify result is MATCH_FAILED"
fi

echo "Backend PID: $BACKEND_PID"
