prompt="""
        You are an expert evaluator. Compare the Generated Answer to the Reference Answer based on the User Query.
        
        User Query: {query}
        Reference Answer: {human_answer}
        Generated Answer: {generated_answer}

        Rate the factual overlap and correctness on a scale of 1 to 5:
        5: Completely accurate and covers all points in the reference.
        4: Mostly accurate, missing only minor details.
        3: Partially accurate, missing core details but contains no contradictions.
        2: Mostly incorrect or heavily hallucinated.
        1: Completely incorrect or unrelated.

        Respond ONLY with a JSON object in this exact format:
        {{"score": 5, "reason": "brief explanation"}}
        """