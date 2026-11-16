// Cria Leo, Barbara e Jonas no Supabase Auth.
// Senhas só em CASA_PWD_LEO, CASA_PWD_BARBARA e CASA_PWD_JONAS.
// Rode a migration 20261116130426_login_usuario_senha antes deste script.

const ACCOUNTS = [
  { env: "CASA_PWD_LEO", email: "leo@casa-control.local", username: "leo" },
  { env: "CASA_PWD_BARBARA", email: "barbara@casa-control.local", username: "barbara" },
  { env: "CASA_PWD_JONAS", email: "jonas@casa-control.local", username: "jonas" },
];

const url = (process.env.NEXT_PUBLIC_SUPABASE_URL || process.env.SUPABASE_URL || "").replace(/\/$/, "");
const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY || "";

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!url) fail("Falta NEXT_PUBLIC_SUPABASE_URL ou SUPABASE_URL.");
if (!serviceKey) fail("Falta SUPABASE_SERVICE_ROLE_KEY.");

for (const account of ACCOUNTS) {
  if (!process.env[account.env]) fail(`Falta ${account.env}.`);
}

async function admin(path, options = {}) {
  const response = await fetch(`${url}/auth/v1${path}`, {
    ...options,
    headers: {
      apikey: serviceKey,
      authorization: `Bearer ${serviceKey}`,
      "content-type": "application/json",
      ...(options.headers || {}),
    },
  });
  const text = await response.text();
  let body = null;
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = { message: text.slice(0, 200) };
    }
  }
  return { ok: response.ok, status: response.status, body };
}

async function findUser(email) {
  const listed = await admin(`/admin/users?page=1&per_page=200`);
  if (!listed.ok) fail(`Não deu para listar usuários (${listed.status}).`);
  const users = listed.body?.users || [];
  return users.find((user) => String(user.email || "").toLowerCase() === email) || null;
}

for (const account of ACCOUNTS) {
  const password = process.env[account.env];
  const created = await admin("/admin/users", {
    method: "POST",
    body: JSON.stringify({
      email: account.email,
      password,
      email_confirm: true,
    }),
  });

  if (created.ok) {
    console.log(`${account.username}: criado`);
    continue;
  }

  const existing = await findUser(account.email);
  if (!existing) {
    const reason = created.body?.msg || created.body?.message || created.body?.error_description || created.status;
    fail(`${account.username}: não criado (${reason}).`);
  }

  const updated = await admin(`/admin/users/${existing.id}`, {
    method: "PUT",
    body: JSON.stringify({
      password,
      email_confirm: true,
    }),
  });
  if (!updated.ok) fail(`${account.username}: não atualizado (${updated.status}).`);
  console.log(`${account.username}: senha atualizada`);
}
