import component
from workflowParser import Parser
import sys
import yaml
import queue
import config

WORKERNODEPATH = config.WORKERNODEPATH
NET_MEM_BANDWIDTH_RATIO = config.NET_MEM_BANDWIDTH_RATIO
GROUP_LIMIT = config.GROUP_LIMIT
group_ip = {}
group_scale = {}

def init_graph(workflow:component.Workflow, group_set:list, node_info):
    global group_ip, group_scale
    ip_list = list(node_info.keys())
    in_degree_vec = dict()
    q = queue.Queue()
    for name in workflow.startFunctions:
        q.put(workflow.nodes[name])
        group_set.append((name, ))
    while q.empty() is False:
        node = q.get()
        for next_node_name in node.next:
            if next_node_name not in in_degree_vec:
                in_degree_vec[next_node_name] = 1
                q.put(workflow.nodes[next_node_name])
                group_set.append((next_node_name, ))
            else:
                in_degree_vec[next_node_name] += 1
    for s in group_set:
        group_ip[s] = ip_list[hash(s) % len(ip_list)]
        group_scale[s] = workflow.nodes[s[0]].scale
        node_info[group_ip[s]] -= workflow.nodes[s[0]].scale
    return in_degree_vec


def find_set(node, group_set):
    for node_set in group_set:
        if node in node_set:
            return node_set
    return None


def topo_search(workflow:component.Workflow, in_degree_vec:dict, group_set:list):
    dist_vec = dict()  # { name: [dist, max_length] }
    prev_vec = dict()  # { name: [prev_name, length] }
    q = queue.Queue()
    for name in workflow.startFunctions:
        q.put(workflow.nodes[name])
        dist_vec[name] = [workflow.nodes[name].runtime, 0]
        prev_vec[name] = []
    while q.empty() is False:
        node = q.get()
        pre_dist = dist_vec[node.name]
        prev_name = node.name
        for index in range(len(node.next)):
            next_node = workflow.nodes[node.next[index]]
            w = node.nextDis[index]
            next_node_name = next_node.name
            if next_node_name in find_set(prev_name, group_set):
                w = w / NET_MEM_BANDWIDTH_RATIO
            if next_node.name not in dist_vec:
                dist_vec[next_node_name] = [pre_dist[0] + w + next_node.runtime, max(pre_dist[1], w)]
                prev_vec[next_node_name] = [prev_name, w]
            elif dist_vec[next_node_name][0] < pre_dist[0] + w + next_node.runtime:
                dist_vec[next_node_name] = [pre_dist[0] + w + next_node.runtime, max(pre_dist[1], w)]
                prev_vec[next_node_name] = [prev_name, w]
            elif dist_vec[next_node_name][0] == pre_dist[0] + w + next_node.runtime and max(pre_dist[1], w) > \
                    dist_vec[next_node_name][1]:
                dist_vec[next_node_name][1] = max(pre_dist[1], w)
                prev_vec[next_node_name] = [prev_name, w]
            in_degree_vec[next_node_name] -= 1
            if in_degree_vec[next_node_name] == 0:
                q.put(next_node)
    return dist_vec, prev_vec

def mergeable(node1, node2, group_set:list, node_info:dict):
    global group_ip, group_scale
    node_set1 = find_set(node1, group_set)

    # same set?
    if node2 in node_set1: # same set
        return False
    node_set2 = find_set(node2, group_set)

    # group size no larger than GROUP_LIMIT
    if len(node_set1) + len(node_set2) > GROUP_LIMIT:
        return False

    # meet scale requirement?
    new_node_info = node_info.copy()
    node_set1_scale = group_scale[node_set1]
    node_set2_scale = group_scale[node_set2]
    new_node_info[group_ip[node_set1]] += node_set1_scale
    new_node_info[group_ip[node_set2]] += node_set2_scale
    best_fit_addr, best_fit_scale = None, 10000000
    for addr in new_node_info:
        if new_node_info[addr] >= node_set1_scale + node_set2_scale and new_node_info[addr] < best_fit_scale:
            best_fit_addr = addr
            best_fit_scale = new_node_info[addr]
    if best_fit_addr is None:
        print('Hit scale threshold', node_set1_scale, node_set2_scale)
        return False

    # merge sets & update scale
    new_group_set = (*node_set1, *node_set2)

    group_set.append(new_group_set)
    group_ip[new_group_set] = best_fit_addr
    node_info[best_fit_addr] -= node_set1_scale + node_set2_scale
    group_scale[new_group_set] = node_set1_scale + node_set2_scale

    node_info[group_ip[node_set1]] += node_set1_scale
    node_info[group_ip[node_set2]] += node_set2_scale
    group_set.remove(node_set1)
    group_set.remove(node_set2) 
    group_ip.pop(node_set1)
    group_ip.pop(node_set2)
    group_scale.pop(node_set1)
    group_scale.pop(node_set2)
    return True

def merge_path(crit_vec, group_set,  node_info:dict):
    for edge in crit_vec:
        if mergeable(edge[1][0], edge[0], group_set, node_info):
            return True
    return False


def get_longest_dis(workflow:component.Workflow, dist_vec):
    dist = 0
    node_name = ''
    for name in workflow.nodes:
        if dist_vec[name][0] > dist:
            dist = dist_vec[name][0]
            node_name = name
    return dist, node_name


def grouping(workflow: component.Workflow, nodeInfo:dict):
    # initialization: get in-degree of each node
    group_set = list()
    in_degree_vec = init_graph(workflow, group_set, nodeInfo)

    while True:

        # break if every node is in same group
        if len(group_set) == 1:
            break

        # topo dp: find each node's longest dis and it's predecessor
        dist_vec, prev_vec = topo_search(workflow, in_degree_vec.copy(), group_set)
        crit_length, tmp_node_name = get_longest_dis(workflow, dist_vec)

        # find the longest path, edge descent sorted
        crit_vec = dict()
        while tmp_node_name not in workflow.startFunctions:
            crit_vec[tmp_node_name] = prev_vec[tmp_node_name]
            tmp_node_name = prev_vec[tmp_node_name][0]
        crit_vec = sorted(crit_vec.items(), key=lambda c: c[1][1], reverse=True)

        # if can't merge every edge of this path, just break
        if not merge_path(crit_vec, group_set, nodeInfo):
            break
    return group_set

def getGroupingResult(workflow: component.Workflow, nodeInfo:dict):
    global group_ip

    group_detail = grouping(workflow, nodeInfo)
    # building function info:
    function_info_dict = {}
    for node_name in workflow.nodes:
        node = workflow.nodes[node_name]
        ip = group_ip[find_set(node_name, group_detail)]
        function_info = {'function_name': node.name, 'container':node.container, 'runtime': node.runtime, 'ip': ip, 'source':node.source,
                         'parent_cnt': workflow.parent_cnt[node.name], 'conditions': node.conditions}
        function_info['next'] = node.next
        function_info['output'] = node.output
        function_info['traverse'] = node.traverse
        function_info_dict[node_name] = function_info
    return nodeInfo, function_info_dict

def groupAndSave(workflowName:str):
    parser = Parser(workflowName)
    workflowData = parser.parse()
    nodeInfoList = yaml.load(open(WORKERNODEPATH), Loader=yaml.FullLoader)
    workerNodeInfo = {}
    for node_info in nodeInfoList['nodes']:
        workerNodeInfo[node_info['worker_address']] = node_info['scale_limit'] * 0.8
    nodeInfo, functionInfo = getGroupingResult(workflowData, workerNodeInfo)

if __name__ == "__main__":
    workflowName = sys.argv[1]
    groupAndSave(workflowName)

