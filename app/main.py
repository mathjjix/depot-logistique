<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Gestion de dépôt logistique</title>
    <style>
        :root {
            --bg: #0f172a;
            --panel: #111827;
            --panel-soft: #1f2937;
            --primary: #22c55e;
            --accent: #38bdf8;
            --warning: #f59e0b;
            --danger: #ef4444;
            --text: #e5e7eb;
            --muted: #94a3b8;
            --border: #334155;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            background: linear-gradient(135deg, #020817, #0f172a);
            color: var(--text);
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 24px;
        }
        h1, h2, h3 { margin-top: 0; }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .card {
            background: rgba(17, 24, 39, 0.96);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 8px 16px rgba(15, 23, 42, 0.3);
        }
        .card .label {
            color: var(--muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .card .value {
            margin-top: 8px;
            font-size: 32px;
            font-weight: bold;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .panel {
            background: rgba(17, 24, 39, 0.96);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
        }
        form {
            display: grid;
            gap: 10px;
        }
        label {
            display: grid;
            gap: 6px;
            color: var(--muted);
            font-size: 14px;
        }
        input, select, textarea, button {
            border-radius: 8px;
            border: 1px solid var(--border);
            padding: 10px 12px;
            background: var(--panel-soft);
            color: var(--text);
        }
        button {
            cursor: pointer;
            background: var(--primary);
            color: #03130a;
            border: none;
            font-weight: bold;
        }
        .secondary {
            background: var(--accent);
            color: #031826;
        }
        .danger {
            background: var(--danger);
            color: white;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
        }
        th, td {
            border-bottom: 1px solid var(--border);
            padding: 10px 8px;
            text-align: left;
            font-size: 14px;
        }
        th {
            color: var(--muted);
        }
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 12px;
            text-transform: uppercase;
            font-weight: bold;
        }
        .free { background: rgba(34, 197, 94, 0.2); color: #86efac; }
        .occupied_our { background: rgba(59, 130, 246, 0.2); color: #93c5fd; }
        .occupied_customer { background: rgba(168, 85, 247, 0.2); color: #d8b4fe; }
        .shared { background: rgba(245, 158, 11, 0.2); color: #fcd34d; }
        .reserved { background: rgba(239, 68, 68, 0.2); color: #fca5a5; }
        .muted { color: var(--muted); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <div class="muted">Gestion logistique</div>
                <h1>Dépôt intelligent</h1>
            </div>
            <button id="refreshBtn" class="secondary">Actualiser</button>
        </div>

        <div class="cards" id="dashboardCards"></div>

        <div class="grid">
            <div class="panel">
                <h2>Créer un dépôt</h2>
                <form id="depotForm">
                    <label>Nom<input name="name" value="Dépôt principal" /></label>
                    <label>Localisation<input name="location" value="Zone Nord" /></label>
                    <label>Nombre d'étages<input type="number" name="floors_count" value="3" /></label>
                    <label>Nombre de palettiers<input type="number" name="racks_count" value="4" /></label>
                    <label>Nombre de palettes par étage<input type="number" name="slots_per_floor" value="10" /></label>
                    <label>Largeur emplacement<input type="number" step="0.1" name="slot_width" value="1.2" /></label>
                    <label>Profondeur emplacement<input type="number" step="0.1" name="slot_depth" value="1.0" /></label>
                    <label>Description<textarea name="description">Dépôt principal avec gestion de palettes et zones de carton.</textarea></label>
                    <button type="submit">Créer le dépôt</button>
                </form>
            </div>

            <div class="panel">
                <h2>Créer un secteur</h2>
                <form id="sectionForm">
                    <label>Nom du secteur<input name="name" value="Secteur Carton B" /></label>
                    <label>Type<select name="section_type">
                        <option value="carton">Carton</option>
                        <option value="shared">Partagé</option>
                        <option value="cold">Froid</option>
                        <option value="fragile">Fragile</option>
                    </select></label>
                    <label>Actif<select name="is_active"><option value="true">Oui</option><option value="false">Non</option></select></label>
                    <label>Description<textarea name="description">Zone dédiée au carton et aux pièces fragiles.</textarea></label>
                    <button type="submit" class="secondary">Ajouter le secteur</button>
                </form>
            </div>

            <div class="panel">
                <h2>Ajouter un client</h2>
                <form id="customerForm">
                    <label>Nom<input name="name" value="Client C" /></label>
                    <label>Entreprise<input name="company_name" value="Gamma Supply" /></label>
                    <label>Contact<input name="contact" value="+33 6 00 00 00 03" /></label>
                    <label>Partenaire<select name="is_partner"><option value="false">Non</option><option value="true">Oui</option></select></label>
                    <label>Notes<textarea name="notes">Client externe avec stockage de cartons.</textarea></label>
                    <button type="submit">Ajouter le client</button>
                </form>
            </div>

            <div class="panel">
                <h2>Ajouter un paletier</h2>
                <form id="rackForm">
                    <label>Nom du paletier<input name="name" value="Paletier B2" /></label>
                    <label>Nombre d'étages<input type="number" name="floors_count" value="3" /></label>
                    <label>Nombre de palettes par étage<input type="number" name="slots_per_floor" value="8" /></label>
                    <label>Largeur<input type="number" step="0.1" name="width" value="1.2" /></label>
                    <label>Profondeur<input type="number" step="0.1" name="depth" value="1.0" /></label>
                    <label>Statut<select name="status"><option value="active">Actif</option><option value="maintenance">Maintenance</option></select></label>
                    <button type="submit" class="secondary">Créer le paletier</button>
                </form>
            </div>
        </div>

        <div class="grid">
            <div class="panel">
                <h2>Créer une palette</h2>
                <form id="palletForm">
                    <label>Code palette<input name="code" value="PAL-001" /></label>
                    <label>Poids<input type="number" step="0.1" name="weight" value="250" /></label>
                    <label>Volume<input type="number" step="0.1" name="volume" value="1.8" /></label>
                    <label>Client<select id="customerSelect"></select></label>
                    <label>Emplacement<select id="slotSelect"></select></label>
                    <label>Partagé<select name="is_shared"><option value="false">Non</option><option value="true">Oui</option></select></label>
                    <label>Notes<textarea name="notes">Palette de cartons pour le client sélectionné.</textarea></label>
                    <button type="submit">Stocker la palette</button>
                </form>
            </div>

            <div class="panel">
                <h2>État des emplacements</h2>
                <div id="slotsList"></div>
            </div>
        </div>

        <div class="panel">
            <h2>Liste des clients</h2>
            <div id="customersList"></div>
        </div>
    </div>

    <script>
        const apiBase = '/api';

        async function fetchJson(url, options = {}) {
            const response = await fetch(url, {
                headers: { 'Content-Type': 'application/json' },
                ...options
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Erreur API');
            }
            return data;
        }

        function renderDashboard(data) {
            const cards = [
                ['Dépôts', data.depots_count],
                ['Palettiers', data.racks_count],
                ['Secteurs', data.sections_count],
                ['Clients', data.customers_count],
                ['Palettes', data.pallets_count],
                ['Libres', data.free_slots],
                ['Occupés', data.occupied_our],
                ['Partagés', data.shared_slots],
            ];
            document.getElementById('dashboardCards').innerHTML = cards.map(([label, value]) => `
                <div class="card">
                    <div class="label">${label}</div>
                    <div class="value">${value}</div>
                </div>
            `).join('');
        }

        function renderCustomers(customers) {
            const list = document.getElementById('customersList');
            list.innerHTML = customers.length ? `
                <table>
                    <thead>
                        <tr><th>Nom</th><th>Entreprise</th><th>Contact</th><th>Partenaire</th></tr>
                    </thead>
                    <tbody>
                        ${customers.map(c => `
                            <tr>
                                <td>${c.name}</td>
                                <td>${c.company_name || '-'}</td>
                                <td>${c.contact || '-'}</td>
                                <td>${c.is_partner ? 'Oui' : 'Non'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            ` : '<p class="muted">Aucun client pour le moment.</p>';
        }

        function renderSlots(slots) {
            const list = document.getElementById('slotsList');
            list.innerHTML = slots.length ? `
                <table>
                    <thead>
                        <tr><th>Paletier</th><th>Étage</th><th>Emplacement</th><th>Statut</th></tr>
                    </thead>
                    <tbody>
                        ${slots.map(s => `
                            <tr>
                                <td>${s.rack_name}</td>
                                <td>${s.floor_number}</td>
                                <td>${s.slot_number}</td>
                                <td><span class="status ${s.status}">${s.status}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            ` : '<p class="muted">Aucun emplacement disponible.</p>';
        }

        function fillSelects(customers, slots) {
            const customerSelect = document.getElementById('customerSelect');
            const slotSelect = document.getElementById('slotSelect');

            customerSelect.innerHTML = customers.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
            slotSelect.innerHTML = slots.filter(s => s.status === 'free').map(s => `<option value="${s.id}">${s.rack_name} - Étage ${s.floor_number} - ${s.slot_number}</option>`).join('');
        }

        async function loadData() {
            try {
                const summary = await fetchJson(`${apiBase}/summary`);
                const customers = await fetchJson(`${apiBase}/customers`);
                const slots = await fetchJson(`${apiBase}/slots`);

                renderDashboard(summary);
                renderCustomers(customers);
                renderSlots(slots);
                fillSelects(customers, slots);
            } catch (error) {
                console.error(error);
                alert(error.message);
            }
        }

        document.getElementById('refreshBtn').addEventListener('click', loadData);

        document.getElementById('depotForm').addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = Object.fromEntries(new FormData(event.target).entries());
            const payload = {
                ...formData,
                floors_count: Number(formData.floors_count),
                racks_count: Number(formData.racks_count),
                slots_per_floor: Number(formData.slots_per_floor),
                slot_width: Number(formData.slot_width),
                slot_depth: Number(formData.slot_depth),
            };
            await fetchJson(`${apiBase}/depots`, { method: 'POST', body: JSON.stringify(payload) });
            loadData();
            event.target.reset();
        });

        document.getElementById('sectionForm').addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = Object.fromEntries(new FormData(event.target).entries());
            await fetchJson(`${apiBase}/sections`, {
                method: 'POST',
                body: JSON.stringify({
                    ...formData,
                    is_active: formData.is_active === 'true',
                })
            });
            loadData();
        });

        document.getElementById('customerForm').addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = Object.fromEntries(new FormData(event.target).entries());
            await fetchJson(`${apiBase}/customers`, {
                method: 'POST',
                body: JSON.stringify({
                    ...formData,
                    is_partner: formData.is_partner === 'true'
                })
            });
            loadData();
        });

        document.getElementById('rackForm').addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = Object.fromEntries(new FormData(event.target).entries());
            await fetchJson(`${apiBase}/racks`, {
                method: 'POST',
                body: JSON.stringify({
                    ...formData,
                    floors_count: Number(formData.floors_count),
                    slots_per_floor: Number(formData.slots_per_floor),
                    width: Number(formData.width),
                    depth: Number(formData.depth),
                    is_active: true,
                })
            });
            loadData();
        });

        document.getElementById('palletForm').addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = Object.fromEntries(new FormData(event.target).entries());
            const payload = {
                code: formData.code,
                weight: Number(formData.weight),
                volume: Number(formData.volume),
                notes: formData.notes,
                is_shared: formData.is_shared === 'true',
                customer_id: Number(formData.customerSelect),
                slot_id: Number(formData.slotSelect),
            };
            await fetchJson(`${apiBase}/pallets`, {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            loadData();
        });

        loadData();
    </script>
</body>
</html>
