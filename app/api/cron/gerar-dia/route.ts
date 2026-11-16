import { houseToday } from "@/lib/dates";
import { ensureHouseDay } from "@/lib/ensure-day";
import { createServiceClient } from "@/lib/supabase/service";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const secret = process.env.CRON_SECRET;
  const header = request.headers.get("authorization");
  if (!secret || header !== `Bearer ${secret}`) {
    return new Response("unauthorized", { status: 401 });
  }

  const supabase = createServiceClient();
  if (!supabase) {
    return Response.json({ ok: false, reason: "service_role" }, { status: 503 });
  }

  const day = houseToday();
  const ok = await ensureHouseDay(supabase, day);
  return Response.json({ ok, day }, { status: ok ? 200 : 500 });
}
