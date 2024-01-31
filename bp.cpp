#include <iostream>
#include <vector>
#include <queue>

const int MIN_DEGREE = 2;

class BpTreeNode {
public:
    std::vector<int> keys;
    std::vector<BpTreeNode*> children;
    bool isLeaf;

    BpTreeNode(bool isLeafNode) : isLeaf(isLeafNode) {}
};

class BpTree {
private:
    BpTreeNode* root;

    // Helper function for insertion
    void insertNonFull(BpTreeNode* node, int value);

    // Helper function for splitting a child
    void splitChild(BpTreeNode* parent, int index);

    // Helper function for searching a key in the tree
    BpTreeNode* searchNode(BpTreeNode* node, int value);

    // Helper function for deleting a key from the tree
    void deleteKey(BpTreeNode* node, int value);

    // Helper function for deleting from a non-leaf node
    void deleteFromNonLeaf(BpTreeNode* node, int value);

    // Helper function for finding the predecessor of a key
    int getPredecessor(BpTreeNode* node);

    // Helper function for finding the successor of a key
    int getSuccessor(BpTreeNode* node);

    // Helper function for filling a child node
    void fillChild(BpTreeNode* node, int index);

    // Helper function for printing the tree in a tree-like manner
    void printTree(BpTreeNode* root);

    // Helper function for getting the maximum degree of the tree
    int getMaxDegree(BpTreeNode* node);

public:
    BpTree() : root(nullptr) {}

    // Function to insert a value into the tree
    void insert(int value);

    // Function to delete a value from the tree
    void remove(int value);

    // Function to search for a value in the tree
    bool search(int value);

    // Function to print the tree in a tree-like manner
    void printTree();

    // Function to get the maximum degree of the tree
    int maxDegree();
};

void BpTree::insert(int value) {
    if (root == nullptr) {
        root = new BpTreeNode(true);
        root->keys.push_back(value);
    } else {
        if (root->keys.size() == 2 * MIN_DEGREE - 1) {
            BpTreeNode* newRoot = new BpTreeNode(false);
            newRoot->children.push_back(root);
            splitChild(newRoot, 0);
            root = newRoot;
        }
        insertNonFull(root, value);
    }
}

void BpTree::insertNonFull(BpTreeNode* node, int value) {
    int index = node->keys.size() - 1;

    if (node->isLeaf) {
        while (index >= 0 && value < node->keys[index]) {
            index--;
        }

        node->keys.insert(node->keys.begin() + index + 1, value);
    } else {
        while (index >= 0 && value < node->keys[index]) {
            index--;
        }

        index++;
        if (node->children[index]->keys.size() == 2 * MIN_DEGREE - 1) {
            splitChild(node, index);

            if (value > node->keys[index]) {
                index++;
            }
        }

        insertNonFull(node->children[index], value);
    }
}

void BpTree::splitChild(BpTreeNode* parent, int index) {
    BpTreeNode* child = parent->children[index];
    BpTreeNode* newChild = new BpTreeNode(child->isLeaf);
    
    parent->keys.insert(parent->keys.begin() + index, child->keys[MIN_DEGREE - 1]);

    parent->children.insert(parent->children.begin() + index + 1, newChild);

    newChild->keys.assign(child->keys.begin() + MIN_DEGREE, child->keys.end());
    child->keys.resize(MIN_DEGREE - 1);

    if (!child->isLeaf) {
        newChild->children.assign(child->children.begin() + MIN_DEGREE, child->children.end());
        child->children.resize(MIN_DEGREE);
    }
}

bool BpTree::search(int value) {
    return searchNode(root, value) != nullptr;
}

BpTreeNode* BpTree::searchNode(BpTreeNode* node, int value) {
    if (node == nullptr) {
        return nullptr;
    }

    int i = 0;
    while (i < node->keys.size() && value > node->keys[i]) {
        i++;
    }

    if (i < node->keys.size() && value == node->keys[i]) {
        return node;
    } else if (node->isLeaf) {
        return nullptr;
    } else {
        return searchNode(node->children[i], value);
    }
}

void BpTree::remove(int value) {
    if (root == nullptr) {
        return;
    }

    deleteKey(root, value);

    if (root->keys.size() == 0 && !root->isLeaf) {
        BpTreeNode* newRoot = root->children[0];
        delete root;
        root = newRoot;
    }
}

void BpTree::deleteKey(BpTreeNode* node, int value) {
    int i = 0;
    while (i < node->keys.size() && value > node->keys[i]) {
        i++;
    }

    if (i < node->keys.size() && value == node->keys[i]) {
        if (node->isLeaf) {
            node->keys.erase(node->keys.begin() + i);
        } else {
            deleteFromNonLeaf(node, value);
        }
    } else {
        if (node->isLeaf) {
            return;
        }

        bool lastChild = (i == node->keys.size());

        if (node->children[i]->keys.size() < MIN_DEGREE) {
            fillChild(node, i);
        }

        if (lastChild && i > node->keys.size()) {
            deleteKey(node->children[i - 1], value);
        } else {
            deleteKey(node->children[i], value);
        }
    }
}

