class DoubleHashing:
    def __init__(self, size=10, load_factor=0.75):
        self.hashtablesize = size
        self.load_factor = load_factor
        self.hashtable = [None] * self.hashtablesize
        self.num_elements = 0

    def h(self, key):
        return key % self.hashtablesize

    def h2(self, element):
        prime = 7
        return prime - (element % prime)

    def dHash(self, element):
        i = self.h(element)
        j = 0
        step = 1
        hash2 = self.h2(element)

        while self.hashtable[(i + j * hash2) % self.hashtablesize] is not None:
            j = (j + step) % self.hashtablesize
            step += 1

        return (i + j * hash2) % self.hashtablesize

    def resize(self, new_size):
        old_table = self.hashtable
        self.hashtablesize = new_size
        self.hashtable = [None] * new_size
        self.num_elements = 0

        for elem in old_table:
            if elem is not None:
                self.insert(elem)

    def insert(self, element):
        if self.num_elements / self.hashtablesize > self.load_factor:
            # Resize the table if load factor exceeds the threshold
            new_size = self.hashtablesize * 2
            self.resize(new_size)

        i = self.h(element)
        if self.hashtable[i] is None:
            self.hashtable[i] = element
            self.num_elements += 1
        else:
            i = self.dHash(element)
            self.hashtable[i] = element
            self.num_elements += 1

    def search(self, key):
        i = self.h(key)
        j = 0
        while self.hashtable[(i + j) % self.hashtablesize] != key:
            if self.hashtable[(i + j) % self.hashtablesize] is None:
                return False
            j += 1
        return True

    def remove_entries(self):
        for i in range(self.hashtablesize):
            self.hashtable[i] = None

    def remove(self, e):
        if not self.search(e):
            return False

        k = self.h(e)
        j = 1
        i = k

        while self.hashtable[i] is not None and self.hashtable[i] != e:
            i = abs((k + j * self.h2(k)) % len(self.hashtable))
            j += 1

        if self.hashtable[i] is not None and self.hashtable[i] == e:
            # A special marker Entry(null, null) is placed for the deleted
            # entry
            self.hashtable[i] = None

        self.num_elements -= 1  # Decrease size
        return True
    
    def display(self):
        for i in range(self.hashtablesize):
            print(f"{i}-> {self.hashtable[i]}", end=" ")
