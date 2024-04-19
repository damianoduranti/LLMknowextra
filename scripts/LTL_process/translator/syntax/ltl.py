# Copyright 2021 WhiteMech
#
# ------------------------------
#
# This file is part of pylogics.
#
# pylogics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylogics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pylogics.  If not, see <https://www.gnu.org/licenses/>.
#

"""Classes for linear temporal logic."""
from abc import ABC
from functools import partial

from pylogics.syntax.base import (
    AbstractAtomic,
    FalseFormula,
    Formula,
    Logic,
    TrueFormula,
    _BinaryOp,
    _UnaryOp,
)


class _LTL(Formula, ABC):
    """Interface for LTL formulae."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.LTL

    def __hash__(self):
        """Delegate the computation of the hash to the superclass."""
        return super(Formula, self).__hash__()


class _LTLUnaryOp(_UnaryOp, _LTL):
    """LTL Unary operation."""

    ALLOWED_LOGICS = {Logic.LTL}


class _LTLBinaryOp(_BinaryOp, _LTL):
    """LTL Unary operation."""

    ALLOWED_LOGICS = {Logic.LTL}


class Atomic(AbstractAtomic, _LTL):
    """An atomic proposition of LTL."""


class PropositionalTrue(TrueFormula, _LTL):
    """
    A propositional true.

    This is equivalent to 'a | ~a'. for some atom 'a'.
    It requires reading any symbol, at least once.
    """

    def __init__(self):
        """Initialize."""
        super().__init__(logic=Logic.LTL)

    def __invert__(self) -> "Formula":
        """Negate."""
        return PropositionalFalse()

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"PropositionalTrue({self.logic})"


class PropositionalFalse(FalseFormula, _LTL):
    """
    A propositional false.

    This is equivalent to 'a & ~a'. for some atom 'a'.
    It requires reading no symbol, at least once.
    The meaning of this formula is a bit blurred with 'ff'
    with respect to 'tt' and 'true'.
    """

    def __init__(self):
        """Initialize."""
        super().__init__(logic=Logic.LTL)

    def __invert__(self) -> "Formula":
        """Negate."""
        return PropositionalTrue()

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"PropositionalFalse({self.logic})"


class Next(_LTLUnaryOp):
    """The "next" formula in LTL."""

    SYMBOL = "next"


class WeakNext(_LTLUnaryOp):
    """The "weak next" formula in LTL."""

    SYMBOL = "weak_next"


class Until(_LTLBinaryOp):
    """The "next" formula in LTL."""

    SYMBOL = "until"


class Release(_LTLBinaryOp):
    """The "release" formula in LTL."""

    SYMBOL = "release"


class Eventually(_LTLUnaryOp):
    """The "eventually" formula in LTL."""

    SYMBOL = "eventually"


class Always(_LTLUnaryOp):
    """The "always" formula in LTL."""

    SYMBOL = "always"


class WeakUntil(_LTLBinaryOp):
    """The "weak until" formula in LTL."""

    SYMBOL = "weak_until"


class StrongRelease(_LTLBinaryOp):
    """The "strong release" formula in LTL."""

    SYMBOL = "strong_release"


Last = partial(Always, FalseFormula(logic=Logic.LTL))
