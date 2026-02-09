import { formatDistanceToNowStrict } from "date-fns";

export function formatRelative(iso: string): string {
  return formatDistanceToNowStrict(new Date(iso), { addSuffix: true });
}
