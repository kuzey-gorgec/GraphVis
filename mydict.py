class MyDict:
    def __init__(self, capacity=5): 
        self.capacity = capacity
        self.size = 0 
        self.memory = [[] for _ in range(capacity)]

    def hash_function(self, key):
        hash_value = 0
        for char in str(key):
            hash_value = (hash_value * 31 + ord(char))
        return hash_value % self.capacity 

    def add(self, key, value):

        if self.size / self.capacity >= 0.66:
            self._resize()

        index = self.hash_function(key)

        for i, (k, v) in enumerate(self.memory[index]):
            if k == key:
                self.memory[index][i] = (key, value)
                return
                

        self.memory[index].append((key, value))
        self.size += 1

    def get(self, key):
        index = self.hash_function(key)
        for k, v in self.memory[index]:
            if k == key:
                return v
        return None

    def get_elements(self):
        elements = []
        for bucket in self.memory:
            for k, v in bucket:
                elements.append((k, v))
        return elements

    def _resize(self):

        old_capacity = self.capacity
        self.capacity = self.capacity * 2
        """
        print(f"\n[SYSTEM ALERT] Dictionary is full! Resizing capacity: {old_capacity} -> {self.capacity}...")
        print(f"old memory: {self.memory}")
        """
        old_memory = self.memory
        self.memory = [[] for _ in range(self.capacity)] 
        self.size = 0 
        

        for bucket in old_memory:
            for k, v in bucket:
                self.add(k, v) 
        """
        print(f"new memory: {self.memory}")
        """
        