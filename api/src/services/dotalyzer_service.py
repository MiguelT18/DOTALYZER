import json
from pathlib import Path
import httpx
import os
import pandas as pd

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
  
  return matches

async def transform_matches_to_dataset(player_id: int, dataset_dir: Path = DATASETS_DIR):
  raw_file_path = RAW_DATA_DIR / f"matches_{player_id}.json"
  dataset_file_path = dataset_dir / f"dataset_{player_id}.csv"

  if not raw_file_path.exists():
    raise FileNotFoundError(f"No se encontró el archivo: {raw_file_path}")

  with open(raw_file_path, "r") as f:
    raw_matches = json.load(f)
  
  print(json.dumps(raw_matches[0], indent=2))

  if not raw_matches:
    raise ValueError("No hay datos en el archivo JSON.")
  
  df = pd.DataFrame(raw_matches)
  columns = [
    "match_id", "hero_id", "kills", "deaths", "assists",
    "xp_per_min", "gold_per_min", "duration", "start_time",
    "lane", "lane_role", "is_roaming", "party_size"
  ]

  for col in columns:
    if col not in df.columns:
      df[col] = 0

  df = df[columns]

  df.to_csv(dataset_file_path, index=False)

  try:
    os.chmod(dataset_file_path, 0o664)
  except PermissionError:
    print(f"No se pudieron cambiar permisos de: {dataset_file_path}")
  
  return dataset_file_path

