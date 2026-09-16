
import kagglehub
import os
from pathlib import Path

os.environ["KAGGLEHUB_CACHE"] = str(Path(os.getcwd()) / "data")

path = kagglehub.dataset_download("harrywang/acquired-podcast-transcripts-and-rag-evaluation")

print("Path to dataset files:", path)