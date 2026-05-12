import { useState } from "react";

type Job = { id: string; title: string };

type Props = {
  jobs: Job[];
  onSelect: (jobId: string) => Promise<void>;
};

export default function JobList({ jobs, onSelect }: Props) {
  const [selecting, setSelecting] = useState<string | null>(null);

  async function handleSelect(id: string) {
    setSelecting(id);
    try {
      await onSelect(id);
    } finally {
      setSelecting(null);
    }
  }

  return (
    <div className="bg-white rounded-xl border border-blue-200 p-5">
      <h2 className="text-base font-semibold text-gray-800 mb-1">
        Matched Positions
      </h2>
      <p className="text-sm text-gray-500 mb-4">
        {jobs.length} job{jobs.length > 1 ? "s" : ""} matched your resume — select one to proceed.
      </p>
      <ul className="space-y-2">
        {jobs.map((job) => (
          <li key={job.id}>
            <button
              disabled={selecting !== null}
              onClick={() => handleSelect(job.id)}
              className={`w-full text-left px-4 py-3 rounded-lg border text-sm font-medium transition
                ${selecting === job.id
                  ? "border-blue-400 bg-blue-50 text-blue-700 cursor-wait"
                  : selecting !== null
                  ? "border-gray-200 bg-gray-50 text-gray-400 cursor-not-allowed"
                  : "border-gray-200 hover:border-blue-400 hover:bg-blue-50 text-gray-800 cursor-pointer"}`}
            >
              {selecting === job.id ? "Processing…" : job.title}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
