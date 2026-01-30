"""
SPDX-License-Identifier: AGPL-3.0-or-later
SPDX-FileCopyrightText: 2026 DXC Technology Company

KnowledgeCatalyst - Knowledge Graph RAG System
Copyright (C) 2026 DXC Technology Company

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

import logging
from langchain_community.document_loaders import WikipediaLoader
from src.shared.llm_graph_builder_exception import LLMGraphBuilderException

def get_documents_from_Wikipedia(wiki_query:str, language:str):
  try:
    pages = WikipediaLoader(query=wiki_query.strip(), lang=language, load_all_available_meta=False,doc_content_chars_max=100000,load_max_docs=1).load()
    file_name = wiki_query.strip()
    logging.info(f"Total Pages from Wikipedia = {len(pages)}") 
    return file_name, pages
  except Exception as e:
    message="Failed To Process Wikipedia Query"
    error_message = str(e)
    logging.exception(f'Failed To Process Wikipedia Query: {file_name}, Exception Stack trace: {error_message}')
    raise LLMGraphBuilderException(error_message+' '+message)
  