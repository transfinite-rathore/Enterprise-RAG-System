from .generator_evauator import GeneratorEvaluator
from .reranker_evaluator import RerankerEvaluator
from .reterival_evaluator import RetrievalEvaluator
from ..model.evaluation_context import EvaluatorContext
from ..model.rag_eval_context import RAGEvaluationPayload
from typing import Dict,List,Any

class RAGEvaluationPipeline:
    def __init__(
        self,
        retrieval_evaluator: RetrievalEvaluator,
        reranker_evaluator: RerankerEvaluator,
        generator_evaluator: GeneratorEvaluator,
    ):
        self.retrieval_evaluator = retrieval_evaluator
        self.reranker_evaluator = reranker_evaluator
        self.generator_evaluator = generator_evaluator

    async def run(self, payload: RAGEvaluationPayload, verdicts: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Build immutable O(1) context
        context = EvaluatorContext(payload=payload, verdicts=verdicts)
        retreived_chunks_id=[result["chunk_id"] for result in payload.retrieved_result]
        # 2. Synchronous Ranking Evaluations (Instant CPU lookup)
        retriever_metrics = self.retrieval_evaluator.evaluate(retreived_chunks_id, context)
        reranked_chunks_id=[result["chunk_id"] for result in payload.reranked_result]
        reranker_metrics = self.reranker_evaluator.evaluate(
            reranked_chunks_id, context
        )

        # 3. Asynchronous Generation Evaluation (Network I/O)
        generator_metrics = await self.generator_evaluator.evaluate(payload, context)

        # 4. Consolidated Evaluation Report
        return {
            "conversation_id": getattr(payload, "conversation_id", None),
            "reterived_chunks_count":len(retreived_chunks_id),
            "reranked_chunks_count":len(reranked_chunks_id),
            "retriever": retriever_metrics,
            "reranker": reranker_metrics,
            "generator": generator_metrics,
        }