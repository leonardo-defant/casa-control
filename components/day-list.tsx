import { progress, type DaySection } from "@/lib/day";
import { toggleCheck } from "@/app/(casa)/checks/actions";

export function DayList({
  sections,
  dueOn,
  returnTo,
  empty,
}: {
  sections: DaySection[];
  dueOn: string;
  returnTo: string;
  empty: string;
}) {
  if (sections.length === 0) {
    return <p className="text-base text-stone-600">{empty}</p>;
  }

  const { done, total } = progress(sections);

  return (
    <div className="space-y-6">
      {total > 0 ? (
        <p className="text-sm font-medium text-stone-600">
          {done} de {total} feitas
        </p>
      ) : null}
      {sections.map((section) => (
        <section key={section.id} className="space-y-2">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-stone-500">
            {section.title}
          </h2>
          <ul className="space-y-2">
            {section.items.map((item) => (
              <li key={item.key}>
                {item.canToggle ? (
                  <form action={toggleCheck}>
                    <input type="hidden" name="dueOn" value={dueOn} />
                    <input type="hidden" name="returnTo" value={returnTo} />
                    <input
                      type="hidden"
                      name="intent"
                      value={item.checked ? "uncheck" : "check"}
                    />
                    {item.templateId ? (
                      <input type="hidden" name="templateId" value={item.templateId} />
                    ) : null}
                    {item.oneOffId ? (
                      <input type="hidden" name="oneOffId" value={item.oneOffId} />
                    ) : null}
                    <button
                      type="submit"
                      aria-pressed={item.checked}
                      className="flex min-h-14 w-full items-start gap-3 rounded-2xl bg-white px-3 py-3 text-left ring-1 ring-stone-200"
                    >
                      <RowBody item={item} />
                    </button>
                  </form>
                ) : (
                  <div className="flex min-h-14 w-full items-start gap-3 rounded-2xl bg-white px-3 py-3 ring-1 ring-stone-200">
                    <RowBody item={item} />
                  </div>
                )}
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}

function RowBody({
  item,
}: {
  item: DaySection["items"][number];
}) {
  return (
    <>
      <span
        aria-hidden
        className={`mt-0.5 flex size-7 shrink-0 items-center justify-center rounded-lg border ${
          item.checked
            ? "border-emerald-800 bg-emerald-800 text-white"
            : "border-stone-300 bg-stone-50"
        }`}
      >
        {item.checked ? "✓" : ""}
      </span>
      <span className="min-w-0 flex-1">
        <span
          className={`block text-base font-medium ${
            item.checked ? "text-stone-400 line-through" : "text-stone-900"
          }`}
        >
          {item.timeLabel ? `${item.timeLabel} ` : ""}
          {item.title}
        </span>
        {item.detail ? (
          <span className="mt-1 block text-sm text-stone-500">{item.detail}</span>
        ) : null}
      </span>
    </>
  );
}
