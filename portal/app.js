/* PetStore API Console — portal mockup.
 * Runs in the browser and reproduces the logic of the Boomi processes:
 *  - "PetStore API - Get Pet"    → [SUB] PetStore Get Pet    (decision "Valid Pet ID?": query_petId ~ ^[0-9]+$)
 *  - "PetStore API - Create Pet" → [SUB] PetStore Create Pet (decision "Pet Name Provided?": name ~ .*\S.*)
 * Response bodies are the exact Message-shape templates from those processes. */
"use strict";

const HOST = "https://<your-atom-cloud>/ws/simple";
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* storage unavailable */ } },
};

/* ---------- Boomi process simulation ---------- */
const MSG_PET = id => `{ "id": ${id}, "category": {"id": 1, "name": "Dogs"}, "name": "doggie", "photoUrls": ["https://petstore.swagger.io/photos/doggie.jpg"], "tags": [{"id": 1, "name": "friendly"}], "status": "available" }`;
const MSG_400 = `{"code": 400, "type": "error", "message": "Invalid ID supplied"}`;
const MSG_405 = `{"code": 405, "type": "error", "message": "Invalid input: pet name is required"}`;

function execGet(petId) {
  const log = [`INFO  WSS listener "PetStore WSS Get Pet" received GET getPetstorePet`, `INFO  Set DPP query_petId = "${petId}"`, `INFO  Process Call → [SUB] PetStore Get Pet`];
  const ok = /^[0-9]+$/.test(petId);
  log.push(`INFO  Decision "Valid Pet ID?" (regex ^[0-9]+$) → ${ok ? "true" : "false"}`);
  log.push(ok ? `INFO  Message: mock Pet with id ${petId}` : `INFO  Message: ApiResponse 400`);
  log.push("INFO  Return Documents (1 document)");
  return { http: 200, body: ok ? MSG_PET(petId) : MSG_400, branch: ok ? "true" : "false", log };
}

function execCreate(raw) {
  const log = [`INFO  WSS listener "PetStore WSS Create Pet" received POST createPetstorePet (${new Blob([raw]).size} bytes)`, `INFO  Process Call → [SUB] PetStore Create Pet`];
  let doc = null;
  if (raw.trim()) {
    try { doc = JSON.parse(raw); } catch (e) {
      log.push(`ERROR Unable to parse document with JSON profile j.PetStore.Pet: ${e.message}`);
      log.push("ERROR Process execution failed");
      return { http: 500, body: `Process execution failed: the request body is not valid JSON for profile j.PetStore.Pet.`, branch: "error", log, text: true };
    }
  }
  const name = doc && typeof doc === "object" && !Array.isArray(doc) && doc.name != null ? String(doc.name) : "";
  const ok = /.*\S.*/.test(name);
  log.push(`INFO  Decision "Pet Name Provided?" (profile element name, regex .*\\S.*) → ${ok ? "true" : "false"}`);
  if (ok) { log.push(`INFO  Notify: Pet accepted: ${raw.replace(/\s+/g, " ").trim()}`); log.push("INFO  Return Documents (echo of the request)"); }
  else { log.push("INFO  Message: ApiResponse 405"); log.push("INFO  Return Documents (1 document)"); }
  return { http: 200, body: ok ? raw : MSG_405, branch: ok ? "true" : "false", log };
}

/* ---------- state ---------- */
const S = { ep: "get", tab: "body", last: null, history: [], req: 0, err: 0, filter: "all", pets: [] };
const GET_PRESETS = [["123", "valid id"], ["1", "valid id"], ["9007199254740993", "very large"], ["abc", "letters"], ["-1", "negative"], ["12 3", "space"], ["", "empty"]];
const POST_PRESETS = {
  "Valid dog": { id: 10, category: { id: 1, name: "Dogs" }, name: "Bobby", photoUrls: ["https://example.com/bobby.jpg"], tags: [{ id: 1, name: "friendly" }], status: "available" },
  "Cat + tags": { id: 21, category: { id: 2, name: "Cats" }, name: "Mochi", photoUrls: [], tags: [{ id: 3, name: "indoor" }, { id: 4, name: "calm" }], status: "pending" },
  "Missing name": { id: 30, category: { id: 1, name: "Dogs" }, photoUrls: [], status: "available" },
  "Blank name": { id: 31, name: "   ", photoUrls: [], status: "sold" },
  "Invalid JSON": null,
};

