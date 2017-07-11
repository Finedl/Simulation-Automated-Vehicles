import numpy as np

from cistar.core.scenario import Scenario
from cistar.scenarios.loop.gen import CircleGenerator


class LoopScenario(Scenario):
    def __init__(self, name, type_params, net_params, cfg_params=None,
                 initial_config=None, cfg=None):
        """
        Initializes a loop scenario. Required net_params: length, lanes,
        speed_limit, resolution. Required initial_config: positions.

        See Scenario.py for description of params.
        """
        super().__init__(name, type_params, net_params, cfg_params=cfg_params,
                         initial_config=initial_config, cfg=cfg,
                         generator_class=CircleGenerator)

        if "length" not in self.net_params:
            raise ValueError("length of circle not supplied")
        self.length = self.net_params["length"]

        if "lanes" not in self.net_params:
            raise ValueError("lanes of circle not supplied")
        self.lanes = self.net_params["lanes"]

        if "speed_limit" not in self.net_params:
            raise ValueError("speed limit of circle not supplied")
        self.speed_limit = self.net_params["speed_limit"]

        if "resolution" not in self.net_params:
            raise ValueError("resolution of circle not supplied")
        self.resolution = self.net_params["resolution"]

        edgelen = self.length / 4
        self.edgestarts = [("bottom", 0), ("right", edgelen),
                           ("top", 2 * edgelen), ("left", 3 * edgelen)]
        self.edgepos = {"bottom": 0, "right": edgelen, "top": 2 * edgelen, "left": 3 * edgelen}

        # generate starting position for vehicles in the network
        if "positions" not in self.initial_config:
            self.initial_config["positions"] = self.generate_starting_positions()

        if "shuffle" not in self.initial_config:
            self.initial_config["shuffle"] = False
        if not cfg:
            # FIXME(cathywu) Resolve this inconsistency. Base class does not
            # call generate, but child class does. What is the convention?
            self.cfg = self.generate()

    def get_edge(self, x):
        """
        Given an absolute position x on the track, returns the edge (name) and
        relative position on that edge.
        :param x: absolute position x
        :return: (edge (name, such as bottom, right, etc.), relative position on
        edge)
        """
        starte = ""
        startx = 0
        for (e, s) in self.edgestarts:
            if x >= s:
                starte = e
                startx = x - s
        return starte, startx

    def get_x(self, edge, position):
        """
        Given an edge name and relative position, return the absolute
        position on the track.
        :param edge: name of edge (string)
        :param position: relative position on edge
        :return:
        """
        return self.edgepos[edge] + position

    def generate_starting_positions(self, x0=1):
        """
        Generates starting positions for vehicles in the network
        :return: list of start positions [(edge0, pos0), (edge1, pos1), ...]
        """
        startpositions = []

        bunch_factor = 0
        if "bunching" in self.initial_config:
            bunch_factor = self.initial_config["bunching"]

        if "spacing" in self.initial_config:
            if self.initial_config["spacing"] == "gaussian":
                downscale = 5
                if "downscale" in self.initial_config:
                    downscale = self.initial_config["downscale"]
                startpositions = self.gen_random_start_pos(downscale, bunch_factor, x0=x0)
        else:
            startpositions = self.gen_even_start_positions(bunch_factor, x0=x0)

        return startpositions

    def gen_even_start_positions(self, bunching, x0=1):
        """
        Generate uniformly spaced start positions.
        :return: list of start positions [(edge0, pos0), (edge1, pos1), ...]
        """
        startpositions = []
        # FIXME(cathywu) Remove this arbitrary "- 10"?
        increment = (self.length - bunching) / self.num_vehicles

        x = x0
        for i in range(self.num_vehicles):
            # pos is a tuple (route, departPos)
            pos = self.get_edge(x)
            startpositions.append(pos)
            x = (x + increment) % self.length

        return startpositions

    def gen_random_start_pos(self, downscale=5, bunching=0, x0=1):
        """
        Generate random start positions via additive Gaussian.

        WARNING: this does not absolutely gaurantee that the order of
        vehicles is preserved.
        :return: list of start positions [(edge0, pos0), (edge1, pos1), ...]
        """
        startpositions = []
        mean = (self.length - bunching) / self.num_vehicles

        # FIXME(cathywu) Why is x=1 the start, instead of x=0?
        x = x0
        for i in range(self.num_vehicles):
            pos = self.get_edge(x)
            startpositions.append(pos)
            x = (x + np.random.normal(scale=mean / downscale, loc=mean)) % self.length

        return startpositions
