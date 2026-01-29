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

import streamlit as st
import requests
import json
import os
import pandas as pd
from urllib.parse import urlparse
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

# --- Helper Functions (from your original code - kept for consistency) ---

DEFAULT_BACKEND_URL = "http://backend:8000"


def drop_create_vector_index(uri, username, password, database):
    data = {
        'uri': uri.replace(" ", "+") if " " in uri else uri,
        'userName': username,
        'password': password,
        'database': database,
        'isVectorIndexExist': 'true',
        'email': ''
    }
    try:
        fixed_backend_url = get_valid_backend_url()
        response = requests.post(f'{fixed_backend_url}/drop_create_vector_index', data=data)
        return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return {"status": "Failed", "error": str(e)}


def delete_documents(uri, username, password, database, filenames, source_types, delete_entities=True):
    """Delete documents from the knowledge graph"""
    data = {
        'uri': uri.replace(" ", "+") if " " in uri else uri,
        'userName': username,
        'password': password,
        'database': database,
        'filenames': json.dumps(filenames),
        'source_types': json.dumps(source_types),
        'deleteEntities': 'true' if delete_entities else 'false',
        'email': ''
    }
    try:
        fixed_backend_url = get_valid_backend_url()
        response = requests.post(f'{fixed_backend_url}/delete_document_and_entities', data=data)
        return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return {"status": "Failed", "error": str(e)}

def get_valid_backend_url():
    """Gets and validates the backend URL, falling back to a default if necessary."""
    backend_url = os.environ.get('BACKEND_URL', DEFAULT_BACKEND_URL)
    parsed_url = urlparse(backend_url)
    if parsed_url.netloc:  # Check for a valid network location (hostname)
        return backend_url
    else:
        st.error(f"Invalid BACKEND_URL: '{backend_url}'. Using default: {DEFAULT_BACKEND_URL}")
        return DEFAULT_BACKEND_URL


def connect_to_neo4j(uri, username, password, database):
    data = {
        'uri': uri.replace(" ", "+") if " " in uri else uri,
        'userName': username,
        'password': password,
        'database': database,
        'email': ''
    }
    fixed_backend_url = get_valid_backend_url()
    response = requests.post(f'{fixed_backend_url}/connect', data=data)
    return response.json()


def upload_file(uri, username, password, database, file, model="azure_ai_gpt_4o_mini"):
    # Helper function for file uploads (keeps chunking logic)
    uri = uri.replace(" ", "+") if " " in uri else uri
    try:
        file_size = len(file.getvalue())
        chunk_size = 5 * 1024 * 1024  # 5MB chunks
        total_chunks = (file_size + chunk_size - 1) // chunk_size
        file_name = file.name
        file_content = file.getvalue()
        for i in range(total_chunks):
            chunk_start = i * chunk_size
            chunk_end = min((i + 1) * chunk_size, file_size)
            chunk_data = file_content[chunk_start:chunk_end]
            form_data = {
                'uri': uri,
                'userName': username,
                'password': password,
                'database': database,
                'chunkNumber': str(i + 1),
                'totalChunks': str(total_chunks),
                'originalname': file_name,
                'model': model,
                'email': ''
            }
            files = {'file': (file_name, chunk_data, 'application/octet-stream')}
            fixed_backend_url = get_valid_backend_url()
            response = requests.post(f'{fixed_backend_url}/upload', data=form_data, files=files)
            if response.status_code != 200:
                st.error(f"Error uploading chunk {i + 1}/{total_chunks}")
                return {"status": "Failed", "error": "Upload failed"}
            if i + 1 == total_chunks:
                return response.json()
        return {"status": "Failed", "error": "Upload incomplete"}
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return {"status": "Failed", "error": str(e)}


