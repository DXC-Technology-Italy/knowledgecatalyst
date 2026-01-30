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

from datetime import datetime

class sourceNode:
    file_name:str=None
    file_size:int=None
    file_type:str=None
    file_source:str=None
    status:str=None
    url:str=None
    gcsBucket:str=None
    gcsBucketFolder:str=None
    gcsProjectId:str=None
    awsAccessKeyId:str=None
    chunkNodeCount:int=None
    chunkRelCount:int=None
    entityNodeCount:int=None
    entityEntityRelCount:int=None
    communityNodeCount:int=None
    communityRelCount:int=None
    node_count:int=None
    relationship_count:str=None
    model:str=None
    created_at:datetime=None
    updated_at:datetime=None
    processing_time:float=None
    error_message:str=None
    total_chunks:int=None
    language:str=None
    is_cancelled:bool=None
    processed_chunk:int=None
    access_token:str=None
    retry_condition:str=None
