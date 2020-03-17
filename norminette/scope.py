class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.name = type(self).__name__
        self.lvl = (parent.lvl + 1) if parent is not None else 0
        self.indent = (parent.indent + 1) if parent is not None else 0
        self.lines = 0
        # ########################################################## #
        self.vdeclarations_allowed = True
        self.vars = 0
        self.vars_alignment = 0
        # ########################################################## #
        self.fdeclarations_allowed = False  # False everywhere but GlobalScope

    def inner(self, sub):
        return sub(self)

    def outer(self):
        if self.parent is not None:
            self.parent.lines += self.lines
        return self.parent


class GlobalScope(Scope):
    def __init__(self):
        super().__init__()
        self.fdeclarations_allowed = True
        self.fnames = []
        self.functions = 0
        self.func_alignment = 0


class Function(Scope):
    """
    Function definition scope, anything between the opening/closing braces of
    a function
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.fname_pos = 0
        self.args = []


class ControlStructure(Scope):
    """
    Control structures scopes (if/else, while, for, do-while, ...), don't
    necessarily have opening/closing braces. If they don't, they can contain
    only one instruction, if that instruction creates a new sub scope, it can
    contain as many instruction as that scope can "hold"
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.multiline = True

class UserDefinedType(Scope):
    """
    User defined type scope (struct, union, enum), only variables declarations
    are allowed within this scope
    """
    def __init__(self, parent, typedef=False):
        super().__init__(parent)
        self.typedef = typedef


class VariableAssignation(Scope):
    """
    This isn't an 'actual' C scope, but it'll help us parse multiple
    assignations (int foo[4] = {0, 0, 0, 0};) easier.
    """
    pass
