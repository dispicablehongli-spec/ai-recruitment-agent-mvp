type Props = {
  onUpload: (file: File) => Promise<void>;
};

export default function ResumeUpload({ onUpload }: Props) {
  return (
    <div>
      <h3>Upload Resume PDF</h3>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onUpload(file);
        }}
      />
    </div>
  );
}
