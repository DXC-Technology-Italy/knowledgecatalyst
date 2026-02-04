"""
SPDX-License-Identifier: AGPL-3.0-or-later
SPDX-FileCopyrightText: 2026 DXC Technology Company

KnowledgeCatalyst - Knowledge Graph RAG System
Copyright (C) 2026 DXC Technology Company

Unit tests for Cytoscape.js graph visualization
"""

import pytest
from cytoscape_graph import (
    render_cytoscape_graph,
    _convert_to_cytoscape_format,
    _escape_property_value,
    COLOR_SCHEME,
    LAYOUT_CONFIGS
)


def test_escape_property_value():
    """Test HTML escaping for security"""
    assert _escape_property_value("<script>alert('xss')</script>") == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"
    assert _escape_property_value("Normal text") == "Normal text"
    assert _escape_property_value(123) == 123


def test_convert_to_cytoscape_format_basic():
    """Test basic node and edge conversion"""
    nodes = [
        {
            'element_id': 'node1',
            'labels': ['Person'],
            'properties': {'name': 'Alice', 'age': 30}
        }
    ]
    relationships = [
        {
            'element_id': 'rel1',
            'start_node_element_id': 'node1',
            'end_node_element_id': 'node2',
            'type': 'KNOWS'
        }
    ]

    result = _convert_to_cytoscape_format(nodes, relationships, set(), COLOR_SCHEME)

    # Check nodes
    assert len(result['nodes']) == 1
    assert result['nodes'][0]['data']['id'] == 'node1'
    assert result['nodes'][0]['data']['label'] == 'Alice'
    assert result['nodes'][0]['data']['color'] == COLOR_SCHEME['Person']

    # Check edges
    assert len(result['edges']) == 1
    assert result['edges'][0]['data']['source'] == 'node1'
    assert result['edges'][0]['data']['target'] == 'node2'
    assert result['edges'][0]['data']['label'] == 'KNOWS'


def test_convert_with_expanded_nodes():
    """Test that expanded nodes are marked correctly"""
    nodes = [
        {'element_id': 'node1', 'labels': ['Document'], 'properties': {'fileName': 'test.pdf'}}
    ]
    expanded = {'node1'}

    result = _convert_to_cytoscape_format(nodes, [], expanded, COLOR_SCHEME)

    assert result['nodes'][0]['data']['expanded'] is True
    assert result['nodes'][0]['data']['size'] == 25
    assert 'expanded' in result['nodes'][0]['classes']


def test_layout_configs_exist():
    """Test that all required layouts are configured"""
    required_layouts = ['cola', 'cose', 'dagre', 'circle', 'random']
    for layout in required_layouts:
        assert layout in LAYOUT_CONFIGS
        assert 'name' in LAYOUT_CONFIGS[layout]


def test_render_empty_graph():
    """Test rendering with no nodes"""
    html = render_cytoscape_graph([], [])
    assert 'No nodes to display' in html
    assert 'No Graph Data' in html


def test_render_invalid_layout():
    """Test fallback for invalid layout"""
    nodes = [{'element_id': 'node1', 'labels': ['Test'], 'properties': {}}]
    html = render_cytoscape_graph(nodes, [], layout='invalid_layout')

    # Should fallback to cola and still render
    assert 'cytoscape' in html.lower()
    assert 'node1' in html


def test_render_basic_graph():
    """Test rendering a basic graph"""
    nodes = [
        {'element_id': 'node1', 'labels': ['Person'], 'properties': {'name': 'Alice'}},
        {'element_id': 'node2', 'labels': ['Person'], 'properties': {'name': 'Bob'}}
    ]
    relationships = [
        {'element_id': 'rel1', 'start_node_element_id': 'node1',
         'end_node_element_id': 'node2', 'type': 'KNOWS'}
    ]

    html = render_cytoscape_graph(nodes, relationships, layout='cola')

    # Check that HTML is generated
    assert '<!DOCTYPE html>' in html
    assert 'cytoscape' in html
    assert 'Alice' in html
    assert 'Bob' in html
    assert 'KNOWS' in html


def test_all_layouts_render():
    """Test that all layout algorithms can render"""
    nodes = [
        {'element_id': f'node{i}', 'labels': ['Test'], 'properties': {'name': f'Node {i}'}}
        for i in range(5)
    ]
    relationships = [
        {'element_id': f'rel{i}', 'start_node_element_id': f'node{i}',
         'end_node_element_id': f'node{i+1}', 'type': 'CONNECTED'}
        for i in range(4)
    ]

    for layout_name in LAYOUT_CONFIGS.keys():
        html = render_cytoscape_graph(nodes, relationships, layout=layout_name)
        assert '<!DOCTYPE html>' in html
        assert 'cytoscape' in html
        assert layout_name in html


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
