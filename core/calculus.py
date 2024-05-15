from typing import TypeVar, Callable

from core.vm import VM, Field

T = TypeVar('T')

class FieldCalculus:
    """
    Class representing field calculus operations.
    """

    def __init__(self, vm: VM):
        self.vm = vm

    def rep(self, init: Callable[[], T], update: Callable[[T], T]) -> T:
        """
        Performs a replication operation.

        Args:
            init: A function that returns the initial value.
            update: A function that updates the current value.

        Returns:
            The updated value.
        """
        self.vm.enter('rep')
        local = self.vm.received
        if local.keys().__contains__(self.vm.context.id):
            current = local.get(self.vm.context.id)
            updated = update(current)
        else:
            updated = init()
        self.vm.store(updated)
        self.vm.exit()
        return updated

    def mid(self) -> int:
        """
        Returns the ID of the current context.

        Returns:
            The ID of the current context.
        """
        return self.vm.context.id

    def nbr(self, query: T) -> Field[T]:
        """
        Sends a query to the neighbors and returns the received data as a Field object.

        Args:
            query: A function that generates the query data.

        Returns:
            A Field object containing the received data.
        """
        self.vm.enter('nbr')
        data = query
        to_send = {nid: data for nid in self.vm.context.neighbours()}
        self.vm.send(to_send)
        received = self.vm.received
        received.update({self.vm.context.id: data})
        self.vm.exit()

        return Field(self.vm, received)

    def branch(self, condition: Callable[[], bool], then: Callable[[], T], or_else: Callable[[], T]) -> T:
        """
        Performs a branching operation based on a condition.

        Args:
            condition: A function that evaluates the condition.
            then: A function to be executed if the condition is True.
            or_else: A function to be executed if the condition is False.

        Returns:
            The result of the executed function.
        """
        evaluated = condition()
        tag = 'branch-' + str(evaluated)
        self.vm.enter(tag)
        data = then() if evaluated else or_else()
        self.vm.exit()
        return data
