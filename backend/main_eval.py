import asyncio
from src.config.config_manager import get_config
from src.rag.model.llm_config import LLMConfig
from src.rag.factories.LLMProvider import ChatModelProvider
from src.rag.factories.judge_factory import create_LLM_judge
from src.rag.evaluation_pipeline.file_store.Evaluation_result import EvaluationFileSave
from src.rag.evaluation_pipeline.file_store.Relevance_verdict import RelevanceVerdictFileSave
from src.rag.evaluation_pipeline.evaluation_orchestrator import RAGEvaluationPipeline
from src.rag.evaluation_pipeline.reterival_evaluator import RetrievalEvaluator
from src.rag.evaluation_pipeline.reranker_evaluator import RerankerEvaluator
from src.rag.evaluation_pipeline.generator_evauator import GeneratorEvaluator
from src.rag.evaluation_pipeline.evaluation_metrics.ranking_metric.MRR import MeanReciprocalRank
from src.rag.evaluation_pipeline.evaluation_metrics.ranking_metric.hit_rate import HitRate 
from src.rag.evaluation_pipeline.evaluation_metrics.ranking_metric.NDCG import NDCGAtK
from src.rag.evaluation_pipeline.evaluation_metrics.ranking_metric.precision import PrecisionAtK
from src.rag.evaluation_pipeline.evaluation_metrics.ranking_metric.recall import RecallAtK
from src.rag.evaluation_pipeline.evaluation_metrics.generation_metric.answer_relevance.relevance_evaluator import AnswerRelevanceMetric
from src.rag.evaluation_pipeline.evaluation_metrics.generation_metric.correctness.correctness_evaluator import CorrectnessEvaluationMetric
from src.rag.evaluation_pipeline.evaluation_metrics.generation_metric.faithfullness.faithfullness_evaluator import FaithfullnessEvaluationMetric 
from src.rag.pipelines.resultstore.file_result_store import RAGFileResultStore

async def run_evaluation():
    # 1. Define the reference human answer
    ans = '''From the attached transcript, it is mentioned that SpaceX is a "7,000 person company." This number refers to the total number of employees working at SpaceX at the time of the discussion in the transcript'''
    print("Process Started")
    dir_path=""
# 1. Find out which provider is currently active (returns "open_router")
    llm=get_config()["llm"]
    active_provider_name = llm["active_provider"]

    # 2. Get the settings for that specific provider
    provider_settings = llm["provider"][active_provider_name]

    # 3. Initialize your config using the nested settings
    llm_config = LLMConfig(
        provider=active_provider_name,                 # "open_router"
        model_name=provider_settings["model_name"],    # "nvidia/nemotron-3-super-120b-a12b:free"
        temperature=provider_settings["temperature"]   # 0.5
    )
    

    llm_model = ChatModelProvider(llm_config).get_model()
    
    result_store = RAGFileResultStore()
    run_id="run_f67d3b20bcb3403b96d142ce1df85b66"
    payload = result_store.load(
        run_id
    )
    # # 3. Instantiate the payload (Pydantic will auto-convert the dictionaries)
    # # payload = RAGEvaluationPayload(**file)
    # # print(f"Successfully loaded payload for query: {payload}")
    
    # judge=create_LLM_judge()
    
    # # 6. Run the judge using the updated method signature
    # print("Evaluating chunks...")
    # verdicts = await judge.judge_chunks(
    #     human_answer=ans,
    #     payload=payload
    # )
    # RelevanceVerdictFileSave().save_file(run_id,verdicts)
    
    
######################################################################
#### Create a separate Judge Relevance Orchestartor to keep this clean
######################################################################

    # print("Evaluation Context Saved!!")
    verdicts= RelevanceVerdictFileSave().load_file(run_id)
    print("Evaluation Starting !!")
    precision_metric=PrecisionAtK()
    recall=RecallAtK()
    mrr=MeanReciprocalRank()
    ndcg=NDCGAtK()
    hit_rate=HitRate()
    faithfull=FaithfullnessEvaluationMetric(llm_model)
    correctness=CorrectnessEvaluationMetric(llm_model)
    relevance=AnswerRelevanceMetric(llm_model)
    
    reterival_evaluator=RetrievalEvaluator([precision_metric,recall,mrr,ndcg,hit_rate])
    reranker_evaluator=RerankerEvaluator([precision_metric,recall,mrr,ndcg,hit_rate])
    generator_evaluator=GeneratorEvaluator([faithfull,correctness,relevance])
    
    evaluator=RAGEvaluationPipeline(reterival_evaluator,reranker_evaluator,generator_evaluator)
    result=await evaluator.run(payload,verdicts)
    print(result)
    EvaluationFileSave().save_file(run_id,result)


if __name__ == "__main__":
    asyncio.run(run_evaluation())