def extract_knowledge_graph(uri, username, password, database, source_type, file_name, model="azure_ai_gpt_4o_mini",
                            additional_params=None):
    # Simplified for clarity.  Keeps core functionality.
    uri = uri.replace(" ", "+") if " " in uri else uri
    data = {
        'uri': uri, 'userName': username, 'password': password, 'database': database,
        'source_type': source_type, 'file_name': file_name, 'model': model,
        'email': '', 'allowedNodes': '', 'allowedRelationship': ''  # Remove allowedNodes and allowedRelationship
    }
    if additional_params:
        data.update(additional_params)
    try:
        fixed_backend_url = get_valid_backend_url()
        response = requests.post(f'{fixed_backend_url}/extract', data=data)
        return response.json()
    except Exception as e:
        st.error(f"Error extracting knowledge graph: {str(e)}")
        return {"status": "Failed", "error": str(e)}


def chat_bot(uri, username, password, database, question, document_names, model="azure_ai_gpt_4o_mini", mode="vector"):
    # Simplified for clarity, keeping core functionality.
    uri = uri.replace(" ", "+") if " " in uri else uri
    data = {
        'uri': uri, 'userName': username, 'password': password, 'database': database,
        'question': question, 'document_names': json.dumps(document_names),
        'model': model, 'session_id': "session_" + str(hash(uri + username + database))[:10],
        'mode': mode, 'email': ''
    }
    try:
        fixed_backend_url = get_valid_backend_url()
        response = requests.post(f'{fixed_backend_url}/chat_bot', data=data)
        return response.json()
    except Exception as e:
        st.error(f"Error chatting with bot: {str(e)}")
        return {"status": "Failed", "error": str(e)}


def get_source_list(uri, username, password, database):
    if " " in uri:
        uri = uri.replace(" ", "+")
    data = {
        'uri': uri,
        'userName': username,
        'password': password,
        'database': database,
        'email': ''
    }
    try:
        fixed_backend_url = get_valid_backend_url()
        response = requests.post(f'{fixed_backend_url}/sources_list', data=data)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching sources: {str(e)}")
        return {"status": "Failed", "error": str(e)}


def get_graph_data(uri, username, password, database, document_names):
    """Fetch graph data from backend /graph_query endpoint"""
    if " " in uri:
        uri = uri.replace(" ", "+")
    data = {
        'uri': uri,
        'userName': username,
        'password': password,
        'database': database,
        'document_names': json.dumps(document_names),
        'email': ''
    }
    try:
        fixed_backend_url = get_valid_backend_url()
        response = requests.post(f'{fixed_backend_url}/graph_query', data=data)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching graph data: {str(e)}")
        return {"status": "Failed", "error": str(e)}


def get_schema_data(uri, username, password, database):
    """Fetch schema visualization data from backend"""
    if " " in uri:
        uri = uri.replace(" ", "+")
    data = {
        'uri': uri,
        'userName': username,
        'password': password,
        'database': database,
        'email': ''
    }
    try:
        fixed_backend_url = get_valid_backend_url()
        response = requests.post(f'{fixed_backend_url}/schema_visualization', data=data)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching schema data: {str(e)}")
        return {"status": "Failed", "error": str(e)}


def get_visible_nodes(all_nodes, all_relationships, expanded_node_ids, view_type="data"):
    """
    Determine which nodes should be visible based on expanded state.
    Initially shows Documents and all nodes one step away from Documents.
    When a node is expanded, it shows its direct neighbors.
    """
    if view_type == "schema":
        # For schema view, show everything
        return all_nodes, all_relationships

    visible_node_ids = set()
    node_id_to_node = {node.get('element_id'): node for node in all_nodes}
    document_ids = set()

    # Step 1: Add all Documents
    for node in all_nodes:
        labels = node.get('labels', [])
        if labels and labels[0] == 'Document':
            node_id = node.get('element_id')
            visible_node_ids.add(node_id)
            document_ids.add(node_id)

    # Step 2: Add all nodes one step away from Documents (first-degree neighbors)
    for rel in all_relationships:
        start_id = rel.get('start_node_element_id', '')
        end_id = rel.get('end_node_element_id', '')

        if start_id in document_ids:
            visible_node_ids.add(end_id)
        if end_id in document_ids:
            visible_node_ids.add(start_id)

    # Step 3: For each expanded node, add its direct neighbors
    if expanded_node_ids:
        for rel in all_relationships:
            start_id = rel.get('start_node_element_id', '')
            end_id = rel.get('end_node_element_id', '')

            if start_id in expanded_node_ids:
                visible_node_ids.add(end_id)
            if end_id in expanded_node_ids:
                visible_node_ids.add(start_id)

    # Filter nodes and relationships
    visible_nodes = [node for node in all_nodes if node.get('element_id') in visible_node_ids]
    visible_relationships = [
        rel for rel in all_relationships
        if rel.get('start_node_element_id') in visible_node_ids
        and rel.get('end_node_element_id') in visible_node_ids
    ]

    return visible_nodes, visible_relationships


