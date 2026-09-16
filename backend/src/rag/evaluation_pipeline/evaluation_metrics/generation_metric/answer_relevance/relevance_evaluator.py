# metrics/generation/relevance.py
import json
from ..metric import BaseGenerationMetric
from .....model.rag_eval_context import RAGEvaluationPayload
from .....model.evaluation_context import EvaluatorContext
from langchain_core.language_models.chat_models import BaseChatModel
from .prompt_builder import AnswerRelevancyPromptBuilder
import re


class AnswerRelevanceMetric(BaseGenerationMetric):
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.prompt_builder = AnswerRelevancyPromptBuilder()

    @property
    def name(self) -> str:
        return "answer_relevance"

    async def compute(self, payload: RAGEvaluationPayload, context: EvaluatorContext) -> float:
        prompt = self.prompt_builder.build_prompt(payload)
        response = await self.llm.ainvoke(prompt)

        if isinstance(response.content, list):
            raw_text = "".join(
                part if isinstance(part, str) else part.get("text", "")
                for part in response.content
            )
        else:
            raw_text = str(response.content)

        cleaned_text = raw_text.strip()
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned_text)
        if match:
            cleaned_text = match.group(1).strip()

        try:
            data = json.loads(cleaned_text)
            score = float(data.get("score", 1.0))
            return (score - 1.0) / 4.0 
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Failed to parse LLM response: {e}")
            return 0.0