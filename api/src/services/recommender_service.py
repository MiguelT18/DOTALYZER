def recommend_heroes(performance: dict[int, dict], top_n: int = 3):
  recommend = []
  
  for hero_id, stats in performance.items():
    games = stats["games"]
    winrate = (stats["wins"] / games) * 100 if games > 0 else 0

    # Evitar héroes con winrate menor al 30%
    if winrate < 30:
      continue

    is_new = games <= 3 and winrate >= 50

    recommend.append({
      "hero_id": hero_id,
      "winrate": round(winrate, 2),
      "kda_ratio": stats["kda_ratio"],
      "games": games,
      "is_new": is_new
    })
  
  recommend.sort(key=lambda h: (h["is_new"], h["kda_ratio"]), reverse=True)
  
  return recommend[:top_n]