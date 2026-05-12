type Props = {
  fields: string[];
  onReupload: () => void;
  onCancel: () => void;
};

export default function MissingInfoAlert({ fields, onReupload, onCancel }: Props) {
  return (
    <div>
      <h3>Missing required fields</h3>
      <p>{fields.join(", ")}</p>
      <button onClick={onReupload}>Reupload PDF</button>
      <button onClick={onCancel}>End this application</button>
    </div>
  );
}
