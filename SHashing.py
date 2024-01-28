class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, size=10, load_factor=0.7):
        self.bucket_count = size
        self.load_factor = load_factor
        self.bucket_array = [LinkedList() for _ in range(size)]
        self.num_elements = 0

    def hash_function(self, value):
        return value % self.bucket_count

    def get_list(self, index):
        return self.bucket_array[index]

    def find(self, value, lst):
        return value in lst

    def find_handler(self, val):
        index = self.get_list(self.hash_function(val))
        exists = self.find(val, index)
        print("Value exists" if exists else "Find unsuccessful: value does not exist")

    def insert(self, value):
        index = self.hash_function(value)
        lst = self.get_list(index)
        lst.append(value)
        self.num_elements += 1

        if self.load_factor < self.num_elements / self.bucket_count:
            self.resize()

    def delete(self, value):
        index = self.hash_function(value)
        lst = self.get_list(index)
        if self.find(value, lst):
            lst.remove(value)
            print("Value deleted")
            self.num_elements -= 1
        else:
            print("Delete unsuccessful: value does not exist")

    def print_table(self):
        for i in range(self.bucket_count):
            lst = self.get_list(i)
            print(f"{i} --> {lst}")
        print("")

    def resize(self):
        new_size = self.bucket_count * 2
        new_array = [LinkedList() for _ in range(new_size)]

        for i in range(self.bucket_count):
            lst = self.get_list(i)
            for elem in lst:
                new_index = elem % new_size
                new_array[new_index].append(elem)

        self.bucket_count = new_size
        self.bucket_array = new_array

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove(self, value):
        current = self.head
        if current and current.value == value:
            self.head = current.next
            return
        prev = None
        while current and current.value != value:
            prev = current
            current = current.next
        if current:
            prev.next = current.next

    def __contains__(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def __str__(self):
        result = []
        current = self.head
        while current:
            result.append(str(current.value))
            current = current.next
        return "[" + ", ".join(result) + "]"
    
    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

if __name__ == "__main__":
    H = HashTable(size=25,load_factor=0.5)

    for elem in [4371, 1323, 6173, 4199, 4344, 9679, 1989, 1241, 5464, 1242, 12342, 12324, 21412, 124124, 7658, 6856, 8578, 23436]:
        H.insert(elem)
    H.find_handler(133223)
    H.print_table()
