import { useState, useCallback, useMemo, useEffect } from "react";

const FIREBASE_CONFIG = {
  apiKey: "SUA_API_KEY",
  authDomain: "SEU_PROJETO.firebaseapp.com",
  databaseURL: "https://SEU_PROJETO-default-rtdb.firebaseio.com",
  projectId: "SEU_PROJETO",
};

const DB_URL = FIREBASE_CONFIG.databaseURL;
const IS_CONFIGURED = !DB_URL.includes("SEU_PROJETO");

async function fbGet(path) {
  if (!IS_CONFIGURED) return null;
  try { const r = await fetch(`${DB_URL}/${path}.json`); return r.ok ? await r.json() : null; } catch { return null; }
}
async function fbSet(path, data) {
  if (!IS_CONFIGURED) return;
  try { await fetch(`${DB_URL}/${path}.json`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }); } catch {}
}

const DAILY_FIXED = [
  { id: "d1", text: "07:30 — Buscar a Letícia e levar para o trabalho" },
  { id: "d2", text: "07:40 — Alimentar os cachorros e aplicar medicações da Bulma" },
];
const DAILY_ROUTINE = [
  { id: "dr1", text: "Checagem rápida das áreas externas" },
  { id: "dr2", text: "Piscina: retirada de folhas e sujeira visível" },
  { id: "dr3", text: "Jardim: recolher folhas e resíduos" },
  { id: "dr4", text: "Depósito: guardar ferramentas e manter organização" },
  { id: "dr5", text: "Monitorar insumos: cloro, produtos, peças, combustível" },
];
const WEEKLY_TASKS = {
  1: [{ id: "w_seg1", text: "08:00 — Levar cachorros na creche" }, { id: "w_seg2", text: "14:00 — Buscar cachorros na creche" }],
  2: [],
  3: [{ id: "w_qua1", text: "08:00 — Levar cachorros na creche" }, { id: "w_qua2", text: "10:00 — Levar Gabriel para aula de música" }, { id: "w_qua3", text: "14:00 — Buscar cachorros na creche" }],
  4: [],
  5: [{ id: "w_sex1", text: "08:00 — Levar cachorros na creche" }, { id: "w_sex2", text: "10:00 — Levar Gabriel para aula de música" }, { id: "w_sex3", text: "14:00 — Buscar cachorros na creche" }, { id: "w_sex4", text: "Carro do Léo: lava a jato + abastecer + calibrar (manhã)" }, { id: "w_sex5", text: "Carro da Bárbara: lava a jato + abastecer + calibrar (tarde)" }, { id: "w_sex6", text: "Piscina: preparação para o fim de semana" }],
  6: [{ id: "w_sab1", text: "Antes de sair: encher galão de água dos cachorros" }, { id: "w_sab2", text: "Revisão geral: piscina, irrigação, iluminação, portões" }],
};
const EVENTUAL_CATEGORIES = [
  { id: "ev_jardim", name: "Jardim", icon: "🌿", color: "#2D6A4F", tasks: [{ id: "ej1", text: "Cortar grama" }, { id: "ej2", text: "Podas maiores" }, { id: "ej3", text: "Adubação e controle de pragas" }, { id: "ej4", text: "Troca/manutenção ferramentas de jardinagem" }] },
  { id: "ev_irrigacao", name: "Irrigação Automática", icon: "💧", color: "#0077B6", tasks: [{ id: "ei1", text: "Ajuste de programação por clima/estação/chuvas" }, { id: "ei2", text: "Desentupir bicos, trocar aspersores, revisar vazamentos" }, { id: "ei3", text: "Ajustes de sensores e setores com falha" }] },
  { id: "ev_piscina", name: "Piscina", icon: "🏊", color: "#219EBC", tasks: [{ id: "ep1", text: "Limpeza pesada e manutenção corretiva" }, { id: "ep2", text: "Ajustes finos de tratamento (uso, clima, chuva)" }, { id: "ep3", text: "Troca de componentes / chamar assistência" }] },
  { id: "ev_infra", name: "Infra Externa", icon: "🔧", color: "#E9C46A", tasks: [{ id: "ein1", text: "Pequenos reparos (torneiras, trincos, dobradiças)" }, { id: "ein2", text: "Troca de lâmpadas e ajustes de iluminação" }, { id: "ein3", text: "Manutenção de portões e interfone" }] },
  { id: "ev_compras", name: "Compras & Recados", icon: "🛒", color: "#7B2CBF", tasks: [{ id: "ec1", text: "Mercado" }, { id: "ec2", text: "Farmácia" }, { id: "ec3", text: "Buscar encomendas / entregas sob demanda" }] },
];

