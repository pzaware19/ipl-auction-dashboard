(function () {
  const data = window.DASHBOARD_DATA;
  const teams = data.scenario.teams;
  const teamMap = new Map(data.teams.teams_2026.map((team) => [team.code, team]));
  const roleMarket = data.auction.role_market;
  const STORAGE_KEY = "ipl-auction-war-room-shortlists";
  const BUCKETS = ["priority", "fallback", "value", "watchlist"];
  const els = {
    team: document.getElementById("war-room-team"),
    role: document.getElementById("war-room-role"),
    bucket: document.getElementById("war-room-bucket"),
    player: document.getElementById("war-room-player"),
    playerOptions: document.getElementById("war-room-player-options"),
    add: document.getElementById("war-room-add"),
    cards: document.getElementById("war-room-cards"),
    targets: document.getElementById("war-room-targets"),
    shortlists: document.getElementById("war-room-shortlists"),
    roleGaps: document.getElementById("war-room-role-gaps"),
    rivals: document.getElementById("war-room-rivals"),
  };

  function formatDecimal(value, digits = 2) {
    return Number(value || 0).toFixed(digits);
  }

  function titleize(value) {
    return String(value || "")
      .replaceAll("_", " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  function setOptions(select, values, formatter) {
    select.innerHTML = "";
    values.forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = formatter ? formatter(value) : value;
      select.appendChild(option);
    });
  }

  function renderTable(table, columns, rows) {
    const head = columns.map((column) => `<th>${column.label}</th>`).join("");
    const body = rows
      .map(
        (row) =>
          `<tr>${columns
            .map((column) => `<td>${column.render ? column.render(row[column.key], row) : row[column.key] ?? ""}</td>`)
            .join("")}</tr>`
      )
      .join("");
    table.innerHTML = `<thead><tr>${head}</tr></thead><tbody>${body}</tbody>`;
  }

  function shortlistState() {
    try {
      return JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (error) {
      return {};
    }
  }

  function saveShortlists(state) {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function currentShortlists() {
    const state = shortlistState();
    const teamCode = els.team.value;
    const current = state[teamCode] || {};
    BUCKETS.forEach((bucket) => {
      current[bucket] = current[bucket] || [];
    });
    state[teamCode] = current;
    saveShortlists(state);
    return current;
  }

  function addToBucket(playerName, bucket) {
    if (!playerName || !bucket) return;
    const state = shortlistState();
    const teamCode = els.team.value;
    const current = state[teamCode] || Object.fromEntries(BUCKETS.map((key) => [key, []]));
    BUCKETS.forEach((key) => {
      current[key] = (current[key] || []).filter((name) => name !== playerName);
    });
    current[bucket].unshift(playerName);
    current[bucket] = [...new Set(current[bucket])].slice(0, 10);
    state[teamCode] = current;
    saveShortlists(state);
    renderShortlists();
  }

  function removeFromBucket(playerName, bucket) {
    const state = shortlistState();
    const teamCode = els.team.value;
    const current = state[teamCode] || {};
    current[bucket] = (current[bucket] || []).filter((name) => name !== playerName);
    state[teamCode] = current;
    saveShortlists(state);
    renderShortlists();
  }

  function buildRoleRows() {
    const teamCode = els.team.value;
    const roleFocus = els.role.value;
    const team = teamMap.get(teamCode);
    const mcShareMap = teams[teamCode].mc_share_map || {};
    const roleWeights = teams[teamCode].role_needs || {};
    const roles =
      roleFocus === "all"
        ? Object.keys(roleMarket.options_by_role)
        : [roleFocus];

    return roles
      .flatMap((role) =>
        (roleMarket.options_by_role[role] || []).map((row) => {
          const needWeight = Number(roleWeights[role] || 0);
          const teamShare = Number(mcShareMap[row.player_name] || 0);
          const score = row.value_surplus + needWeight * 2.4 + teamShare * 8 - row.expected_price * 0.04;
          return {
            ...row,
            team_share: teamShare,
            need_weight: needWeight,
            war_room_score: score,
            fit_note:
              needWeight >= 1.2
                ? "core role gap"
                : needWeight >= 0.8
                  ? "secondary role need"
                  : "depth / optional fit",
          };
        })
      )
      .sort((a, b) => b.war_room_score - a.war_room_score || b.value_surplus - a.value_surplus)
      .slice(0, 18);
  }

  function renderShortlists() {
    const shortlists = currentShortlists();
    els.shortlists.innerHTML = BUCKETS.map((bucket) => {
      const rows = (shortlists[bucket] || [])
        .map(
          (player) => `
            <div class="bucket-chip">
              <span>${player}</span>
              <button data-remove-player="${player}" data-remove-bucket="${bucket}">Remove</button>
            </div>
          `
        )
        .join("");
      return `
        <div class="bucket-panel">
          <div class="tile-header">
            <h5>${titleize(bucket)}</h5>
            <span class="pill">${(shortlists[bucket] || []).length}</span>
          </div>
          <div class="bucket-list">
            ${rows || `<p class="muted">No players in this bucket yet.</p>`}
          </div>
        </div>
      `;
    }).join("");

    els.shortlists.querySelectorAll("button[data-remove-player]").forEach((button) => {
      button.addEventListener("click", () => {
        removeFromBucket(button.dataset.removePlayer, button.dataset.removeBucket);
      });
    });
  }

  function renderCards(rows) {
    const teamCode = els.team.value;
    const scenarioTeam = teams[teamCode];
    const team = teamMap.get(teamCode);
    const best = rows[0];
    els.cards.innerHTML = `
      <div class="replay-card">
        <h4>Purse Left</h4>
        <strong>₹${formatDecimal(scenarioTeam.purse)} Cr</strong>
        <p>${scenarioTeam.open_slots} open slots remain.</p>
      </div>
      <div class="replay-card">
        <h4>Overseas Pressure</h4>
        <strong>${team ? formatDecimal(team.overseas_pressure_pct, 1) : "0.0"}%</strong>
        <p>${scenarioTeam.overseas_slots_left} overseas slots still open.</p>
      </div>
      <div class="replay-card">
        <h4>Top Surplus Target</h4>
        <strong>${best ? best.player_name : "None"}</strong>
        <p>${best ? `${titleize(best.role_bucket)} · +${formatDecimal(best.value_surplus)} Cr surplus` : "No live target."}</p>
      </div>
      <div class="replay-card">
        <h4>Auction Power</h4>
        <strong>${formatDecimal(scenarioTeam.auction_power, 2)}</strong>
        <p>Aggression ${formatDecimal(scenarioTeam.aggression, 2)} with ${scenarioTeam.retained} retained players.</p>
      </div>
    `;
  }

  function renderRoleGaps(rows) {
    const teamCode = els.team.value;
    const scenarioTeam = teams[teamCode];
    const team = teamMap.get(teamCode);
    const fillMap = rows.reduce((acc, row) => {
      if (!acc[row.role_bucket] || row.war_room_score > acc[row.role_bucket].war_room_score) {
        acc[row.role_bucket] = row;
      }
      return acc;
    }, {});
    const items = (team ? team.role_gaps : [])
      .slice(0, 5)
      .map((gap) => {
        const key = gap.role.replaceAll(" ", "_");
        const cap = scenarioTeam.role_caps[key] ?? scenarioTeam.role_caps[gap.role] ?? 0;
        const fill = fillMap[key];
        return `
          <div class="metric-card">
            <h5>${titleize(gap.role)}</h5>
            <strong>${formatDecimal(gap.weight, 2)}</strong>
            <p>Cap ${cap} · best fill ${fill ? `${fill.player_name} at ${formatDecimal(fill.expected_price)} Cr` : "still thin"}</p>
          </div>
        `;
      })
      .join("");
    els.roleGaps.innerHTML = items || `<p class="muted">No major role-gap signal available.</p>`;
  }

  function renderRivals(rows) {
    const teamCode = els.team.value;
    const focusRoles = [...new Set(rows.slice(0, 6).map((row) => row.role_bucket))];
    const rivals = Object.entries(teams)
      .filter(([code]) => code !== teamCode)
      .map(([code, team]) => {
        const pressure = focusRoles.reduce((sum, role) => sum + Number(team.role_needs[role] || 0), 0);
        return {
          code,
          name: team.name,
          pressure,
          auction_power: Number(team.auction_power || 0),
          purse: Number(team.purse || 0),
        };
      })
      .sort((a, b) => b.pressure * 2 + b.auction_power - (a.pressure * 2 + a.auction_power))
      .slice(0, 6);

    els.rivals.innerHTML = rivals
      .map(
        (rival) => `
          <div class="metric-card">
            <h5>${rival.code}</h5>
            <strong>${formatDecimal(rival.pressure, 2)}</strong>
            <p>${rival.name} · auction power ${formatDecimal(rival.auction_power, 2)} · purse ${formatDecimal(rival.purse)} Cr</p>
          </div>
        `
      )
      .join("");
  }

  function renderTargetBoard(rows) {
    renderTable(
      els.targets,
      [
        { key: "player_name", label: "Player" },
        { key: "role_bucket", label: "Role", render: (value) => titleize(value) },
        { key: "expected_price", label: "Exp. Price", render: (value) => `₹${formatDecimal(value)} Cr` },
        { key: "value_surplus", label: "Surplus", render: (value) => `${value >= 0 ? "+" : ""}${formatDecimal(value)} Cr` },
        { key: "team_share", label: `${els.team.value} Buy %`, render: (value) => `${formatDecimal(value * 100, 1)}%` },
        { key: "fit_note", label: "Fit" },
        {
          key: "player_name",
          label: "Bucket",
          render: (value) => `
            <div class="mini-button-row">
              ${BUCKETS.map((bucket) => `<button class="mini-action" data-player="${value}" data-bucket="${bucket}">${titleize(bucket)}</button>`).join("")}
            </div>
          `,
        },
      ],
      rows
    );
    els.targets.querySelectorAll("button[data-player]").forEach((button) => {
      button.addEventListener("click", () => addToBucket(button.dataset.player, button.dataset.bucket));
    });
  }

  function refreshPlayerOptions(rows) {
    const options = rows.map((row) => row.player_name);
    els.playerOptions.innerHTML = options.map((name) => `<option value="${name}"></option>`).join("");
    if (!options.includes(els.player.value)) {
      els.player.value = "";
    }
  }

  function render() {
    const rows = buildRoleRows();
    renderCards(rows);
    renderTargetBoard(rows);
    renderShortlists();
    renderRoleGaps(rows);
    renderRivals(rows);
    refreshPlayerOptions(rows);
  }

  function init() {
    setOptions(els.team, Object.keys(teams));
    setOptions(els.role, ["all", ...roleMarket.roles], (value) => (value === "all" ? "All Role Buckets" : titleize(value)));
    setOptions(els.bucket, BUCKETS, titleize);
    [els.team, els.role].forEach((element) => element.addEventListener("change", render));
    els.add.addEventListener("click", () => addToBucket(els.player.value, els.bucket.value));
    render();
  }

  init();
})();
