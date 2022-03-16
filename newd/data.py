class MyData:
    def __init__(self):
        self._mylist = []

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == len(self._mylist):
            raise StopIteration
        self._index += 1
        return self._mylist[self._index - 1]

    def __getitem__(self, item):
        return self._mylist[item]

    def __setitem__(self, key, value):
        self._mylist[key] = value

    def append(self, item):
        self._mylist.append(item)

    def __len__(self):
        return len(self._mylist)

    def pop(self, index):
        self._mylist.pop(index)

    def get_all(self):
        return self._mylist
