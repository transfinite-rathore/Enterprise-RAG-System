from pydantic import BaseModel,PrivateAttr
from typing import Any, Dict,Set
from .rag_eval_context import RAGEvaluationPayload
from .chunk_relevancy import ChunkRelevantVerdict

class EvaluatorContext(BaseModel):
    
    payload:RAGEvaluationPayload
    verdicts:Dict[str,ChunkRelevantVerdict]
    
    _relevant_ids: Set[str] = PrivateAttr(default_factory=set)
    _score_above_three_ids: Set[str] = PrivateAttr(default_factory=set)
    _perfect_match_ids: Set[str] = PrivateAttr(default_factory=set)
    
    def model_post_init(self, __context) -> None:
        """
        Runs exactly once. Loops through verdicts in O(N) time and 
        populates all three caches simultaneously.
        """
        for chunk_id, verdict in self.verdicts.items():
            # 1. Cache based on the boolean flag
            if verdict.is_relevant:
                self._relevant_ids.add(chunk_id)
            
            # 2 & 3. Cache based on the integer score
            if verdict.score is not None:
                if verdict.score >= 3:
                    self._score_above_three_ids.add(chunk_id)
                if verdict.score == 5:
                    self._perfect_match_ids.add(chunk_id)
    @property         
    def relevant_ids(self):
        return self._relevant_ids
    
    @property
    def perfect_match_id(self):
        return self.perfect_match_id
    
    @property
    def high_scoring_id(self):
        return self.high_scoring_id