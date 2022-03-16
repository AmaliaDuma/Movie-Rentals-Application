class FunctionCall:
    def __init__(self, fun_name, *fun_params):
        self._fun_name = fun_name
        self._fun_params = fun_params

    def call(self):
        return self._fun_name(*self._fun_params)

    def __call__(self):
        return self.call()


class Operation:
    def __init__(self, fun_call_undo, fun_call_redo):
        self._fun_call_undo = fun_call_undo
        self._fun_call_redo = fun_call_redo

    def undo(self):
        self._fun_call_undo()

    def redo(self):
        self._fun_call_redo()


class UndoService:
    def __init__(self):
        # List of operations with support for undo/redo
        self._history = []
        self._index = -1

    def record(self, operation):
        self._history.append(operation)
        if self._index != len(self._history)-1:
            self._index = len(self._history)-1
        else:
            self._index += 1

    def undo(self):
        if self._index == -1:
            return False
        try:
            self._history[self._index].undo()
            self._index -= 1
        except:
            self._index -= 1
        return True

    def redo(self):
        if self._index == len(self._history) - 1:
            return False

        self._index += 1
        self._history[self._index].redo()
        return True
