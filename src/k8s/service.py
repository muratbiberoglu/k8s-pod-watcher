from collections import defaultdict
from typing import List

from src.util.modifiers import Modifiers
from src.k8s.pod import Pod
from src.table.row import Row
from src.table.table import Table


class Service:
    def __init__(self, name: str, detailed: bool = False):
        self.name = name
        self.detailed = detailed
        self.pods: List[Pod] = []

    def add_pod(self, pod: Pod):
        self.pods.append(pod)

    def clear(self):
        self.pods = []

    def __str__(self):
        result = ""
        healthy_count = sum(pod.status == "Running" and pod.ready for pod in self.pods)
        health_color = (Modifiers.BRED if healthy_count == 0 else
                        Modifiers.BYELLOW if healthy_count < len(self.pods) else
                        Modifiers.BGREEN)

        result += f"{health_color} {Modifiers.NORMAL} {Modifiers.BOLD}{self.name}{Modifiers.NORMAL}\n"

        commit_pods_map = defaultdict(list)
        for pod in self.pods:
            commit_pods_map[pod.commit_hash].append(pod)

        for commit_hash, pods in commit_pods_map.items():
            status_items = defaultdict(int)
            for pod in pods:
                status_items[pod.status] += 1

            commit_text = f"\t{Modifiers.BOLD}[{commit_hash}]{Modifiers.NORMAL} | "
            status_text = f"Total: {len(pods)}"
            for status, count in status_items.items():
                status_text += f", {status}: {count}"
            commit_text += status_text + "\n"

            result += commit_text

            if self.detailed:
                table = Table()
                table.add_row(Row(["#", "POD NAME", "READY", "STATUS", "RESTART COUNT", "AGE", "CPU", "MEM"]))
                for pod in pods:
                    table.add_row(pod.to_row())
                result += table.to_string(1) + "\n"

        return result.strip()
