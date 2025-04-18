import pandas as pd
from pathlib import Path

async def download_and_transform(player_id: int, limit: int = 10, dataset_dir: Path = None):
  from src.services.dotalyzer_service import get_recent_matches, transform_matches_to_dataset
  await get_recent_matches(player_id, limit)
  
  csv_path = await transform_matches_to_dataset(player_id, dataset_dir)
  
  df = pd.read_csv(csv_path)

  transformed_path = dataset_dir / f"{player_id}_transformed.csv"
  df.to_csv(transformed_path, index=False)
  
  return transformed_path