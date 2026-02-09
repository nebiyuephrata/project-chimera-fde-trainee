export function confidenceTone(value: number): string {
  if (value >= 0.85) return "bg-emerald-500/20 text-emerald-300";
  if (value >= 0.7) return "bg-yellow-500/20 text-yellow-300";
  return "bg-rose-500/20 text-rose-300";
}
