import matplotlib.pyplot as plt
import random

class Node:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.next_leaf = None

class BPlusTree:
    def __init__(self, degree):
        self.root = Node(leaf=True)
        self.degree = degree

    def insert(self, key):
        if key in self.search(key):
            return  # Key already exists in the tree

        if len(self.root.keys) == (2 * self.degree) - 1:
            new_root = Node()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        index = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while index >= 0 and key < node.keys[index]:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = key
        else:
            while index >= 0 and key < node.keys[index]:
                index -= 1
            index += 1
            if len(node.children[index].keys) == (2 * self.degree) - 1:
                self._split_child(node, index)
                if key > node.keys[index]:
                    index += 1
            self._insert_non_full(node.children[index], key)

    def _split_child(self, parent, index):
        degree = self.degree
        child = parent.children[index]
        new_child = Node(leaf=child.leaf)
        parent.keys.insert(index, child.keys[degree - 1])
        parent.children.insert(index + 1, new_child)

        new_child.keys = child.keys[degree:]
        child.keys = child.keys[:degree]

        if not child.leaf:
            new_child.children = child.children[degree:]
            child.children = child.children[:degree]

    def delete(self, key):
        self._delete_key(self.root, key)

    def _delete_key(self, node, key):
        if not node:
            return None

        # Find the index of the key to be deleted
        index = 0
        while index < len(node.keys) and key > node.keys[index]:
            index += 1

        if index < len(node.keys) and key == node.keys[index]:
            # If the node is a leaf, directly delete the key
            if node.leaf:
                del node.keys[index]
            else:
                # If the node is not a leaf
                # Case 1: Key exists in this node
                if node.children[index].leaf:
                    # Case 1a: Key exists in a leaf node directly under this node
                    del node.keys[index]
                else:
                    # Case 1b: Key exists in a non-leaf node, find the predecessor
                    predecessor = self._get_predecessor(node, index)
                    node.keys[index] = predecessor
                    # Delete the predecessor key from the child node
                    self._delete_key(node.children[index], predecessor)
        else:
            # Key is not in this node, move to the appropriate child node
            if node.leaf:
                # Key not found in the tree
                return None
            # Determine if the child needs to be merged or redistributed
            if len(node.children[index].keys) < self.degree:
                self._borrow_or_merge(node, index)
            # Recursively delete the key in the appropriate child
            self._delete_key(node.children[index], key)

    def _get_predecessor(self, node, index):
        # Find the rightmost key in the subtree to replace the deleted key
        current_node = node.children[index]
        while not current_node.leaf:
            current_node = current_node.children[-1]
        return current_node.keys[-1]

    def _borrow_or_merge(self, node, index):
        # Try to borrow a key from left or right sibling
        if index != 0 and len(node.children[index - 1].keys) >= self.degree:
            self._borrow_from_left_sibling(node, index)
        elif index != len(node.keys) and len(node.children[index + 1].keys) >= self.degree:
            self._borrow_from_right_sibling(node, index)
        else:
            # Merge with the right sibling if borrowing isn't possible
            if index != len(node.keys):
                self._merge_nodes(node, index)
            else:
                self._merge_nodes(node, index - 1)

    def _borrow_from_left_sibling(self, node, index):
        child = node.children[index]
        sibling = node.children[index - 1]

        # Move key from the left sibling to current node
        child.keys.insert(0, node.keys[index - 1])
        node.keys[index - 1] = sibling.keys.pop()

        # If the child is not a leaf, move child pointer as well
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_right_sibling(self, node, index):
        child = node.children[index]
        sibling = node.children[index + 1]

        # Move key from the right sibling to current node
        child.keys.append(node.keys[index])
        node.keys[index] = sibling.keys.pop(0)

        # If the child is not a leaf, move child pointer as well
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def _merge_nodes(self, node, index):
        child = node.children[index]
        sibling = node.children[index + 1]

        # Merge sibling into child
        child.keys.append(node.keys.pop(index))
        child.keys.extend(sibling.keys)

        # If the child is not a leaf, merge child pointers as well
        if not child.leaf:
            child.children.extend(sibling.children)

        # Remove the sibling node from parent
        node.children.pop(index + 1)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None:
            return []

        index = 0
        while index < len(node.keys) and key > node.keys[index]:
            index += 1

        if index < len(node.keys) and key == node.keys[index]:
            return [key]

        if node.leaf:
            return []

        return self._search_recursive(node.children[index], key)

    def print_tree_recursive(self, node=None, level=0):
        if node is None:
            node = self.root

        if node is None:
            return

        # Print the node keys
        print('  ' * level, node.keys)

        # Print the children recursively
        if not node.leaf:
            for child in node.children:
                self.print_tree_recursive(child, level + 1)
        
    def _plot_tree(self, node, ax, x=0, y=0, level=0):
        if node is None:
            return

        # Draw the node
        ax.text(x, y, str(node.keys), ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))

        # Draw the children recursively
        if not node.leaf:
            child_x = x - (len(node.children) * 0.5)
            child_y = y - 1.5
            for child in node.children:
                self._plot_tree(child, ax, child_x, child_y, level + 1)
                child_x += 1

                # Draw the edges
                ax.plot([x, child_x], [y, child_y + 0.5], color='black')

        # Draw the keys
        for i, key in enumerate(node.keys):
            ax.text(x + i, y - 0.5, str(key), ha='center', va='center')

    def visualize_tree(self):
        fig, ax = plt.subplots()
        self._plot_tree(self.root, ax)
        ax.axis('off')
        plt.show()

if __name__ == '__main__':
    b_plus_tree = BPlusTree(degree=3)

    for i in range(10):
        elem = random.randint(0,10000)
        print(f"Inserting {elem} into the tree...")
        b_plus_tree.insert(elem)

    b_plus_tree.print_tree_recursive()
    b_plus_tree.visualize_tree()