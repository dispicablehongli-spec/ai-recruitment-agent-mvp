import { useEffect, useState } from "react";

import { apiClient } from "../api/client";
import InviteSuccess from "../components/InviteSuccess";
import JobList from "../components/JobList";
import MissingInfoAlert from "../components/MissingInfoAlert";
import ResumeUpload from "../components/ResumeUpload";
import StatusTimeline from "../components/StatusTimeline";
import { useSSE } from "../hooks/useSSE";

export default function ApplicationPage() {
  const [applicationId, setApplicationId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("idle");
  const [qualifiedJobs, setQualifiedJobs] = useState<{ id: string; title: string }[]>([]);
  const [missingFields, setMissingFields] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const events = useSSE(
    applicationId ? `http://localhost:8000/applications/${applicationId}/events` : null
  );

  // Re-fetch snapshot whenever backend pushes a status_update event
  useEffect(() => {
    if (!applicationId || events.length === 0) return;
    const latest = events[events.length - 1];
    if (latest?.status) {
      setStatus(latest.status);
      fetchSnapshot(applicationId);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [events]);

  async function fetchSnapshot(appId: string) {
    try {
      const snapshot = await apiClient.get(`/applications/${appId}`);
      setQualifiedJobs(snapshot.data.payload?.qualified_jobs || []);
      setMissingFields(snapshot.data.payload?.missing_required_resume_fields || []);
      setStatus(snapshot.data.status);
    } catch {
      // non-critical, SSE already updated status
    }
  }

  async function upload(file: File) {
    setLoading(true);
    setError(null);
    setQualifiedJobs([]);
    setMissingFields([]);
    setApplicationId(null);
    setStatus("uploading");
    try {
      const response = await apiClient.post("/applications/upload", (() => {
        const fd = new FormData();
        fd.append("file", file);
        return fd;
      })());
      const appId: string = response.data.application_id;
      setApplicationId(appId);
      setStatus(response.data.status);
      await fetchSnapshot(appId);
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Upload failed — make sure the backend is running on :8000";
      setError(msg);
      setStatus("idle");
    } finally {
      setLoading(false);
    }
  }

  async function selectJob(jobId: string) {
    if (!applicationId) return;
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.post(`/applications/${applicationId}/select-job`, {
        job_id: jobId,
      });
      setStatus(response.data.status);
      if (response.data.status === "process_success") {
        setStatus("process_success");
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Failed to select job");
    } finally {
      setLoading(false);
    }
  }

  async function reupload(file: File) {
    if (!applicationId) return;
    setLoading(true);
    setError(null);
    try {
      const fd = new FormData();
      fd.append("file", file);
      const response = await apiClient.post(`/applications/${applicationId}/reupload`, fd);
      setStatus(response.data.status);
      await fetchSnapshot(applicationId);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Re-upload failed");
    } finally {
      setLoading(false);
    }
  }

  async function cancel() {
    if (!applicationId) return;
    try {
      await apiClient.post(`/applications/${applicationId}/cancel`);
      setStatus("user_cancelled_terminated");
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Cancel failed");
    }
  }

  if (status === "process_success") {
    return <InviteSuccess />;
  }

  if (status === "match_failed_terminated") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <div className="max-w-md w-full bg-white rounded-2xl border border-gray-200 shadow-sm p-8 text-center space-y-4">
          <div className="text-5xl">🔍</div>
          <h2 className="text-xl font-semibold text-gray-800">No Matching Positions Found</h2>
          <p className="text-gray-500 text-sm leading-relaxed">
            We reviewed your resume against all current openings, but your skill set
            doesn't closely align with any available role right now. This could be due
            to a skills gap, experience level, or a mismatch in industry focus.
          </p>
          <div className="bg-gray-50 rounded-lg p-4 text-left text-sm text-gray-600 space-y-1">
            <p className="font-medium text-gray-700 mb-2">What you can do next:</p>
            <p>• Tailor your resume to highlight more relevant technical skills</p>
            <p>• Check back when new positions are posted</p>
            <p>• Try uploading an updated version of your resume</p>
          </div>
          <button
            className="w-full py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition"
            onClick={() => { setStatus("idle"); setApplicationId(null); setQualifiedJobs([]); }}
          >
            Upload a Different Resume
          </button>
        </div>
      </div>
    );
  }

  if (status === "user_cancelled_terminated") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <div className="max-w-sm w-full bg-white rounded-2xl border border-gray-200 shadow-sm p-8 text-center space-y-4">
          <div className="text-4xl">👋</div>
          <h2 className="text-xl font-semibold text-gray-800">Application Withdrawn</h2>
          <p className="text-gray-500 text-sm">
            You've withdrawn this application. Feel free to start a new one whenever you're ready.
          </p>
          <button
            className="w-full py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition"
            onClick={() => { setStatus("idle"); setApplicationId(null); }}
          >
            Start Over
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-gray-800">AI Recruitment Agent</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded p-3 text-sm">
            {error}
          </div>
        )}

        {!applicationId && (
          <ResumeUpload onUpload={upload} disabled={loading} />
        )}

        {loading && (
          <div className="flex items-center gap-2 text-gray-500 text-sm">
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
            </svg>
            Processing…
          </div>
        )}

        {applicationId && (
          <p className="text-xs text-gray-400 font-mono">app: {applicationId}</p>
        )}

        <StatusTimeline events={events} currentStatus={status} />

        {missingFields.length > 0 && status === "required_resume_fields_missing_waiting_reupload" && (
          <MissingInfoAlert
            fields={missingFields}
            onReupload={reupload}
            onCancel={cancel}
          />
        )}

        {qualifiedJobs.length > 0 && (
          <JobList jobs={qualifiedJobs} onSelect={selectJob} />
        )}

        {status === "system_error" && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-700 space-y-2">
            <p className="font-medium">Something went wrong during processing.</p>
            <p className="text-red-600">This is usually a temporary issue. Please try uploading your resume again.</p>
            <button
              className="mt-1 text-blue-600 hover:underline text-sm"
              onClick={() => { setStatus("idle"); setApplicationId(null); setError(null); }}
            >
              Try again
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
