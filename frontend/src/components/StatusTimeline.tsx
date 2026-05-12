type Props = {
  events: { status: string; message?: string }[];
  currentStatus: string;
};

type StepState = "done" | "active" | "pending" | "error";

interface Step {
  key: string;
  label: string;
  detail?: string;
}

const STEPS: Step[] = [
  { key: "upload",   label: "Resume Uploaded" },
  { key: "parsing",  label: "Parsing Resume" },
  { key: "matching", label: "Matching Jobs" },
  { key: "action",   label: "Result / Action" },
];

function resolveStepStates(status: string): StepState[] {
  switch (status) {
    case "uploading":
      return ["active", "pending", "pending", "pending"];
    case "created":
    case "parsing_document":
    case "parse_success":
      return ["done", "active", "pending", "pending"];
    case "matching_jobs":
      return ["done", "done", "active", "pending"];
    case "waiting_job_selection":
      return ["done", "done", "done", "active"];
    case "process_success":
      return ["done", "done", "done", "done"];
    case "match_failed_terminated":
      return ["done", "done", "done", "error"];
    case "required_resume_fields_missing_waiting_reupload":
      return ["done", "error", "pending", "pending"];
    case "user_cancelled_terminated":
      return ["done", "done", "done", "error"];
    case "system_error":
      return ["done", "error", "pending", "pending"];
    default:
      return ["pending", "pending", "pending", "pending"];
  }
}

function statusLabel(status: string): string {
  const map: Record<string, string> = {
    uploading: "Uploading resume…",
    created: "Analysing resume…",
    parsing_document: "Reading resume content…",
    parse_success: "Resume parsed, checking fields…",
    matching_jobs: "Matching against available positions…",
    waiting_job_selection: "✋ Please select a position below",
    process_success: "🎉 Interview invitation sent!",
    match_failed_terminated: "No matching positions found",
    required_resume_fields_missing_waiting_reupload: "⚠️ Missing required fields — please re-upload",
    user_cancelled_terminated: "Application cancelled",
    system_error: "Something went wrong — please retry",
    idle: "",
  };
  return map[status] ?? status;
}

function StepIcon({ state }: { state: StepState }) {
  if (state === "done")
    return (
      <span className="w-7 h-7 rounded-full bg-green-500 flex items-center justify-center text-white text-xs font-bold">
        ✓
      </span>
    );
  if (state === "active")
    return (
      <span className="w-7 h-7 rounded-full border-2 border-blue-500 flex items-center justify-center">
        <span className="w-3 h-3 rounded-full bg-blue-500 animate-pulse" />
      </span>
    );
  if (state === "error")
    return (
      <span className="w-7 h-7 rounded-full bg-red-400 flex items-center justify-center text-white text-xs font-bold">
        ✕
      </span>
    );
  return (
    <span className="w-7 h-7 rounded-full border-2 border-gray-300 flex items-center justify-center">
      <span className="w-2 h-2 rounded-full bg-gray-300" />
    </span>
  );
}

export default function StatusTimeline({ currentStatus }: Props) {
  const states = resolveStepStates(currentStatus);
  const label = statusLabel(currentStatus);

  if (currentStatus === "idle") return null;

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
      {/* Step indicators */}
      <ol className="flex items-center gap-0">
        {STEPS.map((step, i) => (
          <li key={step.key} className="flex items-center flex-1 last:flex-none">
            <div className="flex flex-col items-center">
              <StepIcon state={states[i]} />
              <span
                className={`mt-1.5 text-xs text-center leading-tight w-20
                  ${states[i] === "active" ? "text-blue-600 font-semibold" :
                    states[i] === "done"   ? "text-green-600" :
                    states[i] === "error"  ? "text-red-500" :
                                             "text-gray-400"}`}
              >
                {step.label}
              </span>
            </div>
            {i < STEPS.length - 1 && (
              <div
                className={`flex-1 h-0.5 mb-5 mx-1
                  ${states[i] === "done" ? "bg-green-400" : "bg-gray-200"}`}
              />
            )}
          </li>
        ))}
      </ol>

      {/* Current status message */}
      {label && (
        <p className={`text-sm font-medium text-center
          ${currentStatus === "waiting_job_selection" ? "text-blue-700" :
            currentStatus === "process_success"       ? "text-green-700" :
            currentStatus.includes("error") || currentStatus.includes("terminated") ? "text-red-600" :
            "text-gray-600"}`}>
          {label}
        </p>
      )}
    </div>
  );
}
