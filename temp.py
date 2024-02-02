import LinearProbingHashing as lph
import SHashing as sh
import DHashing as dh
import BPTree as bpt

if __name__ == "__main__":
    LinProbHash = lph.LinProbHashSet(size=11, load_factor=0.75)
    print('Table size Before Addition: ', LinProbHash.get_size())
    for elem in [1, 2, 3]:
        LinProbHash.insert(elem)  # Assuming key is the same as the value for simplicity
    print('Table size After Addition: ', LinProbHash.get_size())
    LinProbHash.remove(2)
    print(LinProbHash)
    
if __name__ == "__main__":
    Ha = sh.HashTable(size=11,load_factor=0.75)

    for elem in [4371, 1323, 6173, 4199, 4344, 9679, 1989, 4343, 9678, 1988, 41455, 1626, 3478, 60798]:
        Ha.insert(elem)
    Ha.remove_elements()
    Ha.find_handler(133223)
    Ha.print_table()

if __name__ == "__main__":
    H = dh.DoubleHashing(size=11)
    
    for elem in [4371, 1323, 6173, 4199, 4344, 9679, 1989, 1241, 5464, 1242]:
        H.insert(elem)
    H.remove(4344)
    H.display()
    
if __name__ == "__main__":
    tree = bpt.BpTree()

    # Insert some values
    for value in [4371, 1323, 6173, 4199, 4344, 9679, 1989, 4343, 9678, 1988, 41455, 1626, 3478, 60798]:
        tree.insert(value)

    # Print the tree
    print("B+ Tree:")
    tree.printTree()

    # Delete a value
    delete_value = 4371
    tree.remove(delete_value)

    # Print the tree after deletion
    print("B+ Tree after deletion:")
    tree.printTree()

    # Get the maximum degree
    print("Maximum degree of the tree:", tree.maxDegree())
    tree.plotTree()