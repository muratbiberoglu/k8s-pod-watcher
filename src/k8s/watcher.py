import datetime
import time
from typing import Callable
from typing import List

from src.k8s.k8s_service import K8SService
from src.util.modifiers import Modifiers
from src.config.config import config
from src.k8s.service import Service


class Watcher:
    def __init__(self, context: str, namespace: str, periodic: bool, detailed: bool, service_patterns: List[str]):
        self.__k8s_service = K8SService(context, namespace)
        self.__detailed = detailed

        self.__build_namespace_text(namespace)
        self.__build_context_text(context)

        self.__services: dict = {}
        self.__fetch_deployments_and_build_name_service_map(service_patterns)

        if periodic:
            self.__run_periodically(lambda: self.__run())
        else:
            self.__run()

    def __run_periodically(self, runnable):
        while True:
            self.__print_separator()
            start_time = time.time()
            runnable()
            elapsed_time = time.time() - start_time
            time.sleep(max(0, config.get("INTERVAL") - elapsed_time))

    @staticmethod
    def __print_separator():
        separator_text = Modifiers.DIMMED
        separator_text += "-" * 60 + "\n"
        separator_text += datetime.datetime.now().strftime("%c")
        separator_text += Modifiers.NORMAL
        print(separator_text)

    def __run(self):
        print(self.__context_text, "|", self.__namespace_text)

        pod_map = self.__fetch_pods_and_build_pod_map()
        self.__fetch_pod_usages_and_update_pod_map(pod_map)
        self.__add_pods_to_services(pod_map)

        for service in self.__services.values():
            print(service)
            service.clear()

    def __build_context_text(self, context: str):
        self.__context_text = f"CONTEXT: {Modifiers.BOLD}"
        self.__context_text += Modifiers.RED if context == config.get("PROD_CONTEXT") else Modifiers.GREEN
        self.__context_text += context
        self.__context_text += Modifiers.NORMAL

    def __build_namespace_text(self, namespace: str):
        self.__namespace_text = f"NAMESPACE: {Modifiers.BOLD}"
        self.__namespace_text += namespace
        self.__namespace_text += Modifiers.NORMAL

    def __fetch_deployments_and_build_name_service_map(self, service_patterns: List[str]):
        deployment_names = self.__k8s_service.get_deployment_names()

        should_monitored: Callable[[str], bool] = lambda x: any(pattern in x for pattern in service_patterns)
        for deployment_name in deployment_names:
            if should_monitored(deployment_name):
                self.__services[deployment_name] = Service(deployment_name, self.__detailed)

    def __fetch_pods_and_build_pod_map(self) -> dict:
        pods = self.__k8s_service.get_pods()
        return {pod.fullname: pod for pod in filter(lambda pod: pod.service in self.__services, pods)}

    def __fetch_pod_usages_and_update_pod_map(self, pod_map: dict):
        if not self.__detailed:
            return

        result = self.__k8s_service.get_pod_resource_usages()
        for name, cpu, mem in result:
            if name in pod_map:
                pod_map[name].cpu = cpu
                pod_map[name].mem = mem

    def __add_pods_to_services(self, pod_map: dict):
        for pod in pod_map.values():
            service = pod.service
            self.__services[service].add_pod(pod)