/* ---------- rendering helpers ---------- */
function highlight(text) {
  let pretty = text, parsed = true;
  // Integers beyond 2^53 would lose precision when re-serialised, so keep such bodies verbatim.
  if (/\d{16,}/.test(text)) parsed = false;
  else try { pretty = JSON.stringify(JSON.parse(text), null, 2); } catch { parsed = false; }
  if (!parsed) return esc(text);
  return esc(pretty).replace(/(&quot;(?:[^&]|&(?!quot;))*?&quot;)(\s*:)?|\b(true|false|null)\b|(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)/gi,
    (m, str, colon, lit, num) => str ? `<span class="${colon ? "j-k" : "j-s"}">${str}</span>${colon || ""}` : lit ? `<span class="j-b">${lit}</span>` : `<span class="j-n">${num}</span>`);
}
const parseBody = t => { try { return JSON.parse(t); } catch { return null; } };
function apiCode(res) { const j = parseBody(res.body); return j && j.type === "error" ? j.code : null; }
function curlFor(req) {
  if (req.ep === "get") return `curl -u "$BOOMI_USER:$BOOMI_TOKEN" \\\n  "${HOST}/getPetstorePet?petId=${encodeURIComponent(req.petId)}"`;
  return `curl -u "$BOOMI_USER:$BOOMI_TOKEN" -X POST \\\n  -H "Content-Type: application/json" \\\n  "${HOST}/createPetstorePet" \\\n  -d '${req.body.replace(/'/g, "'\\''")}'`;
}
function toast(msg) { const t = $("toast"); t.textContent = msg; t.classList.add("show"); clearTimeout(toast.h); toast.h = setTimeout(() => t.classList.remove("show"), 2200); }

/* ---------- flow diagrams ---------- */
const node = (k, title, sub, cls = "") => `<div class="node ${cls}"><span class="k">${k}</span><b>${esc(title)}</b>${sub ? esc(sub) : ""}</div>`;
const arrow = hit => `<div class="arrow ${hit ? "hit" : ""}"></div>`;
function flowHTML(ep, branch) {
  const ran = !!branch, t = branch === "true", f = branch === "false", e = branch === "error";
  const G = ep === "get";
  const api = `<div class="flow-title"><span class="m ${G ? "get" : "post"}">${G ? "GET" : "POST"}</span>PetStore API - ${G ? "Get Pet" : "Create Pet"}</div>
    <div class="flow">${node("start · wss listen", G ? "PetStore WSS Get Pet" : "PetStore WSS Create Pet", G ? "GET, no input" : "CREATE, single JSON", ran ? "hit" : "")}${arrow(ran)}
    ${node("process call", G ? "[SUB] PetStore Get Pet" : "[SUB] PetStore Create Pet", "", ran ? "hit" : "")}${arrow(ran && !e)}
    ${node("return documents", "WSS response", "", ran && !e ? "hit" : e ? "dim" : "")}</div>`;
  const dec = G ? node("decision", "Valid Pet ID?", "DPP query_petId ~ ^[0-9]+$", "dec " + (t || f ? "hit" : e ? "" : "")) : node("decision", "Pet Name Provided?", "name ~ .*\\S.*", "dec " + (t || f ? "hit" : ""));
  const trueRow = G
    ? `${node("message", "Mock Pet", "id = petId, name doggie", t ? "hit" : ran ? "dim" : "")}${arrow(t)}${node("return", "Return Documents", "", t ? "hit" : ran ? "dim" : "")}`
    : `${node("notify", "Pet accepted: {1}", "INFO in process log", t ? "hit" : ran ? "dim" : "")}${arrow(t)}${node("return", "Return Documents", "echo of request", t ? "hit" : ran ? "dim" : "")}`;
  const falseRow = `${node("message", G ? "ApiResponse 400" : "ApiResponse 405", G ? "Invalid ID supplied" : "pet name is required", "err " + (f ? "hit" : ran ? "dim" : ""))}${arrow(f)}${node("return", "Return Documents", "", "err " + (f ? "hit" : ran ? "dim" : ""))}`;
  const sub = `<div class="sub-call"><div class="flow-title">[SUB] PetStore ${G ? "Get" : "Create"} Pet <span class="meta">passthrough start · testable standalone</span></div>
    <div class="flow">${node("start", "Passthrough", "", ran ? "hit" : "")}${arrow(ran)}${dec}
    <div class="branches"><div class="branch ${t ? "hit" : ""}"><span class="lbl">true</span>${arrow(t)}${trueRow}</div>
    <div class="branch ${f ? "hit" : ""}"><span class="lbl">false</span>${arrow(f)}${falseRow}</div></div></div>
    ${e ? `<div class="note crit"><b>Execution error</b>The body could not be parsed with JSON profile j.PetStore.Pet, so the process failed before the decision.</div>` : ""}</div>`;
  return api + sub;
}

