"""
KnowledgeCatalyst - Knowledge Graph RAG System
Copyright (C) 2025 DXC Technology Company

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import List
import logging
from src.llm import get_combined_chunks, get_llm

logging.basicConfig(format='%(asctime)s - %(message)s',level='INFO')

def get_graph_from_diffbot(graph,chunkId_chunkDoc_list:List):
    combined_chunk_document_list = get_combined_chunks(chunkId_chunkDoc_list)
    llm,model_name = get_llm('diffbot')
    graph_documents = llm.convert_to_graph_documents(combined_chunk_document_list)
    return graph_documents
