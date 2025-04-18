from fastapi import HTTPException
from collections import defaultdict
from src.services.dotalyzer_service import get_recent_matches
import pandas as pd

async def fetch_player_stats(player_id: int):
  try:
    matches = await get_recent_matches(player_id)
    df = pd.DataFrame(matches)

    return df.to_dict(orient="records")
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

def analyze_hero_performance(matches: list[dict]) -> dict[int, dict]:
  stats = defaultdict(lambda: {
    "games": 0,
    "wins": 0,
    "losses": 0,
    "kills_total": 0,
    "deaths_total": 0,
    "assists_total": 0,
    "gpm_total": 0,
    "xpm_total": 0,
    "hero_damage_total": 0,
    "tower_damage_total": 0,
    "last_hits_total": 0,
    "hero_healing_total": 0
  })

  for match in matches:
    hero_id = match["hero_id"]
    is_radiant = match["player_slot"] < 128
    won = match["radiant_win"] if is_radiant else not match["radiant_win"]

    stats[hero_id]["games"] += 1
    stats[hero_id]["wins"] += int(won)
    stats[hero_id]["losses"] += int(not won)
    stats[hero_id]["kills_total"] += match.get("kills", 0)
    stats[hero_id]["deaths_total"] += match.get("deaths", 0)
    stats[hero_id]["assists_total"] += match.get("assists", 0)
    stats[hero_id]["gpm_total"] += match.get("gold_per_min", 0)
    stats[hero_id]["xpm_total"] += match.get("xp_per_min", 0)
    stats[hero_id]["hero_damage_total"] += match.get("hero_damage", 0)
    stats[hero_id]["tower_damage_total"] += match.get("tower_damage", 0)
    stats[hero_id]["last_hits_total"] += match.get("last_hits", 0)
    stats[hero_id]["hero_healing_total"] += match.get("hero_healing", 0)

  result = {}

  for hero_id, data in stats.items():
    games = data["games"]
    deaths = data["deaths_total"]
    result[hero_id] = {
      "games": games,
      "wins": data["wins"],
      "losses": data["losses"],
      "winrate": round((data["wins"] / games) * 100, 2),
      "kills_avg": round(data["kills_total"] / games, 2),
      "deaths_avg": round(deaths / games, 2),
      "assists_avg": round(data["assists_total"] / games, 2),
      "kda_ratio": round((data["kills_total"] + data["assists_total"]) / max(1, deaths), 2),
      "gpm_avg": round(data["gpm_total"] / games, 2),
      "xpm_avg": round(data["xpm_total"] / games, 2),
      "hero_damage_avg": round(data["hero_damage_total"] / games, 2),
      "tower_damage_avg": round(data["tower_damage_total"] / games, 2),
      "last_hits_avg": round(data["last_hits_total"] / games, 2),
      "hero_healing_avg": round(data["hero_healing_total"] / games, 2)
    }
    
  return result
