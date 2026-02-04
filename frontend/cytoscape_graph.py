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

"""
Cytoscape.js graph visualization module.

This module provides rendering functions for interactive knowledge graph visualization
using Cytoscape.js. Supports multiple layout algorithms (CoLA, CoSE, Dagre, Circular, Random)
and interactive features like hover tooltips and progressive disclosure.
"""

import json
import html
import logging

# Color scheme for entity types
COLOR_SCHEME = {
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

# Layout configurations for Cytoscape.js
LAYOUT_CONFIGS = {
    'cola': {
        'name': 'cola',
        'animate': True,
        'animationDuration': 1000,
        'maxSimulationTime': 4000,
        'ungrabifyWhileSimulating': True,
        'fit': True,
        'avoidOverlap': True,
        'handleDisconnected': True,
        'convergenceThreshold': 0.01,
        'nodeSpacing': 50
    },
    'cose': {
        'name': 'cose',
        'animate': True,
        'animationDuration': 1000,
        'animationEasing': 'ease-out',
        'nodeRepulsion': 400000,
        'idealEdgeLength': 100,
        'edgeElasticity': 100,
        'gravity': 80,
        'numIter': 1000,
        'initialTemp': 200,
        'coolingFactor': 0.95,
        'minTemp': 1.0
    },
    'dagre': {
        'name': 'dagre',
        'animate': True,
        'animationDuration': 800,
        'rankDir': 'TB',
        'ranker': 'tight-tree',  # Faster than network-simplex for schema graphs
        'nodeSep': 50,
        'edgeSep': 10,
        'rankSep': 75,
        'fit': True,
        'padding': 30
    },
    'circle': {
        'name': 'circle',
        'animate': True,
        'animationDuration': 800,
        'animationEasing': 'ease-in-out-cubic',
        'avoidOverlap': True,
        'startAngle': 4.71238898,  # 3/2 * PI (270°, starts at bottom)
        'clockwise': True
    },
    'random': {
        'name': 'random',
        'animate': False,
        'fit': True
    }
}


def _escape_property_value(value):
    """Escape user-generated content for safe HTML injection."""
    if isinstance(value, str):
        return html.escape(value)
    return value


def _convert_to_cytoscape_format(nodes, relationships, expanded_nodes, color_scheme):
    """
    Convert Neo4j graph data to Cytoscape.js elements format.

    Args:
        nodes: List of Neo4j node objects with element_id, labels, properties
        relationships: List of Neo4j relationship objects
        expanded_nodes: Set of expanded node IDs
        color_scheme: Dictionary mapping labels to colors

    Returns:
        Dictionary with 'nodes' and 'edges' arrays in Cytoscape.js format
    """
    cy_nodes = []
    cy_edges = []

    # Convert nodes
    for node in nodes:
        node_id = node.get('element_id', '')
        labels = node.get('labels', [])
        properties = node.get('properties', {})

        # Get node label/caption
        node_caption = (
            properties.get('id') or
            properties.get('name') or
            properties.get('fileName') or
            (labels[0] if labels else 'Node')
        )

        # Get color based on first label
        node_color = color_scheme.get(labels[0], '#94a3b8') if labels else '#94a3b8'

        # Create tooltip content
        tooltip_parts = [f"<strong>{_escape_property_value(node_caption)}</strong>"]
        tooltip_parts.append(f"Type: {', '.join(labels)}")

        if node_id in expanded_nodes:
            tooltip_parts.append("<em>Expanded</em>")

        for key, value in properties.items():
            if key not in ['embedding', 'text', 'summary'] and value:
                escaped_value = str(_escape_property_value(value))[:100]
                tooltip_parts.append(f"{key}: {escaped_value}")

        tooltip = '<br>'.join(tooltip_parts)

        # Node size - larger for expanded nodes
        size = 25 if node_id in expanded_nodes else 20

        # Create Cytoscape.js node object
        cy_node = {
            'data': {
                'id': node_id,
                'label': str(node_caption)[:30],  # Truncate long labels
                'labels': labels,
                'color': node_color,
                'size': size,
                'tooltip': tooltip,
                'properties': properties,
                'expanded': node_id in expanded_nodes
            },
            'classes': 'expanded' if node_id in expanded_nodes else ''
        }

        cy_nodes.append(cy_node)

    # Build node ID set for edge validation
    node_ids = {node.get('element_id') for node in nodes}

    # Convert relationships to edges (only if both endpoints exist)
    for rel in relationships:
        start_id = rel.get('start_node_element_id', '')
        end_id = rel.get('end_node_element_id', '')
        rel_type = rel.get('type', '')

        # Validate that both endpoints exist in the node set
        if start_id and end_id and start_id in node_ids and end_id in node_ids:
            cy_edge = {
                'data': {
                    'id': rel.get('element_id', f"{start_id}-{end_id}"),
                    'source': start_id,
                    'target': end_id,
                    'label': rel_type
                }
            }
            cy_edges.append(cy_edge)

    return {'nodes': cy_nodes, 'edges': cy_edges}


def _build_html_template(elements, layout, view_type, height):
    """
    Generate complete HTML with Cytoscape.js visualization.

    Args:
        elements: Dictionary with 'nodes' and 'edges' arrays
        layout: Layout algorithm name ('cola', 'cose', 'dagre', 'circle', 'random')
        view_type: 'data' or 'schema'
        height: Height in pixels

    Returns:
        Complete HTML string with embedded Cytoscape.js
    """
    # Get layout configuration
    layout_config = LAYOUT_CONFIGS.get(layout, LAYOUT_CONFIGS['cola'])

    # Convert Python objects to JSON and escape script tags to prevent injection
    elements_json = json.dumps(elements).replace('</', '<\\/')
    layout_json = json.dumps(layout_config).replace('</', '<\\/')

    # Build HTML template
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
    <script src="https://unpkg.com/webcola@3.4.0/WebCola/cola.min.js"></script>
    <script src="https://unpkg.com/cytoscape-cola@2.5.1/cytoscape-cola.js"></script>
    <script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
    <script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        #cy {{
            width: 100%;
            height: {height}px;
            background-color: #ffffff;
        }}

        #tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.85);
            color: white;
            padding: 12px;
            border-radius: 6px;
            font-size: 13px;
            pointer-events: none;
            display: none;
            z-index: 9999;
            max-width: 300px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div id="cy"></div>
    <div id="tooltip"></div>

    <script>
        try {{
            // Initialize Cytoscape
            var cy = cytoscape({{
                container: document.getElementById('cy'),

                elements: {elements_json},

                style: [
                    {{
                        selector: 'node',
                        style: {{
                            'label': 'data(label)',
                            'background-color': 'data(color)',
                            'width': 'data(size)',
                            'height': 'data(size)',
                            'font-size': '12px',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'text-wrap': 'wrap',
                            'text-max-width': '80px',
                            'border-width': 2,
                            'border-color': '#fff'
                        }}
                    }},
                    {{
                        selector: 'node.expanded',
                        style: {{
                            'border-color': '#3b82f6',
                            'border-width': 3
                        }}
                    }},
                    {{
                        selector: 'node.highlighted',
                        style: {{
                            'border-color': '#3b82f6',
                            'border-width': 4,
                            'border-opacity': 0.8
                        }}
                    }},
                    {{
                        selector: 'edge',
                        style: {{
                            'width': 2,
                            'line-color': '#888',
                            'target-arrow-color': '#888',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier',
                            'label': 'data(label)',
                            'font-size': '10px',
                            'text-rotation': 'autorotate',
                            'text-margin-y': -10,
                            'opacity': 0.7,
                            'arrow-scale': 1.5
                        }}
                    }},
                    {{
                        selector: 'edge.highlighted',
                        style: {{
                            'line-color': '#000',
                            'target-arrow-color': '#000',
                            'opacity': 1,
                            'width': 3
                        }}
                    }}
                ],

                layout: {layout_json}
            }});

            // Tooltip and hover highlight handling
            var tooltip = document.getElementById('tooltip');

            cy.on('mouseover', 'node', function(evt) {{
                var node = evt.target;
                var data = node.data();

                // Add highlight class
                node.addClass('highlighted');

                // Use innerHTML since tooltip is already HTML-escaped on server side
                tooltip.innerHTML = data.tooltip || '';
                tooltip.style.display = 'block';
            }});

            cy.on('mouseout', 'node', function(evt) {{
                var node = evt.target;

                // Remove highlight class
                node.removeClass('highlighted');

                tooltip.style.display = 'none';
            }});

            cy.on('mouseover', 'edge', function(evt) {{
                var edge = evt.target;
                edge.addClass('highlighted');
            }});

            cy.on('mouseout', 'edge', function(evt) {{
                var edge = evt.target;
                edge.removeClass('highlighted');
            }});

            cy.on('mousemove', function(evt) {{
                tooltip.style.left = evt.originalEvent.clientX + 15 + 'px';
                tooltip.style.top = evt.originalEvent.clientY + 15 + 'px';
            }});

            // Fit graph after layout completes
            cy.ready(function() {{
                cy.fit(50);
            }});

        }} catch (error) {{
            console.error('Cytoscape initialization error:', error);
            var errorDiv = document.createElement('div');
            errorDiv.style.cssText = 'padding: 20px; color: red; font-family: sans-serif;';
            errorDiv.textContent = 'Error initializing graph: ' + error.message;
            var container = document.getElementById('cy');
            container.innerHTML = '';
            container.appendChild(errorDiv);
        }}
    </script>
