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



def create_api_response(status,success_count=None,failed_count=None, data=None, error=None,message=None,file_source=None,file_name=None):
    """
    Create a response to be sent to the API. This is a helper function to create a JSON response that can be sent to the API.
    
    Args:
        status: The status of the API call. Should be one of the constants in this module.
        data: The data that was returned by the API call.
        error: The error that was returned by the API call.
        success_count: Number of files successfully processed.
        failed_count: Number of files failed to process.
    Returns: 
      A dictionary containing the status data and error if any
    """
    response = {"status": status}

    # Set the data of the response
    if data is not None:
      response["data"] = data

    # Set the error message to the response.
    if error is not None:
      response["error"] = error
    
    if success_count is not None:
      response['success_count']=success_count
      response['failed_count']=failed_count
    
    if message is not None:
      response['message']=message

    if file_source is not None:
      response['file_source']=file_source

    if file_name is not None:
      response['file_name']=file_name
      
    return response