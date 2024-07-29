from subprocess import run, PIPE, CalledProcessError
from typing import List, Callable

from src.k8s.pod import Pod
from src.util.utils import format_string


class K8SService:
    def __init__(self, context: str, namespace: str):
        self.__context = context
        self.__namespace = namespace

    def get_deployment_names(self):
        try:
            result = self.__execute_kubectl_command(["get", "deployment"])
            result.check_returncode()
            get_deployment_name: Callable[[str], str] = lambda x: format_string(x).split(",")[0]
            return list(map(get_deployment_name, result.stdout.decode().strip().split("\n")[1:]))
        except CalledProcessError as e:
            print("Error occurred while getting deployment names:", e)
            raise e

    def get_pods(self) -> List[Pod]:
        try:
            result = self.__execute_kubectl_command(["get", "pods"])
            result.check_returncode()
            to_pod: Callable[[str], Pod] = lambda x: Pod(format_string(x))
            return list(map(to_pod, result.stdout.decode().strip().split("\n")[1:]))
        except CalledProcessError as e:
            print("Error occurred while getting pods:", e)
            raise e

    def get_pod_resource_usages(self) -> List[tuple]:
        try:
            result = self.__execute_kubectl_command(["top", "pods"])
            result.check_returncode()
            to_name_cpu_mem: Callable[[str], tuple] = lambda x: format_string(x).strip().split(",")
            return list(map(to_name_cpu_mem, result.stdout.decode().strip().split("\n")[1:]))
        except CalledProcessError as e:
            print("Error occurred while getting resource usages of pods:", e)
            raise e

    def __execute_kubectl_command(self, commands: List[str]):
        kubectl_args = ["kubectl"]
        kubectl_args.extend(commands)
        kubectl_args.append(f"--context={self.__context}")
        kubectl_args.append(f"--namespace={self.__namespace}")
        return run(kubectl_args, stdout=PIPE, stderr=PIPE)