def render_graph_visualization(nodes, relationships, view_type="data", expanded_nodes=None):
    """Render graph visualization using PyVis"""
    # Define color scheme for entity types
    color_scheme = {
        'Document': '#3b82f6',
        'Chunk': '#8b5cf6',
        'Person': '#10b981',
        'Organization': '#f59e0b',
        'Location': '#ef4444',
        'Event': '#ec4899',
        'Concept': '#06b6d4',
        'Technology': '#8b5cf6',
        '__Community__': '#64748b',
        '__Entity__': '#94a3b8'
    }

    expanded_nodes = expanded_nodes or set()

    # Create PyVis network
    net = Network(height='700px', width='100%', bgcolor='#ffffff', font_color='#000000')

    # Configure physics to be OFF (static layout)
    net.set_options("""
    {
        "physics": {
            "enabled": false
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "zoomView": true
        },
        "nodes": {
            "font": {
                "size": 14
            }
        },
        "edges": {
            "color": {
                "color": "#888888",
                "highlight": "#000000"
            },
            "smooth": {
                "enabled": true,
                "type": "continuous"
            }
        }
    }
    """)

    # Build networkx graph for layout computation
    G = nx.DiGraph()
    node_id_map = {}

    for node in nodes:
        node_id = node.get('element_id', '')
        G.add_node(node_id)
        node_id_map[node_id] = node

    for rel in relationships:
        start_node = rel.get('start_node_element_id', '')
        end_node = rel.get('end_node_element_id', '')
        if start_node and end_node:
            G.add_edge(start_node, end_node)

    # Compute static layout using Kamada-Kawai (better distribution, less circular)
    if len(G.nodes()) > 0:
        pos = nx.kamada_kawai_layout(G, scale=1000)
    else:
        pos = {}

    # Add nodes to PyVis network
    for node in nodes:
        node_id = node.get('element_id', '')
        if node_id in pos:
            labels = node.get('labels', [])
            properties = node.get('properties', {})

            # Get node label/caption
            node_caption = properties.get('id') or properties.get('name') or properties.get('fileName') or (labels[0] if labels else 'Node')

            # Get color based on first label
            node_color = color_scheme.get(labels[0], '#94a3b8') if labels else '#94a3b8'

            # Create hover title with properties
            title = f"<b>{node_caption}</b><br>"
            title += f"Type: {', '.join(labels)}<br>"
            if node_id in expanded_nodes:
                title += f"<i>Expanded</i><br>"
            for key, value in properties.items():
                if key not in ['embedding', 'text', 'summary'] and value:
                    title += f"{key}: {str(value)[:100]}<br>"

            # Node size - larger for expanded nodes
            size = 25 if node_id in expanded_nodes else (20 if view_type == 'data' else 30)

            # Add node with fixed position
            x, y = pos[node_id]
            net.add_node(
                node_id,
                label=str(node_caption)[:30],  # Truncate long labels
                title=title,
                color=node_color,
                size=size,
                x=float(x),
                y=float(y),
                physics=False  # Disable physics for this node
            )

    # Add edges to PyVis network
    for rel in relationships:
        start_node = rel.get('start_node_element_id', '')
        end_node = rel.get('end_node_element_id', '')
        rel_type = rel.get('type', '')

        if start_node in pos and end_node in pos:
            net.add_edge(start_node, end_node, title=rel_type)

    # Generate HTML
    html = net.generate_html()

    # Render in Streamlit
    components.html(html, height=720, scrolling=False)