const DAYS_PT = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
const DAYS_FULL = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"];
const MONTHS_PT = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

function getDateKey(d) { return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`; }
function getWeekDates(ref) {
  const d = new Date(ref); const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  const mon = new Date(d.setDate(diff));
  return Array.from({ length: 7 }, (_, i) => { const dt = new Date(mon); dt.setDate(mon.getDate() + i); return dt; });
}
function CheckItem({ checked, text, onToggle, accent = "#2D6A4F", who }) {
  return (
    <button onClick={onToggle} style={{ width: "100%", display: "flex", alignItems: "flex-start", gap: 12, padding: "11px 12px", border: "none", background: checked ? `${accent}08` : "transparent", borderRadius: 10, cursor: "pointer", textAlign: "left", transition: "all 0.15s ease" }}>
      <div style={{ width: 22, height: 22, borderRadius: 7, flexShrink: 0, marginTop: 1, border: checked ? "none" : "2px solid #334155", background: checked ? `linear-gradient(135deg, ${accent}, ${accent}bb)` : "transparent", display: "flex", alignItems: "center", justifyContent: "center", transition: "all 0.2s ease" }}>
        {checked && <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12" /></svg>}
      </div>
      <div style={{ flex: 1 }}>
        <span style={{ fontSize: 14, fontWeight: 500, lineHeight: 1.45, color: checked ? "#64748b" : "#cbd5e1", textDecoration: checked ? "line-through" : "none", transition: "all 0.2s ease" }}>{text}</span>
        {checked && who && <div style={{ fontSize: 11, color: "#475569", marginTop: 2 }}>✓ por {who}</div>}
      </div>
    </button>
  );
}

function SectionCard({ title, icon, accent, count, total, defaultOpen, children }) {
  const [open, setOpen] = useState(defaultOpen || false);
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  const done = count === total && total > 0;
  return (
    <div style={{ background: "#111827", borderRadius: 18, border: `1px solid ${open ? accent + "33" : "#1e293b"}`, overflow: "hidden", transition: "all 0.3s ease", marginBottom: 10 }}>
      <button onClick={() => setOpen(!open)} style={{ width: "100%", padding: "15px 16px", border: "none", background: "transparent", cursor: "pointer", display: "flex", alignItems: "center", gap: 12, textAlign: "left" }}>
        <div style={{ width: 40, height: 40, borderRadius: 12, flexShrink: 0, background: `${accent}15`, border: `1px solid ${accent}25`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20 }}>{icon}</div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9", marginBottom: 5 }}>{title}</div>
          <div style={{ height: 3, borderRadius: 2, background: "#1e293b", overflow: "hidden" }}><div style={{ height: "100%", borderRadius: 2, width: `${pct}%`, background: done ? accent : `${accent}aa`, transition: "width 0.4s ease" }} /></div>
        </div>
        <div style={{ textAlign: "right", flexShrink: 0 }}>
          <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 13, fontWeight: 700, color: done ? accent : "#94a3b8" }}>{count}/{total}</div>
          <div style={{ fontSize: 16, color: "#475569", marginTop: 2, transform: open ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s ease" }}>▾</div>
        </div>
      </button>
      {open && <div style={{ padding: "0 8px 10px" }}>{children}</div>}
    </div>
  );
}

function TabBtn({ active, label, count, onClick }) {
  return (
    <button onClick={onClick} style={{ flex: 1, padding: "10px 4px", border: "none", borderRadius: 12, background: active ? "#2D6A4F" : "transparent", color: active ? "#e2f5ec" : "#64748b", fontSize: 13, fontWeight: 600, cursor: "pointer", transition: "all 0.2s ease", display: "flex", alignItems: "center", justifyContent: "center", gap: 6 }}>
      {label}
      {count > 0 && <span style={{ fontSize: 11, fontWeight: 700, fontFamily: "'Space Mono', monospace", background: active ? "#1B433288" : "#1e293b", borderRadius: 6, padding: "2px 6px", color: active ? "#a7f3d0" : "#475569" }}>{count}</span>}
    </button>
  );
}

function LoginScreen({ onLogin }) {
  const users = [{ name: "Léo", emoji: "👨", color: "#2D6A4F" }, { name: "Bárbara", emoji: "👩", color: "#7B2CBF" }, { name: "Funcionário", emoji: "👷", color: "#E76F51" }];
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", background: "linear-gradient(160deg, #080c14 0%, #0f1623 50%, #0b1120 100%)", fontFamily: "'DM Sans', sans-serif", padding: 20 }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet" />
      <h1 style={{ fontFamily: "'Space Mono', monospace", fontSize: 28, color: "#f8fafc", marginBottom: 8 }}>🏠 Casa Control</h1>
      <p style={{ color: "#64748b", fontSize: 14, marginBottom: 40 }}>Quem está acessando?</p>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, width: "100%", maxWidth: 300 }}>
        {users.map(u => (
          <button key={u.name} onClick={() => onLogin(u.name)} style={{ padding: "18px 24px", borderRadius: 16, border: `1px solid ${u.color}33`, background: `${u.color}11`, cursor: "pointer", display: "flex", alignItems: "center", gap: 16, transition: "all 0.2s ease" }}>
            <span style={{ fontSize: 32 }}>{u.emoji}</span>
            <span style={{ fontSize: 16, fontWeight: 600, color: "#f1f5f9" }}>{u.name}</span>
          </button>
        ))}
      </div>
      {!IS_CONFIGURED && <p style={{ color: "#E76F51", fontSize: 12, marginTop: 30, textAlign: "center", maxWidth: 280, lineHeight: 1.5 }}>⚠️ Firebase não configurado. O app funciona localmente mas não sincroniza entre dispositivos.</p>}
    </div>
  );
}
export default function App() {
  const [user, setUser] = useState(null);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [checks, setChecks] = useState({});
  const [tab, setTab] = useState("diario");
  const [notes, setNotes] = useState({});
  const [syncing, setSyncing] = useState(false);
  const [lastSync, setLastSync] = useState(null);

  const dateKey = getDateKey(selectedDate);
  const dow = selectedDate.getDay();
  const isSunday = dow === 0;
  const weekDates = getWeekDates(selectedDate);

  const loadData = useCallback(async () => {
    if (!IS_CONFIGURED) return;
    setSyncing(true);
    const [cd, nd] = await Promise.all([fbGet(`checks/${dateKey}`), fbGet(`notes/${dateKey}`)]);
    if (cd) setChecks(p => { const m = { ...p }; Object.entries(cd).forEach(([k, v]) => { m[`${dateKey}__${k}`] = v; }); return m; });
    if (nd) setNotes(p => ({ ...p, [dateKey]: nd }));
    setSyncing(false);
    setLastSync(new Date());
  }, [dateKey]);

  useEffect(() => { if (user) { loadData(); const iv = setInterval(loadData, 30000); return () => clearInterval(iv); } }, [dateKey, user, loadData]);

  const toggle = useCallback((id) => {
    setChecks(prev => {
      const key = `${dateKey}__${id}`;
      const wasChecked = typeof prev[key] === "object" ? prev[key]?.checked : !!prev[key];
      const newVal = wasChecked ? null : { checked: true, by: user, at: new Date().toISOString() };
      fbSet(`checks/${dateKey}/${id}`, newVal);
      return { ...prev, [key]: newVal };
    });
  }, [dateKey, user]);

  const isChecked = useCallback((id) => { const v = checks[`${dateKey}__${id}`]; return typeof v === "object" ? !!v?.checked : !!v; }, [checks, dateKey]);
  const getWho = useCallback((id) => { const v = checks[`${dateKey}__${id}`]; return typeof v === "object" ? v?.by : null; }, [checks, dateKey]);
  const saveNote = useCallback((text) => { setNotes(p => ({ ...p, [dateKey]: text })); fbSet(`notes/${dateKey}`, text || null); }, [dateKey]);

  const weeklyToday = useMemo(() => WEEKLY_TASKS[dow] || [], [dow]);
  const dailyAll = [...DAILY_FIXED, ...DAILY_ROUTINE];
  const dailyDone = dailyAll.filter(t => isChecked(t.id)).length;
  const weeklyDone = weeklyToday.filter(t => isChecked(t.id)).length;
  const allTotal = dailyAll.length + weeklyToday.length;
  const allDone = dailyDone + weeklyDone;
  const dayPct = allTotal > 0 ? Math.round((allDone / allTotal) * 100) : 0;

  const getDatePct = useCallback((d) => {
    const dk = getDateKey(d); const dw = d.getDay(); if (dw === 0) return -1;
    const wt = WEEKLY_TASKS[dw] || []; const all = [...DAILY_FIXED, ...DAILY_ROUTINE, ...wt];
    const done = all.filter(t => { const v = checks[`${dk}__${t.id}`]; return typeof v === "object" ? !!v?.checked : !!v; }).length;
    return all.length > 0 ? Math.round((done / all.length) * 100) : 0;
  }, [checks]);

  const evDone = EVENTUAL_CATEGORIES.reduce((a, c) => a + c.tasks.filter(t => isChecked(t.id)).length, 0);
  const evTotal = EVENTUAL_CATEGORIES.reduce((a, c) => a + c.tasks.length, 0);

  if (!user) return <LoginScreen onLogin={setUser} />;

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(160deg, #080c14 0%, #0f1623 50%, #0b1120 100%)", fontFamily: "'DM Sans', sans-serif", color: "#e2e8f0" }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet" />
      <div style={{ position: "fixed", top: -200, right: -200, width: 600, height: 600, background: "radial-gradient(circle, rgba(45,106,79,0.1) 0%, transparent 70%)", pointerEvents: "none" }} />

      <div style={{ maxWidth: 480, margin: "0 auto", padding: "0 16px", position: "relative", zIndex: 1 }}>
        <div style={{ paddingTop: 20, paddingBottom: 4 }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <div>
              <h1 style={{ fontFamily: "'Space Mono', monospace", fontSize: 20, fontWeight: 700, color: "#f8fafc", margin: 0 }}>🏠 Casa Control</h1>
              <p style={{ fontSize: 12, color: "#64748b", margin: "3px 0 0" }}>{DAYS_FULL[dow]}, {selectedDate.getDate()} de {MONTHS_PT[selectedDate.getMonth()]} · <span style={{ color: "#94a3b8" }}>{user}</span></p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <button onClick={loadData} style={{ width: 34, height: 34, borderRadius: 10, border: "1px solid #1e293b", background: "#111827", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, color: syncing ? "#2D6A4F" : "#475569" }} title="Atualizar">{syncing ? "⏳" : "🔄"}</button>
              <button onClick={() => setUser(null)} style={{ width: 34, height: 34, borderRadius: 10, border: "1px solid #1e293b", background: "#111827", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, color: "#475569" }} title="Trocar usuário">👤</button>
              {!isSunday && (
                <div style={{ background: dayPct === 100 ? "linear-gradient(135deg,#2D6A4F,#40916C)" : "linear-gradient(135deg,#1e293b,#253347)", borderRadius: 14, padding: "8px 14px", textAlign: "center", border: `1px solid ${dayPct === 100 ? "#40916C44" : "#334155"}` }}>
                  <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 20, fontWeight: 700, color: dayPct === 100 ? "#a7f3d0" : "#f8fafc" }}>{dayPct}%</div>
                  <div style={{ fontSize: 8, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1 }}>{dayPct === 100 ? "✓" : "do dia"}</div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div style={{ display: "flex", gap: 4, margin: "12px 0 14px" }}>
          {weekDates.map((date, i) => {
            const dk = getDateKey(date); const sel = dk === dateKey; const today = dk === getDateKey(new Date()); const sun = date.getDay() === 0; const pct = getDatePct(date);
            return (
              <button key={i} onClick={() => setSelectedDate(new Date(date))} style={{ flex: 1, minWidth: 46, padding: "8px 2px", borderRadius: 14, border: "none", background: sel ? "linear-gradient(135deg,#2D6A4F,#1B4332)" : sun ? "#0d0a12" : "#0f1623", cursor: "pointer", display: "flex", flexDirection: "column", alignItems: "center", gap: 3, outline: today && !sel ? "1px solid #2D6A4F44" : "none", opacity: sun ? 0.35 : 1, transition: "all 0.2s" }}>
                <span style={{ fontSize: 9, fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5, color: sel ? "#a7f3d0" : "#64748b" }}>{DAYS_PT[date.getDay()]}</span>
                <span style={{ fontSize: 16, fontWeight: 700, color: sel ? "#f8fafc" : "#94a3b8", fontFamily: "'Space Mono', monospace" }}>{date.getDate()}</span>
                {!sun && <div style={{ width: 22, height: 3, borderRadius: 2, background: "#1e293b", overflow: "hidden" }}><div style={{ width: `${pct}%`, height: "100%", borderRadius: 2, background: pct === 100 ? "#40916C" : "#2D6A4F", transition: "width 0.3s" }} /></div>}
              </button>
            );
          })}
        </div>

        {isSunday ? (
          <div style={{ textAlign: "center", padding: "60px 20px" }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>😴</div>
            <p style={{ fontFamily: "'Space Mono', monospace", fontSize: 16, fontWeight: 600, color: "#64748b" }}>Domingo — Dia de folga!</p>
          </div>
        ) : (
          <>
            <div style={{ display: "flex", gap: 4, background: "#0b1120", borderRadius: 14, padding: 4, marginBottom: 14, border: "1px solid #1e293b" }}>
              <TabBtn active={tab === "diario"} label="Diário" count={allTotal - allDone} onClick={() => setTab("diario")} />
              <TabBtn active={tab === "eventual"} label="Eventual" count={evTotal - evDone} onClick={() => setTab("eventual")} />
            </div>

            {tab === "diario" && (
              <div style={{ paddingBottom: 40 }}>
                <SectionCard title="Compromissos Fixos" icon="📌" accent="#E76F51" count={DAILY_FIXED.filter(t => isChecked(t.id)).length} total={DAILY_FIXED.length} defaultOpen={true}>
                  {DAILY_FIXED.map(t => <CheckItem key={t.id} checked={isChecked(t.id)} text={t.text} onToggle={() => toggle(t.id)} accent="#E76F51" who={getWho(t.id)} />)}
                </SectionCard>
                <SectionCard title="Rotina Base Diária" icon="🔄" accent="#2D6A4F" count={DAILY_ROUTINE.filter(t => isChecked(t.id)).length} total={DAILY_ROUTINE.length} defaultOpen={true}>
                  {DAILY_ROUTINE.map(t => <CheckItem key={t.id} checked={isChecked(t.id)} text={t.text} onToggle={() => toggle(t.id)} accent="#2D6A4F" who={getWho(t.id)} />)}
                </SectionCard>
                {weeklyToday.length > 0 && (
                  <SectionCard title={`Tarefas de ${DAYS_FULL[dow]}`} icon="📅" accent="#0077B6" count={weeklyDone} total={weeklyToday.length} defaultOpen={true}>
                    {weeklyToday.map(t => <CheckItem key={t.id} checked={isChecked(t.id)} text={t.text} onToggle={() => toggle(t.id)} accent="#0077B6" who={getWho(t.id)} />)}
                  </SectionCard>
                )}
                <textarea placeholder="Observações do dia..." value={notes[dateKey] || ""} onChange={e => saveNote(e.target.value)} style={{ width: "100%", padding: "12px 14px", borderRadius: 14, border: "1px solid #1e293b", background: "#0b1120", color: "#94a3b8", fontSize: 13, fontFamily: "'DM Sans', sans-serif", resize: "vertical", minHeight: 48, outline: "none", boxSizing: "border-box", marginTop: 6 }} />
              </div>
            )}

            {tab === "eventual" && (
              <div style={{ paddingBottom: 40 }}>
                <p style={{ fontSize: 12, color: "#475569", marginBottom: 14, padding: "0 4px", lineHeight: 1.5 }}>Tarefas sob demanda — marque quando realizadas.</p>
                {EVENTUAL_CATEGORIES.map(cat => {
                  const cd = cat.tasks.filter(t => isChecked(t.id)).length;
                  return (
                    <SectionCard key={cat.id} title={cat.name} icon={cat.icon} accent={cat.color} count={cd} total={cat.tasks.length}>
                      {cat.tasks.map(t => <CheckItem key={t.id} checked={isChecked(t.id)} text={t.text} onToggle={() => toggle(t.id)} accent={cat.color} who={getWho(t.id)} />)}
                    </SectionCard>
                  );
                })}
              </div>
            )}
          </>
        )}
        {lastSync && <div style={{ textAlign: "center", padding: "8px 0 20px", fontSize: 11, color: "#334155" }}>Sincronizado: {lastSync.toLocaleTimeString("pt-BR")}</div>}
      </div>
    </div>
  );
}
