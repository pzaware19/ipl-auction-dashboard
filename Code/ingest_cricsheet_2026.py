"""
ingest_cricsheet_2026.py
------------------------
Author : Piyush Zaware
Updated: 2026-03-28

Purpose
-------
Download the latest Cricsheet IPL JSON zip, extract any new 2026 match files,
parse them into ball-by-ball rows, append to the master CSV, and recompute all
12 phase ranking CSVs (batting + bowling × powerplay / middle / death × all-time
/ active).

Inputs
------
- https://cricsheet.org/downloads/ipl_json.zip  (downloaded to a temp file)
- Data/ipl_json/                                (existing match JSON files)
- Data/ipl_ball_by_ball.csv                     (existing ball-by-ball master)

Outputs
-------
- Data/ipl_json/<new_files>.json
- Data/ipl_ball_by_ball.csv          (appended)
- Data/powerplay_batting_all_time.csv
- Data/middle_batting_all_time.csv
- Data/death_batting_all_time.csv
- Data/powerplay_bowling_all_time.csv
- Data/middle_bowling_all_time.csv
- Data/death_bowling_all_time.csv
- Data/powerplay_batting_active.csv
- Data/middle_batting_active.csv
- Data/death_batting_active.csv
- Data/powerplay_bowling_active.csv
- Data/middle_bowling_active.csv
- Data/death_bowling_active.csv

Exit codes
----------
0  - New matches were found and ingested; caller (GitHub Action) should commit.
2  - No new matches found; caller should skip commit.
1  - Script-level error (unexpected exception).
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import traceback
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT       = Path(__file__).resolve().parent.parent
DATA_DIR   = ROOT / "Data"
JSON_DIR   = DATA_DIR / "ipl_json"
BBB_CSV    = DATA_DIR / "ipl_ball_by_ball.csv"

CRICSHEET_URL = "https://cricsheet.org/downloads/ipl_json.zip"

# ---------------------------------------------------------------------------
# Constants that mirror build_dashboard_data.py / phase CSV conventions
# ---------------------------------------------------------------------------
TARGET_SEASON    = "2026"
ACTIVE_CUTOFF    = 2025        # a player is "active" if last_year >= this value

# Bayesian shrinkage hyper-parameter (same k for batting and bowling)
K_SHRINK         = 195

# Bowling impact formula calibration constant
BOWLING_IMPACT_C = 4.1

# Minimum ball thresholds for phase CSVs
MIN_BALLS_BAT    = 20
MIN_BALLS_BOWL   = 24

# Phase boundary (over numbers, 0-indexed)
PHASE_MAP = {
    "powerplay": range(0, 6),
    "middle":    range(6, 15),
    "death":     range(15, 20),
}

# All 12 output file stems  (phase)_(role)_(scope).csv
PHASE_NAMES  = ["powerplay", "middle", "death"]
ROLE_NAMES   = ["batting", "bowling"]
SCOPE_NAMES  = ["all_time", "active"]


# ===========================================================================
# 1. Download + extraction helpers
# ===========================================================================

def download_zip(url: str, dest: Path) -> None:
    print(f"Downloading {url} …", flush=True)
    urlretrieve(url, dest)
    print(f"  Saved to {dest} ({dest.stat().st_size / 1_048_576:.1f} MB)", flush=True)


def extract_zip(zip_path: Path, extract_dir: Path) -> list[Path]:
    """Extract zip and return list of extracted .json file paths."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    return sorted(extract_dir.rglob("*.json"))


def filter_new_2026_files(all_json: list[Path], existing_names: set[str]) -> list[Path]:
    """Return only JSON files whose season is 2026 and that are not already in ipl_json/."""
    new_files: list[Path] = []
    for jf in all_json:
        if jf.name in existing_names:
            continue
        try:
            with jf.open(encoding="utf-8") as fh:
                info = json.load(fh).get("info", {})
            if str(info.get("season", "")) == TARGET_SEASON:
                new_files.append(jf)
        except Exception as exc:  # noqa: BLE001
            print(f"  WARNING: could not read {jf.name}: {exc}", flush=True)
    return new_files


# ===========================================================================
# 2. Ball-by-ball parsing
# ===========================================================================

def _phase(over: int) -> str:
    if over < 6:
        return "powerplay"
    if over < 15:
        return "middle"
    return "death"


def _get_winner(info: dict) -> str:
    outcome = info.get("outcome", {})
    return outcome.get("winner", "")


