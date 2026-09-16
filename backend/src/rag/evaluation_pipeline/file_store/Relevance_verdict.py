from typing import Dict
from ...model.chunk_relevancy import ChunkRelevantVerdict
from pathlib import Path
import json

from .base import FileStoreInterface

class RelevanceVerdictFileSave(FileStoreInterface):
    def __init__(self, dir_path: str="rag_results") -> None:
        self.dir_path = Path(dir_path)
        # We define a single, unique file name for this store
        self.file_name = "relevance_verdict.json"

    def save_file(self, run_id: str, file: Dict[str, ChunkRelevantVerdict]) -> None:
        run_dir = self.dir_path / run_id
        print("run_dir",run_dir)
        # 1. Error if the run directory does not exist
        if not run_dir.is_dir():
            raise FileNotFoundError(
                f"Cannot save file: The run directory '{run_dir}' does not exist."
            )
        
        storage_path = run_dir / self.file_name
        
        # 2. ENFORCE UNIQUENESS: Error if the file already exists
        # (Remove these two lines if you want `save_file` to safely overwrite existing data)
        if storage_path.exists():
            raise FileExistsError(f"A relevance file already exists at '{storage_path}'.")
        
        # 3. Convert Pydantic models to dictionaries
        data_to_save = {
            key: verdict.model_dump() for key, verdict in file.items()
        }
        
        # 4. Save to JSON
        with storage_path.open("w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2)

    def load_file(self, run_id: str) -> Dict[str, ChunkRelevantVerdict]:
        run_dir = self.dir_path / run_id
        storage_path = run_dir / self.file_name
        
        # 1. Check if the directory and file exist
        if not run_dir.is_dir():
            raise FileNotFoundError(f"The run directory '{run_dir}' does not exist.")
        if not storage_path.is_file():
            raise FileNotFoundError(f"The relevance file '{self.file_name}' does not exist in '{run_dir}'.")
        
        # 2. Load the raw JSON dictionary
        with storage_path.open("r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        # 3. Parse the raw dictionaries back into ChunkRelevantVerdict models
        return {
            key: ChunkRelevantVerdict.model_validate(value) 
            for key, value in raw_data.items()
        }