from src.get_alipour_nodes import get_alipour_nodes


def get_run_results(G, G_mdsa, G_brain_adap, G_rad_dam, m, rand_props):
    """Takes in the orignal graph and mdsa, along with the brain adaptation and
    radiation damaged graphs (if they exist). Then computes which nodes the
    Alipour algorithm selects and compares that node selection with the node
    selection generated by the mdsa-, brain-adaptation- and radiation-damaged
    graphs respectively. Returns two lists, one with the lists for node
    selections, and another with the 3 boolean pass/fail values per SNN. The
    first list contains up to 4 lists of selected nodes for: the
    Alipour algorithm and the mdsa-, brain-adaptation- and radiation-damaged
     SNN graphs respectively. The second list contains 3 booleans for the
     mdsa-, brain-adaptation- and radiation-damaged SNN graphs respectively."""

    # Compute the count for each node according to Alipour et al.'s algorithm.
    alipour_node_counts = get_alipour_nodes(
        G,
        m,
        rand_props,
    )
    print(f"alipour_node_counts={alipour_node_counts}")
    mdsa_node_counts = get_nx_LIF_count(G, G_mdsa)
    brain_adap_node_counts = get_nx_LIF_count(G, G_brain_adap)
    rad_dam_node_counts = get_nx_LIF_count(G, G_rad_dam)
    print(f"mdsa_node_counts={mdsa_node_counts}")
    print(f"brain_adap_node_counts={brain_adap_node_counts}")
    print(f"rad_dam_node_counts={rad_dam_node_counts}")
    get_results(
        alipour_node_counts,
        mdsa_node_counts,
        brain_adap_node_counts,
        rad_dam_node_counts,
    )


def get_results(
    alipour_node_counts,
    mdsa_node_counts,
    brain_adap_node_counts,
    rad_dam_node_counts,
):
    results_equal_alipour = lists_are_equal(
        [], alipour_node_counts, mdsa_node_counts, topic=None
    )
    results_equal_alipour = lists_are_equal(
        results_equal_alipour,
        alipour_node_counts,
        mdsa_node_counts,
        topic=None,
    )
    if brain_adap_node_counts is not None:
        results_equal_alipour = lists_are_equal(
            results_equal_alipour,
            alipour_node_counts,
            brain_adap_node_counts,
            topic=None,
        )
    if rad_dam_node_counts is not None:
        results_equal_alipour = lists_are_equal(
            results_equal_alipour,
            alipour_node_counts,
            rad_dam_node_counts,
            topic=None,
        )
    return results_equal_alipour


def lists_are_equal(results, left, right, topic=None):
    if len(left) != len(right):
        raise Exception(
            "Error, the lists are not of equal length.\n "
            + f"left={left}\nright={right}\ntopic={topic}"
        )
    if left == right:
        results.append(True)
    else:
        results.append(False)
    return results


def get_nx_LIF_count(G, nx_SNN_G):
    node_counts = []
    counter = 0
    for nodename in nx_SNN_G.nodes:
        if nodename[:7] == "counter":
            if nodename == f"counter_{counter}":

                node_counts.append(nx_SNN_G.nodes[nodename]["nx_LIF"].u.get())
                counter = +1
            else:
                raise Exception(
                    f"Counter node names and node indices are not in sync:counter={counter},nodename={nodename}"
                )
    if len(G) != len(node_counts):
        raise Exception("Insufficient node counts encountered.")
    return node_counts
