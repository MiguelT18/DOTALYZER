import json
from pathlib import Path
import httpx
import os
from src.utils.data_pipeline import transform_json_file_to_csv

BASE_URL = "https://api.opendota.com/api"

BASE_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DATA_DIR = BASE_DATA_DIR / "raw_data"
DATASETS_DIR = BASE_DATA_DIR / "datasets"

for directory in [RAW_DATA_DIR, DATASETS_DIR]:
  try:
    directory.mkdir(parents=True, exist_ok=True) 
    os.chmod(directory, 0o775)
  except:
    print(f"No se pudieron cambiar permisos de: {directory}")

async def get_recent_matches(player_id: int):
  async with httpx.AsyncClient() as client:
    url = f"{BASE_URL}/players/{player_id}/recentMatches"
    response = await client.get(url)
    response.raise_for_status()
    matches = response.json()
  
  # Guardar en archivo JSON
  raw_file_path = RAW_DATA_DIR / f"matches_{player_id}.json"

  with open(raw_file_path, "w") as f:
    json.dump(matches, f, indent=2)

  try:
    os.chmod(raw_file_path, 0o664)
  except PermissionError:
    print(f"No se pudieron cambiar permisos del archivo: {raw_file_path}")
  
  await transform_json_file_to_csv(json_path=raw_file_path, output_dir=DATASETS_DIR)
  
  return matches