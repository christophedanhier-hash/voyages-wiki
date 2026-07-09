# 📊 Monitoring — Coûts & Activité

<div id="monitoring-live"><em>Chargement des données...</em></div>

<script>
(async function(){
  try {
    const r = await fetch('/api/metrics');
    const m = await r.json();
    const voyages = m.voyages || [];
    const bavi = m.bavi || {};
    const sylvia = (bavi.bureaux || []).find(b => b.id === 'sylvia') || {};

    let html = '';

    // Résumé
    html += `<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px">
      <div style="background:var(--md-code-bg);border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;padding:10px 16px;text-align:center;flex:1;min-width:100px">
        <div style="font-size:1.4rem;font-weight:700;color:#06b6d4">${voyages.length||0}</div>
        <div style="font-size:.65rem;color:var(--md-default-fg-color--light)">Roadbooks</div>
      </div>
      <div style="background:var(--md-code-bg);border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;padding:10px 16px;text-align:center;flex:1;min-width:100px">
        <div style="font-size:1.4rem;font-weight:700">${sylvia.analyses||0}</div>
        <div style="font-size:.65rem;color:var(--md-default-fg-color--light)">Analyses Sylvia</div>
      </div>
    </div>`;

    // Roadbooks table
    if(voyages.length){
      html += '<h3>🗺️ Roadbooks</h3><table><thead><tr><th>Roadbook</th><th style="text-align:center">Statut</th></tr></thead><tbody>';
      voyages.forEach(v => {
        html += `<tr><td>${v.name||v}</td><td style="text-align:center">📋 En préparation</td></tr>`;
      });
      html += '</tbody></table>';
    }

    // Coûts
    html += `<h3 style="margin-top:16px">💳 Tarification</h3>`;
    html += `<table><thead><tr><th>Qui</th><th>Abonnement</th><th>Documents</th></tr></thead>
      <tbody>
        <tr><td>🧑‍✈️ Christophe</td><td>0 €</td><td>Tokens IN/OUT réels</td></tr>
        <tr><td>👥 Amis</td><td>12 €/an</td><td>Tokens + 2,50 €/document</td></tr>
      </tbody></table>`;

    html += `<p style="font-size:.75rem;color:var(--md-default-fg-color--light);margin-top:16px">
      🪙 Tarif DeepSeek Flash : $0,15/1M tokens IN · $0,60/1M tokens OUT<br>
      📅 Abonnement ami : démarre le 1er du mois du premier dossier<br>
      💬 Chat seul = 0 € · Seuls les documents produits sont facturés
    </p>`;

    document.getElementById('monitoring-live').innerHTML = html;
  } catch(e) {
    document.getElementById('monitoring-live').innerHTML = '<em>Données non disponibles</em>';
  }
})();
</script>
