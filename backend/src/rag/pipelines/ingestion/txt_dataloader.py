import os
import uuid
import pandas as pd
from typing import List,Iterable
from pathlib import Path
from langchain_core.documents import Document
# from ...factories
from ...factories.DataLoader import DataLoader
# from ..factories.DataLoader import DataLoader

class TxtDataLoader(DataLoader):

    def __init__(
        self,
        file_path: str,
        metadata_file_path: str = ""
    ) -> None:
        self.file_path = Path(file_path)
        self.metadata_file_path = (
            Path(metadata_file_path)
            if metadata_file_path
            else None
        )

    # def load_document(self) -> Iterable[Document]:
    #     metadata_df = None

    #     if (
    #         self.metadata_file_path
    #         and self.metadata_file_path.suffix.lower() == ".csv"
    #     ):
    #         metadata_df = pd.read_csv(self.metadata_file_path)

    #         # Add document_id column if it doesn't exist
    #         if "document_id" not in metadata_df.columns:
    #             metadata_df["document_id"] = pd.NA
    #     # count=25
    #     for file_path in self.file_path.iterdir():

    #         if not file_path.is_file():
    #             continue

    #         if file_path.suffix.lower() != ".txt":
    #             continue

    #         with file_path.open(
    #             mode="r",
    #             encoding="utf-8"
    #         ) as file:
    #             data = file.read()

    #         metadata = {}

    #         if metadata_df is not None:

    #             metadata_rows = metadata_df.loc[
    #                 metadata_df["file_name"] == file_path.stem
    #             ]

    #             if not metadata_rows.empty:

    #                 row_index = metadata_rows.index[0]
    #                 metadata = metadata_rows.iloc[0].to_dict()

    #                 # Standardize metadata name
    #                 metadata["title"] = metadata.pop("post_title")

    #                 # Reuse existing ID
    #                 document_id = metadata_df.at[
    #                     row_index,
    #                     "document_id"
    #                 ]

    #                 # Generate ID only if missing
    #                 if pd.isna(document_id) or document_id == "":
    #                     document_id = str(uuid.uuid4())

    #                     metadata_df.at[
    #                         row_index,
    #                         "document_id"
    #                     ] = document_id

    #                 metadata["document_id"] = document_id
    #         # count-=1
    #         # if count==0:
    #         #     return
    #         yield Document(
    #             page_content=data,
    #             metadata=metadata
    #         )

    #     # Save updated IDs back to CSV
    #     if metadata_df is not None:
    #         metadata_df.to_csv(
    #             self.metadata_file_path,
    #             index=False
    #         )
    def load_document(self) -> Iterable[Document]:
        metadata_df = None
        metadata_lookup = {}

        if self.metadata_file_path and self.metadata_file_path.suffix.lower() == ".csv":
            metadata_df = pd.read_csv(self.metadata_file_path)
            if "document_id" not in metadata_df.columns:
                metadata_df["document_id"] = pd.NA
            # Build an O(1) lookup once, instead of filtering the whole df per file
            metadata_lookup = {
                stem: idx for idx, stem in metadata_df["file_name"].items()
            }

        for file_path in self.file_path.iterdir():
            if not file_path.is_file() or file_path.suffix.lower() != ".txt":
                continue

            with file_path.open(mode="r", encoding="utf-8") as file:
                data = file.read()

            metadata = {}
            if metadata_df is not None:
                row_index = metadata_lookup.get(file_path.stem)
                if row_index is not None:
                    metadata = metadata_df.iloc[row_index].to_dict()
                    metadata["title"] = metadata.pop("post_title")
                    metadata.pop("content", None)
                    document_id = metadata_df.at[row_index, "document_id"]
                    if pd.isna(document_id) or document_id == "":
                        document_id = str(uuid.uuid4())
                        metadata_df.at[row_index, "document_id"] = document_id
                    metadata["document_id"] = document_id

            yield Document(page_content=data, metadata=metadata)

        if metadata_df is not None:
            metadata_df.to_csv(self.metadata_file_path, index=False)
            