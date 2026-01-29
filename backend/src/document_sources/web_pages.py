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

from langchain_community.document_loaders import WebBaseLoader
from src.shared.llm_graph_builder_exception import LLMGraphBuilderException
from src.shared.common_fn import last_url_segment

def get_documents_from_web_page(source_url:str):
  try:
    pages = WebBaseLoader(source_url, verify_ssl=False).load()
    return pages
  except Exception as e:
    raise LLMGraphBuilderException(str(e))
