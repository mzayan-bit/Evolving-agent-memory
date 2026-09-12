"""Minimal typed configuration and seed management for reproducible research."""

import os
import random
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExperimentConfig:
    """Base configuration container for reproducible experiments.

    Attributes:
        seed: Random seed for reproducibility. Defaults to 42.
        project_name: Name of the research project.
        experiment_name: Identifier for the current experiment run.
        tags: List of descriptive tags for experiment tracking.
    """

    seed: int = 42
    project_name: str = "evomem"
    experiment_name: str = "default"
    tags: tuple[str, ...] = field(default_factory=tuple)


def set_seed(seed: int = 42) -> int:
    """Set random seed across standard library generators and environment.

    Args:
        seed: Integer seed value.

    Returns:
        The integer seed applied.
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    return seed
