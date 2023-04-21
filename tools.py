# -*- coding: utf-8 -*-
# Python modules
from abc import ABC, abstractmethod

# Third Party Packages
from optapy import planning_id, problem_fact

from uuid import uuid4


@problem_fact
class Tool(ABC):
    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError("Calling function on abstract base class")

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Calling function on abstract base class")


@problem_fact
class Glue(Tool):
    def __init__(self, name: str, id: str, expiration_date) -> None:
        self.name = name
        self.id = str(id)
        self.expiration_date = expiration_date

    @planning_id  # "The class has 2 members with a PlanningId annotation"
    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return f"Glue(id={self.id}, name={self.name})"


@problem_fact
class Lock(Tool):
    def __init__(self, name: str, id: str) -> None:
        self.name = name
        self.id = str(id)

    @planning_id  # "The class has 2 members with a PlanningId annotation"
    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return f"Lock(id={str(self.id)}, name={str(self.name)})"


@problem_fact
class NullTool(Tool):
    def __init__(self) -> None:
        self.name = "UNSCHEDULED"
        self.id = str(uuid4())

    @planning_id
    def get_id(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.name