void BpTree::deleteFromNonLeaf(BpTreeNode* node, int value) {
    int i = 0;
    while (i < node->keys.size() && value > node->keys[i]) {
        i++;
    }

    int keyValue = node->keys[i];

    if (node->children[i]->keys.size() >= MIN_DEGREE) {
        int predecessor = getPredecessor(node->children[i]);
        node->keys[i] = predecessor;
        deleteKey(node->children[i], predecessor);
    } else if (node->children[i + 1]->keys.size() >= MIN_DEGREE) {
        int successor = getSuccessor(node->children[i + 1]);
        node->keys[i] = successor;
        deleteKey(node->children[i + 1], successor);
    } else {
        node->children[i]->keys.push_back(keyValue);
        node->children[i]->keys.insert(
            node->children[i]->keys.end(),
            node->children[i + 1]->keys.begin(),
            node->children[i + 1]->keys.end()
        );

        if (!node->children[i]->isLeaf) {
            node->children[i]->children.insert(
                node->children[i]->children.end(),
                node->children[i + 1]->children.begin(),
                node->children[i + 1]->children.end()
            );
        }

        delete node->children[i + 1];
        node->children.erase(node->children.begin() + i + 1);

        deleteKey(node->children[i], value);
    }
}

int BpTree::getPredecessor(BpTreeNode* node) {
    while (!node->isLeaf) {
        node = node->children.back();
    }
    return node->keys.back();
}

int BpTree::getSuccessor(BpTreeNode* node) {
    while (!node->isLeaf) {
        node = node->children.front();
    }
    return node->keys.front();
}

void BpTree::fillChild(BpTreeNode* node, int index) {
    if (index != 0 && node->children[index - 1]->keys.size() >= MIN_DEGREE) {
        BpTreeNode* child = node->children[index];
        BpTreeNode* sibling = node->children[index - 1];

        child->keys.insert(child->keys.begin(), node->keys[index - 1]);
        node->keys[index - 1] = sibling->keys.back();

        if (!child->isLeaf) {
            child->children.insert(child->children.begin(), sibling->children.back());
            sibling->children.pop_back();
        }

        sibling->keys.pop_back();
    } else if (index != node->keys.size() && node->children[index + 1]->keys.size() >= MIN_DEGREE) {
        BpTreeNode* child = node->children[index];
        BpTreeNode* sibling = node->children[index + 1];

        child->keys.push_back(node->keys[index]);
        node->keys[index] = sibling->keys.front();

        if (!child->isLeaf) {
            child->children.push_back(sibling->children.front());
            sibling->children.erase(sibling->children.begin());
        }

        sibling->keys.erase(sibling->keys.begin());
    } else {
        if (index != node->keys.size()) {
            BpTreeNode* child = node->children[index];
            BpTreeNode* sibling = node->children[index + 1];

            child->keys.push_back(node->keys[index]);
            child->keys.insert(
                child->keys.end(),
                sibling->keys.begin(),
                sibling->keys.end()
            );

            if (!child->isLeaf) {
                child->children.insert(
                    child->children.end(),
                    sibling->children.begin(),
                    sibling->children.end()
                );
            }

            node->keys.erase(node->keys.begin() + index);
            node->children.erase(node->children.begin() + index + 1);
            delete sibling;
        } else {
            BpTreeNode* child = node->children[index];
            BpTreeNode* sibling = node->children[index - 1];

            sibling->keys.push_back(node->keys[index - 1]);
            sibling->keys.insert(
                sibling->keys.end(),
                child->keys.begin(),
                child->keys.end()
            );

            if (!child->isLeaf) {
                sibling->children.insert(
                    sibling->children.end(),
                    child->children.begin(),
                    child->children.end()
                );
            }

            node->keys.erase(node->keys.begin() + index - 1);
            node->children.erase(node->children.begin() + index);
            delete child;
        }
    }
}

int BpTree::maxDegree() {
    return getMaxDegree(root);
}

int BpTree::getMaxDegree(BpTreeNode* node) {
    if (node == nullptr) {
        return 0;
    }

    int maxDegree = node->keys.size();

    if (!node->isLeaf) {
        for (auto child : node->children) {
            maxDegree = std::max(maxDegree, getMaxDegree(child));
        }
    }

    return maxDegree;
}

void BpTree::printTree() {
    printTree(root);
    std::cout << std::endl;
}

void BpTree::printTree(BpTreeNode* root) {
    if (root != nullptr) {
        std::queue<BpTreeNode*> nodesQueue;
        nodesQueue.push(root);

        while (!nodesQueue.empty()) {
            int nodesCount = nodesQueue.size();

            while (nodesCount > 0) {
                BpTreeNode* currentNode = nodesQueue.front();
                nodesQueue.pop();

                for (int i = 0; i < currentNode->keys.size(); ++i) {
                    std::cout << currentNode->keys[i] << " ";
                }

                if (!currentNode->isLeaf) {
                    for (auto child : currentNode->children) {
                        nodesQueue.push(child);
                    }
                }

                std::cout << "| ";

                nodesCount--;
            }

            std::cout << std::endl;
        }
    }
}

int main() {
    BpTree tree;

    // Insert some values
    for (int value : {4371, 1323, 6173, 4199, 4344, 9679, 1989}) { // , 1241, 5464, 1242, 1342, 1224, 2141, 1244, 7658, 6856, 8578, 2346
        tree.insert(value);
    }

    // Print the tree
    std::cout << "B+ Tree:" << std::endl;
    tree.printTree();

    // Search for a value
    int searchValue = 6;
    std::cout << "Search for value " << searchValue << ": " << (tree.search(searchValue) ? "Found" : "Not found") << std::endl;

    // Delete a value
    int deleteValue = 4371;
    tree.remove(deleteValue);

    // Print the tree after deletion
    std::cout << "B+ Tree after deletion:" << std::endl;
    tree.printTree();

    // Get the maximum degree
    std::cout << "Maximum degree of the tree: " << tree.maxDegree() << std::endl;

    return 0;
}
