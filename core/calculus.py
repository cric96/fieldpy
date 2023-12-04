from core.vm import VM


class FieldCalculus:
    def __init__(self, vm: VM):
        self.vm = vm

    def rep(self, init, update):
        self.vm.enter('rep')
        local = self.vm.received
        # if local has id it takes that value, otherwise it takes the init value
        if local.keys().__contains__(self.vm.context.id):
            current = local.get(self.vm.context.id)
            updated = update(current)
        else:
            updated = init()
        self.vm.store(updated)
        self.vm.exit()
        return updated

    def mid(self):
        return self.vm.context.id

    def nbr(self, query):
        self.vm.enter('nbr')
        data = query()
        toSend = {nid: data for nid in self.vm.context.neighbours}
        self.vm.send(toSend)
        self.vm.exit()
        return self.vm.received

    def branch(self, condition, then, orElse):
        evaluated = condition()
        tag = 'branch-' + str(evaluated)
        self.vm.enter(tag)
        data = then() if evaluated else orElse()
        self.vm.exit()
        return data
