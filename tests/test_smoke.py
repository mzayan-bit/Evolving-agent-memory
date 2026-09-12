"""Smoke tests to verify package integrity and deterministic configuration."""

import random

import evomem
from evomem.config import ExperimentConfig, set_seed


def test_package_version() -> None:
    """Verify package version is defined and follows semantic versioning."""
    assert isinstance(evomem.__version__, str)
    assert evomem.__version__ == "0.1.0"


def test_experiment_config_defaults() -> None:
    """Verify default ExperimentConfig initialization."""
    config = ExperimentConfig()
    assert config.seed == 42
    assert config.project_name == "evomem"
    assert config.experiment_name == "default"
    assert config.tags == ()


def test_experiment_config_custom() -> None:
    """Verify custom ExperimentConfig values."""
    config = ExperimentConfig(
        seed=1337,
        project_name="evomem_pilot",
        experiment_name="phase0_smoke",
        tags=("baseline", "pilot"),
    )
    assert config.seed == 1337
    assert config.project_name == "evomem_pilot"
    assert config.experiment_name == "phase0_smoke"
    assert config.tags == ("baseline", "pilot")


def test_set_seed_deterministic() -> None:
    """Verify set_seed produces deterministic random number generation."""
    applied_seed = set_seed(12345)
    assert applied_seed == 12345
    val1 = random.random()

    set_seed(12345)
    val2 = random.random()

    assert val1 == val2