# --- Streamlit App Setup ---

if 'connected' not in st.session_state:
    st.session_state.connected = False
    st.session_state.connection_info = {}
    st.session_state.sources = []
    st.session_state.selected_sources = []
    st.session_state.chat_history = []
    st.session_state.expanded_nodes = set()  # Track expanded nodes for graph viz
    st.session_state.all_graph_nodes = []  # Store complete node data
    st.session_state.all_graph_relationships = []  # Store complete relationship data

st.title("Knowledge Graph Builder")

# --- Sidebar: Database Connection ---
with st.sidebar:
    st.header("Database Connection")
    with st.form("neo4j_connection"):
        uri = st.text_input("URI", value=os.environ.get('NEO4J_URI', ''))
        username = st.text_input("Username", value=os.environ.get('NEO4J_USERNAME', ''))
        password = st.text_input("Password", type="password", value=os.environ.get('NEO4J_PASSWORD', ''))
        database = st.text_input("Database", value=os.environ.get('NEO4J_DATABASE', 'neo4j'))
        connect_button = st.form_submit_button("Connect")

        if connect_button:
            with st.spinner("Connecting to Neo4j..."):
                response = connect_to_neo4j(uri, username, password, database)
                if response.get("status") == "Success":
                    st.success("Connection successful!")
                    st.session_state.connected = True
                    st.session_state.connection_info = {'uri': uri, 'userName': username, 'password': password,
                                                        'database': database}
                    # Get the source files.
                    sources_response = get_source_list(uri, username, password, database)
                    if sources_response.get("status") == "Success":
                        st.session_state.sources = sources_response.get("data", [])
                    else:
                        st.error(f"Failed to fetch sources: {sources_response.get('message', 'Unknown error')}")

                    st.rerun()  # Re-run to update the main area.
                else:
                    st.error(f"Connection failed: {response.get('message', 'Unknown error')}")

    if st.session_state.connected:
        st.success("✅ Connected to Neo4j")

# --- Main Area: Tabs ---
if not st.session_state.connected:
    st.info("Please connect to Neo4j database first.")

