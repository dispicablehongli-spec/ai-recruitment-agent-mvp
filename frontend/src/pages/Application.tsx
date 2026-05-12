import { useState } from "react";

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
  const events = useSSE(applicationId ? `http://localhost:8000/applications/${applicationId}/events` : null);

  async function upload(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await apiClient.post("/applications/upload", formData);
    setApplicationId(response.data.application_id);
    setStatus(response.data.status);
    const snapshot = await apiClient.get(`/applications/${response.data.application_id}`);
    setQualifiedJobs(snapshot.data.payload.qualified_jobs || []);
    setMissingFields(snapshot.data.payload.missing_required_resume_fields || []);
    setStatus(snapshot.data.status);
  }

  async function selectJob(jobId: string) {
    if (!applicationId) return;
    const response = await apiClient.post(`/applications/${applicationId}/select-job`, { job_id: jobId });
    setStatus(response.data.status);
  }

  async function cancel() {
    if (!applicationId) return;
    const response = await apiClient.post(`/applications/${applicationId}/cancel`);
    setStatus(response.data.status);
  }

  if (status === "process_success") {
    return <InviteSuccess />;
  }

  return (
    <div>
      <h1>AI Recruitment MVP</h1>
      <ResumeUpload onUpload={upload} />
      <StatusTimeline events={events} />
      {missingFields.length > 0 && <MissingInfoAlert fields={missingFields} onReupload={() => {}} onCancel={cancel} />}
      {qualifiedJobs.length > 0 && <JobList jobs={qualifiedJobs} onSelect={selectJob} />}
    </div>
  );
}
