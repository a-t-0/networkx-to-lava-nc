"""Contains a single setting of the experiment configuration settings.

(The values of the settings may vary, yet the types should be the same.)
"""


from src.experiment_settings.Adaptation_Rad_settings import (
    Adaptations_settings,
    Radiation_settings,
)
from src.experiment_settings.Supported_experiment_settings import (
    Supported_experiment_settings,
    convert_algorithm_to_setting_list,
)
from src.experiment_settings.Supported_run_settings import (
    Supported_run_settings,
)
from src.experiment_settings.verify_experiment_settings import (
    verify_adap_and_rad_settings,
    verify_experiment_config,
    verify_has_unique_id,
)
from src.experiment_settings.verify_run_settings import verify_run_config
from src.export_results.Output import (
    create_results_directories,
    performed_stage,
)


class Experiment_runner:
    """Stores the configuration of a single run."""

    # pylint: disable=R0903

    def __init__(
        self, experi_config: dict, export_snns: bool, show_snns: bool
    ) -> None:

        # Ensure output directories are created for stages 1 to 4.
        create_results_directories()

        # Store the experiment configuration settings.
        self.experi_config = experi_config

        # Load the ranges of supported settings.
        self.supp_experi_setts = Supported_experiment_settings()

        # Verify the experiment experi_config are complete and valid.
        verify_experiment_config(
            self.supp_experi_setts,
            experi_config,
            has_unique_id=False,
            strict=True,
        )

        # If the experiment experi_config does not contain a hash-code,
        # create the unique hash code for this configuration.
        if not self.supp_experi_setts.has_unique_config_id(self.experi_config):
            self.supp_experi_setts.append_unique_config_id(self.experi_config)

        # Verify the unique hash code for this configuration is valid.
        verify_has_unique_id(self.experi_config)

        # Append the export_snns and show_snns arguments.
        self.experi_config["export_snns"] = export_snns
        self.experi_config["show_snns"] = show_snns

        # Perform runs accordingly.
        self.__perform_run(self.experi_config)

    # pylint: disable=W0238
    def __perform_run(self, experi_config):
        """Private method that runs the experiment.

        The 2 underscores indicate it is private. This method executes
        the run in the way the processed configuration settings specify.
        """
        # Generate run configurations.
        run_configs = experiment_config_to_run_configs(experi_config)

        to_run = determine_what_to_run(run_configs)

        if to_run["stage_1"]:

            pass
        if to_run["stage_2"]:
            pass
        if to_run["stage_3"]:
            pass
        if to_run["stage_4"]:
            pass


def experiment_config_to_run_configs(experi_config: dict):
    """Generates all the run_config dictionaries of a single experiment
    configuration.

    Verifies whether each run_config is valid.
    """
    # pylint: disable=R0914
    supp_run_setts = Supported_run_settings()
    run_configs = []

    # pylint: disable=R1702
    # TODO: make it loop through a list of keys.
    # for algorithm in experi_config["algorithms"]:
    for algorithm_name, algo_setts_dict in experi_config["algorithms"].items():
        for algo_config in convert_algorithm_to_setting_list(algo_setts_dict):
            algorithm = {algorithm_name: algo_config}
            for key, value in experi_config["adaptations"].items():
                adaptation = {
                    key: value,
                }
                for radiation_name, radiation_setts_list in experi_config[
                    "radiations"
                ].items():
                    # TODO: verify it is of type list.
                    for rad_config in radiation_setts_list:
                        radiation = {radiation_name: rad_config}
                        for iteration in experi_config["iterations"]:
                            for size_and_max_graph in experi_config[
                                "size_and_max_graphs"
                            ]:
                                for simulator in experi_config["simulators"]:
                                    for graph_nr in range(
                                        0, size_and_max_graph[1]
                                    ):
                                        run_configs.append(
                                            run_parameters_to_dict(
                                                adaptation,
                                                algorithm,
                                                iteration,
                                                size_and_max_graph,
                                                graph_nr,
                                                radiation,
                                                experi_config,
                                                simulator,
                                            )
                                        )

    for run_config in run_configs:
        verify_run_config(
            supp_run_setts, run_config, has_unique_id=False, strict=True
        )

        # Append unique_id to run_config
        supp_run_setts.append_unique_config_id(run_config)

        # Append show_snns and export_snns to run config.
        supp_run_setts.assert_has_key(experi_config, "show_snns", bool)
        supp_run_setts.assert_has_key(experi_config, "export_snns", bool)
        run_config["show_snns"] = experi_config["show_snns"]
        run_config["export_snns"] = experi_config["export_snns"]
    return run_configs


