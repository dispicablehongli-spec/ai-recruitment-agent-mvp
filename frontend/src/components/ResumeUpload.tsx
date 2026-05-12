type Props = {
  onUpload: (file: File) => Promise<void>;
  disabled?: boolean;
};

export default function ResumeUpload({ onUpload, disabled }: Props) {
  return (
    <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center bg-white">
      <p className="text-gray-500 mb-3 text-sm">Upload a PDF resume to start</p>
      <label className={`cursor-pointer inline-block px-5 py-2.5 rounded font-medium text-sm
        ${disabled
          ? "bg-gray-200 text-gray-400 cursor-not-allowed"
          : "bg-blue-600 text-white hover:bg-blue-700"}`}>
        {disabled ? "Uploading…" : "Choose PDF"}
        <input
          type="file"
          accept=".pdf"
          className="hidden"
          disabled={disabled}
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) onUpload(file);
            e.target.value = "";
          }}
        />
      </label>
    </div>
  );
}
