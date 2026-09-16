prompt="""
        You are an expert evaluator. Determine if the Generated Answer directly addresses the User Query.
        
        User Query: {query}
        Generated Answer: {generated_answer}

        Rate the relevance on a scale of 1 to 5:
        5: Directly and fully answers the query without extra fluff.
        4: Answers the query but includes slight conversational filler or tangential info.
        3: Partially answers the query but misses the core intent.
        2: Vaguely related to the topic, but does not answer the specific query.
        1: Completely unrelated to the query.

        Respond ONLY with a JSON object in this exact format:
        {{"score": 5, "reason": "brief explanation"}}
        """