/* ---------- console ---------- */
function urlHTML() {
  return S.ep === "get" ? `${esc(HOST)}/getPetstorePet?petId=<b>${esc($("petId").value)}</b>` : `${esc(HOST)}/<b>createPetstorePet</b>`;
}
function setEp(ep) {
  S.ep = ep;
  document.querySelectorAll("#epSeg button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.ep === ep)));
  $("reqGet").hidden = ep !== "get"; $("reqCreate").hidden = ep !== "create";
  $("urlMethod").textContent = ep === "get" ? "GET" : "POST"; $("urlMethod").className = "m " + (ep === "get" ? "get" : "post");
  $("urlText").innerHTML = urlHTML();
  if (!S.last || S.last.req.ep !== ep) { $("trace").innerHTML = flowHTML(ep, null); }
}
function renderResp() {
  const L = S.last;
  if (!L) return;
  const { res, ms, req } = L, code = apiCode(res);
  $("respStatus").innerHTML = `<span class="badge ${res.http >= 400 ? "b-crit" : code ? "b-warn" : "b-ok"}">HTTP ${res.http}${res.http === 200 ? " OK" : " Error"}</span>
    ${code ? `<span class="badge b-crit" title="Petstore-style ApiResponse in the body; Boomi WSS still answers HTTP 200">ApiResponse ${code}</span>` : ""} <span class="meta">${ms} ms · ${new Blob([res.body]).size} B</span>`;
  const out = $("respOut");
  if (S.tab === "body") out.innerHTML = res.text ? esc(res.body) : highlight(res.body);
  if (S.tab === "headers") out.textContent = `HTTP/1.1 ${res.http} ${res.http === 200 ? "OK" : "Internal Server Error"}\nContent-Type: ${res.text ? "text/plain" : "application/json"}; charset=utf-8\nContent-Length: ${new Blob([res.body]).size}\nX-Boomi-Process: PetStore API - ${req.ep === "get" ? "Get Pet" : "Create Pet"}\nX-Simulated: true`;
  if (S.tab === "log") out.textContent = res.log.join("\n");
  if (S.tab === "curl") out.textContent = curlFor(req);
  document.querySelectorAll("#respTabs button").forEach(b => b.setAttribute("aria-selected", String(b.dataset.tab === S.tab)));
}
function run(req, { record = true } = {}) {
  const t0 = performance.now();
  const res = req.ep === "get" ? execGet(req.petId) : execCreate(req.body);
  const ms = Math.round(90 + Math.random() * 210 + (performance.now() - t0));
  S.req++; const err = res.http >= 400 || apiCode(res); if (err) S.err++;
  $("hReq").textContent = S.req; $("hErr").textContent = S.err;
  const entry = { req, res, ms, at: new Date() };
  if (record) S.history.unshift(entry);
  return entry;
}
function send() {
  const req = S.ep === "get" ? { ep: "get", petId: $("petId").value } : { ep: "create", body: $("body").value };
  const btn = $("sendBtn"); btn.disabled = true; btn.textContent = "Sending…";
  setTimeout(() => {
    S.last = run(req);
    renderResp(); $("trace").innerHTML = flowHTML(req.ep, S.last.res.branch);
    btn.disabled = false; btn.textContent = "Send"; renderHistory();
  }, 260);
}
function loadEntry(e) {
  show("console"); setEp(e.req.ep);
  if (e.req.ep === "get") $("petId").value = e.req.petId; else $("body").value = e.req.body;
  $("urlText").innerHTML = urlHTML(); S.last = e; renderResp(); $("trace").innerHTML = flowHTML(e.req.ep, e.res.branch);
}

/* ---------- pet shop demo ---------- */
const EMOJI = { Dogs: "🐕", Cats: "🐈", Birds: "🦜", Fish: "🐠", Rabbits: "🐇", Reptiles: "🦎" };
const CAT_ID = { Dogs: 1, Cats: 2, Birds: 3, Fish: 4, Rabbits: 5, Reptiles: 6 };
const STATUS_BADGE = { available: "b-ok", pending: "b-warn", sold: "b-mute" };
const SEED = [
  { id: 1, category: { id: 1, name: "Dogs" }, name: "doggie", photoUrls: [], tags: [{ id: 1, name: "friendly" }], status: "available" },
  { id: 2, category: { id: 2, name: "Cats" }, name: "Kitty", photoUrls: [], tags: [{ id: 3, name: "indoor" }], status: "pending" },
  { id: 3, category: { id: 3, name: "Birds" }, name: "Tweety", photoUrls: [], tags: [{ id: 5, name: "singer" }], status: "sold" },
  { id: 4, category: { id: 4, name: "Fish" }, name: "Nemo", photoUrls: [], tags: [], status: "available" },
];
function loadPets() {
  try { const p = JSON.parse(store.get("petstore-pets") || "null"); if (Array.isArray(p) && p.length) return p; } catch { /* ignore */ }
  return SEED.map(p => ({ ...p }));
}
const savePets = () => store.set("petstore-pets", JSON.stringify(S.pets));
const safeUrl = u => (/^https:\/\//i.test(u || "") ? u : "");

function petCard(p) {
  const cat = p.category?.name || "Dogs", img = safeUrl(p.photoUrls?.[0]);
  return `<article class="pet"><div class="pic">${img ? `<img src="${esc(img)}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.replaceWith(document.createTextNode('${EMOJI[cat] || "🐾"}'))">` : EMOJI[cat] || "🐾"}</div>
    <div class="info"><b>${esc(p.name)}</b><span class="meta">#${esc(p.id)} · ${esc(cat)}</span>
    <span><span class="badge ${STATUS_BADGE[p.status] || "b-mute"}">${esc(p.status || "unknown")}</span></span>
    ${p.tags?.length ? `<div class="tags">${p.tags.map(t => `<span>${esc(t.name)}</span>`).join("")}</div>` : ""}</div></article>`;
}
function renderShop() {
  const list = S.pets.filter(p => S.filter === "all" || p.status === S.filter);
  const count = s => S.pets.filter(p => s === "all" || p.status === s).length;
  $("shopPage").innerHTML = `<p class="lead">A tiny storefront built on top of the two endpoints. “Add pet” calls <code>createPetstorePet</code>; “Fetch” calls <code>getPetstorePet</code>.
    The Boomi mock does not store anything, so this list lives only in your browser.</p>
  <div class="shop-top">
    <div class="card"><h3>Add a pet · POST createPetstorePet</h3>
      <form id="petForm" class="form-grid" autocomplete="off">
        <div><label for="pfName">Name</label><input id="pfName" placeholder="e.g. Luna"></div>
        <div><label for="pfCat">Category</label><select id="pfCat">${Object.keys(EMOJI).map(c => `<option>${c}</option>`).join("")}</select></div>
        <div><label for="pfStatus">Status</label><select id="pfStatus"><option>available</option><option>pending</option><option>sold</option></select></div>
        <div><label for="pfTags">Tags</label><input id="pfTags" placeholder="friendly, small"></div>
        <div class="full"><label for="pfPhoto">Photo URL (optional, https)</label><input id="pfPhoto" placeholder="https://…"></div>
        <div class="full"><button class="btn primary" type="submit">Add pet</button> <span class="meta">Leave the name empty to see the 405 response.</span></div>
      </form><div id="petFormOut"></div></div>
    <div class="card"><h3>Find by ID · GET getPetstorePet</h3>
      <form id="fetchForm" style="display:flex;gap:8px"><input id="fetchId" class="grow" placeholder="petId, e.g. 42" style="flex:1;padding:8px 10px;border:1px solid var(--line);border-radius:9px;background:var(--bg)"><button class="btn primary" type="submit">Fetch</button></form>
      <div id="fetchOut"><p class="meta">The mock always answers with “doggie” using the id you send — handy for testing clients, not a real lookup.</p></div></div>
  </div>
  <div class="filters">${["all", "available", "pending", "sold"].map(s => `<button class="chip" data-filter="${s}" aria-pressed="${S.filter === s}">${s} (${count(s)})</button>`).join("")}
    <button class="chip" id="resetPets" style="margin-left:auto">Reset demo data</button></div>
  <div class="pets">${list.map(petCard).join("") || `<p class="lead">No pets with status “${esc(S.filter)}”.</p>`}</div>`;
}
function addPet(e) {
  e.preventDefault();
  const cat = $("pfCat").value, nextId = Math.max(0, ...S.pets.map(p => +p.id || 0)) + 1;
  const pet = { id: nextId, category: { id: CAT_ID[cat], name: cat }, name: $("pfName").value, photoUrls: $("pfPhoto").value.trim() ? [$("pfPhoto").value.trim()] : [],
    tags: $("pfTags").value.split(",").map(s => s.trim()).filter(Boolean).map((n, i) => ({ id: i + 1, name: n })), status: $("pfStatus").value };
  const body = JSON.stringify(pet), entry = run({ ep: "create", body });
  const code = apiCode(entry.res);
  if (code) { $("petFormOut").innerHTML = `<div class="note crit"><b>ApiResponse ${code}</b>${esc(parseBody(entry.res.body).message)}</div>`; renderHistory(); return; }
  S.pets.unshift(parseBody(entry.res.body)); savePets();
  renderShop(); renderHistory();
  $("petFormOut").innerHTML = `<div class="note ok"><b>Pet accepted</b>Boomi echoed the pet back (${entry.ms} ms). Logged: “Pet accepted: …”.</div>`;
  toast(`Added ${pet.name}`);
}
function fetchPet(e) {
  e.preventDefault();
  const entry = run({ ep: "get", petId: $("fetchId").value.trim() }), code = apiCode(entry.res);
  $("fetchOut").innerHTML = code ? `<div class="note crit"><b>ApiResponse ${code}</b>${esc(parseBody(entry.res.body).message)}</div>`
    : `<div class="pets" style="margin-top:10px">${petCard(parseBody(entry.res.body))}</div>`;
  renderHistory();
}

/* ---------- static pages ---------- */
function renderReference() {
  const schema = [["id", "integer (int64)", "Pet ID", ""], ["category", "object {id, name}", "Pet category", ""], ["name", "string", "Pet name — <b>required</b>, must contain a non-space character", "doggie"],
    ["photoUrls", "array of string", "Photo URLs", ""], ["tags", "array of {id, name}", "Tags", ""], ["status", "string", "available | pending | sold", "available"]];
  $("refPage").innerHTML = `<p class="lead">Boomi Web Services Server listeners that mimic two operations of the public <a href="https://petstore.swagger.io/" target="_blank" rel="noopener">Swagger Petstore</a>.
    Both use Basic authentication with the Atom Cloud shared web server user.</p>
  <h2>Endpoints</h2><div class="scroll"><table class="tbl"><thead><tr><th>Boomi endpoint</th><th>Swagger Petstore</th><th>Process</th><th>Input → output</th></tr></thead><tbody>
    <tr><td><span class="m get">GET</span> <code>/ws/simple/getPetstorePet?petId=</code></td><td><code>GET /pet/{petId}</code></td><td>PetStore API - Get Pet → [SUB] PetStore Get Pet</td><td>none → single data</td></tr>
    <tr><td><span class="m post">POST</span> <code>/ws/simple/createPetstorePet</code></td><td><code>POST /pet</code></td><td>PetStore API - Create Pet → [SUB] PetStore Create Pet</td><td>single JSON → single data</td></tr></tbody></table></div>
  <h2>Pet schema · profile j.PetStore.Pet</h2><div class="scroll"><table class="tbl"><thead><tr><th>Field</th><th>Type</th><th>Description</th><th>Example</th></tr></thead><tbody>
    ${schema.map(r => `<tr><td><code>${r[0]}</code></td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3] ? `<code>${r[3]}</code>` : ""}</td></tr>`).join("")}</tbody></table></div>
  <h2>Responses</h2><div class="scroll"><table class="tbl"><thead><tr><th>Case</th><th>HTTP</th><th>Body</th></tr></thead><tbody>
    <tr><td>GET with numeric petId</td><td>200</td><td>Mock Pet “doggie” with the requested id</td></tr>
    <tr><td>GET with missing / non-numeric petId</td><td>200</td><td><code>{"code": 400, "type": "error", "message": "Invalid ID supplied"}</code></td></tr>
    <tr><td>POST with a name</td><td>200</td><td>The request body, echoed back</td></tr>
    <tr><td>POST without a usable name</td><td>200</td><td><code>{"code": 405, "type": "error", "message": "Invalid input: pet name is required"}</code></td></tr>
    <tr><td>POST with malformed JSON</td><td>500</td><td>Process execution error (simulated)</td></tr></tbody></table></div>
  <div class="note">Errors use the Petstore <code>ApiResponse</code> shape in the body. The processes don't set an HTTP status, so the listener answers 200 — clients should check <code>type == "error"</code>.</div>
  <h2>Try it with cURL</h2>
  <pre class="cmd">${esc(curlFor({ ep: "get", petId: "123" }))}</pre>
  <pre class="cmd">${esc(curlFor({ ep: "create", body: JSON.stringify(POST_PRESETS["Valid dog"]) }))}</pre>`;
}
function renderFlowPage() {
  $("flowPage").innerHTML = `<p class="lead">Each API process is a thin Web Services listener that calls a sub-process with the business logic, so the logic can be unit-tested on its own.
    Run a request in API Console to highlight the path it takes.</p>
    <h2>Get Pet</h2><div class="card">${flowHTML("get", S.last?.req.ep === "get" ? S.last.res.branch : null)}</div>
    <h2>Create Pet</h2><div class="card">${flowHTML("create", S.last?.req.ep === "create" ? S.last.res.branch : null)}</div>`;
}
function renderHistory() {
  const H = S.history;
  $("historyPage").innerHTML = H.length ? `<p class="lead">Click a row to open it in API Console.</p><div class="scroll"><table class="tbl"><thead><tr><th>Time</th><th>Request</th><th>Result</th><th class="num">ms</th></tr></thead><tbody>
    ${H.map((e, i) => { const c = apiCode(e.res); return `<tr class="click" data-hist="${i}"><td>${e.at.toLocaleTimeString()}</td>
      <td><span class="m ${e.req.ep === "get" ? "get" : "post"}">${e.req.ep === "get" ? "GET" : "POST"}</span> <code>${e.req.ep === "get" ? `getPetstorePet?petId=${esc(e.req.petId)}` : "createPetstorePet"}</code></td>
      <td><span class="badge ${e.res.http >= 400 ? "b-crit" : c ? "b-warn" : "b-ok"}">${e.res.http}${c ? " · " + c : ""}</span></td><td class="num">${e.ms}</td></tr>`; }).join("")}</tbody></table></div>`
    : `<p class="lead">No requests yet. Send one from API Console or Pet Shop Demo.</p>`;
  renderFlowPage();
}