else:
    tab1, tab2, tab3, tab4 = st.tabs(["Upload & Extract", "Chat", "Graph Visualization", "Admin"])

    with tab1:  # Upload & Extract Documents
        st.header("Upload & Extract Knowledge Graph")
        upload_type = st.selectbox("Select upload type", ["File Upload", "Web URL", "YouTube", "Wikipedia"])
        model = st.selectbox("Model", ["azure_ai_gpt_4o_mini", "openai_gpt_4o", "gemini_1.5_pro"])

        if upload_type == "File Upload":
            uploaded_files = st.file_uploader("Choose files", type=["pdf", "txt", "csv", "json", "xlsx"],
                                              accept_multiple_files=True)
            if uploaded_files and st.button("Upload Files"):
                for file in uploaded_files:
                    with st.spinner(f"Uploading {file.name}..."):
                        response = upload_file(st.session_state.connection_info['uri'],
                                               st.session_state.connection_info['userName'],
                                               st.session_state.connection_info['password'],
                                               st.session_state.connection_info['database'], file, model)
                        if response.get("status") == "Success":
                            st.success(f"Uploaded {file.name}")
                        else:
                            st.error(f"Failed to upload {file.name}: {response.get('message', 'Unknown error')}")
                # Refresh the source file list
                sources_response = get_source_list(st.session_state.connection_info['uri'],
                                                   st.session_state.connection_info['userName'],
                                                   st.session_state.connection_info['password'],
                                                   st.session_state.connection_info['database'])
                if sources_response.get("status") == "Success":
                    st.session_state.sources = sources_response.get("data", [])
                else:
                    st.error(f"Failed to fetch sources: {sources_response.get('message', 'Unknown error')}")

        elif upload_type in ["Web URL", "YouTube", "Wikipedia"]:  # Handles the other types of sources
            url = st.text_input("Enter URL" if upload_type != "Wikipedia" else "Enter Wikipedia Article")
            if url and st.button(f"Process {upload_type}"):
                with st.spinner(f"Processing {upload_type}..."):
                    source_type = upload_type.lower().replace(" ", "-")
                    if source_type == "wikipedia":
                        additional_params = {"wiki_query": url, "language": "en"}  # Add parameters to wikipedia call
                    else:
                        additional_params = {"source_url": url}  # Parameter for youtube or web url
                    response = extract_knowledge_graph(
                        st.session_state.connection_info['uri'],
                        st.session_state.connection_info['userName'],
                        st.session_state.connection_info['password'],
                        st.session_state.connection_info['database'],
                        source_type,
                        "",  # file_name is not needed for URLs
                        model,
                        additional_params
                    )
                    if response.get("status") == "Success":
                        st.success(f"Successfully processed {upload_type}: {url}")
                        # Refresh sources
                        sources_response = get_source_list(st.session_state.connection_info['uri'],
                                                           st.session_state.connection_info['userName'],
                                                           st.session_state.connection_info['password'],
                                                           st.session_state.connection_info['database'])
                        if sources_response.get("status") == "Success":
                            st.session_state.sources = sources_response.get("data", [])
                        else:
                            st.error(f"Failed to fetch sources: {sources_response.get('message', 'Unknown error')}")

                    else:
                        st.error(f"Failed to process {upload_type}: {response.get('message', 'Unknown error')}")

        st.markdown("---")
        st.header("Build Knowledge Graph")

        # Refresh button
        if st.button("Refresh Source List"):
            with st.spinner("Fetching sources..."):
                sources_response = get_source_list(
                    st.session_state.connection_info.get('uri'),
                    st.session_state.connection_info.get('userName'),
                    st.session_state.connection_info.get('password'),
                    st.session_state.connection_info.get('database')
                )
                if sources_response.get("status") == "Success":
                    st.session_state.sources = sources_response.get("data", [])
                    st.success("Sources refreshed successfully!")
                else:
                    st.error(f"Failed to refresh sources: {sources_response.get('message', 'Unknown error')}")

        if st.session_state.sources:
            # Convert sources to DataFrame for display
            source_data = []
            for source in st.session_state.sources:
                chunks = source.get("total_chunks", 0)
                entities = source.get("nodeCount", 0)

                # Add status indicator
                status = source.get("status", "")
                if status == "Completed" and chunks > 1 and entities > 0:
                    status_icon = "✅"
                elif status == "Completed" and (chunks <= 1 or entities == 0):
                    status_icon = "⚠️"
                elif status == "Processing":
                    status_icon = "🔄"
                else:
                    status_icon = "❓"

                source_data.append({
                    "": status_icon,
                    "File Name": source.get("fileName", ""),
                    "Status": status,
                    "Chunks": chunks,
                    "Entities": entities,
                    "File Size": source.get("fileSize", ""),
                    "File Type": source.get("fileType", "")
                })
            df = pd.DataFrame(source_data)

            st.dataframe(df, use_container_width=True)

            # Show legend
            st.caption("✅ Ready | ⚠️ Low content extracted | 🔄 Processing | ❓ Unknown")

            # Check for problematic documents
            low_content_docs = [s.get("fileName") for s in st.session_state.sources
                               if s.get("status") == "Completed" and s.get("total_chunks", 0) <= 1]
            if low_content_docs:
                st.warning(f"⚠️ These documents have minimal content extracted (likely only title): {', '.join(low_content_docs)}. "
                          "Delete them in the Admin tab and re-upload for better results.")

            # Multiselect for source extraction
            extraction_selection = st.multiselect(
                "Select sources to extract knowledge graph",
                options=[s.get("fileName") for s in st.session_state.sources],
                help="Select files to process and build the knowledge graph. This will take a few minutes per document."
            )

            # Extraction button
            if extraction_selection:
                if st.button("🚀 Extract Knowledge Graph for Selected Sources", type="primary"):
                    progress_bar = st.progress(0)
                    total_docs = len(extraction_selection)

                    for idx, source in enumerate(extraction_selection):
                        source_info = next((s for s in st.session_state.sources if s.get("fileName") == source), None)
                        if source_info:
                            progress_bar.progress((idx) / total_docs, text=f"Processing {idx+1}/{total_docs}: {source}")
                            with st.spinner(f"Extracting knowledge graph for {source}..."):
                                response = extract_knowledge_graph(
                                    st.session_state.connection_info.get('uri'),
                                    st.session_state.connection_info.get('userName'),
                                    st.session_state.connection_info.get('password'),
                                    st.session_state.connection_info.get('database'),
                                    source_info.get("fileSource", ""),
                                    source,
                                    model="azure_ai_gpt_4o_mini"
                                )
                                if response.get("status") == "Success":
                                    st.success(f"✅ Successfully extracted knowledge graph for {source}")
                                else:
                                    st.error(f"❌ Failed to extract knowledge graph for {source}: {response.get('message', 'Unknown error')}")

                    progress_bar.progress(1.0, text="Complete!")
                    st.info("🔄 Refreshing source list...")

                    # Refresh sources to show updated stats
                    sources_response = get_source_list(
                        st.session_state.connection_info.get('uri'),
                        st.session_state.connection_info.get('userName'),
                        st.session_state.connection_info.get('password'),
                        st.session_state.connection_info.get('database')
                    )
                    if sources_response.get("status") == "Success":
                        st.session_state.sources = sources_response.get("data", [])

                    st.rerun()
        else:
            st.info("📤 No sources found. Upload files above to get started.")

    with tab2:  # Chat
        st.header("Chat with your Knowledge Graph")

        # Document selection for chat
        if st.session_state.sources:
            st.subheader("Select Documents")
            selection = st.multiselect(
                "Choose documents to query",
                options=[source.get("fileName") for source in st.session_state.sources],
                default=st.session_state.selected_sources,
                help="Select which documents you want to query. Leave empty to query all documents."
            )
            st.session_state.selected_sources = selection

            if st.session_state.selected_sources:
                st.info(f"📄 Querying: {', '.join(st.session_state.selected_sources)}")
            else:
                st.info("📚 Querying all documents")
        else:
            st.warning("⚠️ No documents found. Upload and extract documents first.")

        st.markdown("---")

        # Model and mode selection in columns
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            chat_model = st.selectbox("Chat Model", ["azure_ai_gpt_4o_mini", "openai_gpt_4o", "gemini_1.5_pro"])
        with col2:
            chat_mode = st.selectbox("Chat Mode", ["vector", "graph+vector", "graph"])
        with col3:
            st.write("")  # Spacer
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        st.markdown("---")

        # Chat history display (show before input for better UX)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.write(f'🧑 **You**: {msg["content"]}')
            else:
                st.write(f'🤖 **Bot**: {msg["content"]}')
                if "info" in msg and "sources" in msg["info"] and msg["info"]["sources"]:
                    with st.expander("📚 Sources"):
                        for source in msg["info"]["sources"]:
                            st.write(f"- {source}")

        # Chat input with Enter key support
        user_input = st.chat_input("Ask a question (press Enter to send)")

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = chat_bot(
                    st.session_state.connection_info.get('uri'),
                    st.session_state.connection_info.get('userName'),
                    st.session_state.connection_info.get('password'),
                    st.session_state.connection_info.get('database'),
                    user_input,
                    st.session_state.selected_sources,
                    chat_model,
                    chat_mode
                )

                if response.get("status") == "Success":
                    data = response.get("data", {})
                    bot_message = data.get("message", "")
                    st.session_state.chat_history.append(
                        {"role": "bot", "content": bot_message, "info": data.get("info", {})})
                else:
                    error_msg = f"Error: {response.get('message', 'Unknown error')}"
                    st.session_state.chat_history.append(
                        {"role": "bot", "content": error_msg})

                st.rerun()

    with tab3:  # Graph Visualization
        st.header("Graph Visualization")

        # View type toggle
        view_type = st.radio("View Type", ["Data", "Schema"], horizontal=True)

        if view_type == "Data":
            # Fetch all documents for graph query
            if st.session_state.sources:
                document_names = [source.get('fileName') for source in st.session_state.sources]

                # Load graph data only if not already loaded
                if not st.session_state.all_graph_nodes:
                    with st.spinner("Loading graph data..."):
                        graph_data = get_graph_data(
                            st.session_state.connection_info['uri'],
                            st.session_state.connection_info['userName'],
                            st.session_state.connection_info['password'],
                            st.session_state.connection_info['database'],
                            document_names
                        )

                    if graph_data.get("status") == "Failed":
                        st.error(f"Error loading graph: {graph_data.get('error', 'Unknown error')}")
                    elif graph_data.get("status") == "Success" and "data" in graph_data:
                        data = graph_data.get("data", {})
                        st.session_state.all_graph_nodes = data.get("nodes", [])
                        st.session_state.all_graph_relationships = data.get("relationships", [])
                    else:
                        st.error("Unexpected response format from backend")

                # Use cached data
                all_nodes = st.session_state.all_graph_nodes
                all_relationships = st.session_state.all_graph_relationships

                if all_nodes:
                    # Create expandable node selector
                    with st.expander("🔍 Expand Documents (Show Entities & Chunks)", expanded=False):
                        # Get list of Document nodes for selection
                        expandable_nodes = []
                        node_id_to_label = {}
                        for node in all_nodes:
                            labels = node.get('labels', [])
                            if labels and labels[0] == 'Document':
                                node_id = node.get('element_id', '')
                                properties = node.get('properties', {})
                                node_label = properties.get('fileName') or properties.get('id') or node_id
                                expandable_nodes.append(node_label)
                                node_id_to_label[node_label] = node_id

                        # Multiselect for node expansion
                        selected_labels = st.multiselect(
                            "Select documents to expand (shows connected entities and chunks)",
                            options=expandable_nodes,
                            default=[],
                            key="expand_selector"
                        )

                        # Convert selected labels to node IDs
                        st.session_state.expanded_nodes = {node_id_to_label[label] for label in selected_labels if label in node_id_to_label}

                        col_reset, col_help = st.columns([1, 3])
                        with col_reset:
                            if st.button("Reset View"):
                                st.session_state.expanded_nodes = set()
                                st.rerun()
                        with col_help:
                            st.caption(f"💡 {len(st.session_state.expanded_nodes)} documents expanded")

                    # Get visible nodes based on expansion state
                    visible_nodes, visible_relationships = get_visible_nodes(
                        all_nodes,
                        all_relationships,
                        st.session_state.expanded_nodes,
                        view_type="data"
                    )

                    # Show statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Nodes", len(all_nodes))
                    with col2:
                        st.metric("Visible Nodes", len(visible_nodes))
                    with col3:
                        st.metric("Relationships", len(all_relationships))
                    with col4:
                        st.metric("Expanded", len(st.session_state.expanded_nodes))

                    if len(visible_nodes) == 0:
                        st.info("No nodes to display.")
                    else:
                        # Render graph
                        render_graph_visualization(
                            visible_nodes,
                            visible_relationships,
                            view_type="data",
                            expanded_nodes=st.session_state.expanded_nodes
                        )
                else:
                    st.info("No graph data found. Upload and extract documents first.")
            else:
                st.info("No documents found. Upload documents in the 'Upload & Extract' tab first.")

        else:  # Schema view
            with st.spinner("Loading schema..."):
                schema_data = get_schema_data(
                    st.session_state.connection_info['uri'],
                    st.session_state.connection_info['userName'],
                    st.session_state.connection_info['password'],
                    st.session_state.connection_info['database']
                )

            if schema_data.get("status") == "Failed":
                st.error(f"Error loading schema: {schema_data.get('error', 'Unknown error')}")
            elif schema_data.get("status") == "Success" and "data" in schema_data:
                data = schema_data.get("data", {})
                nodes = data.get("nodes", [])
                relationships = data.get("relationships", [])

                # Show statistics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Entity Types", len(nodes))
                with col2:
                    st.metric("Relationship Types", len(relationships))

                if len(nodes) == 0:
                    st.info("No schema found. Extract documents first to build the knowledge graph schema.")
                else:
                    # Render schema
                    render_graph_visualization(nodes, relationships, view_type="schema")
            else:
                st.error("Unexpected response format from backend")

    with tab4:  # Admin
        st.header("Admin Functions")

        # Fix vector index section
        st.subheader("Fix Vector Index")
        st.markdown("""
        If you're experiencing issues with vector or graph+vector chat modes due to dimension mismatches,
        use this function to recreate the vector index with the correct dimensions.
        """)

        if st.button("Drop and Recreate Vector Index"):
            with st.spinner("Fixing vector index..."):
                response = drop_create_vector_index(
                    st.session_state.connection_info.get('uri'),
                    st.session_state.connection_info.get('userName'),
                    st.session_state.connection_info.get('password'),
                    st.session_state.connection_info.get('database')
                )
                if response.get("status") == "Success":
                    st.success(f"Vector index fixed successfully: {response.get('message', '')}")
                else:
                    st.error(f"Failed to fix vector index: {response.get('message', 'Unknown error')}")

        st.markdown("---")

        # Delete documents section
        st.subheader("Delete Documents")
        st.markdown("""
        Remove documents from the knowledge graph. You can choose to delete just the document and chunks,
        or also delete the entities extracted from those documents.
        """)

        if st.session_state.sources:
            # Create a dataframe for document selection
            docs_df = pd.DataFrame(st.session_state.sources)
            if not docs_df.empty:
                # Show document information
                display_cols = ['fileName', 'status', 'total_chunks', 'nodeCount', 'fileSource']
                available_cols = [col for col in display_cols if col in docs_df.columns]

                st.dataframe(docs_df[available_cols], use_container_width=True)

                # Multiselect for documents to delete
                docs_to_delete = st.multiselect(
                    "Select documents to delete",
                    options=[doc.get("fileName") for doc in st.session_state.sources],
                    help="Select one or more documents to delete"
                )

                if docs_to_delete:
                    # Option to delete entities
                    delete_entities = st.checkbox(
                        "Also delete entities extracted from these documents",
                        value=True,
                        help="If checked, entities that are only connected to these documents will be deleted. If unchecked, only documents and chunks are deleted."
                    )

                    st.warning(f"You are about to delete {len(docs_to_delete)} document(s). This action cannot be undone!")

                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("Delete Selected", type="primary"):
                            # Get source types for selected documents
                            source_types = []
                            for doc_name in docs_to_delete:
                                doc_info = next((s for s in st.session_state.sources if s.get("fileName") == doc_name), None)
                                if doc_info:
                                    source_types.append(doc_info.get("fileSource", "local file"))
                                else:
                                    source_types.append("local file")

                            with st.spinner(f"Deleting {len(docs_to_delete)} document(s)..."):
                                response = delete_documents(
                                    st.session_state.connection_info.get('uri'),
                                    st.session_state.connection_info.get('userName'),
                                    st.session_state.connection_info.get('password'),
                                    st.session_state.connection_info.get('database'),
                                    docs_to_delete,
                                    source_types,
                                    delete_entities
                                )

                                if response.get("status") == "Success":
                                    st.success(f"Successfully deleted {len(docs_to_delete)} document(s): {response.get('message', '')}")
                                    # Refresh sources list
                                    sources_response = get_source_list(
                                        st.session_state.connection_info.get('uri'),
                                        st.session_state.connection_info.get('userName'),
                                        st.session_state.connection_info.get('password'),
                                        st.session_state.connection_info.get('database')
                                    )
                                    if sources_response.get("status") == "Success":
                                        st.session_state.sources = sources_response.get("data", [])
                                        # Clear selected sources if they were deleted
                                        st.session_state.selected_sources = [s for s in st.session_state.selected_sources if s not in docs_to_delete]
                                    st.rerun()
                                else:
                                    st.error(f"Failed to delete documents: {response.get('message', 'Unknown error')}")
                    with col2:
                        if st.button("Cancel"):
                            st.rerun()
        else:
            st.info("No documents found. Upload files in the Upload tab.")