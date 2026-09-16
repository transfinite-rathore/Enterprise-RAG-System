import json
from pathlib import Path
from typing import Dict, Any, Optional

from .base import FileStoreInterface

class EvaluationFileSave(FileStoreInterface):
    def __init__(self, dir_path: str="rag_results") -> None:
        self.dir_path = Path(dir_path)

    def save_file(self, run_id: str, file: Dict[str, Any]) -> None:
        run_dir = self.dir_path / run_id
        
        # Error if directory does not exist
        if not run_dir.is_dir():
            raise FileNotFoundError(
                f"Cannot save file: The run directory '{run_dir}' does not exist."
            )
        
        # Count existing eval_result files to determine the next count
        existing_files = list(run_dir.glob("eval_result*.json"))
        count = len(existing_files) + 1
        
        storage_path = run_dir / f"eval_result{count}.json"
        
        # Save the dictionary as JSON
        with storage_path.open("w", encoding="utf-8") as f:
            json.dump(file, f, indent=2)

    def load_file(self, run_id: str, file_name: Optional[str] = None) -> Dict[str, Any]:
        run_dir = self.dir_path / run_id
        
        if not run_dir.is_dir():
            raise FileNotFoundError(f"The run directory '{run_dir}' does not exist.")
        
        if file_name:
            # 1. If a specific file name is provided, load exactly that file
            storage_path = run_dir / file_name
            if not storage_path.is_file():
                raise FileNotFoundError(f"The file '{file_name}' does not exist in '{run_dir}'.")
        else:
            # 2. If no file name is provided, default to the most recent eval_result file
            existing_files = list(run_dir.glob("eval_result*.json"))
            if not existing_files:
                raise FileNotFoundError(f"No eval_result files found in '{run_dir}'.")
            
            storage_path = max(existing_files, key=lambda p: p.stat().st_mtime)
        
        # Load and return the JSON payload
        with storage_path.open("r", encoding="utf-8") as f:
            return json.load(f)