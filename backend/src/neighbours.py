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

import logging
from src.graph_query import *

NEIGHBOURS_FROM_ELEMENT_ID_QUERY = """
MATCH (n) 
WHERE elementId(n) = $element_id

MATCH (n)<-[rels]->(m)  
WITH n, 
     ([n] + COLLECT(DISTINCT m)) AS allNodes, 
     COLLECT(DISTINCT rels) AS allRels

RETURN 
    [node IN allNodes | 
        node {
            .*,
            embedding: null,
            text: null,
            summary: null,
            labels: [coalesce(apoc.coll.removeAll(labels(node), ['__Entity__'])[0], "*")],
            element_id: elementId(node),
            properties: { 
                id: CASE WHEN node.id IS NOT NULL THEN node.id ELSE node.fileName END,
                title:  CASE WHEN node.title IS NOT NULL THEN node.title ELSE " " END
            }
        }
    ] AS nodes,
    
    [r IN allRels | 
        {
            start_node_element_id: elementId(startNode(r)),
            end_node_element_id: elementId(endNode(r)),
            type: type(r),
            element_id: elementId(r)
        }
    ] AS relationships
"""


def get_neighbour_nodes(uri, username, password, database, element_id, query=NEIGHBOURS_FROM_ELEMENT_ID_QUERY):
    driver = None

    try:
        logging.info(f"Querying neighbours for element_id: {element_id}")
        driver = get_graphDB_driver(uri, username, password, database)
        driver.verify_connectivity()
        logging.info("Database connectivity verified.")

        records, summary, keys = driver.execute_query(query,element_id=element_id)
        nodes = records[0].get("nodes", [])
        relationships = records[0].get("relationships", [])
        result = {"nodes": nodes, "relationships": relationships}
        
        logging.info(f"Successfully retrieved neighbours for element_id: {element_id}")
        return result
    
    except Exception as e:
        logging.error(f"Error retrieving neighbours for element_id: {element_id}: {e}")
        return {"nodes": [], "relationships": []}
    
    finally:
        if driver is not None:
            driver.close()
            logging.info("Database driver closed.")