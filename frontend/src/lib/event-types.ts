// Event kinds an invitation can be for. `value` is stored in invitation.event.type; `label` is what themes show.
export const EVENT_TYPES = [
  { value: "pernikahan", label: "Pernikahan" },
  { value: "tunangan", label: "Tunangan" },
  { value: "akad", label: "Akad Nikah" },
  { value: "ngunduh-mantu", label: "Ngunduh Mantu" },
  { value: "khitan", label: "Khitanan" },
  { value: "aqiqah", label: "Aqiqah" },
  { value: "ulang-tahun", label: "Ulang Tahun" },
  { value: "syukuran", label: "Syukuran" },
  { value: "wisuda", label: "Syukuran Wisuda" },
  { value: "lainnya", label: "Acara" },
] as const;

/** Label for a stored event type; unknown/empty values fall back to "Pernikahan". */
export function eventTypeLabel(value?: string) {
  const match = EVENT_TYPES.find((type) => type.value === value);
  if (match) return match.label;
  if (value && value !== "reception") return value.charAt(0).toUpperCase() + value.slice(1);
  return "Pernikahan";
}
