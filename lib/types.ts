export type AppRole = "executor" | "manager";

export type TaskCategory = "fixed" | "routine" | "weekday" | "eventual";

export type RecurrenceKind = "none" | "daily" | "weekly" | "eventual";

export type Profile = {
  id: string;
  full_name: string;
  role: AppRole;
};

export type TaskTemplate = {
  id: string;
  code: string | null;
  title: string;
  category: TaskCategory;
  group_name: string | null;
  weekday: number | null;
  scheduled_time: string | null;
  sort_order: number;
  active: boolean;
  recurrence_kind: RecurrenceKind;
  recurrence_interval: number;
  active_weekdays: number[];
  starts_on: string | null;
  ends_on: string | null;
};

export type OneOffTask = {
  id: string;
  title: string;
  due_on: string;
  active: boolean;
  sort_order: number;
};

export type TaskCheck = {
  id: string;
  template_id: string | null;
  one_off_id: string | null;
  due_on: string;
  checked_at: string;
  checked_by: string | null;
  actor_name: string;
  source: "app" | "archive";
  legacy_code: string | null;
};
