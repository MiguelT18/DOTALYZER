import pandas as pd
from pathlib import Path

async def transform_json_file_to_csv(json_path: Path, output_dir: Path = None):
  """
  Transforma un archivo JSON de matches a CSV directamente.

  Args:
    json_path (Path): Ruta al archivo JSON.
    output_dir (Path, optional): Carpeta donde se guarda el CSV.

  Returns:
    Path: Ruta del archivo CSV generado.
  """
  import json

  with open(json_path, "r", encoding="utf-8") as f:
    matches = json.load(f)

  df = pd.json_normalize(matches)

  player_id = json_path.stem.split("_")[-1]
  output_path = (output_dir or json_path.parent) / f"{player_id}_transformed.csv"

  df.to_csv(output_path, index=False)
  return output_path