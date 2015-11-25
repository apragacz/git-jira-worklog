class WorklogError(ValueError):
    pass


class CommandError(WorklogError):
    pass


class GitError(WorklogError):
    pass
