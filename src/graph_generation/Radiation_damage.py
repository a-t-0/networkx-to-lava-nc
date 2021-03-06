"""Simulates radiation damage on SNN.

Currently simulates it through simulating neuron death by setting the
threshold voltage to 1000 V (which will not be reached used in the
current MDSA approximation). TODO: include other radiation effects such
as "unexpected/random" changes in neuronal and synaptic properties.
"""
import random


class Radiation_damage:
    """Creates expected properties of the spike_once neuron."""

    def __init__(self, probability):
        self.neuron_death_probability = (
            probability  # % of neurons that will decay.
        )

    def get_random_list_of_len_n(self, n, max_val):
        """Does not include max, only below.

        :param n:
        :param max_val:
        """
        randomlist = []
        for _ in range(int(0), int(n)):
            n = random.randint(0, max_val)  # nosec - using a random seed.
        randomlist.append(n)
        print(randomlist)
        return randomlist

    def inject_simulated_radiation(self, get_degree, probability):
        """

        :param get_degree: Graph with the MDSA SNN approximation solution.
        :param probability:

        """
        # Get list of dead neurons.
        # dead_neurons = self.get_list_of_dead_neurons(get_degree)

        # Get random neurons from list.
        dead_neuron_names = self.get_random_neurons(get_degree, probability)

        # Kill neurons.
        self.kill_neurons(get_degree, dead_neuron_names)

        return dead_neuron_names

    def get_random_neurons(self, get_degree, probability):
        """

        :param get_degree: Graph with the MDSA SNN approximation solution.
        :param probability:
        :param adaptation_only:  (Default value = False)

        """
        dead_neuron_names = []
        for node_name in get_degree:
            if self.kill_neuron(probability):
                dead_neuron_names.append(node_name)
        return dead_neuron_names

    def kill_neuron(self, probability):
        """probabiltiy: 0 to 1 (exc. 1)
        Returns bool true or false

        :param probability:

        """

        return random.random() < probability  # nosec - using a random seed.

    def get_list_of_dead_neurons(self, get_degree):
        """

        :param get_degree: Graph with the MDSA SNN approximation solution.

        """
        spike_once_neurons = self.get_spike_once_nodes(get_degree)
        self.get_selector_nodes(get_degree)
        self.get_degree_receiver_nodes(get_degree)
        return spike_once_neurons

    def get_spike_once_nodes(self, get_degree):
        """

        :param get_degree: Graph with the MDSA SNN approximation solution.
        :param m: The amount of approximation iterations used in the MDSA
        approximation.  (Default value = None)

        """
        spike_once_nodes = []
        for node_name in get_degree.nodes:
            if node_name[:11] == "spike_once_":
                spike_once_nodes.append(node_name)
        return spike_once_nodes

        # vth = get_degree.nodes[node_name]["vth"] + 1
        # if node_name == "spike_once_0":
        #    vth = 9999

    def get_degree_receiver_nodes(self, get_degree):
        """

        :param get_degree: Graph with the MDSA SNN approximation solution.
        :param m: The amount of approximation iterations used in the MDSA
        approximation.  (Default value = None)

        """
        degree_receiver_nodes = []
        for node_name in get_degree.nodes:
            if node_name[:16] == "degree_receiver_":
                degree_receiver_nodes.append(node_name)
        return degree_receiver_nodes

    def get_selector_nodes(self, get_degree):
        """

        :param get_degree: Graph with the MDSA SNN approximation solution.
        :param m: The amount of approximation iterations used in the MDSA
        approximation.  (Default value = None)

        """
        selector_nodes = []
        for node_name in get_degree.nodes:
            if node_name[:9] == "selector_":
                selector_nodes.append(node_name)
        return selector_nodes

    def kill_neurons(self, get_degree, dead_node_names):
        """Simulates dead neurons by setting spiking voltage threshold to near
        infinity.

        Ensures neuron does not spike.

        :param get_degree: Graph with the MDSA SNN approximation solution.
        :param dead_node_names:
        """
        for node_name in dead_node_names:
            if node_name in dead_node_names:
                get_degree.nodes[node_name]["vth"] = 9999


def store_dead_neuron_names_in_graph(G, dead_neuron_names):
    """

    :param G: The original graph on which the MDSA algorithm is ran.
    :param dead_neuron_names:

    """

    for nodename in G.nodes:
        if nodename in dead_neuron_names:
            G.nodes[nodename]["rad_death"] = True
            print(G.nodes[nodename]["rad_death"])
        else:
            G.nodes[nodename]["rad_death"] = False
