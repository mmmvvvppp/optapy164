# -*- coding: utf-8 -*-

# Python Packages
from typing import Optional, Any

# Third Party Packages
from optapy import constraint_provider
from optapy.constraint import ConstraintFactory, Joiners
from optapy.score import HardSoftScore

# Local Packages
from scheduling_domain import ToolNeed
from tools import NullTool, Tool


def is_real_tool(r: Optional[Tool]) -> bool:
    if isinstance(r, NullTool):
        return False
    elif isinstance(r, Tool):
        return True
    else:
        return False


@constraint_provider
def tool_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        constraint_tool_simultaneous_needs(constraint_factory),
        # Soft constraints
        preference_scheduled_tool(constraint_factory),
    ]


def constraint_tool_simultaneous_needs(
    constraint_factory: ConstraintFactory,
):
    return (
        # For every unique pair of ToolNeeds in the problem space
        constraint_factory.for_each_unique_pair(
            ToolNeed,
            # ... if they support overlapping times
            (Joiners.overlapping(lambda RN: RN.start_time, lambda RN: RN.end_time),),
        )
        # Then, if they share a selected Tool
        .filter(
            lambda RN1, RN2: is_real_tool(RN1.selected_tool)
            and is_real_tool(RN2.selected_tool)
            and RN1.selected_tool.get_id() == RN2.selected_tool.get_id()
        )
        # Then penalize it!
        .penalize("Overlapping Needs share a Tool", HardSoftScore.ONE_HARD)
    )


def preference_scheduled_tool(
    constraint_factory: ConstraintFactory,
):
    return (
        # For every ToolNeed in the problem space
        constraint_factory.for_each_including_null_vars(ToolNeed)
        # If there hasn't been a real Tool assigned
        .filter(lambda RN1: not is_real_tool(RN1.selected_tool))
        # Then penalize it!
        .penalize("Prefer real Tool", HardSoftScore.ONE_SOFT)
    )