# pylint: disable=R0913
def run_parameters_to_dict(
    adaptation,
    algorithm,
    iteration,
    size_and_max_graph,
    graph_nr,
    radiation,
    experi_config,
    simulator,
):
    """Stores selected parameters into a dictionary.

    Written as separate argument to keep code width under 80 lines.
    """
    return {
        "adaptation": adaptation,
        "algorithm": algorithm,
        "iteration": iteration,
        "graph_size": size_and_max_graph[0],
        "graph_nr": graph_nr,
        "radiation": radiation,
        "overwrite_sim_results": experi_config["overwrite_sim_results"],
        "overwrite_visualisation": experi_config["overwrite_visualisation"],
        "seed": experi_config["seed"],
        "simulator": simulator,
    }


def determine_what_to_run(run_config) -> dict:
    """Scans for existing output and then combines the run configuration
    settings to determine what still should be computed."""
    to_run = {
        "stage_1": False,
        "stage_2": False,
        "stage_3": False,
        "stage_4": False,
    }
    # Determine which of the 4 stages have been performed and which stages
    # still have to be completed.

    if (
        not performed_stage(
            run_config,
            1,
        )
        or run_config["overwrite_sim_results"]
    ):
        # If original graphs do not yet exist, or a manual overwrite is
        # requested, create them (Note it only asks for an overwrite of
        # the sim results, but it is assumed this means re-do the
        # simulation).
        to_run["stage_1"] = True
    if (
        not performed_stage(run_config, 2)
        or run_config["overwrite_sim_results"]
    ):
        to_run["stage_2"] = True
    if (
        not performed_stage(run_config, 3)
        or run_config["overwrite_visualisation"]
    ):
        # Note this allows the user to create inconsistent simulation
        # results and visualisation. E.g. the simulated behaviour may
        # have changed due to code changes, yet the visualisation would
        # not be updated stage 3 has already been performed, with
        # overwrite_sim_results=True, and overwrite_visualisation=False.
        to_run["stage_3"] = True
    # Throw warning to user about potential discrepancy between graph
    # behaviour and old visualisation.
    if (
        performed_stage(run_config, 3)
        and run_config["overwrite_sim_results"]
        and not run_config["overwrite_visualisation"]
    ):
        input(
            "Warning, if you have changed the graph behaviour without "
            + "overwrite_visualisation=True, your visualisation may/will "
            + "not match with what the graphs actually do. We suggest you "
            + "try this again with:overwrite_visualisation=True"
        )
    if (
        not performed_stage(run_config, 4)
        or run_config["overwrite_sim_results"]
    ):
        to_run["stage_4"] = True
    return to_run


def example_experi_config():
    """Creates example experiment configuration settings."""
    # Create prerequisites
    supp_experi_setts = Supported_experiment_settings()
    adap_sets = Adaptations_settings()
    rad_sets = Radiation_settings()

    # Create the experiment configuration settings for a run with adaptation
    # and with radiation.
    with_adaptation_with_radiation = {
        "algorithms": {
            "MDSA": {
                "m_vals": list(range(0, 4, 1)),
            }
        },
        "adaptations": verify_adap_and_rad_settings(
            supp_experi_setts, adap_sets.with_adaptation, "adaptations"
        ),
        "iterations": list(range(0, 3, 1)),
        "min_max_graphs": 1,
        "max_max_graphs": 15,
        "min_graph_size": 3,
        "max_graph_size": 20,
        "overwrite_sim_results": True,
        "overwrite_visualisation": True,
        "radiations": verify_adap_and_rad_settings(
            supp_experi_setts, rad_sets.with_radiation, "radiations"
        ),
        "seed": 42,
        "size_and_max_graphs": [(3, 15), (4, 15)],
        "simulators": ["nx"],
    }
    return with_adaptation_with_radiation
