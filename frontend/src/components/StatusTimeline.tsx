type Props = {
  events: { status: string; message?: string }[];
};

export default function StatusTimeline({ events }: Props) {
  return (
    <div>
      <h3>Status Timeline</h3>
      <ul>
        {events.map((event, idx) => (
          <li key={idx}>
            {event.status} {event.message ? `- ${event.message}` : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}