</body>
</html>
"""

    return html_template


def _build_empty_graph_template(message):
    """Generate HTML template for empty graph state."""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 700px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #f8f9fa;
        }}
        .message {{
            padding: 30px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <div class="message">
        <h3 style="margin: 0 0 10px 0;">No Graph Data</h3>
        <p style="margin: 0;">{html.escape(message)}</p>
    </div>
</body>
</html>
"""


def _build_error_template(error_message):
    """Generate HTML template for error state."""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 700px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #fff5f5;
        }}
        .error {{
            padding: 30px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #ef4444;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-width: 500px;
        }}
    </style>
</head>
<body>
    <div class="error">
        <h3 style="margin: 0 0 10px 0; color: #ef4444;">Visualization Error</h3>
        <p style="margin: 0; color: #6c757d;">{html.escape(error_message)}</p>
    </div>
</body>
</html>
"""


def render_cytoscape_graph(nodes, relationships, layout='cola', expanded_nodes=None, view_type='data', height=720):
    """
    Render graph visualization using Cytoscape.js.

    Args:
        nodes: List of Neo4j node objects with element_id, labels, properties
        relationships: List of Neo4j relationship objects
        layout: Layout algorithm ('cola', 'cose', 'dagre', 'circle', 'random')
        expanded_nodes: Set of expanded node IDs for special styling
        view_type: 'data' or 'schema'
        height: Visualization height in pixels

    Returns:
        Complete HTML string for rendering with streamlit.components.html()
    """
    try:
        # Validation
        if not nodes:
            return _build_empty_graph_template("No nodes to display. Upload and extract documents first.")

        # Safety limit for schema view to prevent browser crashes
        if view_type == 'schema' and len(nodes) > 100:
            logging.warning(f"Schema has {len(nodes)} nodes, limiting to 100 to prevent browser crash")
            nodes = nodes[:100]
            # Filter relationships to only include those between visible nodes
            node_ids = {n.get('element_id') for n in nodes}
            relationships = [r for r in relationships
                           if r.get('start_node_element_id') in node_ids
                           and r.get('end_node_element_id') in node_ids]

        if layout not in LAYOUT_CONFIGS:
            logging.warning(f"Unknown layout: {layout}, falling back to 'cola'")
            layout = 'cola'

        # For schema view with many nodes, use simpler circular layout
        if view_type == 'schema' and len(nodes) > 50 and layout == 'dagre':
            logging.info(f"Schema has {len(nodes)} nodes, using circular layout instead of dagre")
            layout = 'circle'

        # Convert to Cytoscape.js format
        expanded_nodes = expanded_nodes or set()
        elements = _convert_to_cytoscape_format(nodes, relationships, expanded_nodes, COLOR_SCHEME)

        # Generate HTML
        html_output = _build_html_template(elements, layout, view_type, height)

        return html_output

    except Exception as e:
        logging.error(f"Error rendering Cytoscape graph: {str(e)}", exc_info=True)
        return _build_error_template(str(e))
