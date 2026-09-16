from __future__ import annotations
from abc import ABC, abstractmethod
from langchain_core.documents import Document
from typing import Iterable


class ChunkingStrategy(ABC):
    @abstractmethod
    def chunk_document(self,document:Document) -> Iterable[Document]:
        pass
