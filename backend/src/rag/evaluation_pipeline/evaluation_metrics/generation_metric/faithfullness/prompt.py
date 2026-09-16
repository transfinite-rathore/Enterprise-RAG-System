prompt="""
        You are an strict fact-checker. Determine if the Generated Answer can be directly inferred from the Provided Context.
        
        Provided Context:
        {context_string}
        
        Generated Answer: 
        {generated_answer}

        Are all claims in the Generated Answer fully supported by the Provided Context?
        Score 1 if completely supported (faithful).
        Score 0 if the answer contains details, numbers, or claims NOT found in the context (hallucination).

        Respond ONLY with a JSON object in this exact format:
        {{"score": 1, "reason": "brief explanation"}}
        """