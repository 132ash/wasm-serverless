from collections import defaultdict
from config import YAMLPATH
import yaml


# Helper function to generate a balanced DAG
def generate_balanced_dag(node_count):
    # Calculate the number of edges per node
    # Aiming for roughly 2-3 edges per node as seen in the example
    avg_edges = 3
    nodes = [{'name': f'func{i+1}', 'source': 'func', 'scale': 1, 'runtime': 1} for i in range(node_count)]
    edges = defaultdict(list)
    for i in range(1, node_count):
        # Distribute edges among the nodes in a balanced way
        edges[f'func{i}'].append(f'func{min(i+1, node_count)}')
        if i % avg_edges == 0:
            edges[f'func{i}'].append(f'func{min(i+2, node_count)}')
        if (i+1) % (avg_edges*2) == 0:
            edges[f'func{i}'].append('end')
    edges[f'func{node_count}'].append('end')
    
    # Update the nodes with the edges
    for node in nodes:
        node_name = node['name']
        if node_name in edges:
            node['next'] = {'type': 'PASS', 'size': 4, 'funcs': edges[node_name]}
        else:
            node['next'] = {'type': 'PASS', 'size': 4, 'funcs': ['end']}
            
    # Adding the end node manually
    nodes.append({'name': 'end', 'source': 'func', 'scale': 1, 'runtime': 1, 'output': [{'input': 'DEFAULT'}]})
    
    return {'functions': nodes}

# Now we generate the YAML content for each DAG with specified number of nodes
node_counts = [10, 25, 50, 100, 150, 200, 300]
dags_yaml = {count: generate_balanced_dag(count) for count in node_counts}

# Saving the generated DAGs to YAML files
for count, dag in dags_yaml.items():
    
    yaml_path = YAMLPATH+f'/workflow_{count}_nodes.yaml'
    with open(yaml_path, 'w') as file:
        yaml.dump(dag, file)