def parse_json_to_rows(match_json: dict) -> list[dict]:
    """
    Convert one Cricsheet match JSON into a list of row dicts that match
    the schema of ipl_ball_by_ball.csv.
    """
    info    = match_json.get("info", {})
    dates   = info.get("dates", [""])
    date    = dates[0] if dates else ""
    venue   = info.get("venue", "")
    city    = info.get("city", "")
    gender  = info.get("gender", "male")
    m_type  = info.get("match_type", "T20")
    winner  = _get_winner(info)

    # Use filename stem as a stable match_id proxy; actual id from meta if present
    meta     = match_json.get("meta", {})
    match_id = meta.get("data_version", date.replace("-", ""))

    rows: list[dict] = []

    for innings_idx, innings_data in enumerate(match_json.get("innings", []), start=1):
        batting_team = innings_data.get("team", "")
        overs_data   = innings_data.get("overs", [])

        innings_runs_cum     = 0
        innings_wickets_cum  = 0
        legal_balls_bowled   = 0

        for over_data in overs_data:
            over_num    = int(over_data.get("over", 0))
            deliveries  = over_data.get("deliveries", [])

            for delivery in deliveries:
                batter      = delivery.get("batter", "")
                bowler      = delivery.get("bowler", "")
                non_striker = delivery.get("non_striker", "")

                runs_dict    = delivery.get("runs", {})
                runs_batter  = int(runs_dict.get("batter", 0))
                runs_extras  = int(runs_dict.get("extras", 0))
                runs_total   = int(runs_dict.get("total", 0))

                extras_dict    = delivery.get("extras", {})
                extras_wides   = int(extras_dict.get("wides",   0))
                extras_noballs = int(extras_dict.get("noballs", 0))
                extras_byes    = int(extras_dict.get("byes",    0))
                extras_legbyes = int(extras_dict.get("legbyes", 0))

                # legal delivery?
                legal_ball = 1 if (extras_wides == 0 and extras_noballs == 0) else 0

                # Wicket info
                wickets_list = delivery.get("wickets", [])
                if wickets_list:
                    wkt           = wickets_list[0]
                    wicket        = 1
                    dismissal_kind = wkt.get("kind", "")
                    player_out    = wkt.get("player_out", "")
                    fielders      = wkt.get("fielders", [])
                    fielder       = fielders[0].get("name", "") if fielders else ""
                else:
                    wicket         = 0
                    dismissal_kind = ""
                    player_out     = ""
                    fielder        = ""

                # Update cumulative counters BEFORE storing in row
                # (row captures state *after* the ball, consistent with existing data)
                innings_runs_cum    += runs_total
                innings_wickets_cum += wicket
                if legal_ball:
                    legal_balls_bowled += 1

                balls_remaining = 120 - legal_balls_bowled

                rows.append({
                    "match_id":            match_id,
                    "date":                date,
                    "venue":               venue,
                    "city":                city,
                    "gender":              gender,
                    "match_type":          m_type,
                    "innings":             innings_idx,
                    "batting_team":        batting_team,
                    "winner":              winner,
                    "over":               over_num,
                    "ball_in_over":        delivery.get("ball_in_over", ""),
                    "batter":              batter,
                    "bowler":              bowler,
                    "non_striker":         non_striker,
                    "runs_batter":         runs_batter,
                    "runs_extras":         runs_extras,
                    "runs_total":          runs_total,
                    "extras_wides":        extras_wides,
                    "extras_noballs":      extras_noballs,
                    "extras_byes":         extras_byes,
                    "extras_legbyes":      extras_legbyes,
                    "wicket":              wicket,
                    "dismissal_kind":      dismissal_kind,
                    "player_out":          player_out,
                    "fielder":             fielder,
                    "phase":               _phase(over_num),
                    "legal_ball":          legal_ball,
                    "innings_runs_cum":    innings_runs_cum,
                    "innings_wickets_cum": innings_wickets_cum,
                    "legal_balls_bowled":  legal_balls_bowled,
                    "balls_remaining":     balls_remaining,
                })

    return rows


# ===========================================================================
# 3. Phase CSV recomputation
# ===========================================================================

