import os
from pathlib import Path

import pytest
from autoverify.util.env import get_file_path
from autoverify.util.instances import VerificationInstance
from autoverify.verifier.verifier import CompleteVerifier
from pytest_lazyfixture import lazy_fixture
from result import Ok

pytestmark = pytest.mark.parametrize(
    "verifier",
    [
        pytest.param(lazy_fixture("nnenum"), marks=[pytest.mark.verifier]),
        # pytest.param(
        #     lazy_fixture("abcrown"),
        #     marks=[pytest.mark.gpu, pytest.mark.verifier],
        # ),
        # pytest.param(
        #     lazy_fixture("ovalbab"),
        #     marks=[pytest.mark.gpu, pytest.mark.verifier],
        # ),
        # pytest.param(
        #     lazy_fixture("verinet"),
        #     marks=[pytest.mark.gpu, pytest.mark.verifier],
        # ),
    ],
)


@pytest.fixture(autouse=True)
def cleanup_compiled_vnnlib():
    """Cleans up any .vnnlib.compiled files that get left behind."""
    yield

    abs_path = get_file_path(Path(__file__))
    dir_name = abs_path / "../trivial_props/"

    for item in os.listdir(dir_name):
        if item.endswith(".vnnlib.compiled"):
            os.remove(dir_name / item)


def test_sat(
    verifier: CompleteVerifier,
    trivial_sat: VerificationInstance,
):
    result = verifier.verify_instance(trivial_sat)

    assert isinstance(result, Ok)
    assert result.value.result == "SAT"


def test_unsat(
    verifier: CompleteVerifier,
    trivial_unsat: VerificationInstance,
):
    result = verifier.verify_instance(trivial_unsat)

    assert isinstance(result, Ok)
    assert result.value.result == "UNSAT"


def test_timeout(
    verifier: CompleteVerifier,
    trivial_timeout: VerificationInstance,
):
    result = verifier.verify_instance(trivial_timeout)

    assert isinstance(result, Ok)
    assert result.value.result == "TIMEOUT"


def test_verify_batch(
    verifier: CompleteVerifier,
    trivial_sat: VerificationInstance,
):
    with pytest.raises(NotImplementedError):
        verifier.verify_batch([trivial_sat])
