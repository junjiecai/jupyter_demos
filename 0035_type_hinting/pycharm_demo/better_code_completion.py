# better auto-hinting
class Command:
    def execute(self):
        pass


class Task:
    # def __init__(self, cmd):
    def __init__(self, cmd: Command):
        self.cmd = cmd

    # 比较存在/缺失type hinting情况下，self.cmd的code completion表现
    def run(self):
        self.cmd.execute()


# def create_command(command):
def create_command(command) -> Command:
    return command


def get_object():
    return create_command()


# 比较存在/缺失type hinting情况下，get_object()的code completion表现
get_object().execute()