def _compute_batting_phase(df: pd.DataFrame, phase: str) -> pd.DataFrame:
    """
    Batting phase CSV: batter, phase, runs, balls, strike_rate,
    sr_bayes, impact_score, last_year
    """
    sub = df[(df["phase"] == phase) & (df["legal_ball"] == 1)].copy()

    # League-level average SR for this phase (all batters)
    lg_runs  = sub["runs_batter"].sum()
    lg_balls = len(sub)
    lg_sr    = (lg_runs / lg_balls * 100) if lg_balls > 0 else 100.0

    grp = sub.groupby("batter").agg(
        runs  = ("runs_batter", "sum"),
        balls = ("legal_ball",  "count"),
    ).reset_index()

    # Year of last appearance (from 'date' column in the ball data)
    last_year = (
        df[(df["phase"] == phase) & (df["legal_ball"] == 1)]
        .groupby("batter")["date"]
        .max()
        .apply(lambda d: int(str(d)[:4]))
        .reset_index()
        .rename(columns={"date": "last_year"})
    )
    grp = grp.merge(last_year, on="batter", how="left")

    # Filter minimum balls
    grp = grp[grp["balls"] >= MIN_BALLS_BAT].copy()

    grp["phase"]        = phase
    grp["strike_rate"]  = grp["runs"] / grp["balls"] * 100
    # Bayesian shrinkage: sr_bayes = (runs + k * lg_sr/100) / (balls + k) * 100
    grp["sr_bayes"]     = (grp["runs"] + K_SHRINK * lg_sr / 100) / (grp["balls"] + K_SHRINK) * 100
    grp["impact_score"] = grp["balls"] * grp["sr_bayes"]

    return grp[["batter", "phase", "runs", "balls", "strike_rate", "sr_bayes", "impact_score", "last_year"]]


def _compute_bowling_phase(df: pd.DataFrame, phase: str) -> pd.DataFrame:
    """
    Bowling phase CSV: bowler, phase, runs, balls, wickets, economy,
    bowling_sr, econ_bayes, impact_score, last_year
    """
    sub = df[(df["phase"] == phase) & (df["legal_ball"] == 1)].copy()

    # League-level economy for this phase
    lg_runs  = sub["runs_batter"].sum() + sub.get("extras_wides", pd.Series(0, index=sub.index)).fillna(0).sum() + sub.get("extras_noballs", pd.Series(0, index=sub.index)).fillna(0).sum()
    lg_balls = len(sub)
    lg_econ  = (lg_runs / lg_balls * 6) if lg_balls > 0 else 8.0

    # Aggregate: use runs_total for economy (includes extras charged to bowler)
    grp = sub.groupby("bowler").agg(
        runs    = ("runs_total",  "sum"),
        balls   = ("legal_ball",  "count"),
        wickets = ("wicket",      "sum"),
    ).reset_index()

    # Year of last appearance
    last_year = (
        df[(df["phase"] == phase) & (df["legal_ball"] == 1)]
        .groupby("bowler")["date"]
        .max()
        .apply(lambda d: int(str(d)[:4]))
        .reset_index()
        .rename(columns={"date": "last_year"})
    )
    grp = grp.merge(last_year, on="bowler", how="left")

    # Filter minimum balls
    grp = grp[grp["balls"] >= MIN_BALLS_BOWL].copy()

    grp["phase"]    = phase
    grp["economy"]  = grp["runs"] / grp["balls"] * 6
    # bowling_sr = balls / wickets (0 wickets → 999)
    grp["bowling_sr"] = grp.apply(
        lambda r: r["balls"] / r["wickets"] if r["wickets"] > 0 else 999.0,
        axis=1,
    )
    # Bayesian shrinkage for economy
    grp["econ_bayes"] = (
        (grp["economy"] * grp["balls"] + K_SHRINK * lg_econ) / (grp["balls"] + K_SHRINK)
    )
    # Bowling impact formula (calibrated)
    grp["impact_score"] = grp["wickets"] ** 2 / grp["econ_bayes"] * BOWLING_IMPACT_C

    return grp[["bowler", "phase", "runs", "balls", "wickets", "economy", "bowling_sr", "econ_bayes", "impact_score", "last_year"]]


def recompute_phase_csvs(df: pd.DataFrame) -> None:
    """Recompute and write all 12 phase CSVs from the full ball-by-ball DataFrame."""
    # Extract year from date for active filtering
    df = df.copy()
    df["_year"] = df["date"].apply(lambda d: int(str(d)[:4]))

    for phase in PHASE_NAMES:
        # --- Batting ---
        bat_all   = _compute_batting_phase(df, phase)
        bat_active = bat_all[bat_all["last_year"] >= ACTIVE_CUTOFF].copy()

        bat_all.to_csv(DATA_DIR / f"{phase}_batting_all_time.csv", index=False)
        bat_active.to_csv(DATA_DIR / f"{phase}_batting_active.csv", index=False)
        print(f"  Wrote {phase}_batting_all_time.csv  ({len(bat_all)} rows)", flush=True)
        print(f"  Wrote {phase}_batting_active.csv    ({len(bat_active)} rows)", flush=True)

        # --- Bowling ---
        bowl_all   = _compute_bowling_phase(df, phase)
        bowl_active = bowl_all[bowl_all["last_year"] >= ACTIVE_CUTOFF].copy()

        bowl_all.to_csv(DATA_DIR / f"{phase}_bowling_all_time.csv", index=False)
        bowl_active.to_csv(DATA_DIR / f"{phase}_bowling_active.csv", index=False)
        print(f"  Wrote {phase}_bowling_all_time.csv  ({len(bowl_all)} rows)", flush=True)
        print(f"  Wrote {phase}_bowling_active.csv    ({len(bowl_active)} rows)", flush=True)


