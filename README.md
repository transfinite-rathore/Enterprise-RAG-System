# Enterprise RAG — Production-Oriented RAG System

A production-oriented **Enterprise Retrieval-Augmented Generation (RAG)** system built to explore how large-scale knowledge retrieval systems can be designed with a focus on **modularity, scalability, retrieval quality, evaluation, observability, and maintainability**.

The project goes beyond a basic document chatbot by treating ingestion, retrieval, reranking, generation, and evaluation as independent components that can evolve separately.

---

## Overview

Enterprise knowledge bases can contain millions of documents across different sources and formats. Building a reliable RAG system for such a knowledge base requires more than connecting an LLM to a vector database.

This project explores the engineering challenges involved in building such a system, including:

* Scalable document ingestion
* Parallel and batch processing
* Dense and sparse retrieval
* Reranking
* LLM-based generation
* Retrieval and generation evaluation
* Result persistence
* Observability
* Modular and extensible architecture

The primary goal was to develop a deeper understanding of **RAG systems while applying software engineering and system-design principles**.

---

# High-Level Architecture

```text
                    ┌─────────────────────┐
                    │     Data Sources    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Ingestion Pipeline │
                    │ Load / Process /     │
                    │ Chunk / Embed        │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             Dense Embeddings      Sparse Embeddings
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │    Qdrant Cloud     │
                    └──────────┬──────────┘
                               │
                         User Query
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Retrieval      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Reranking       │
                    │   Cross Encoder     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    LLM Generation  │
                    │      OpenRouter     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Response       │
                    └─────────────────────┘

                    ┌─────────────────────┐
                    │ Evaluation & Result │
                    │      Storage        │
                    └─────────────────────┘
```

---

# Key Highlights

### Modular Architecture

The RAG system is organized into independent components for:

* Data ingestion
* Preprocessing
* Embedding
* Vector storage
* Retrieval
* Reranking
* Generation
* Evaluation
* Result storage

This allows individual components to be replaced or extended without tightly coupling the entire pipeline.

---

### Parallel & Batch Ingestion

The ingestion pipeline is designed for large datasets using:

* **Multiprocessing** for parallel document processing
* **Asynchronous operations** for I/O-bound workloads
* Batch embedding
* Batch vector database writes
* Incremental processing

The design considers the difference between CPU-bound and I/O-bound workloads instead of relying on a single concurrency model.

---

### Dense + Sparse Retrieval

The system supports both semantic and lexical retrieval approaches.

**Dense embeddings** help capture semantic similarity, while **sparse embeddings** help preserve important lexical information such as technical terminology and exact terms.

This provides a foundation for hybrid retrieval in enterprise knowledge systems.

---

### Cross-Encoder Reranking

Retrieved candidates are reranked using a cross-encoder model before being passed to the generation stage.

This creates a two-stage retrieval architecture:

```text
Fast Candidate Retrieval
          ↓
    Candidate Set
          ↓
   Cross-Encoder
          ↓
   Ranked Context
          ↓
      Generation
```

This balances retrieval efficiency with ranking quality.

---

### Offline Evaluation

RAG quality is evaluated separately from the online execution path.

The system stores RAG execution results so that they can be evaluated later without rerunning the complete pipeline.

Evaluation includes retrieval metrics such as:

* **Precision@K**
* **Recall@K**
* **HitRate@K**

Generation quality can additionally be evaluated using reference answers and LLM-based evaluation where appropriate.

---

### Persistent Results

RAG execution results are stored for future analysis.

Persisted information includes the query, retrieved/reranked results, generated response, and execution information.

This provides a foundation for:

* Evaluation
* Debugging
* Regression testing
* Comparing retrieval strategies
* Comparing model versions
* Latency analysis

---

### Observability

Long-running ingestion and RAG operations include structured logging and progress information.

This makes it easier to understand:

* Processing progress
* Ingestion throughput
* Batch processing
* Vector database operations
* Pipeline execution

---

### Extensible Design

The project uses software engineering principles such as:

* Interfaces and abstractions
* Dependency injection
* Factory pattern
* Strategy pattern
* Separation of concerns

The objective is to keep infrastructure-specific implementations separate from the core RAG pipeline.

For example, the retrieval layer is abstracted from the underlying vector database implementation.

---

# Technology Stack

| Category          | Technology                                    |
| ----------------- | --------------------------------------------- |
| Language          | **Python**                                    |
| RAG Framework     | **LangChain**                                 |
| Vector Database   | **Qdrant Cloud**                              |
| LLM               | **OpenRouter**                                |
| Dense Embeddings  | **Sentence Transformers / BGE**               |
| Sparse Retrieval  | **Sparse Encoder**                            |
| Reranking         | **Cross-Encoder**                             |
| Data Processing   | **Pandas / Hugging Face Datasets**            |
| Backend Framework | **FastAPI**                                   |
| Concurrency       | **AsyncIO / Multiprocessing**                 |
| Data Validation   | **Pydantic**                                  |
| Model Persistence | **Locally Saved Embedding & Reranker Models** |
| Language Models   | **Hugging Face Transformers**                 |

