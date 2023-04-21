# -*- coding: utf-8 -*-

# Python Packages
from typing import List, Optional, Union

# Third Party Packages
from optapy import (
    planning_entity,
    planning_entity_collection_property,
    planning_id,
    planning_pin,
    planning_score,
    planning_solution,
    planning_variable,
    problem_fact_collection_property,
    value_range_provider,
    # inverse_relation_shadow_variable,
)
from optapy.score import HardSoftScore

# Local Pakcages
from tools import Tool


def format_list(a_list):
    return ",\n".join(map(str, a_list))


@planning_entity
class ToolNeed:
    def __init__(
        self,
        tool_need_uuid: str,  # Unique ID for this instance
        list_of_suitable_tools: List[Tool],
        description: str,
        start_time: float = 0.0,
        end_time: float = 1000000000.0,
        selected_tool: Optional[Tool] = None,
    ):
        self.tool_need_uuid = tool_need_uuid
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.list_of_suitable_tools = list_of_suitable_tools
        self.selected_tool = selected_tool

    @planning_id
    def get_id(self) -> str:
        return self.tool_need_uuid

    @planning_pin
    def is_pinned(self) -> bool:
        if self.get_id() == "A" or self.get_id() == "B":
            return True
        else:
            return False

    @planning_variable(
        Tool, value_range_provider_refs=["list_of_suitable_tools"]
    )  # ,   nullable=True, )
    def get_selected_tool(self) -> Optional[Tool]:
        return self.selected_tool

    def set_selected_tool(self, new_selected_tool: Union[Tool, None]) -> None:
        self.selected_tool = new_selected_tool

    @problem_fact_collection_property(Tool)
    @value_range_provider(range_id="list_of_suitable_tools")
    def get_allowable_tools(self) -> List[Tool]:
        """Provide the solver with the problem space"""
        return self.list_of_suitable_tools

    def __str__(self) -> str:
        return (
            f"ToolNeed("
            f"id={self.tool_need_uuid}, "
            f"description={self.description}, "
            f"start_time={self.start_time}, "
            f"end_time={self.end_time}, "
            f"selected_tool={self.selected_tool})"
        )


@planning_solution
class PlanState:
    def __init__(
        self,
        tool_list: List[Tool],
        tool_requirements_list: List[ToolNeed],
        score: Optional[float] = None,
    ):
        self.tool_list = tool_list
        self.tool_requirements_list = tool_requirements_list
        self.score = score

    @problem_fact_collection_property(Tool)
    def get_tool_list(self) -> List[Tool]:
        return self.tool_list

    @planning_entity_collection_property(ToolNeed)
    def get_tool_requirements_list(self) -> List[ToolNeed]:
        return self.tool_requirements_list

    @planning_score(HardSoftScore)
    def get_score(self) -> HardSoftScore:
        return self.score

    def set_score(self, score: HardSoftScore) -> None:
        self.score = score

    def __str__(self) -> str:
        return (
            f"PlanState("
            # f"tool_list={format_list(self.tool_list)},\n"
            f"tool_requirements_list={format_list(self.tool_requirements_list)},\n"
            f"score={str(self.score)}"
            f")"
        )
