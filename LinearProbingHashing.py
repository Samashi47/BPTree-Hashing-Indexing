class MyHashSet:
    def __init__(self, size=11, load_factor=0.75):
        self.capacity = size + 11
        self.loadFactorThreshold = load_factor
        self.size = size
        self.table = [None] * self.capacity

    def clear(self):
        self.size = 0
        self.remove_elements()

    def contains(self, e):
        i = self.hash(e)
        k = i
        while self.table[i] is not None:
            if self.table[i] != 'X' and self.table[i] == e:
                return True
            i = (i + 1) % len(self.table)
            if i == k:
                return False
        return False

    def remove_entries(self):
        for i in range(len(self.table)):
            self.table[i] = None

    def add(self, e):
        if self.contains(e):
            return False

        if self.size + 1 > self.capacity * self.loadFactorThreshold:
            self.rehash()

        i = self.hash(e)

        while self.table[i] is not None and self.table[i] != 'X':
            i = (i + 1) % len(self.table)

        self.table[i] = e
        self.size += 1
        return True

    def remove(self, e):
        if not self.contains(e):
            return False

        i = self.hash(e)

        while self.table[i] is not None and self.table[i] != e:
            i = (i + 1) % len(self.table)

        if self.table[i] is not None and self.table[i] == e:
            self.table[i] = 'X'

        self.size -= 1
        return True

    def is_empty(self):
        return self.size == 0

    def get_size(self):
        return self.size

    def hash(self, hash_code):
        return hash_code % self.capacity

    def remove_elements(self):
        for i in range(len(self.table)):
            if self.table[i] is not None:
                self.table[i] = None

    def rehash(self):
        lst = self.set_to_list()
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in lst:
            self.add(item)

    def set_to_list(self):
        lst = []
        for i in range(len(self.table)):
            if self.table[i] is not None and self.table[i] != 'X':
                lst.append(self.table[i])
        return lst

    def __str__(self):
        lst = self.table
        builder = ""

        for i in range(len(lst)):
            if lst[i] is None:
                builder += str(i) + " -> None\n"
            else:
                builder += str(i) + " -> " + str(lst[i]) + "\n"

        return builder


if __name__ == "__main__":
    LinProbHash = MyHashSet(size=11, load_factor=0.75)
    print('Table size Before Addition: ', LinProbHash.get_size())
    for elem in [4371, 1323, 6173, 4199, 4344, 9679, 1989, 1241, 5464, 1242, 12342, 12324, 21412, 124124, 7658, 6856,
                 8578, 23436]:
        LinProbHash.add(elem)  # Assuming key is the same as the value for simplicity
    print('Table size After Addition: ', LinProbHash.get_size())
    print(LinProbHash)
