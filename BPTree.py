from graphviz import Digraph, nohtml
import math
import os

class MyBPlusTreeNode:

    def __init__(self, m, keys=None, children=None, father=None, next_node=None):
        self.keys = keys if keys else []
        self.children = children if children else []
        self.is_leaf = len(self.children) == 0
        self.count = len(self.keys)
        self.degree = m
        self.father = father
        self.next_node = next_node

    def root_divide(self):
        mid_point = self.degree // 2
        left_child_keys = self.keys[:mid_point+1]
        right_child_keys = self.keys[mid_point+1:]
        left_child_children = self.children[:mid_point+1]
        right_child_children = self.children[mid_point+1:]
        right_child = MyBPlusTreeNode(self.degree, right_child_keys, right_child_children, self)
        left_child = MyBPlusTreeNode(self.degree, left_child_keys, left_child_children, self, right_child)
        for child in left_child_children:
            child.father = left_child
        for child in right_child_children:
            child.father = right_child
        self.keys = [self.keys[mid_point], self.keys[self.degree]]
        self.children = [left_child, right_child]
        self.count = 2
        self.is_leaf = False

    def branch_divide(self):
        mid_point = self.degree // 2
        new_self_keys = self.keys[:mid_point+1]
        new_node_keys = self.keys[mid_point+1:]
        new_self_children = self.children[:mid_point+1]
        new_node_children = self.children[mid_point+1:]
        new_node = MyBPlusTreeNode(self.degree, new_node_keys, new_node_children, self.father, self.next_node)
        for child in new_node_children:
            child.father = new_node
        father = self.father
        i = self.find_self_index()
        father.keys.insert(i, self.keys[mid_point])
        father.children.insert(i+1, new_node)
        father.count += 1
        self.keys = new_self_keys
        self.children = new_self_children
        self.next_node = new_node
        self.count = len(new_self_keys)
        self.is_leaf = len(new_self_children) == 0

    def check_count_too_big(self):
        if self.count > self.degree:
            if self.father:
                self.branch_divide()
            else:
                self.root_divide()

    def add_key(self, key):
        i = 0
        while i < self.count:
            if key < self.keys[i]:
                break
            i += 1
        if self.is_leaf:
            self.keys.insert(i, key)
            self.count += 1
        else:
            if i == self.count:
                i -= 1
                self.keys[i] = key
            self.children[i].add_key(key)
        self.check_count_too_big()

    def find_key(self, key):
        if self.count == 0:
            return None, -1
        i = 0
        while i < self.count:
            if key <= self.keys[i]:
                break
            i += 1
        if self.is_leaf:
            if self.keys[i] == key:
                return self, i
            else:
                return None, -1
        else:
            return self.children[i].find_key(key)

    def borrow_from_right_brother_node(self, self_index):
        right_brother_node = self.next_node
        if right_brother_node.count <= math.ceil(self.degree/2):
            return False
        self.keys.append(right_brother_node.keys.pop(0))
        if not self.is_leaf:
            self.children.append(right_brother_node.children.pop(0))
        self.count += 1
        right_brother_node.count -= 1
        self.father.keys[self_index] = self.keys[-1]
        return True

    def merge_into_right_brother_node(self, self_index):
        right_brother_node = self.next_node
        for child in self.children:
            child.father = right_brother_node
        right_brother_node.keys = self.keys + right_brother_node.keys
        right_brother_node.children = self.children + right_brother_node.children
        right_brother_node.count += self.count
        father = self.father
        if self_index > 0:
            father.children[self_index-1].next_node = right_brother_node
        father.children.pop(self_index)
        father.keys.pop(self_index)
        father.count -= 1

    def merge_with_left_brother_code(self, self_index):
        father = self.father
        left_brother_index = self_index-1
        left_brother_node = father.children[left_brother_index]
        for child in left_brother_node.children:
            child.father = self
        self.keys = left_brother_node.keys + self.keys
        self.children = left_brother_node.children + self.children
        self.count += left_brother_node.count
        if self_index > 1:
            father.children[self_index - 2].next_node = self
        father.keys.pop(left_brother_index)
        father.children.pop(left_brother_index)
        father.count -= 1

    def find_self_index(self):
        father = self.father
        i = 0
        while i < self.count:
            if father.children[i] is self:
                break
            i += 1
        return i

    def borrow_from_left_brother_node(self, left_brother_index):
        father = self.father
        left_brother_node = father.children[left_brother_index]
        if left_brother_node.count <= math.ceil(self.degree/2):
            return False
        self.keys.append(left_brother_node.keys.pop())
        if not self.is_leaf:
            self.children.append(left_brother_node.children.pop())
        father.keys[left_brother_index] = left_brother_node.keys[-1]
        self.count += 1
        left_brother_node.count -= 1
        return True

    def merge_with_child_node(self):
        child_node = self.children[0]
        for child in child_node.children:
            child.father = self
        self.children = child_node.children
        self.keys = child_node.keys
        self.count = child_node.count
        self.is_leaf = len(self.children) == 0

    def check_count_too_small(self):
        least_count = math.ceil(self.degree/2)
        if self.count >= least_count:
            return
        if not self.father:
            if self.count == 1:
                self.merge_with_child_node()
        else:
            self_index = self.find_self_index()
            father_count = self.father.count
            if self_index+1 < father_count and self.borrow_from_right_brother_node(self_index):
                return
            if self_index > 0 and self.borrow_from_left_brother_node(self_index-1):
                return
            if self_index+1 < father_count:
                self.merge_into_right_brother_node(self_index)
                self.father.check_count_too_small()
                return
            if self_index > 0:
                self.merge_with_left_brother_code(self_index)
                self.father.check_count_too_small()

    def change_key_recursively(self, changed_child, new_key):
        i = 0
        while i < self.count:
            if self.children[i] is changed_child:
                self.keys[i] = new_key
                if self.father and i == self.count-1:
                    self.father.change_key_recursively(self, new_key)
                break
            i += 1

    def delete_key(self, index):
        if index == self.count-1 and index > 0 and self.keys[index] != self.keys[index-1] and self.father:
            self.father.change_key_recursively(self, self.keys[index - 1])
        self.keys.pop(index)
        self.count -= 1
        if self.father:
            self.check_count_too_small()


