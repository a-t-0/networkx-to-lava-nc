"""Verifies the Supported_settings object catches invalid iterations
specifications."""
# pylint: disable=R0801
import copy
import unittest

from src.experiment_settings.experiment_settings import (
    Adaptation_settings,
    Radiation_settings,
)
from src.experiment_settings.Supported_settings import Supported_settings
from src.experiment_settings.verify_supported_settings import (
    verify_adap_and_rad_settings,
    verify_configuration_settings,
)

supp_sets = Supported_settings()
adap_sets = Adaptation_settings()
rad_sets = Radiation_settings()
with_adaptation_with_radiation = {
    "iterations": list(range(0, 3, 1)),
    "m": list(range(0, 1, 1)),
    "min_max_graphs": 1,
    "max_max_graphs": 15,
    "min_graph_size": 3,
    "max_graph_size": 20,
    "size_and_max_graphs": [(3, 15), (4, 15)],
    "adaptation": verify_adap_and_rad_settings(
        supp_sets, adap_sets.with_adaptation, "adaptation"
    ),
    "radiation": verify_adap_and_rad_settings(
        supp_sets, rad_sets.with_radiation, "radiation"
    ),
    "overwrite_sim_results": True,
    "overwrite_visualisation": True,
    "simulators": ["nx"],
}


class Test_iterations_settings(unittest.TestCase):
    """Tests whether the verify_configuration_settings_types function catches
    invalid iterations settings.."""

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.supp_sets = Supported_settings()

        self.invalid_iterations_value = {
            "iterations": "invalid value of type string iso list of floats",
        }

        self.supp_sets = supp_sets
        self.adap_sets = adap_sets
        self.rad_sets = rad_sets
        self.with_adaptation_with_radiation = with_adaptation_with_radiation
        self.valid_iterations = self.supp_sets.iterations

    def test_iterations_is_none(self):
        """Verifies an error is thrown if configuration settings do not contain
        m."""

        with self.assertRaises(Exception) as context:
            # Configuration Settings of type None throw error.
            verify_configuration_settings(
                self.supp_sets, None, has_unique_id=False
            )

        self.assertEqual(
            "Error, the experiment_config is of type:"
            + f"{type(None)}, yet it was expected to be of"
            + " type dict.",
            str(context.exception),
        )

    def test_catch_invalid_iterations_type(self):
        """."""

        with self.assertRaises(Exception) as context:
            # iterations dictionary of type None throws error.
            verify_configuration_settings(
                self.supp_sets, "string_instead_of_dict", has_unique_id=False
            )
        self.assertEqual(
            "Error, the experiment_config is of type:"
            + f'{type("")}, yet it was expected to be of'
            + " type dict.",
            str(context.exception),
        )

    def test_catch_invalid_iterations_value_type_too_low(self):
        """."""
        # Create deepcopy of configuration settings.
        config_settings = copy.deepcopy(self.with_adaptation_with_radiation)
        # Set negative value of iterations in copy.
        config_settings["iterations"] = [-2]

        with self.assertRaises(Exception) as context:
            verify_configuration_settings(
                self.supp_sets, config_settings, has_unique_id=False
            )

        self.assertEqual(
            "Error, iterations was expected to be in range:"
            + f'{self.with_adaptation_with_radiation["iterations"]}.'
            + f" Instead, it contains:{-2}.",
            str(context.exception),
        )

    def test_catch_invalid_iterations_value_type_too_high(self):
        """."""
        # Create deepcopy of configuration settings.
        config_settings = copy.deepcopy(self.with_adaptation_with_radiation)
        # Set negative value of iterations in copy.
        config_settings["iterations"] = [50]

        with self.assertRaises(Exception) as context:
            verify_configuration_settings(
                self.supp_sets, config_settings, has_unique_id=False
            )

        self.assertEqual(
            "Error, iterations was expected to be in range:"
            + f'{self.with_adaptation_with_radiation["iterations"]}.'
            + f" Instead, it contains:{50}.",
            str(context.exception),
        )

    def test_catch_empty_iterations_value_list(self):
        """."""
        # Create deepcopy of configuration settings.
        config_settings = copy.deepcopy(self.with_adaptation_with_radiation)
        # Set negative value of iterations in copy.
        config_settings["iterations"] = []

        with self.assertRaises(Exception) as context:
            verify_configuration_settings(
                self.supp_sets, config_settings, has_unique_id=False
            )

        self.assertEqual(
            "Error, list was expected contain at least 1 integer."
            + f" Instead, it has length:{0}",
            str(context.exception),
        )

    def test_returns_valid_m(self):
        """Verifies a valid iterations is returned."""
        returned_dict = verify_configuration_settings(
            self.supp_sets,
            self.with_adaptation_with_radiation,
            has_unique_id=False,
        )
        self.assertIsInstance(returned_dict, dict)

    def test_empty_iterations(self):
        """Verifies an exception is thrown if an empty iterations dict is
        thrown."""

        # Create deepcopy of configuration settings.
        config_settings = copy.deepcopy(self.with_adaptation_with_radiation)
        # Remove key and value of m.

        config_settings.pop("iterations")

        with self.assertRaises(Exception) as context:
            verify_configuration_settings(
                self.supp_sets, config_settings, has_unique_id=False
            )

        self.assertEqual(
            "'iterations'",
            str(context.exception),
        )