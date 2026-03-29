(function () {
  const data = window.DASHBOARD_DATA;
  const els = {
    phaseHorizon: document.getElementById("phase-horizon"),
    phaseDiscipline: document.getElementById("phase-discipline"),
    phasePhase: document.getElementById("phase-phase"),
    phasePlayerSearch: document.getElementById("phase-player-search"),
    phasePlayerCompare: document.getElementById("phase-player-compare"),
    phasePlayerOptions: document.getElementById("phase-player-options"),
    phaseMatchup: document.getElementById("phase-matchup"),
    phaseBars: document.getElementById("phase-bars"),
    phaseTable: document.getElementById("phase-table"),
  };

  function formatNumber(value) {
    return new Intl.NumberFormat("en-IN").format(value);
  }

  function formatDecimal(value, digits = 2) {
    return Number(value).toFixed(digits);
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

  function renderBars(container, rows, valueKey, labelKey) {
    if (!rows.length) {
      container.innerHTML = `<p class="muted">No records available.</p>`;
      return;
    }
    const maxValue = Math.max(...rows.map((row) => Number(row[valueKey] || 0)), 1);
    container.innerHTML = rows
      .map((row) => {
        const value = Number(row[valueKey] || 0);
        const width = (value / maxValue) * 100;
        return `
          <div class="bar-row">
            <div class="bar-label" title="${row[labelKey]}">${row[labelKey]}</div>
            <div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div>
            <div class="bar-value">${formatNumber(Math.round(value))}</div>
          </div>
        `;
      })
      .join("");
  }

  function renderPhaseStudio() {
    const key = `${els.phaseDiscipline.value}_${els.phasePhase.value}`;
    const baseRows = data.phase_rankings[els.phaseHorizon.value][key] || [];
    els.phasePlayerOptions.innerHTML = baseRows.map((row) => `<option value="${row.player}"></option>`).join("");

    let rows = baseRows.slice();
    const searchValue = (els.phasePlayerSearch.value || "").trim().toLowerCase();
    const compareValue = (els.phasePlayerCompare.value || "").trim().toLowerCase();
    if (searchValue || compareValue) {
      rows.sort((a, b) => {
        const aPrimary = a.player.toLowerCase() === searchValue ? 2 : a.player.toLowerCase() === compareValue ? 1 : 0;
        const bPrimary = b.player.toLowerCase() === searchValue ? 2 : b.player.toLowerCase() === compareValue ? 1 : 0;
        if (bPrimary !== aPrimary) return bPrimary - aPrimary;
        return a.rank - b.rank;
      });
    }

    const comparedRows = rows.filter((row) => {
      const name = row.player.toLowerCase();
      return name === searchValue || name === compareValue;
    });

    els.phaseMatchup.innerHTML = comparedRows
      .slice(0, 2)
      .map(
        (row) => `
          <div class="compare-card">
            <h5>${row.player}</h5>
            <div class="summary-line"><span>Impact</span><strong>${formatNumber(Math.round(row.impact_score))}</strong></div>
            <div class="summary-line"><span>Rank</span><strong>${row.rank}</strong></div>
            <div class="summary-line"><span>Balls</span><strong>${row.balls}</strong></div>
            <div class="summary-line"><span>${els.phaseDiscipline.value === "batting" ? "SR Bayes" : "Econ Bayes"}</span><strong>${formatDecimal(els.phaseDiscipline.value === "batting" ? row.sr_bayes : row.econ_bayes)}</strong></div>
          </div>
        `
      )
      .join("");

    renderBars(els.phaseBars, rows.slice(0, 10), "impact_score", "player");

    const columns =
      els.phaseDiscipline.value === "batting"
        ? [
            { key: "rank", label: "Rank" },
            { key: "player", label: "Player" },
            { key: "runs", label: "Runs" },
            { key: "balls", label: "Balls" },
            { key: "strike_rate", label: "SR", render: (value) => formatDecimal(value) },
            { key: "sr_bayes", label: "SR Bayes", render: (value) => formatDecimal(value) },
            { key: "impact_score", label: "Impact", render: (value) => formatNumber(Math.round(value)) },
          ]
        : [
            { key: "rank", label: "Rank" },
            { key: "player", label: "Player" },
            { key: "wickets", label: "Wkts" },
            { key: "runs", label: "Runs" },
            { key: "balls", label: "Balls" },
            { key: "economy", label: "Econ", render: (value) => formatDecimal(value) },
            { key: "econ_bayes", label: "Econ Bayes", render: (value) => formatDecimal(value) },
            { key: "impact_score", label: "Impact", render: (value) => formatNumber(Math.round(value)) },
          ];

    renderTable(els.phaseTable, columns, rows);
  }

  function init() {
    setOptions(els.phaseHorizon, ["all_time", "active"], (value) => (value === "all_time" ? "All-Time" : "Active"));
    setOptions(els.phaseDiscipline, ["batting", "bowling"], (value) => value.charAt(0).toUpperCase() + value.slice(1));
    setOptions(els.phasePhase, ["powerplay", "middle", "death"], (value) => value.charAt(0).toUpperCase() + value.slice(1));

    [els.phaseHorizon, els.phaseDiscipline, els.phasePhase].forEach((el) => el.addEventListener("change", renderPhaseStudio));
    els.phasePlayerSearch.addEventListener("change", renderPhaseStudio);
    els.phasePlayerCompare.addEventListener("change", renderPhaseStudio);
    renderPhaseStudio();
  }

  init();
})();
