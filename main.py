import itertools as it
import time as ti
import numpy as np


class Node:
    def __init__(self, cost, state, flashlight, steps):
        self.cost = cost
        self.state = state
        self.flashlight = flashlight
        self.steps = steps
        self.depth = 0
        self.heuristic = 0

    def __gt__(self, other):
        return self.cost > other.cost


class Problem:

    def __init__(self, arr, algorithm):

        self.arr = arr
        self.id = []
        self.visited_ids = []
        self.search_cost_ids = 0
        self.space_req_ids = 0
        letters = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(len(arr)):
            self.id.append(letters[i])

        root = Node(0, [0] * len(arr), 0, [])
        self.fringe = [root]
        self.algorithm = algorithm

    def is_goal(self, node, search_cost, space_requirement):
        algo = ["UCS", "IDS", 'A*']
        if node.state == [1] * len(self.arr):
            print(f"Solution:\t ({algo[self.algorithm]}) ")
            for i in node.steps:
                print(i)
            print(f"\nSolution Cost: {node.cost}")
            print(f"Search Cost: {search_cost}")
            print(f"Space Requirement: {space_requirement}\n========")
            return True
        return False

    def a_star(self):
        search_cost = 0
        space_requirement = 0
        start_node = Node(0, [0] * len(self.arr), 0, [])
        explored = []
        fringe = [start_node]
        while fringe:
            if len(fringe) > space_requirement:
                space_requirement = len(fringe)
            node = fringe.pop(0)
            search_cost += 1
            if self.is_goal(node, search_cost, space_requirement):
                return
            explored.append(node)
            children = self.expand(node)
            for i in children:

                if not self.found(explored, i) or not self.found(fringe, i):
                    self.insert(fringe, i)

                elif self.found(fringe, i):
                    self.replace(fringe, i)

    def ucs(self):
        search_cost = 0
        space_requirement = 0
        start_node = Node(0,[0]*len(self.arr),0,[])
        explored = []
        fringe = [start_node]
        while fringe:
            if len(fringe) > space_requirement:
                space_requirement = len(fringe)
            node = fringe.pop(0)
            search_cost +=1
            if self.is_goal(node,search_cost,space_requirement):
                return
            explored.append(node)
            children = self.expand(node)
            for i in children:

                if not self.found(explored,i) or not self.found(fringe,i):
                    self.insert(fringe,i)

                elif self.found(fringe,i):
                    self.replace(fringe,i)


    def add_node(self, node):

        if self.algorithm == 1:
            self.fringe.append(node)

        else:
            self.insert(self.fringe,node)

    def get_heuristic(self,arr):
        h = self.arr[0]
        for i in range(len(arr)):

            if arr[i] == 0 and self.arr[i] > h:
                h = self.arr[i]

        return h

    def is_goal_dls(self,node):
        if node.state == [1]*len(self.arr):
            return True

    def recursive_dls(self,node,limit):
        self.visited_ids.append(node)
        self.search_cost_ids += 1 # to Here
        cutoff_occurred = False
        if self.is_goal_dls(node):
            self.is_goal(node,self.search_cost_ids,self.space_req_ids)
            return node

        elif limit <= 0:
            return 'cutoff'

        else:
            # self.search_cost_ids += 1 // change from here
            children = self.expand(node)
            if self.space_req_ids < len(children):
                self.space_req_ids = len(children)

            for child in children:
                if self.found(self.visited_ids,child):
                    continue

                result = self.recursive_dls(child,limit-1)

                if result == 'cutoff':
                    cutoff_occurred = True

                elif result != 'failure':
                    return result

            return 'cutoff' if cutoff_occurred else 'failure'

    def depth_limited_search(self,root,limit):
        return self.recursive_dls(root,limit)

    def iterative_deepening_search(self):
        depth = 0
        root = Node(0,[0]*len(time),0,[])
        while True:
            self.visited_ids = []
            result = self.depth_limited_search(root, depth)
            if result != 'cutoff':
                return result

            depth +=1

    def expand(self, node):
        # for the ids algorithm ; we don't want to keep adding to the list
        self.fringe = []

        if node.flashlight == 0:
            # loop through combinations and create nodes
            x = it.combinations(list(range(len(time))), 2)

            for i in x:
                i1 = i[0]
                i2 = i[1]
                if node.state[i1] == 0 and node.state[i2] == 0:

                    # copy list so we don't change original the list
                    tmp_state = [*node.state]

                    # change where is the person
                    tmp_state[i1] = 1
                    tmp_state[i2] = 1
                    steps = [*node.steps, "({},{}) move to the west side".format(self.id[i1], self.id[i2])]

                    cost_max = node.cost + max(time[i1], time[i2])

                    n = Node(cost_max, tmp_state, 1, steps)
                    n.heuristic = self.get_heuristic(n.state) + cost_max
                    n.depth = node.depth + 1

                    self.add_node(n)

        # if flashlight is on the west side
        if node.flashlight == 1:
            for i in list(range(len(time))):
                if node.state[i] == 1:
                    tmp_state = [*node.state]
                    tmp_state[i] = 0

                    cost = node.cost + time[i]

                    steps = [*node.steps, "({}) returns with the flashlight".format(self.id[i])]

                    n = Node(cost, tmp_state, 0, steps)
                    n.heuristic = self.get_heuristic(n.state) + cost
                    n.depth = node.depth + 1

                    self.add_node(n)

        return self.fringe

    def insert(self,arr,node):
        if self.algorithm == 0:
            for i in range(len(arr)):
                if node.cost < arr[i].cost:
                    arr.insert(i,node)
                    return
            arr.append(node)

        if self.algorithm == 2:

            for i in range(len(arr)):
                if node.heuristic < arr[i].heuristic:
                    arr.insert(i,node)
                    return
            arr.append(node)

    def replace(self,arr,node):
        x = 0
        if self.algorithm == 0:
            for i in arr:
                if (i.state == node.state) and (i.cost > node.cost):
                    arr.pop(x)
                    self.insert(arr,node)
                    return
                x +=1

        if self.algorithm == 2:

            for i in arr:
                if (i.state == node.state) and (i.heuristic > node.heuristic):
                    arr.pop(x)
                    self.insert(arr,node)
                    return
                x +=1

    def found(self,visited,node):
        for i in visited:
            if i.state == node.state:
                return True
        return False


# handling Input
C = int(input("How many cases ? C = "))
lists = [[] for i in range(C)]
cn = 1
for i in range(C):
    people = int(input(f"How many people in case {cn} ? K= "))
    while people < 2:
        people = int(input(f"How many people in case {cn} ? K= "))
    cn += 1

cn = 1

for j in range(C):
    array1 = input(f"Type the time of each person in case {cn}: ")

    combine = list(map(int, array1.split(',')))

    while len(combine) <= 1:
        array1 = input(f"Type the time of each person in case {cn}: ")
        combine = list(map(int, array1.split(',')))

    cn += 1

    for k in range(len(combine)):
        lists[j].append(combine[k])


cn = 1
algorithm = int(input("Choose an Algorithm(0-UCS 1-IDS 2-A*): "))
for i in range(C):
    print(f"\nCase {cn}\n")
    cn += 1
    time = lists[i]
    print(time)
    p = Problem(time, algorithm)
    t = ti.time()
    if algorithm == 0: p.ucs()
    if algorithm == 1:
        p.iterative_deepening_search()
    if algorithm == 2: p.a_star()
    time_elapsed = ti.time() - t
    print(time_elapsed)