/* ---------- nav, theme ---------- */
const TITLES = {
  console: ["API Console", "Try the Boomi Web Services endpoints and see which process path runs"],
  shop: ["Pet Shop Demo", "A small storefront that uses the two endpoints"],
  flow: ["Process Flow", "How the Boomi processes are wired"],
  reference: ["API Reference", "Endpoints, schema, responses and cURL examples"],
  history: ["Request History", "Every request sent in this session"],
};
function show(view) {
  document.querySelectorAll(".nav button").forEach(b => (b.dataset.view === view ? b.setAttribute("aria-current", "page") : b.removeAttribute("aria-current")));
  document.querySelectorAll(".view").forEach(v => (v.hidden = v.id !== "view-" + view));
  $("title").textContent = TITLES[view][0]; $("subtitle").textContent = TITLES[view][1];
  $("side").classList.remove("open"); $("scrim").classList.remove("open");
}
function applyTheme(t) {
  if (t) document.documentElement.setAttribute("data-theme", t); else document.documentElement.removeAttribute("data-theme");
  $("themeLbl").textContent = t === "dark" ? "Dark" : t === "light" ? "Light" : "Auto";
}

/* ---------- wiring ---------- */
$("getPresets").innerHTML = GET_PRESETS.map(([v, l]) => `<button class="chip" type="button" data-pid="${esc(v)}" title="${esc(l)}">${v === "" ? "(empty)" : esc(v)}</button>`).join("");
$("postPresets").innerHTML = Object.keys(POST_PRESETS).map(k => `<button class="chip" type="button" data-preset="${esc(k)}">${esc(k)}</button>`).join("");
$("body").value = JSON.stringify(POST_PRESETS["Valid dog"], null, 2);

