"""Verifies the graph represents a connected and valid SNN, with all required
neuron and synapse properties specified."""

# Import the networkx module.
import networkx as nx


def verify_networkx_snn_spec(G: nx.DiGraph) -> None:
    """

    :param G: The original graph on which the MDSA algorithm is ran.
    :param G: The original graph on which the MDSA algorithm is ran.

    """
    for node in G.nodes:
        verify_neuron_properties_are_specified(G.nodes[node])

    # TODO: verify synapse properties
    for edge in G.edges:
        assert_synapse_properties_are_specified(G, edge)


def verify_neuron_properties_are_specified(node: nx.DiGraph.nodes) -> None:
    """

    :param node: nx.DiGraph.nodes:
    :param node: nx.DiGraph.nodes:

    """
    if not isinstance(node["nx_LIF"].bias.get(), float):
        raise Exception("Bias is not a float.")
    if not isinstance(node["nx_LIF"].du.get(), float):
        raise Exception("du is not a float.")
    if not isinstance(node["nx_LIF"].dv.get(), float):
        raise Exception("dv is not a float.")
    if not isinstance(node["nx_LIF"].vth.get(), float):
        raise Exception("vth is not a float.")


def assert_synaptic_edgeweight_type_is_correct(
    G: nx.DiGraph, edge: nx.DiGraph.edges
) -> None:
    """

    :param edge: nx.DiGraph.edges:
    :param G: The original graph on which the MDSA algorithm is ran.
    :param edge: nx.DiGraph.edges:

    """
    if nx.get_edge_attributes(G, "weight") != {}:

        if not isinstance(G.edges[edge]["weight"], float):
            raise Exception(
                f"Weight of edge {edge} is not a"
                + " float. It is"
                + f'a: {G.edges[edge]["weight"]}'
            )
    else:
        raise Exception(
            f"Weight of edge {edge} is an attribute (in the"
            + ' form of: "weight").'
        )


def assert_synapse_properties_are_specified(G, edge):
    """

    :param G: The original graph on which the MDSA algorithm is ran.
    :param edge:

    """
    if not check_if_synapse_properties_are_specified(G, edge):
        raise Exception(
            f"Not all synapse properties of edge: {edge} are"
            + " specified. It only contains attributes:"
            + f"{get_synapse_property_names(G,edge)}"
        )


def check_if_synapse_properties_are_specified(G, edge):
    """

    :param G: The original graph on which the MDSA algorithm is ran.
    :param edge:

    """
    synapse_property_names = get_synapse_property_names(G, edge)
    if "weight" in synapse_property_names:
        # if 'delay' in synapse_property_names:
        # TODO: implement delay using a chain of neurons in series since this
        # is not yet supported by lava-nc.

        return True
    return False


def get_synapse_property_names(G, edge):
    """

    :param G: The original graph on which the MDSA algorithm is ran.
    :param edge:

    """
    return G.edges[edge].keys()


def assert_no_duplicate_edges_exist(G):
    """Asserts no duplicate edges exist, throws error otherwise.

    :param G: The original graph on which the MDSA algorithm is ran.
    """
    visited_edges = []
    for edge in G.edges:
        if edge not in visited_edges:
            visited_edges.append(edge)
        else:
            raise Exception(
                f"Error, edge:{edge} is a duplicate edge as it"
                + f" already is in:{visited_edges}"
            )