# ===========================================================================
# 4. Main pipeline
# ===========================================================================

def main() -> int:
    """
    Returns
    -------
    0  if new 2026 matches were ingested
    2  if no new matches were found
    """
    JSON_DIR.mkdir(parents=True, exist_ok=True)

    existing_names: set[str] = {p.name for p in JSON_DIR.glob("*.json")}
    print(f"Existing JSON files in Data/ipl_json/: {len(existing_names)}", flush=True)

    with tempfile.TemporaryDirectory() as tmp_str:
        tmp_dir  = Path(tmp_str)
        zip_path = tmp_dir / "ipl_json.zip"
        ext_dir  = tmp_dir / "extracted"
        ext_dir.mkdir()

        # 1. Download
        download_zip(CRICSHEET_URL, zip_path)

        # 2. Extract
        all_json = extract_zip(zip_path, ext_dir)
        print(f"Total JSON files in zip: {len(all_json)}", flush=True)

        # 3. Find truly new 2026 files
        new_files = filter_new_2026_files(all_json, existing_names)
        print(f"New 2026 files to ingest: {len(new_files)}", flush=True)

        if not new_files:
            print("No new matches — skipping update.", flush=True)
            return 2

        # 4. Parse each new file into rows and copy JSON to ipl_json/
        all_new_rows: list[dict] = []
        ingested = 0
        for jf in new_files:
            try:
                with jf.open(encoding="utf-8") as fh:
                    match_json = json.load(fh)
                rows = parse_json_to_rows(match_json)
                if rows:
                    all_new_rows.extend(rows)
                    # Copy JSON to Data/ipl_json/
                    shutil.copy2(jf, JSON_DIR / jf.name)
                    ingested += 1
                    print(f"  Ingested {jf.name}  ({len(rows)} deliveries)", flush=True)
                else:
                    print(f"  WARNING: {jf.name} produced no rows — skipped.", flush=True)
            except Exception as exc:  # noqa: BLE001
                print(f"  WARNING: failed to parse {jf.name}: {exc}", flush=True)
                traceback.print_exc()

        if not all_new_rows:
            print("Parsing produced no valid rows — aborting.", flush=True)
            return 2

    # 5. Append new rows to master CSV
    new_df = pd.DataFrame(all_new_rows)

    # Ensure column order matches master CSV
    master_cols = [
        "match_id", "date", "venue", "city", "gender", "match_type",
        "innings", "batting_team", "winner", "over", "ball_in_over",
        "batter", "bowler", "non_striker",
        "runs_batter", "runs_extras", "runs_total",
        "extras_wides", "extras_noballs", "extras_byes", "extras_legbyes",
        "wicket", "dismissal_kind", "player_out", "fielder",
        "phase", "legal_ball",
        "innings_runs_cum", "innings_wickets_cum",
        "legal_balls_bowled", "balls_remaining",
    ]
    for col in master_cols:
        if col not in new_df.columns:
            new_df[col] = ""
    new_df = new_df[master_cols]

    print(f"\nAppending {len(new_df):,} new delivery rows to {BBB_CSV.name} …", flush=True)
    new_df.to_csv(BBB_CSV, mode="a", header=False, index=False)
    print("  Done.", flush=True)

    # 6. Reload full master CSV and recompute phase CSVs
    print(f"\nReloading full {BBB_CSV.name} for phase CSV recomputation …", flush=True)
    full_df = pd.read_csv(BBB_CSV, low_memory=False)
    # Ensure numeric columns are numeric
    for col in ["runs_batter", "runs_total", "wicket", "legal_ball", "extras_wides", "extras_noballs"]:
        if col in full_df.columns:
            full_df[col] = pd.to_numeric(full_df[col], errors="coerce").fillna(0).astype(int)

    print("\nRecomputing phase CSVs …", flush=True)
    recompute_phase_csvs(full_df)

    print(
        f"\nAdded {ingested} new 2026 matches. Updated ball-by-ball and phase CSVs.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", flush=True)
        traceback.print_exc()
        exit_code = 1
    sys.exit(exit_code)
