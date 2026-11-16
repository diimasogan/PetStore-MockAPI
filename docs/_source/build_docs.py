"""Build the PetStore Mock API documentation (English + Bahasa Indonesia).

Usage:  python3 -I docs/_source/build_docs.py
Writes: docs/PetStore-Mock-API-Documentation.html and docs/id/PetStore-Mock-API-Dokumentasi.html

Every text is a pair T(en, id) so both languages always have the same structure.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = {"en": ROOT / "docs" / "PetStore-Mock-API-Documentation.html",
       "id": ROOT / "docs" / "id" / "PetStore-Mock-API-Dokumentasi.html"}
LINK = {"en": "PetStore-Mock-API-Documentation.html", "id": "id/PetStore-Mock-API-Dokumentasi.html"}
PORTAL = "https://diimasogan.github.io/PetStore-MockAPI/portal/"
REPO = "https://github.com/diimasogan/PetStore-MockAPI"
LANG = "en"


class T(tuple):
    def __new__(cls, en, id_=None):
        return super().__new__(cls, (en, en if id_ is None else id_))

    def __str__(self):
        return self[0] if LANG == "en" else self[1]


def s(x):
    return str(x) if isinstance(x, T) else x


# ---------------------------------------------------------------- building blocks
def icon(path):
    return f'<svg class="ico" viewBox="0 0 24 24">{path}</svg>'


ICONS = {
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c.8-3.5 3.6-5.5 7-5.5s6.2 2 7 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7"/>',
    "doc": '<path d="M4 4h11l5 5v11H4z"/><path d="M15 4v5h5M8 13h8M8 17h5"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
}


def card(ic, title, text, amber=False):
    return (f'<div class="card{" amber" if amber else ""}"><div class="ihead">{icon(ICONS[ic])}<h3>{s(title)}</h3></div>'
            f'<p>{s(text)}</p></div>')


def grid(cards, cols=3):
    return f'<div class="grid g{cols}">{"".join(cards)}</div>'


def table(head, rows):
    h = "".join(f"<th>{s(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{s(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def section(sid, title, body):
    return f'<section id="{sid}"><h2>{s(title)}</h2>{body}</section>'


def stats(items):
    return '<div class="stats">' + "".join(f'<div class="stat"><b>{n}</b><span>{s(t)}</span></div>' for n, t in items) + "</div>"


def ul(items):
    return '<ul class="clean">' + "".join(f"<li>{s(i)}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------- diagram
def architecture_svg():
    L = lambda en, id_: s(T(en, id_))
    return f"""<figure><svg viewBox="0 0 980 470" role="img" aria-label="{L('Solution architecture','Arsitektur solusi')}">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" class="mk"/></marker></defs>
