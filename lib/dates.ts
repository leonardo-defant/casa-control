export const HOUSE_TIMEZONE = "America/Cuiaba";

const EARLY_MS = 60 * 60 * 1000;
const LATE_MS = 3 * 60 * 60 * 1000;

export const WEEKDAY_NAMES = [
  "Domingo",
  "Segunda",
  "Terça",
  "Quarta",
  "Quinta",
  "Sexta",
  "Sábado",
] as const;

export type MarkTiming = "early" | "on_time" | "late";

export function isDateKey(value: string): boolean {
  return /^(\d{4})-(\d{2})-(\d{2})$/.test(value) && parseDateKey(value) !== null;
}

export function parseDateKey(dateKey: string): Date | null {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(dateKey);
  if (!match) return null;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const date = new Date(year, month - 1, day);
  if (
    date.getFullYear() !== year ||
    date.getMonth() !== month - 1 ||
    date.getDate() !== day
  ) {
    return null;
  }
  return date;
}

export function houseToday(now = new Date()): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: HOUSE_TIMEZONE,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(now);
}

export function weekdayName(dow: number): string {
  return WEEKDAY_NAMES[dow] ?? "";
}

export function formatLongDate(dateKey: string): string {
  const date = parseDateKey(dateKey);
  if (!date) return dateKey;
  const formatted = new Intl.DateTimeFormat("pt-BR", {
    weekday: "long",
    day: "numeric",
    month: "long",
  }).format(date);
  return formatted.charAt(0).toUpperCase() + formatted.slice(1);
}

export function formatClock(iso: string): string {
  return formatHouseClock(new Date(iso));
}

export function formatHouseClock(date: Date): string {
  return new Intl.DateTimeFormat("pt-BR", {
    timeZone: HOUSE_TIMEZONE,
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function timeZoneOffsetMs(date: Date): number {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: HOUSE_TIMEZONE,
    hourCycle: "h23",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).formatToParts(date);
  const bag = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  const hour = Number(bag.hour) % 24;
  const asUtc = Date.UTC(
    Number(bag.year),
    Number(bag.month) - 1,
    Number(bag.day),
    hour,
    Number(bag.minute),
    Number(bag.second),
  );
  return asUtc - date.getTime();
}

export function zonedWallTimeToUtc(dateKey: string, time: string): Date | null {
  const parsed = parseDateKey(dateKey);
  const match = /^(\d{2}):(\d{2})/.exec(time);
  if (!parsed || !match) return null;
  const utcGuess = new Date(
    Date.UTC(
      parsed.getFullYear(),
      parsed.getMonth(),
      parsed.getDate(),
      Number(match[1]),
      Number(match[2]),
      0,
    ),
  );
  const corrected = new Date(utcGuess.getTime() - timeZoneOffsetMs(utcGuess));
  return new Date(utcGuess.getTime() - timeZoneOffsetMs(corrected));
}

export function releaseAt(dueOn: string, scheduled: string | null): Date | null {
  if (!scheduled) return null;
  const start = zonedWallTimeToUtc(dueOn, scheduled);
  if (!start) return null;
  return new Date(start.getTime() - EARLY_MS);
}

export function isBeforeWindow(input: {
  dueOn: string;
  todayKey: string;
  scheduled: string | null;
  now: Date;
}): boolean {
  if (input.dueOn > input.todayKey) return true;
  if (input.dueOn < input.todayKey) return false;
  const release = releaseAt(input.dueOn, input.scheduled);
  if (!release) return false;
  return input.now < release;
}

export function markTiming(input: {
  dueOn: string;
  scheduled: string | null;
  checkedAt: string;
}): MarkTiming {
  const at = new Date(input.checkedAt).getTime();
  if (input.scheduled) {
    const start = zonedWallTimeToUtc(input.dueOn, input.scheduled);
    if (!start) return "on_time";
    if (at < start.getTime() - EARLY_MS) return "early";
    if (at > start.getTime() + LATE_MS) return "late";
    return "on_time";
  }
  if (houseToday(new Date(input.checkedAt)) > input.dueOn) return "late";
  return "on_time";
}
