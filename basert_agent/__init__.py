"""BaseRT Local Coding Agent Runtime & Orchestrator."""

__version__ = "1.0.0"
__author__ = "Joseph Skrobynets"

from .runner import LocalBaseRTAgent
from .attestation import BaseRTReceipt

__all__ = [
    "LocalBaseRTAgent",
    "BaseRTReceipt",
]
