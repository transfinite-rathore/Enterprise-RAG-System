from .result_store import RAGResultStore
from datetime import datetime
from pathlib import Path
from ...model.rag_eval_context import RAGEvaluationPayload
import uuid

import json

class RAGFileResultStore(RAGResultStore):
    
    def __init__(self,base_dir:str="rag_results") -> None:
        self.base_dir=Path(base_dir)

    def save(
        self,
        rag_result,
        manifest_details: dict
    ) -> str:

        run_id = f"run_{uuid.uuid4().hex}"

        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=False)

        result_path = run_dir / "result.json"
        manifest_path = run_dir / "manifest.json"

        with result_path.open("w", encoding="utf-8") as f:
            f.write(
                rag_result.model_dump_json(indent=2)
            )

        manifest = {
            "run_id": run_id,
            **manifest_details
        }

        with manifest_path.open("w", encoding="utf-8") as f:
            json.dump(
                manifest,
                f,
                indent=2,
                ensure_ascii=False
            )

        return run_id

    def load(self, run_id: str) -> RAGEvaluationPayload:
        result_file = self.base_dir / run_id / "result.json"

        if not result_file.exists():
            raise FileNotFoundError(
                f"RAG result not found: {run_id}"
            )

        with result_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return RAGEvaluationPayload(**data)


# class RagFileResultStore(RAGResultStore):
    
#     def save(self, rag_result):
#         timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
#         result_dir = Path("rag_results")
#         result_dir.mkdir(parents=True, exist_ok=True)
#         with open(f"rag_results/{timestamp}.json", "w",encoding="utf-8") as f:
#             f.write(rag_result.model_dump_json(indent=2))
