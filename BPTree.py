from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Node:
    def __init__(self, isLeafNode):
        self.keys = []
        self.children = []
        self.isLeaf = isLeafNode

class BpTree:
    def __init__(self, degree=2):
        self.root = None
        self.degree = degree
        
    def insert(self, value):
        if self.root is None:
            self.root = Node(True)
            self.root.keys.append(value)
        else:
            if len(self.root.keys) == 2 * self.degree - 1:
                newRoot = Node(False)
                newRoot.children.append(self.root)
                self.splitChild(newRoot, 0)
                self.root = newRoot
            self.insertNonFull(self.root, value)

    def insertNonFull(self, node, value):
        index = len(node.keys) - 1

        if node.isLeaf:
            while index >= 0 and value < node.keys[index]:
                index -= 1

            node.keys.insert(index + 1, value)
        else:
            while index >= 0 and value < node.keys[index]:
                index -= 1

            index += 1
            if len(node.children[index].keys) == 2 * self.degree - 1:
                self.splitChild(node, index)

                if value > node.keys[index]:
                    index += 1

            self.insertNonFull(node.children[index], value)

    def splitChild(self, parent, index):
        child = parent.children[index]
        newChild = Node(child.isLeaf)
        
        parent.keys.insert(index, child.keys[self.degree - 1])

        parent.children.insert(index + 1, newChild)

        newChild.keys = child.keys[self.degree:]
        child.keys = child.keys[:self.degree - 1]

        if not child.isLeaf:
            newChild.children = child.children[self.degree:]
            child.children = child.children[:self.degree]

    def search(self, value):
        return self.searchNode(self.root, value) is not None

    def searchNode(self, node, value):
        if node is None:
            return None
        i = 0
        while i < len(node.keys) and value > node.keys[i]:
            i += 1
        if i < len(node.keys) and value == node.keys[i]:
            return node
        elif node.isLeaf:
            return None
        else:
            return self.searchNode(node.children[i], value)

    def remove(self, value):
        if self.root is None:
            return

        self.deleteKey(self.root, value)

        if len(self.root.keys) == 0 and not self.root.isLeaf:
            newRoot = self.root.children[0]
            del self.root
            self.root = newRoot

    def deleteKey(self, node, value):
        i = 0
        while i < len(node.keys) and value > node.keys[i]:
            i += 1

        if i < len(node.keys) and value == node.keys[i]:
            if node.isLeaf:
                del node.keys[i]
            else:
                self.deleteFromNonLeaf(node, value)
        else:
            if node.isLeaf:
                return

            lastChild = (i == len(node.keys))

            if len(node.children[i].keys) < self.degree:
                self.fillChild(node, i)

            if lastChild and i > len(node.keys):
                self.deleteKey(node.children[i - 1], value)
            else:
                self.deleteKey(node.children[i], value)

    def deleteFromNonLeaf(self, node, value):
        i = 0
        while i < len(node.keys) and value > node.keys[i]:
            i += 1

        keyValue = node.keys[i]

        if len(node.children[i].keys) >= self.degree:
            predecessor = self.getPredecessor(node.children[i])
            node.keys[i] = predecessor
            self.deleteKey(node.children[i], predecessor)
        elif len(node.children[i + 1].keys) >= self.degree:
            successor = self.getSuccessor(node.children[i + 1])
            node.keys[i] = successor
            self.deleteKey(node.children[i + 1], successor)
        else:
            node.children[i].keys.append(keyValue)
            node.children[i].keys.extend(node.children[i + 1].keys)

            if not node.children[i].isLeaf:
                node.children[i].children.extend(node.children[i + 1].children)

            del node.children[i + 1]
            del node.children[i + 1]

            self.deleteKey(node.children[i], value)

    def getPredecessor(self, node):
        while not node.isLeaf:
            node = node.children[-1]
        return node.keys[-1]

    def getSuccessor(self, node):
        while not node.isLeaf:
            node = node.children[0]
        return node.keys[0]

    def fillChild(self, node, index):
        if index != 0 and len(node.children[index - 1].keys) >= self.degree:
            child = node.children[index]
            sibling = node.children[index - 1]

            child.keys.insert(0, node.keys[index - 1])
            node.keys[index - 1] = sibling.keys[-1]

            if not child.isLeaf:
                child.children.insert(0, sibling.children[-1])
                sibling.children.pop()

            sibling.keys.pop()
        elif index != len(node.keys) and len(node.children[index + 1].keys) >= self.degree:
            child = node.children[index]
            sibling = node.children[index + 1]

            child.keys.append(node.keys[index])
            node.keys[index] = sibling.keys[0]

            if not child.isLeaf:
                child.children.append(sibling.children[0])
                sibling.children.pop(0)

            sibling.keys.pop(0)
        else:
            if index != len(node.keys):
                child = node.children[index]
                sibling = node.children[index + 1]

                child.keys.append(node.keys[index])
                child.keys.extend(sibling.keys)

                if not child.isLeaf:
                    child.children.extend(sibling.children)

                node.keys.pop(index)
                node.children.pop(index + 1)
            else:
                child = node.children[index]
                sibling = node.children[index - 1]

                sibling.keys.append(node.keys[index - 1])
                sibling.keys.extend(child.keys)

                if not child.isLeaf:
                    sibling.children.extend(child.children)

                node.keys.pop(index - 1)
                node.children.pop(index)

    def maxDegree(self):
        return self.getMaxDegree(self.root)

    def getMaxDegree(self, node):
        if node is None:
            return 0

        maxDegree = len(node.keys)

        if not node.isLeaf:
            for child in node.children:
                maxDegree = max(maxDegree, self.getMaxDegree(child))

        return maxDegree

    def printTree(self):
        self._printTree(self.root)
        print()

    def _printTree(self, root):
        if root is not None:
            nodesQueue = deque()
            nodesQueue.append(root)

            while nodesQueue:
                nodesCount = len(nodesQueue)

                while nodesCount > 0:
                    currentNode = nodesQueue.popleft()

                    for key in currentNode.keys:
                        print(key, end=" ")

                    if not currentNode.isLeaf:
                        for child in currentNode.children:
                            nodesQueue.append(child)

                    print("|", end=" ")

                    nodesCount -= 1

                print()

    def plotTree(self):
        fig, ax = plt.subplots()
        self.plotNode(ax, self.root, 0, 0, self.maxDegree())

        ax.set_aspect('equal', adjustable='datalim')
        plt.axis('off')
        plt.show()

    def plotNode(self, ax, node, level, x, max_degree):
        if node is not None:
            y = -level * 2  # Adjust the spacing between levels

            for i, key in enumerate(node.keys):
                ax.text(x + i, y, str(key), ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))

            if not node.isLeaf:
                for i, child in enumerate(node.children):
                    child_x = x + i * max_degree
                    self.plotNode(ax, child, level + 1, child_x, max_degree)

                    ax.add_patch(patches.FancyArrow(x + i, y - 0.5, child_x - x - i, 1, color='black', lw=1))
