import functools
from typing import Sequence

from pylogics.exceptions import PylogicsError
from pylogics.syntax.base import (
    AbstractAtomic,
    And,
    Equivalence,
    FalseFormula,
    Formula,
    Implies,
    Logic,
    Not,
    Or,
    TrueFormula,
)
from pylogics.syntax.ltl import Always, Eventually, Next
from pylogics.syntax.ltl import PropositionalFalse as LTLPropositionalFalse
from pylogics.syntax.ltl import PropositionalTrue as LTLPropositionalTrue
from pylogics.syntax.ltl import Release, StrongRelease, Until, WeakNext, WeakUntil

@functools.singledispatch
def to_f2i(formula: Formula) -> str:
    """Transform a formula to a parsable string."""
    raise PylogicsError(f"formula '{formula}' is not supported")

def _map_operands_to_f2i(operands: Sequence[Formula]):
    """Map a list of operands to a list of strings (with brackets)."""
    return map(lambda sub_formula: f"({to_f2i(sub_formula)})", operands)

@to_f2i.register(And)
def to_f2i_and(formula: And) -> str:
    """Transform an And into string."""
    return " & ".join(_map_operands_to_f2i(formula.operands))

@to_f2i.register(Or)
def to_f2i_or(formula: Or) -> str:
    """Transform an Or into string."""
    return " | ".join(_map_operands_to_f2i(formula.operands))

@to_f2i.register(Not)
def to_f2i_not(formula: Not) -> str:
    """Transform a Not into string."""
    return f"!({to_f2i(formula.argument)})"

@to_f2i.register(Implies)
def to_f2i_implies(formula: Implies) -> str:
    """Transform an Implies into string."""
    return " -> ".join(_map_operands_to_f2i(formula.operands))

@to_f2i.register(Equivalence)
def to_f2i_equivalence(formula: Equivalence) -> str:
    """Transform an Equivalence into string."""
    return " <-> ".join(_map_operands_to_f2i(formula.operands))

@to_f2i.register(AbstractAtomic)
def to_f2i_atomic(formula: AbstractAtomic) -> str:
    """Transform an atomic formula into string."""
    return formula.name

@to_f2i.register(TrueFormula)
def to_f2i_logical_true(formula: TrueFormula) -> str:
    """Transform the "tt" formula into string."""
    return "tt" if formula.logic != Logic.PL else "true"

@to_f2i.register(FalseFormula)
def to_f2i_logical_false(formula: FalseFormula) -> str:
    """Transform the "ff" formula into string."""
    return "ff" if formula.logic != Logic.PL else "false"

@to_f2i.register
def to_f2i_ltl_propositional_true(_formula: LTLPropositionalTrue) -> str:
    """Transform the "tt" formula into string."""
    return "true"

@to_f2i.register
def to_f2i_ltl_propositional_false(_formula: LTLPropositionalFalse) -> str:
    """Transform the "ff" formula into string."""
    return "false"

@to_f2i.register(Next)
def to_f2i_next(formula: Next) -> str:
    """Transform a next formula into string."""
    return f"X({to_f2i(formula.argument)} & !End)"

@to_f2i.register(WeakNext)
def to_f2i_weak_next(formula: WeakNext) -> str:
    """Transform a weak next formula into string."""
    return f"X({to_f2i(formula.argument)} | End)"

@to_f2i.register(Until)
def to_f2i_until(formula: Until) -> str:
    """Transform an Until formula into string with & !End appended to the second operand."""
    operands_str = list(_map_operands_to_f2i(formula.operands))
    operands_str[1] = f"({operands_str[1]} & !End)"
    return " U ".join(operands_str)

# @to_f2i.register(WeakUntil)
# def to_f2i_weak_until(formula: WeakUntil) -> str:
#     """Transform a weak until formula into string."""
#     return " W ".join(_map_operands_to_f2i(formula.operands))

@to_f2i.register(Release)
def to_f2i_release(formula: Release) -> str:
    """Transform a release formula into string with & !End appended to the first operand and | End appended to the second"""
    operands_str = list(_map_operands_to_f2i(formula.operands))
    operands_str[0] = f"({operands_str[0]} & !End)"
    operands_str[1] = f"({operands_str[1]} | End)"
    return " V ".join(operands_str)

# @to_f2i.register(StrongRelease)
# def to_f2i_strong_release(formula: StrongRelease) -> str:
#     """Transform a strong release formula into string."""
#     return " M ".join(_map_operands_to_f2i(formula.operands))

@to_f2i.register(Eventually)
def to_f2i_eventually(formula: Eventually) -> str:
    """Transform a eventually formula into string with & !End appended."""
    return f"F({to_f2i(formula.argument)} & !End)"

@to_f2i.register(Always)
def to_f2i_always(formula: Always) -> str:
    """Transform a always formula into string with | End appended."""
    return f"G({to_f2i(formula.argument)} | End)"