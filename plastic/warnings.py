""":mod:`plastic.warnings` --- Warning categories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


class PlasticWarning(Warning):
    """The top-level warning category for Plastic-specific warnings."""


class AppWarning(PlasticWarning):
    """Warnings related to :mod:`plastic.app` module."""