class BpTree:

    def __init__(self, degree=3):
        self.degree = degree
        self.root = MyBPlusTreeNode(self.degree)
        self.count = 0
    def insert(self, key):
        self.root.add_key(key)

    def find_key(self, key):
        return self.root.find_key(key)

    def contains(self, key):
        if self.find_key(key)[0]:
            return True
        return False
    
    def remove(self, key):
        node, index = self.find_key(key)
        if self.contains(key):
            node.delete_key(index)
            return True
        return False
            
    def add_to_graph_recursively(self, g, node:MyBPlusTreeNode, father_count, node_index):
        self.count += 1
        current_count = self.count
        nohtml_str = ""
        i = 0
        if node.is_leaf:
            for i in range(node.count):
                nohtml_str = nohtml_str+"<%d>%d|"%(i,node.keys[i])
            nohtml_str = nohtml_str[:-1]
            g.node(str(current_count),nohtml(nohtml_str))
            if father_count >= 0:
                g.edge("%d:%d" % (father_count, node_index),
                    "%d:%d" % (current_count, node.count//2))
        else:
            for i in range(node.count):
                nohtml_str = nohtml_str + "<%d>|" % (2 * i)
                self.add_to_graph_recursively(g, node.children[i], current_count, 2 * i)
                if i<node.count-1:
                    nohtml_str = nohtml_str + "<%d>%d|" % (2 * i + 1, node.keys[i])
            nohtml_str = nohtml_str[:-1]
            g.node(str(current_count), nohtml(nohtml_str))
            if father_count >= 0:
                g.edge("%d:%d" % (father_count, node_index),
                    "%d:%d" % (current_count, node.count-1))   
                    
    def plotTree(self):
        output_dir = os.path.join(os.environ['TEMP'], 'bptree')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'bptree_graph')
        g = Digraph('g', filename=output_path,
                    node_attr={'shape': 'record', 'height': '.1'},format='png')
        self.count = 0
        self.add_to_graph_recursively(g, self.root, -1, -1)
        g.render(filename=output_path, format='png', cleanup=True)
        