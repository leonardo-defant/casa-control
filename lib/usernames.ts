const ACCOUNTS = {
  leo: "leo@casa-control.local",
  barbara: "barbara@casa-control.local",
  jonas: "jonas@casa-control.local",
} as const;

export type HouseUsername = keyof typeof ACCOUNTS;

export function normalizeUsername(value: string): string {
  return value
    .trim()
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toLowerCase();
}

export function emailForUsername(value: string): string | null {
  const key = normalizeUsername(value);
  if (key in ACCOUNTS) return ACCOUNTS[key as HouseUsername];
  return null;
}