<g class="lane"><rect x="10" y="20" width="170" height="430" rx="14"/><text x="95" y="46" class="lt">{L('Clients','Klien')}</text></g>
<g class="lane"><rect x="196" y="20" width="774" height="430" rx="14"/><text x="583" y="46" class="lt">Boomi Atom Cloud · shared web server</text></g>
<g class="bx"><rect x="26" y="90" width="138" height="54" rx="10"/><text x="95" y="114">cURL / Postman</text><text x="95" y="132" class="sm">{L('manual tests','uji manual')}</text></g>
<g class="bx"><rect x="26" y="170" width="138" height="54" rx="10"/><text x="95" y="194">{L('Front-end app','Aplikasi front-end')}</text><text x="95" y="212" class="sm">{L('client development','pengembangan klien')}</text></g>
<g class="bx"><rect x="26" y="250" width="138" height="54" rx="10"/><text x="95" y="274">{L('Web console','Konsol web')}</text><text x="95" y="292" class="sm">GitHub Pages</text></g>
<g class="bx hl"><rect x="212" y="150" width="150" height="110" rx="10"/><text x="287" y="182">/ws/simple</text><text x="287" y="204" class="sm">Basic auth</text><text x="287" y="224" class="sm">{L('routes by operation','rute per operasi')}</text><text x="287" y="244" class="sm">HTTPS</text></g>
<g class="bx"><rect x="390" y="76" width="150" height="62" rx="10"/><text x="465" y="102">API - Get Pet</text><text x="465" y="122" class="sm">WSS GET · no input</text></g>
<g class="bx"><rect x="566" y="76" width="130" height="62" rx="10"/><text x="631" y="102">Decision</text><text x="631" y="122" class="sm">petId ~ ^[0-9]+$</text></g>
<g class="bx"><rect x="724" y="64" width="230" height="40" rx="10"/><text x="839" y="89" class="sm">{L('true → Message: mock Pet','true → Message: Pet mock')}</text></g>
<g class="bx err"><rect x="724" y="112" width="230" height="40" rx="10"/><text x="839" y="137" class="sm">{L('false → Message: ApiResponse 400','false → Message: ApiResponse 400')}</text></g>
<g class="bx"><rect x="390" y="270" width="150" height="62" rx="10"/><text x="465" y="296">API - Create Pet</text><text x="465" y="316" class="sm">WSS CREATE · JSON</text></g>
<g class="bx"><rect x="566" y="270" width="130" height="62" rx="10"/><text x="631" y="296">Decision</text><text x="631" y="316" class="sm">name ~ .*\\S.*</text></g>
<g class="bx"><rect x="724" y="258" width="230" height="40" rx="10"/><text x="839" y="283" class="sm">{L('true → Notify “Pet accepted” · echo','true → Notify “Pet accepted” · echo')}</text></g>
<g class="bx err"><rect x="724" y="306" width="230" height="40" rx="10"/><text x="839" y="331" class="sm">{L('false → Message: ApiResponse 405','false → Message: ApiResponse 405')}</text></g>
<g class="bx amb"><rect x="390" y="380" width="564" height="50" rx="10"/><text x="672" y="402">Return Documents → {L('HTTP response (JSON)','respons HTTP (JSON)')}</text><text x="672" y="420" class="sm">{L('each API process calls its [SUB] process; the sub-process holds the decision and messages','setiap proses API memanggil proses [SUB]; sub-proses berisi decision dan message')}</text></g>
<g class="ln"><path d="M164 117h20v60h28M164 197h48M164 277h20v-40h28" marker-end="url(#ar)"/>
<path d="M362 180h10v-73h18" marker-end="url(#ar)"/><path d="M362 230h10v71h18" marker-end="url(#ar)"/>
<path d="M540 107h26" marker-end="url(#ar)"/><path d="M540 301h26" marker-end="url(#ar)"/>
<path d="M696 100h10v-16h18M696 114h10v18h18" marker-end="url(#ar)"/><path d="M696 294h10v-16h18M696 308h10v18h18" marker-end="url(#ar)"/>
<path d="M465 332v48" marker-end="url(#ar)"/></g>
</svg><figcaption>{L('Two Web Services listeners mimic Swagger Petstore. All validation happens in the [SUB] processes, which can be tested on their own.','Dua listener Web Services meniru Swagger Petstore. Semua validasi terjadi di proses [SUB], yang dapat diuji secara terpisah.')}</figcaption></figure>"""


def code(text):
    return f'<pre class="cmd">{text}</pre>'


# ---------------------------------------------------------------- content
def content():
    return [
        section("summary", T("Executive summary", "Ringkasan eksekutif"),
            f'<p class="lead">{s(T("PetStore Mock API is a small Boomi Web Services project that mimics two operations of the public Swagger Petstore: <b>get a pet by ID</b> and <b>create a pet</b>. It gives front-end and integration teams a stable endpoint to build against before the real back end exists.", "PetStore Mock API adalah project Boomi Web Services kecil yang meniru dua operasi Swagger Petstore publik: <b>ambil pet berdasarkan ID</b> dan <b>buat pet</b>. Project ini memberi tim front-end dan integrasi endpoint yang stabil untuk dikembangkan sebelum back end sebenarnya tersedia."))}</p>'
            f'<p>{s(T("It is also a clean reference for the layering used in larger projects: a thin listener process, a sub-process with the business logic, a JSON profile for the contract, and Petstore-style error responses.", "Project ini juga menjadi referensi rapi untuk pola berlapis yang dipakai di project yang lebih besar: proses listener yang tipis, sub-proses berisi logika bisnis, profil JSON sebagai kontrak, dan respons error bergaya Petstore."))}</p>'
            + stats([("2", T("REST endpoints", "endpoint REST")), ("4", T("Boomi processes", "proses Boomi")),
                     ("1", T("JSON profile (Pet)", "profil JSON (Pet)")), ("2", T("validation rules", "aturan validasi"))])),

        section("background", T("Purpose", "Tujuan"),
            grid([card("bolt", T("Unblock client teams", "Membuka jalan tim klien"), T("Front-end and mobile developers get a working Petstore-compatible API on day one.", "Developer front-end dan mobile langsung mendapat API yang kompatibel dengan Petstore sejak hari pertama.")),
                  card("check", T("Contract testing", "Uji kontrak"), T("Predictable responses — including errors — make it easy to test client error handling.", "Respons yang dapat diprediksi — termasuk error — memudahkan pengujian penanganan error di klien.")),
                  card("layers", T("Reference pattern", "Pola referensi"), T("Shows the API → [SUB] layering, regex decisions and Message-shape responses in their simplest form.", "Menunjukkan pola API → [SUB], decision regex, dan respons Message-shape dalam bentuk paling sederhana."))])),

        section("value", T("What it demonstrates", "Yang didemonstrasikan"),
            grid([card("globe", T("Web Services Server", "Web Services Server"), T("Exposing Boomi processes as REST endpoints on the Atom Cloud shared web server.", "Mengekspos proses Boomi sebagai endpoint REST di shared web server Atom Cloud.")),
                  card("list", T("Query parameters as DPPs", "Parameter query sebagai DPP"), T("petId arrives as dynamic process property <code>query_petId</code>.", "petId diterima sebagai dynamic process property <code>query_petId</code>.")),
                  card("doc", T("JSON profile", "Profil JSON"), T("<code>j.PetStore.Pet</code> follows the Swagger Petstore Pet schema and is used for field access in decisions.", "<code>j.PetStore.Pet</code> mengikuti skema Pet Swagger Petstore dan dipakai untuk akses field di decision.")),
                  card("shield", T("Input validation", "Validasi input"), T("Regex decisions reject bad IDs and missing names before anything else runs.", "Decision regex menolak ID yang salah dan nama kosong sebelum langkah lain berjalan.")),
                  card("chat", T("Consistent errors", "Error yang konsisten"), T("Errors use the Petstore <code>ApiResponse</code> shape: code, type, message.", "Error memakai bentuk <code>ApiResponse</code> Petstore: code, type, message.")),
                  card("eye", T("Observability", "Observabilitas"), T("A Notify shape logs every accepted pet in the process log.", "Shape Notify mencatat setiap pet yang diterima di process log."))])),

        section("architecture", T("Solution architecture", "Arsitektur solusi"), architecture_svg()),

        section("api", T("API reference", "Referensi API"),
            f'<p>{s(T("Base URL: <code>https://&lt;atom-cloud&gt;/ws/simple</code> · Basic authentication with the Atom Cloud shared web server user.", "Base URL: <code>https://&lt;atom-cloud&gt;/ws/simple</code> · autentikasi Basic dengan user shared web server Atom Cloud."))}</p>'
            + table([T("Boomi endpoint", "Endpoint Boomi"), "Swagger Petstore", T("Process", "Proses"), T("Input → output", "Input → output")], [
                ['<span class="pill">GET</span> <code>/getPetstorePet?petId=</code>', "<code>GET /pet/{petId}</code>", "PetStore API - Get Pet", T("none → single data", "tidak ada → single data")],
                ['<span class="pill">POST</span> <code>/createPetstorePet</code>', "<code>POST /pet</code>", "PetStore API - Create Pet", T("single JSON → single data", "single JSON → single data")]])
            + f'<h3 style="margin-top:24px">{s(T("Pet schema (profile j.PetStore.Pet)", "Skema Pet (profil j.PetStore.Pet)"))}</h3>'
            + table([T("Field", "Field"), T("Type", "Tipe"), T("Description", "Keterangan")], [
                ["<code>id</code>", "integer (int64)", T("Pet ID", "ID pet")], ["<code>category</code>", "object {id, name}", T("Category", "Kategori")],
                ["<code>name</code>", "string", T("<b>Required</b> — must contain at least one non-space character", "<b>Wajib</b> — harus berisi minimal satu karakter selain spasi")],
                ["<code>photoUrls</code>", "array of string", T("Photo URLs", "URL foto")], ["<code>tags</code>", "array of {id, name}", T("Tags", "Tag")],
                ["<code>status</code>", "string", "available | pending | sold"]])
            + f'<h3 style="margin-top:24px">{s(T("Responses", "Respons"))}</h3>'
            + table([T("Case", "Kasus"), "HTTP", T("Body", "Body")], [
                [T("GET with a numeric petId", "GET dengan petId angka"), "200", T("Mock Pet “doggie” with the requested id", "Pet mock “doggie” dengan id yang diminta")],
                [T("GET with a missing or non-numeric petId", "GET dengan petId kosong atau bukan angka"), "200", '<code>{"code": 400, "type": "error", "message": "Invalid ID supplied"}</code>'],
                [T("POST with a name", "POST dengan nama"), "200", T("The request body, echoed back", "Body request, dikembalikan apa adanya")],
                [T("POST without a usable name", "POST tanpa nama yang valid"), "200", '<code>{"code": 405, "type": "error", "message": "Invalid input: pet name is required"}</code>']])
            + f'<div class="note" style="margin-top:16px">{s(T("<b>Note:</b> the processes do not set an HTTP status, so the listener answers <b>200</b> even for errors. Clients should check <code>type == &quot;error&quot;</code> in the body.", "<b>Catatan:</b> proses tidak mengatur status HTTP, sehingga listener menjawab <b>200</b> bahkan untuk error. Klien perlu mengecek <code>type == &quot;error&quot;</code> di body."))}</div>'
            + f'<h3 style="margin-top:24px">{s(T("Examples", "Contoh"))}</h3>'
            + code('curl -u "$BOOMI_USER:$BOOMI_TOKEN" \\\n  "https://&lt;atom-cloud&gt;/ws/simple/getPetstorePet?petId=123"')
            + code('{ "id": 123, "category": {"id": 1, "name": "Dogs"}, "name": "doggie",\n  "photoUrls": ["https://petstore.swagger.io/photos/doggie.jpg"],\n  "tags": [{"id": 1, "name": "friendly"}], "status": "available" }')
            + code('curl -u "$BOOMI_USER:$BOOMI_TOKEN" -X POST -H "Content-Type: application/json" \\\n  "https://&lt;atom-cloud&gt;/ws/simple/createPetstorePet" \\\n  -d \'{"id": 10, "name": "Bobby", "category": {"id": 1, "name": "Dogs"}, "status": "available"}\'')),

        section("design", T("Process design", "Desain proses"),
            table([T("Process", "Proses"), T("Shapes", "Shape"), T("Logic", "Logika")], [
                ["PetStore API - Get Pet", "Start (WSS Listen: PetStore WSS Get Pet) → Process Call → Return Documents", T("Receives GET, passes the request to the sub-process.", "Menerima GET, meneruskan request ke sub-proses.")],
                ["[SUB] PetStore Get Pet", "Start (passthrough) → Decision “Valid Pet ID?” → Message → Return Documents", T("<code>query_petId</code> matches <code>^[0-9]+$</code> → mock Pet with that id; otherwise ApiResponse 400.", "<code>query_petId</code> cocok dengan <code>^[0-9]+$</code> → Pet mock dengan id tersebut; selain itu ApiResponse 400.")],
                ["PetStore API - Create Pet", "Start (WSS Listen: PetStore WSS Create Pet) → Process Call → Return Documents", T("Receives the JSON body, passes it to the sub-process.", "Menerima body JSON, meneruskannya ke sub-proses.")],
                ["[SUB] PetStore Create Pet", "Start (passthrough) → Decision “Pet Name Provided?” → Notify / Message → Return Documents", T("<code>name</code> matches <code>.*\\S.*</code> → Notify “Pet accepted: {1}” and echo the body; otherwise ApiResponse 405.", "<code>name</code> cocok dengan <code>.*\\S.*</code> → Notify “Pet accepted: {1}” dan body dikembalikan; selain itu ApiResponse 405.")]])
            + f'<h3 style="margin-top:24px">{s(T("Design decisions", "Keputusan desain"))}</h3>'
            + ul([T("<b>Thin listener, testable logic.</b> The [SUB] processes use a passthrough start, so they can be run in Test Mode with a sample document — no HTTP call needed.", "<b>Listener tipis, logika mudah diuji.</b> Proses [SUB] memakai start passthrough, sehingga bisa dijalankan di Test Mode dengan dokumen contoh — tanpa perlu panggilan HTTP."),
                  T("<b>Regex decisions</b> keep validation explicit and visible on the canvas.", "<b>Decision regex</b> membuat validasi eksplisit dan terlihat di canvas."),
                  T("<b>Message shapes</b> produce the exact Petstore JSON, so clients written for Swagger Petstore work unchanged.", "<b>Message shape</b> menghasilkan JSON Petstore yang persis sama, sehingga klien yang dibuat untuk Swagger Petstore bisa langsung dipakai."),
                  T("<b>No persistence</b> on purpose: the mock is stateless and safe to call repeatedly.", "<b>Tanpa penyimpanan</b> secara sengaja: mock bersifat stateless dan aman dipanggil berulang kali.")])),

        section("testing", T("Test cases", "Kasus uji"),
            table(["#", T("Request", "Request"), T("Expected result", "Hasil yang diharapkan")], [
                ["1", "GET petId=123", T("Pet doggie, id 123", "Pet doggie, id 123")],
                ["2", "GET petId=abc", "ApiResponse 400"], ["3", "GET petId=-1", T("ApiResponse 400 (minus sign is not a digit)", "ApiResponse 400 (tanda minus bukan digit)")],
                ["4", T("GET without petId", "GET tanpa petId"), "ApiResponse 400"],
                ["5", T("POST with name “Bobby”", "POST dengan nama “Bobby”"), T("Body echoed; “Pet accepted” in the process log", "Body dikembalikan; “Pet accepted” di process log")],
                ["6", T("POST without name", "POST tanpa nama"), "ApiResponse 405"], ["7", T("POST with name of only spaces", "POST dengan nama hanya spasi"), "ApiResponse 405"],
                ["8", T("POST with empty body", "POST dengan body kosong"), "ApiResponse 405"]])
            + f'<p style="margin-top:12px">{s(T("All cases can be run interactively in the web console.", "Semua kasus dapat dijalankan secara interaktif di konsol web."))}</p>'),

        section("portal", T("Web console mockup", "Mockup konsol web"),
            f'<p class="lead">{s(T("A static console reproduces both endpoints in the browser with the same logic as the Boomi processes.", "Konsol statis menjalankan kedua endpoint di browser dengan logika yang sama seperti proses Boomi."))}</p>'
            + grid([card("bolt", "API Console", T("Build a GET or POST request, use presets for every test case, and read the body, headers, process log and cURL.", "Susun request GET atau POST, pakai preset untuk setiap kasus uji, dan baca body, header, process log, serta cURL.")),
                    card("layers", T("Execution path", "Jalur eksekusi"), T("The process diagram highlights the branch each request takes.", "Diagram proses menyorot cabang yang dilalui setiap request.")),
                    card("users", "Pet Shop Demo", T("A tiny storefront that adds pets via POST and fetches them via GET.", "Toko kecil yang menambah pet lewat POST dan mengambilnya lewat GET.")),
                    card("doc", T("API reference", "Referensi API"), T("Endpoints, schema, responses and cURL examples.", "Endpoint, skema, respons, dan contoh cURL.")),
                    card("list", T("Request history", "Riwayat request"), T("Every request in the session; click to replay.", "Setiap request dalam sesi; klik untuk menjalankan ulang.")),
                    card("globe", T("Runs anywhere", "Jalan di mana saja"), T("Plain HTML, CSS and JavaScript on GitHub Pages; light and dark themes.", "HTML, CSS, dan JavaScript biasa di GitHub Pages; tema terang dan gelap."))])
            + f'<p style="margin-top:16px"><a class="btn" href="{PORTAL}">{s(T("Open the console →", "Buka konsol →"))}</a></p>'),

        section("components", T("Components", "Komponen"),
            table([T("Type", "Jenis"), T("Component", "Komponen"), T("Purpose", "Fungsi")], [
                ["Process (WSS)", "PetStore API - Get Pet", T("Listener for GET getPetstorePet", "Listener untuk GET getPetstorePet")],
                ["Process (WSS)", "PetStore API - Create Pet", T("Listener for POST createPetstorePet", "Listener untuk POST createPetstorePet")],
                ["Sub-process", "[SUB] PetStore Get Pet", T("Validate petId, build the mock Pet", "Validasi petId, bangun Pet mock")],
                ["Sub-process", "[SUB] PetStore Create Pet", T("Validate name, log and echo", "Validasi nama, catat log, dan kembalikan body")],
                ["Connector operation", "PetStore WSS Get Pet", "Web Services Server · GET · input none · output single data"],
                ["Connector operation", "PetStore WSS Create Pet", "Web Services Server · CREATE · input single JSON · output single data"],
                ["JSON profile", "j.PetStore.Pet", T("Swagger Petstore Pet schema", "Skema Pet Swagger Petstore")]])
            + f'<h3 style="margin-top:24px">{s(T("Repository layout", "Struktur repositori"))}</h3>'
            + ul([T("<code>active-development/</code> — Boomi component XML (processes, operations, profile).", "<code>active-development/</code> — XML komponen Boomi (proses, operasi, profil)."),
                  T("<code>portal/</code> — static web console mockup.", "<code>portal/</code> — mockup konsol web statis."),
                  T("<code>docs/</code> — this documentation (source in <code>docs/_source/</code>).", "<code>docs/</code> — dokumentasi ini (sumber di <code>docs/_source/</code>)."),
                  T("<code>.env.example</code> — the settings needed to push and deploy; copy it to <code>.env</code> (never committed).", "<code>.env.example</code> — pengaturan yang diperlukan untuk push dan deploy; salin ke <code>.env</code> (tidak pernah di-commit).")])),

        section("operate", T("Setup & deployment", "Penyiapan & deployment"),
            '<ol class="clean">' + "".join(f"<li>{s(x)}</li>" for x in [
                T("Copy <code>.env.example</code> to <code>.env</code> and fill in the Boomi account, API token, target folder, environment and test atom.", "Salin <code>.env.example</code> ke <code>.env</code> lalu isi akun Boomi, API token, folder tujuan, environment, dan test atom."),
                T("Push the components in <code>active-development/</code> to the platform folder.", "Push komponen di <code>active-development/</code> ke folder platform."),
                T("Deploy <b>PetStore API - Get Pet</b> and <b>PetStore API - Create Pet</b> to an Atom Cloud environment with the shared web server enabled.", "Deploy <b>PetStore API - Get Pet</b> dan <b>PetStore API - Create Pet</b> ke environment Atom Cloud dengan shared web server aktif."),
                T("Call the endpoints with the shared web server user (Basic auth) and run the test cases above.", "Panggil endpoint dengan user shared web server (Basic auth) dan jalankan kasus uji di atas.")]) + "</ol>"),

        section("next", T("Limitations & next steps", "Keterbatasan & langkah berikutnya"),
            grid([card("doc", T("Static GET data", "Data GET statis"), T("GET always returns “doggie”; created pets are not stored.", "GET selalu mengembalikan “doggie”; pet yang dibuat tidak disimpan.")),
                  card("shield", T("HTTP status codes", "Kode status HTTP"), T("Set the HTTP status (400/405) through the response headers so clients don’t need to inspect the body.", "Atur status HTTP (400/405) lewat header respons agar klien tidak perlu memeriksa body."), True),
                  card("layers", T("Persistence", "Penyimpanan"), T("Store pets in a database or Disk V2 and look them up by id.", "Simpan pet di database atau Disk V2 dan cari berdasarkan id.")),
                  card("list", T("More operations", "Operasi tambahan"), T("Add PUT /pet, DELETE /pet/{petId} and findByStatus.", "Tambahkan PUT /pet, DELETE /pet/{petId}, dan findByStatus.")),
                  card("globe", T("API Management", "API Management"), T("Publish through a Boomi API Service component with an OpenAPI spec.", "Publikasikan lewat komponen Boomi API Service dengan spesifikasi OpenAPI.")),
                  card("check", T("Schema validation", "Validasi skema"), T("Validate status against available | pending | sold and the types of every field.", "Validasi status terhadap available | pending | sold serta tipe setiap field."))])),
    ]


# ---------------------------------------------------------------- page template
CSS = """
:root{--bg:#F8F6F3;--surface:#FFFFFF;--surface2:#F2EEE9;--ink:#241B13;--muted:#6E6257;--line:#E4DDD4;
 --navy:#2A1E14;--acc:#D9631E;--acc-ink:#B04A0F;--acc-tint:#FBEADF;--amber:#2D6CB5;--amber-tint:#E4EEFA;--hero:#241B13;--hero-ink:#EBD9C8;--eyebrow:#FFB27A;
 --shadow:0 1px 2px rgba(36,27,19,.06),0 6px 20px rgba(36,27,19,.06)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#14100C;--surface:#1E1812;--surface2:#29211A;--ink:#F3ECE4;--muted:#B3A595;
 --line:#3A2F25;--navy:#F6E3D2;--acc:#F07A33;--acc-ink:#FFA463;--acc-tint:#3A2516;--amber:#7FB2F0;--amber-tint:#132E52;--hero:#0F0C09;--shadow:none}}
:root[data-theme="dark"]{--bg:#14100C;--surface:#1E1812;--surface2:#29211A;--ink:#F3ECE4;--muted:#B3A595;--line:#3A2F25;--navy:#F6E3D2;
 --acc:#F07A33;--acc-ink:#FFA463;--acc-tint:#3A2516;--amber:#7FB2F0;--amber-tint:#132E52;--hero:#0F0C09;--shadow:none}
th{background:#2A1E14!important}
pre.cmd{background:var(--surface2);border:1px solid var(--line);border-radius:10px;padding:12px 14px;overflow:auto;font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;margin:8px 0}
"""
CSS_COMMON = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Segoe UI",Calibri,Arial,sans-serif}
a{color:var(--acc-ink)}code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.88em;background:var(--surface2);padding:1px 5px;border-radius:5px}
.wrap{max-width:1120px;margin:0 auto;padding:0 16px}
header.hero{background:var(--hero);color:#fff;padding:56px 0 44px}
.hero .eyebrow{color:var(--eyebrow);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:13px}
.hero h1{font:700 clamp(32px,5vw,52px)/1.1 Cambria,Georgia,serif;margin:10px 0 12px}
.hero p{color:var(--hero-ink);max-width:760px;margin:0;font-size:18px}
.hero .meta{margin-top:18px;color:var(--hero-ink);opacity:.8;font-size:14px}
nav.toc{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav.toc .wrap{display:flex;gap:6px;overflow-x:auto;padding-top:10px;padding-bottom:10px;align-items:center}
nav.toc a{white-space:nowrap;text-decoration:none;color:var(--muted);font-size:14px;padding:6px 10px;border-radius:999px}
nav.toc a:hover{background:var(--surface2);color:var(--ink)}
nav.toc .spacer{flex:1}
.tgl{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;cursor:pointer;white-space:nowrap;text-decoration:none}
a.tgl{color:var(--ink)!important}
section{padding:44px 0 8px;scroll-margin-top:56px}
h2{font:700 30px/1.2 Cambria,Georgia,serif;color:var(--navy);margin:0 0 14px}
h3{font-size:18px;margin:0 0 6px;color:var(--ink)}
.lead{font-size:18px;color:var(--muted);max-width:820px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px}
.stat{background:var(--acc-tint);border-radius:14px;padding:18px;text-align:center}
.stat b{display:block;font:700 34px/1.1 Cambria,Georgia,serif;color:var(--acc-ink)}
.stat span{color:var(--muted);font-size:14px}
.grid{display:grid;gap:14px}.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:var(--shadow)}
.card p{margin:0;color:var(--muted)}
.ihead{display:flex;gap:12px;align-items:center;margin-bottom:8px}
.ico{width:40px;height:40px;flex:none;padding:9px;border-radius:50%;background:var(--acc);stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.amber .ico{background:var(--amber)}
figure{margin:18px 0;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:10px;overflow:auto}
figure svg{display:block;width:100%;height:auto;min-width:720px;font-family:"Segoe UI",Calibri,Arial,sans-serif}
figcaption{color:var(--muted);font-size:14px;text-align:center;padding:6px}
svg .lane rect{fill:var(--surface2);stroke:var(--line)}svg .lt{fill:var(--muted);font-size:13px;font-weight:700;text-anchor:middle;letter-spacing:.04em;text-transform:uppercase}
svg .bx rect{fill:var(--surface);stroke:var(--line);stroke-width:1.5}svg .bx text{fill:var(--ink);font-size:14px;font-weight:600;text-anchor:middle}
svg .bx text.sm{fill:var(--muted);font-size:11.5px;font-weight:400}
svg .bx.hl rect{stroke:var(--acc);stroke-width:2;fill:var(--acc-tint)}svg .bx.amb rect{stroke:var(--amber);stroke-width:2;fill:var(--amber-tint)}
svg .bx.err rect{stroke:#D0505D;stroke-width:1.5;stroke-dasharray:5 4}
svg .ln path{fill:none;stroke:var(--acc);stroke-width:2}svg .mk{fill:var(--acc)}
ul.clean,ol.clean{padding-left:22px;margin:10px 0}ul.clean li,ol.clean li{margin:6px 0}
.note{background:var(--amber-tint);border-radius:12px;padding:14px 16px;color:var(--ink)}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:15px}
th{background:var(--navy-th,#141B3C);color:#fff;text-align:left;padding:10px 14px;font-weight:600}
td{padding:10px 14px;border-top:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:var(--surface2)}
.pill{display:inline-block;background:var(--acc-tint);color:var(--acc-ink);font-weight:700;border-radius:999px;padding:2px 10px;font-size:13px}
.q{font-weight:700;color:var(--navy);margin:0 0 6px!important;font-size:17px}
.starter{display:flex;gap:16px;align-items:flex-start}.starter p{margin:0 0 6px}
.snum{flex:none;width:40px;height:40px;border-radius:50%;background:var(--acc);color:#fff;font:700 18px/40px Cambria,Georgia,serif;text-align:center}
.snum.amber{background:var(--amber)}
.outcome{color:var(--acc-ink)!important;font-weight:600;margin-top:8px!important}
.uc h3{font-size:19px;margin-bottom:6px}.uc .meta{font-size:14px;margin:0 0 10px}
.ba{display:grid;grid-template-columns:1fr 1fr;gap:12px}.ba div{border-radius:12px;padding:12px 14px;font-size:15px;color:var(--ink)}
.ba span{display:block;font-weight:700;font-size:12px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}
.before{background:var(--surface2)}.before span{color:var(--muted)}.after{background:var(--acc-tint)}.after span{color:var(--acc-ink)}
a.btn{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;font-weight:600;padding:10px 18px;border-radius:10px}
footer{padding:40px 0 60px;color:var(--muted);font-size:14px;border-top:1px solid var(--line);margin-top:40px}
body.present nav.toc{display:none}
body.present section,body.present header.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center}
body.present section{border-top:1px solid var(--line)}
@media (max-width:820px){.stats{grid-template-columns:repeat(2,1fr)}.g2,.g3{grid-template-columns:1fr}.ba{grid-template-columns:1fr}h2{font-size:26px}}
@media print{nav.toc,.tgl{display:none}section{break-inside:avoid}body{background:#fff}}
"""
JS = """<script>
(function(){var r=document.documentElement,k='doc-theme';
function set(t){if(t)r.setAttribute('data-theme',t);else r.removeAttribute('data-theme');try{localStorage.setItem(k,t)}catch(e){}}
try{var t=localStorage.getItem(k);if(t)r.setAttribute('data-theme',t)}catch(e){}
document.getElementById('theme').onclick=function(){var c=r.getAttribute('data-theme');set(c==='dark'?'light':c==='light'?'':'dark')};
document.getElementById('present').onclick=function(){document.body.classList.toggle('present')};
document.addEventListener('keydown',function(e){if(e.key==='f'&&document.body.classList.contains('present')){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()}});
})();
</script>"""

TOC = [("summary", T("Summary", "Ringkasan")), ("background", T("Purpose", "Tujuan")), ("value", T("Demonstrates", "Demonstrasi")),
       ("architecture", T("Architecture", "Arsitektur")), ("api", "API"), ("design", T("Process design", "Desain proses")),
       ("testing", T("Tests", "Uji")), ("portal", T("Console", "Konsol")), ("components", T("Components", "Komponen")),
       ("operate", T("Setup", "Penyiapan")), ("next", T("Next steps", "Selanjutnya"))]


def page():
    other = "id" if LANG == "en" else "en"
    other_href = ("../" + LINK["en"]) if LANG == "id" else LINK["id"]
    toc = "".join(f'<a href="#{i}">{s(t)}</a>' for i, t in TOC)
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PetStore Mock API</title>
<meta name="description" content="{s(T("Solution documentation for the Boomi PetStore Mock API.", "Dokumentasi solusi PetStore Mock API berbasis Boomi."))}">
<style>{CSS}{CSS_COMMON}</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="eyebrow">{s(T("Solution Documentation &amp; Developer Guide", "Dokumentasi Solusi &amp; Panduan Developer"))}</div>
  <h1>PetStore Mock API</h1>
  <p>{s(T("Swagger Petstore–compatible mock endpoints built with Boomi Web Services", "Endpoint mock yang kompatibel dengan Swagger Petstore, dibangun dengan Boomi Web Services"))}</p>
  <div class="meta">{s(T("Version 1.0 · November 2026 · For integration engineers and front-end developers", "Versi 1.0 · November 2026 · Untuk integration engineer dan developer front-end"))}</div>
</div></header>
<nav class="toc" aria-label="Contents"><div class="wrap">{toc}<span class="spacer"></span>
  <a class="tgl" href="{other_href}" hreflang="{other}">{"Bahasa Indonesia" if LANG == "en" else "English"}</a>
  <button class="tgl" id="present" title="One section per screen (F = full screen)">{s(T("Presentation mode", "Mode presentasi"))}</button>
  <button class="tgl" id="theme">{s(T("Theme", "Tema"))}</button>
</div></nav>
<main class="wrap">
{"".join(content())}
</main>
<footer><div class="wrap">PetStore Mock API · {s(T("Based on the public Swagger Petstore sample.", "Berdasarkan contoh publik Swagger Petstore."))} · <a href="{REPO}">GitHub</a> · <a href="{PORTAL}">{s(T("Console", "Konsol"))}</a></div></footer>
{JS}
</body>
</html>
"""


if __name__ == "__main__":
    for LANG in ("en", "id"):
        OUT[LANG].parent.mkdir(parents=True, exist_ok=True)
        OUT[LANG].write_text(page(), encoding="utf-8")
        print("wrote", OUT[LANG].relative_to(ROOT))