document.querySelector(".nav").addEventListener("click", e => { const b = e.target.closest("button[data-view]"); if (b) show(b.dataset.view); });
$("epSeg").addEventListener("click", e => { const b = e.target.closest("button[data-ep]"); if (b) setEp(b.dataset.ep); });
$("petId").addEventListener("input", () => ($("urlText").innerHTML = urlHTML()));
$("petId").addEventListener("keydown", e => { if (e.key === "Enter") send(); });
$("body").addEventListener("input", () => $("body").classList.toggle("bad", !!$("body").value.trim() && parseBody($("body").value) === null));
$("body").addEventListener("keydown", e => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) send(); });
$("sendBtn").addEventListener("click", send);
$("fmtBtn").addEventListener("click", () => { const j = parseBody($("body").value); if (j === null) toast("Body is not valid JSON"); else { $("body").value = JSON.stringify(j, null, 2); $("body").classList.remove("bad"); } });
$("respTabs").addEventListener("click", e => { const b = e.target.closest("button[data-tab]"); if (b) { S.tab = b.dataset.tab; renderResp(); } });
document.addEventListener("click", e => {
  const pid = e.target.closest("[data-pid]"); if (pid) { $("petId").value = pid.dataset.pid; $("urlText").innerHTML = urlHTML(); send(); return; }
  const pre = e.target.closest("[data-preset]");
  if (pre) { const v = POST_PRESETS[pre.dataset.preset]; $("body").value = v ? JSON.stringify(v, null, 2) : '{\n  "id": 40,\n  "name": "Broken",\n  "status": "available",\n}'; $("body").dispatchEvent(new Event("input")); return; }
  const f = e.target.closest("[data-filter]"); if (f) { S.filter = f.dataset.filter; renderShop(); return; }
  if (e.target.closest("#resetPets")) { S.pets = SEED.map(p => ({ ...p })); savePets(); renderShop(); toast("Demo data reset"); return; }
  const h = e.target.closest("[data-hist]"); if (h) loadEntry(S.history[+h.dataset.hist]);
});
document.addEventListener("submit", e => { if (e.target.id === "petForm") addPet(e); if (e.target.id === "fetchForm") fetchPet(e); });
$("burger").addEventListener("click", () => { $("side").classList.add("open"); $("scrim").classList.add("open"); });
$("scrim").addEventListener("click", () => { $("side").classList.remove("open"); $("scrim").classList.remove("open"); });
$("themeBtn").addEventListener("click", () => {
  const cur = document.documentElement.getAttribute("data-theme");
  const next = cur === "dark" ? "light" : cur === "light" ? "" : "dark";
  applyTheme(next); store.set("petstore-theme", next);
});

applyTheme(store.get("petstore-theme") || "");
S.pets = loadPets();
setEp("get");
renderShop(); renderReference(); renderHistory();
