# -*- coding: utf-8 -*-
from typing import List
from uuid import uuid4
import pathlib
from optapy import solver_config_create_from_xml_file, solver_factory_create
import optapy.config
import optapy.optaplanner_python_logger
from scheduling_domain import PlanState, format_list, ToolNeed
from scheduling_constraints import tool_constraints
from tools import Tool, Glue, Lock, NullTool


def solve_tool(problem: PlanState) -> PlanState:
    # 50: Critical, 40, Error, 30, Warn, 20 Info, 10, Debug, 0, info
    optapy.optaplanner_python_logger.optapy_logger.setLevel(10)
    tool_solver_config_path = pathlib.Path("./tool_solver.xml")
    tool_solver_config = solver_config_create_from_xml_file(
        tool_solver_config_path.absolute()
    )
    solver_factory = solver_factory_create(tool_solver_config)
    solver = solver_factory.buildSolver()
    solution = solver.solve(problem)
    return solution


def get_glues() -> List[Tool]:
    return [Glue("Super", "1", 123), Glue("Crazy", "2", 123), NullTool()]


def get_locks() -> List[Tool]:
    return [Lock("Master", "10"), NullTool()]


def main():
    # Job 1 needs a glue and lock
    tn1g = ToolNeed("A", get_glues(), "job1glues", 1, 2)
    tn1l = ToolNeed("B", get_locks(), "job1locks", 1, 2)
    # Job2 also needs glue and lock but occurs at same time
    tn2g = ToolNeed(str(uuid4()), get_glues(), "job2glues", 1, 2)
    tn2l = ToolNeed(str(uuid4()), get_locks(), "job2locks", 1, 2)

    all_needs = [tn1g, tn1l, tn2g, tn2l]
    all_tools = [*get_glues(), *get_locks()]

    solution = PlanState(all_tools, all_needs)
    solution = solve_tool(solution)
    for need in solution.get_tool_requirements_list():
        print(f"ToolNeed(id={need.tool_need_uuid}, selected_tool={need.selected_tool}")


if __name__ == "__main__":
    main()
