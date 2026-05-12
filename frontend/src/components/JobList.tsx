type Job = { id: string; title: string };

type Props = {
  jobs: Job[];
  onSelect: (jobId: string) => Promise<void>;
};

export default function JobList({ jobs, onSelect }: Props) {
  return (
    <div>
      <h3>Qualified Jobs</h3>
      {jobs.map((job) => (
        <button key={job.id} onClick={() => onSelect(job.id)}>
          {job.title}
        </button>
      ))}
    </div>
  );
}
