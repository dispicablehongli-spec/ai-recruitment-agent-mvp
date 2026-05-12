import { useEffect, useState } from "react";

export function useSSE(url: string | null) {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    if (!url) return;
    const source = new EventSource(url);
    source.addEventListener("status_update", (evt) => {
      const message = JSON.parse((evt as MessageEvent).data);
      setEvents((prev) => [...prev, message]);
    });
    return () => source.close();
  }, [url]);

  return events;
}
