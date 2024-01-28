class DoubleHashing:
    def __init__(self, size=10, load_factor=0.7):
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

    def display(self):
        for i in range(self.hashtablesize):
            print(f"{i}-> {self.hashtable[i]}", end=" ")


if __name__ == "__main__":
    H = DoubleHashing(size=11)
    
    for elem in [4371, 1323, 6173, 4199, 4344, 9679, 1989, 1241, 5464, 1242]:
        H.insert(elem)
    
    H.display()