> The project uses locally saved model artifacts for important embedding/reranking components, reducing dependence on downloading models during every execution.

---

# Models

The project uses locally persisted models for the retrieval pipeline.

### Dense Embedding Model

**BAAI/bge-small-en-v1.5**

Used to generate dense semantic embeddings.

### Reranker

**Cross-Encoder**

Used to improve the ordering of retrieved candidates before generation.

### Sparse Encoder

A locally persisted sparse encoder is used to generate sparse representations for lexical retrieval.

The models are kept separately from the application logic so that they can be replaced or upgraded independently.

---

# Evaluation

The evaluation pipeline focuses on measuring different stages of the RAG system rather than evaluating only the final answer.

### Retrieval Evaluation

**Precision@K**

Measures the proportion of retrieved results that are relevant.

**Recall@K**

Measures how much of the relevant information was successfully retrieved.

**HitRate@K**

Measures whether at least one relevant result was retrieved within the top K results.

### Generation Evaluation

Generation can be evaluated against reference answers and the retrieved context to assess:

* Answer correctness
* Relevance
* Groundedness

The evaluation workflow is designed to remain independent from the main RAG execution path.

---

# Engineering Focus

The main engineering areas explored in this project are:

### Scalable Processing

Designed ingestion around batching, multiprocessing, asynchronous I/O, and incremental processing.

### Retrieval Architecture

Explored dense retrieval, sparse retrieval, and cross-encoder reranking.

### Software Design

Applied abstraction, interfaces, dependency injection, and design patterns to keep the system modular.

### Evaluation

Built a workflow for measuring retrieval and generation quality instead of relying solely on manual inspection.

### Observability

Persisted pipeline results and maintained logging to support debugging and future analysis.

### Extensibility

Designed major components independently so models, retrieval strategies, vector stores, and evaluation methods can evolve without rewriting the entire system.

---

# What I Learned

This project helped me move from understanding RAG primarily as an AI/ML concept to thinking about it as a **software engineering system**.

Key areas I developed practical experience in:

* Designing RAG pipelines
* Dense and sparse retrieval
* Vector databases
* Embedding and reranking models
* Async programming
* Multiprocessing
* Batch processing
* Backend-oriented architecture
* Interfaces and design patterns
* Evaluation methodology
* Observability and debugging
* Performance and scalability trade-offs

The biggest takeaway was learning to ask:

> **How do I build a RAG system that can be measured, debugged, extended, and scaled — rather than simply making an LLM answer questions?**

---

# Future Work

The current project focuses primarily on the **RAG, ingestion, retrieval, and evaluation layers**.

Planned next steps:

### Backend API

Expose the RAG pipeline through a production-oriented **FastAPI** service.

### User Interface

Build a frontend for:

* Chat interaction
* Source/citation display
* Retrieved context inspection
* Evaluation results
* Query history

### Deployment

Containerize and deploy the system using **Docker** and cloud infrastructure.

### CI/CD

Introduce automated testing, build, and deployment pipelines.

### Production Features

Future iterations can include:

* Authentication and authorization
* Document-level access control
* Caching
* Distributed ingestion
* Queue-based processing
* Horizontal API scaling
* Production monitoring

---

# Project Status

### Completed

* [x] Modular ingestion pipeline
* [x] Document preprocessing
* [x] Batch processing
* [x] Multiprocessing
* [x] Async processing
* [x] Dense embeddings
* [x] Sparse embeddings
* [x] Qdrant vector storage
* [x] Retrieval pipeline
* [x] Cross-encoder reranking
* [x] LLM generation through OpenRouter
* [x] RAG result persistence
* [x] Offline evaluation workflow
* [x] Retrieval metrics
* [x] Logging and observability
* [x] Extensible component architecture

### Future

* [ ] FastAPI serving layer
* [ ] Frontend/UI
* [ ] Docker deployment
* [ ] Cloud deployment
* [ ] Production authentication/authorization
* [ ] Distributed ingestion

---

# Why This Project?

This project was built as a practical exploration of **production-oriented RAG and backend system design**.

Rather than focusing only on getting an LLM to generate an answer, the project focuses on the complete lifecycle:

```text
        Ingest
          ↓
       Process
          ↓
        Embed
          ↓
        Store
          ↓
       Retrieve
          ↓
       Rerank
          ↓
       Generate
          ↓
       Evaluate
          ↓
        Analyze
```

The project demonstrates my ability to combine **Python, backend engineering, machine learning, information retrieval, concurrency, evaluation, and system-design principles** into a single extensible system.
