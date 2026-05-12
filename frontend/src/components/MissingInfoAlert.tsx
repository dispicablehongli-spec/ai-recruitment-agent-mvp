type Props = {
  fields: string[];
  onReupload: (file: File) => void;
  onCancel: () => void;
};

const FIELD_LABELS: Record<string, string> = {
  name: "Full name",
  date_of_birth: "Date of birth",
  gender: "Gender",
  email: "Email address",
  phone: "Phone number",
  experiences: "Work experience",
  skills: "Skills",
  education: "Education",
};

export default function MissingInfoAlert({ fields, onReupload, onCancel }: Props) {
  return (
    <div className="bg-white rounded-2xl border border-amber-200 shadow-sm p-8 space-y-5">
      <div className="flex items-start gap-3">
        <span className="text-3xl">📋</span>
        <div>
          <h2 className="text-lg font-semibold text-gray-800">Resume Incomplete</h2>
          <p className="text-sm text-gray-500 mt-1">
            Your resume is missing some required information. Please update it and upload again to continue.
          </p>
        </div>
      </div>

      <div className="bg-amber-50 border border-amber-100 rounded-lg p-4 space-y-2">
        <p className="text-sm font-medium text-amber-800 mb-2">Missing fields:</p>
        <ul className="space-y-1">
          {fields.map((f) => (
            <li key={f} className="flex items-center gap-2 text-sm text-amber-700">
              <span className="w-4 h-4 rounded-full border-2 border-amber-400 flex items-center justify-center flex-shrink-0">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
              </span>
              {FIELD_LABELS[f] ?? f}
            </li>
          ))}
        </ul>
      </div>

      <p className="text-xs text-gray-400">
        Make sure the listed fields are clearly written in your PDF and re-upload. You have up to 2 attempts.
      </p>

      <div className="flex gap-3">
        <label className="flex-1 cursor-pointer">
          <span className="block w-full py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition text-center">
            Re-upload Resume
          </span>
          <input
            type="file"
            accept=".pdf"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) onReupload(file);
              e.target.value = "";
            }}
          />
        </label>
        <button
          onClick={onCancel}
          className="flex-1 py-2.5 border border-gray-200 text-gray-600 rounded-lg text-sm font-medium hover:bg-gray-50 transition"
        >
          Withdraw Application
        </button>
      </div>
    </div>
  );
}
