"""Verifies the Supported_experiment_settings object catches invalid
min_max_graphs specifications."""
# pylint: disable=R0801
import copy
import unittest

from src.experiment_settings.Supported_experiment_settings import (
    Supported_experiment_settings,
)
from src.experiment_settings.verify_experiment_settings import (
    verify_experiment_config,
)
from tests.experiment_settings.test_generic_experiment_settings import (
    adap_sets,
    rad_sets,
    supp_experi_setts,
    verify_error_is_thrown_on_invalid_configuration_setting_value,
    with_adaptation_with_radiation,
)


class Test_min_max_graphs_settings(unittest.TestCase):
    """Tests whether the verify_experiment_config_types function catches
    invalid min_max_graphs settings.."""

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supp_experi_setts = Supported_experiment_settings()
        self.valid_min_max_graphs = self.supp_experi_setts.min_max_graphs

        self.invalid_min_max_graphs_value = {
            "min_max_graphs": "invalid value of type string iso list of"
            + " floats",
        }

        self.supp_experi_setts = supp_experi_setts
        self.adap_sets = adap_sets
        self.rad_sets = rad_sets
        self.with_adaptation_with_radiation = with_adaptation_with_radiation

    def test_error_is_thrown_if_min_max_graphs_key_is_missing(self):
        """Verifies an exception is thrown if the min_max_graphs key is missing
        from the configuration settings dictionary."""

        # Create deepcopy of configuration settings.
        experi_config = copy.deepcopy(self.with_adaptation_with_radiation)
        # Remove key and value of m.

        experi_config.pop("min_max_graphs")

        with self.assertRaises(Exception) as context:
            verify_experiment_config(
                self.supp_experi_setts,
                experi_config,
                has_unique_id=False,
                strict=True,
            )

        self.assertEqual(
            # "'min_max_graphs'",
            "Error:min_max_graphs is not in the configuration"
            + f" settings:{experi_config.keys()}",
            str(context.exception),
        )

    def test_error_is_thrown_for_invalid_min_max_graphs_value_type(self):
        """Verifies an exception is thrown if the min_max_graphs dictionary
        value, is of invalid type.

        (Invalid types None, and string are tested, a list with floats
        is expected).
        """

        # Create deepcopy of configuration settings.
        experi_config = copy.deepcopy(self.with_adaptation_with_radiation)
        expected_type = type(self.supp_experi_setts.min_max_graphs)

        # Verify it throws an error on None and string.
        for invalid_config_setting_value in [None, ""]:
            experi_config["min_max_graphs"] = invalid_config_setting_value
            verify_error_is_thrown_on_invalid_configuration_setting_value(
                invalid_config_setting_value,
                experi_config,
                expected_type,
                self,
            )

    # TODO: test_catch_empty_min_max_graphs_value_list

    def test_catch_min_max_graphs_value_too_low(self):
        """Verifies an exception is thrown if the min_max_graphs dictionary
        value is lower than the supported range of min_max_graphs values
        permits."""
        # Create deepcopy of configuration settings.
        experi_config = copy.deepcopy(self.with_adaptation_with_radiation)
        # Set negative value of min_max_graphs in copy.
        experi_config["min_max_graphs"] = -2

        with self.assertRaises(Exception) as context:
            verify_experiment_config(
                self.supp_experi_setts,
                experi_config,
                has_unique_id=False,
                strict=True,
            )

        self.assertEqual(
            "Error, setting expected to be at least "
            + f"{self.supp_experi_setts.min_max_graphs}. "
            + f"Instead, it is:{-2}",
            str(context.exception),
        )

    def test_catch_min_max_graphs_value_too_high(self):
        """Verifies an exception is thrown if the min_max_graphs dictionary
        value is higher than the supported range of min_max_graphs values
        permits."""
        # Create deepcopy of configuration settings.
        experi_config = copy.deepcopy(self.with_adaptation_with_radiation)
        # Set negative value of min_max_graphs in copy.
        experi_config["min_max_graphs"] = 50

        with self.assertRaises(Exception) as context:
            verify_experiment_config(
                self.supp_experi_setts,
                experi_config,
                has_unique_id=False,
                strict=True,
            )

        self.assertEqual(
            "Error, setting expected to be at most "
            + f"{self.supp_experi_setts.max_max_graphs}. Instead, it is:"
            + "50",
            str(context.exception),
        )
