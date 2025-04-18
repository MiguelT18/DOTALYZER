from fastapi import APIRouter
from src.services.dotalyzer_service import get_recent_matches
from controllers.dotalyzer_controller import fetch_player_stats, analyze_hero_performance
from services.recommender_service import recommend_heroes

router = APIRouter(prefix="/dotalyzer", tags=["dotalyzer"])

@router.get("/matches/{player_id}")
async def get_matches(player_id: int):
  return await fetch_player_stats(player_id)

@router.get("/players/{player_id}/hero-performance")
async def get_hero_performance(player_id: int):
  matches = await fetch_player_stats(player_id)
  hero_stats = analyze_hero_performance(matches)
  return hero_stats

@router.get("/players/{player_id}/recommended-heroes")
async def get_recommended_heroes(player_id: int):
  matches = await get_recent_matches(player_id)
  performance = analyze_hero_performance(matches)
  recommended = recommend_heroes(performance)

  if not recommended:
    return {
      "recommended_heroes": [],
      "message": "No se encontraron héroes recomendables. Intenta jugar más partidas o probar nuevos héroes."
    }
  
  return { "recommended_heroes": recommended }