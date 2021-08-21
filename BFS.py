import copy


class Node(object):
    def __init__(self):
        self.environments = []
        self.children = []
        self.parent = None
        self.goal_way = None
        self.process = ""
        self.visited = False

    def add_environment(self, environment):
        self.environments.append(environment)

    def add_environments(self, environments):
        self.environments = copy.deepcopy(environments)

    def add_child(self, obj):
        self.children.append(obj)

    def add_parent(self, obj):
        self.parent = obj

    def define_process(self, process):
        self.process += process

    def is_goal(self):
        for e in self.environments:
            global n
            if string_to_card(e[0])[0] != n and string_to_card(e[0])[1] != "#":
                return False
            for i in range(len(e) - 1):
                if string_to_card(e[i])[0] != string_to_card(e[i + 1])[0] + 1:
                    return False
                if string_to_card(e[i])[1] != string_to_card(e[i + 1])[1]:
                    return False

        return True

    def expand(self):
        for i, e1 in enumerate(self.environments):
            card1 = e1[len(e1) - 1]
            num1, color1 = string_to_card(card1)
            for j, e2 in enumerate(self.environments):
                if i == j:
                    continue
                card2 = e2[len(e2) - 1]
                num2, color2 = string_to_card(card2)
                if num2 > num1:
                    global nodes_count
                    nodes_count += 1
                    newChild = Node()
                    newChild.add_environments(self.environments)
                    card = newChild.environments[i].pop()
                    if len(newChild.environments[i]) == 0:
                        newChild.environments[i].append("#")
                    if color2 == "#":
                        newChild.environments[j].pop()
                    newChild.environments[j].append(card)
                    newChild.define_process("from column %d to column %d" % (i + 1, j + 1))
                    newChild.add_parent(self)
                    self.add_child(newChild)
        self.visited = True


def string_to_card(str):
    l = len(str) - 1
    if l > 0:
        number = int(str[:l])
        color = str[l]
        return number, color
    if l == 0:
        global n
        return n + 1, "#"


def define_way(root, goal):
    count = 0
    while goal != root:
        p = goal.parent
        p.goal_way = goal
        goal = p
        count += 1
    return count


def print_way(root, depth):
    node = root
    for i in range(depth + 1):
        if i > 0:
            print(node.process)
        print(node.environments, end="\n\n")
        node = node.goal_way


def BFS(root):
    queue = [root]
    for node in queue:
        global visited_nodes_count
        visited_nodes_count += 1
        if node.is_goal():
            return node
        node.expand()
        for child in node.children:
            queue.append(child)


def main():
    global k, m, n
    k, m, n = [int(x) for x in input().split()]
    root = Node()
    for i in range(k):
        root.add_environment(input().split())
    global nodes_count, visited_nodes_count
    nodes_count = visited_nodes_count = 0
    goal = BFS(root)
    depth = define_way(root, goal)
    print("N = %d" % depth)
    print_way(root, depth)
    print("Number of Generated Nodes : %d" % (nodes_count + 1))
    print("Number of Visited nodes : %d" % visited_nodes_count)


if __name__ == '__main__':
    main()
