from src.util.modifiers import Modifiers
from src.table.row import Row


class Pod:
    def __init__(self, pod_str: str):
        self.fullname, ready, status, restart_count, age = pod_str.split(",")

        # parse full name and set service, commit and container hashes
        split_fullname = self.fullname.split("-")
        self.container_hash = split_fullname[-1]
        self.commit_hash = split_fullname[-2]
        self.service = "-".join(split_fullname[:-2])

        # set ready, status, restart count and age
        self.ready = ready == "1/1"
        self.status = status
        self.restart_count = int(restart_count)
        self.age = age

        self.cpu = ""
        self.mem = ""

    def __str__(self) -> str:
        return f"{self.service} [{self.commit_hash}] ({self.container_hash}) ---> {self.status}"

    def to_row(self) -> Row:
        return Row([
            " ",
            self.fullname,
            "1" if self.ready else "0",
            self.status,
            str(self.restart_count),
            self.age,
            self.cpu,
            self.mem
        ],
            [(
                Modifiers.BGREEN if self.status == "Running" and self.ready else
                Modifiers.BYELLOW if self.status == "Running" else
                Modifiers.BRED
            )]
        )
