class Progress:
    """ Represents the progress of something.
    Examples:
        - Number of tasks completed
        - Number of story points achieved
    """

    def __init__(self, total: int, completed: int) -> None:
        if total < completed:
            raise ValueError('total cannot be less than completed')
        self.total = total
        self.completed = completed
        self.remaining = total - completed
        self.percent = int(completed / total * 100) if total != 0 else 0
