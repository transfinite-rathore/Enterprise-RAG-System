prompt = """
Evaluate the relevance of multiple retrieved context chunks against the question and reference answer.

Question: {query}
Reference Answer: {human_answer}

Context Chunks:
{formatted_chunks_json}

Evaluation Rubric:
- Score 5: Perfect match. Contains the exact information needed to formulate the reference answer.
- Score 4: Highly relevant. Contains most of the necessary information, missing only minor details.
- Score 3: Partially relevant. Contains related background information, but cannot fully answer the question alone.
- Score 2: Marginally relevant. Shares keywords or topics, but does not help answer the specific question.
- Score 1: Completely irrelevant.

Relevance Threshold:
Set "relevant": true ONLY if the score is 3, 4, or 5. Otherwise, set it to false.

Respond ONLY with a valid JSON array of objects matching this exact schema for every chunk provided. Do not include markdown formatting like ```json.
[
    {{"chunk_id": "id", "relevant": true/false, "reason": "brief explanation", "score": 1-5}}
]
"""