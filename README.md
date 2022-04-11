
# Simulation-Automated-Vehicles
we presented the updating Connected and Automated Vehicles (CAVs) model as the scanner of heterogeneous traffic flow, which uses various sensors to detect the characteristics of traffic flow in several traffic scenes on the roads. The model contains the hardware platform, software algorithm of CAV, and the analysis of traffic flow detection and simulation by Flow Project, where the driving of vehicles is mainly controlled by Reinforcement Learning (RL). Finally, the effectiveness of the proposed model and the corresponding swarm intelligence strategy is evaluated through simulation experiments. The results showed that the traffic flow scanning, tracking, and data recording performed continuously by CAVs are effective. The increase in the penetration rate of CAVs in the overall traffic flow has a significant effect on vehicle detection and identification. In addition, the vehicle occlusion rate is independent of the CAV lane position in all cases. The complete street scanner is a new technology that realizes the perception of the human settlement environment with the help of the Internet of Vehicles based on 5G communications and sensors. Although there are some shortcomings in the experiment, it still provides an experimental reference for the development of smart vehicles.

# How to use？
1. Install anaconda2 (refer to anaconda official website https://www.anaconda.com/), then create a dedicated operating environment in the flow directory and install dependencies
conda env create -f environment.yml
source activate flow
2. Install Project and SUMO:
pip install -e .
3. Check if SUMO is installed successfully:
which sumo
sumo --version
sumo-gui
4. Check if the project is installed successfully:
source activate flow
python examples/sumo/sugiyama.py

# Qusetion
There is a high probability that this step is unsuccessful, or it is unsuccessful after restarting, there will be a problem that the flow cannot be activated, or an error will be reported due to the Python version. The default python version of my system is Python2 under /usr/bin .7, but the Flow Project relies on python3.5 in the anaconda directory, and casually changing the system environment variables can easily break many framework dependencies. The solution is to run the following three sentences before running the script of Flow Project for the first time every time you boot up (the UBUNTU in the third line is changed to your home directory name):

export PATH=/usr/local/anaconda2/bin:$PATH
source activate flow
export PYTHONPATH="/home/UBUNTU/.conda/envs/flow/lib/python3.5/site-packages:$PYTHONPATH"

# How to secondary development?

After this, enter python examples/sumo/sugiyama.py or other scripts under examples/sumo/ in Terminal in the flow directory to successfully run the simulation, which also means that flow is installed.

Run the model with Python, output the coordinates.
As can be seen from the official novice tutorial, the core of the simulation lies in the scripts in the examples/sumo/ directory. The author takes the modification and expansion of the one-way N-lane highway simulation creation script highway.py in this directory as an example to introduce how to Run the simulation with Python and output the coordinates of each vehicle on the road at each moment.

The road shape in the Project is limited, and the creation of new roads should be customized based on the bottom layer of SUMO, which remains to be studied in the future. Among the official road forms, the N-lane expressway is a relatively simple model. The running effect of the original script is as shown in the introduction of the simulation image above. The script has been modified:

(1) Change the source code to increase the function of changing the length of the body
Change the def add() function in class VehicleParams in params.py in the flow/core directory, and add these lines:

`
def add(self,
            veh_id,
            length=5,
            acceleration_controller=(SimCarFollowingController, {}),
            lane_change_controller=(SimLaneChangeController, {}),
            routing_controller=None,
            initial_speed=0,
            num_vehicles=1,
            car_following_params=None,
            lane_change_params=None):
        """Add a sequence of vehicles to the list of vehicles in the network.

        Parameters
        ----------
        veh_id : str
            base vehicle ID for the vehicles (will be appended by a number)
        acceleration_controller : tup, optional
            1st element: flow-specified acceleration controller
            2nd element: controller parameters (may be set to None to maintain
            default parameters)
        lane_change_controller : tup, optional
            1st element: flow-specified lane-changer controller
            2nd element: controller parameters (may be set to None to maintain
            default parameters)
        routing_controller : tup, optional
            1st element: flow-specified routing controller
            2nd element: controller parameters (may be set to None to maintain
            default parameters)
        initial_speed : float, optional
            initial speed of the vehicles being added (in m/s)
        num_vehicles : int, optional
            number of vehicles of this type to be added to the network
        car_following_params : flow.core.params.SumoCarFollowingParams
            Params object specifying attributes for Sumo car following model.
        lane_change_params : flow.core.params.SumoLaneChangeParams
            Params object specifying attributes for Sumo lane changing model.
        """
        if car_following_params is None:
            # FIXME: depends on simulator
            car_following_params = SumoCarFollowingParams()

        if lane_change_params is None:
            # FIXME: depends on simulator
            lane_change_params = SumoLaneChangeParams()

        type_params = {}
        type_params.update(car_following_params.controller_params)
        type_params.update(lane_change_params.controller_params)

        # If a vehicle is not sumo or RL, let the minGap be zero so that it
        # does not tamper with the dynamics of the controller
        if acceleration_controller[0] != SimCarFollowingController \
                and acceleration_controller[0] != RLController:
            type_params["minGap"] = 0.0

        type_params['length'] = length

        # This dict will be used when trying to introduce new vehicles into
        # the network via a Flow. It is passed to the vehicle kernel object
        # during environment instantiation.
        self.type_parameters[veh_id] = \
            {undefined"length": length,
             "acceleration_controller": acceleration_controller,
             "lane_change_controller": lane_change_controller,
             "routing_controller": routing_controller,
             "initial_speed": initial_speed,
             "car_following_params": car_following_params,
             "lane_change_params": lane_change_params}

        # TODO: delete?
        self.initial.append({undefined
            "veh_id":
                veh_id,
            "length":
                length,
            "acceleration_controller":
                acceleration_controller,
            "lane_change_controller":
                lane_change_controller,
            "routing_controller":
                routing_controller,
            "initial_speed":
                initial_speed,
            "num_vehicles":
                num_vehicles,
            "car_following_params":
                car_following_params,
            "lane_change_params":
                lane_change_params
        })

        # This is used to return the actual headways from the vehicles class.
        # It is passed to the vehicle kernel class during environment
        # instantiation.
        self.minGap[veh_id] = type_params["minGap"]

        for i in range(num_vehicles):
            v_id = veh_id + '_%d' % i

            # add the vehicle to the list of vehicle ids
            self.ids.append(v_id)

            self.__vehicles[v_id] = dict()

            # specify the type
            self.__vehicles[v_id]["type"] = veh_id

            # update the number of vehicles
            self.num_vehicles += 1
            if acceleration_controller[0] == RLController:
                self.num_rl_vehicles += 1

        # increase the number of unique types of vehicles in the network, and
        # add the type to the list of types
        self.num_types += 1
        self.types.append({"veh_id": veh_id, "type_params": type_params})
`
# Change the Python script
highway.py:
`
1.	"""Example of an open multi-lane network with human-driven vehicles."""
2.	 
3.	from flow.controllers import IDMController, SimLaneChangeController, ContinuousRouter, RLController
4.	from flow.core.experiment import Experiment
5.	from flow.core.params import SumoParams, EnvParams, \
6.	    NetParams, InitialConfig, InFlows, SumoLaneChangeParams, SumoCarFollowingParams
7.	from flow.core.params import VehicleParams
8.	from flow.envs.loop.lane_changing import LaneChangeAccelEnv, \
9.	    ADDITIONAL_ENV_PARAMS
10.	from flow.scenarios.highway import HighwayScenario, ADDITIONAL_NET_PARAMS
11.	 
12.	#from flow.core.params import SimParams
13.	 
14.	 
15.	def highway_example(render=None):
16.	    """
17.	    Perform a simulation of vehicles on a highway.
18.	    Parameters
19.	    ----------
20.	    render : bool, optional
21.	        specifies whether to use the gui during execution
22.	    Returns
23.	    -------
24.	    exp: flow.core.experiment.Experiment
25.	        A non-rl experiment demonstrating the performance of human-driven
26.	        vehicles on a figure eight.
27.	    """
28.	    sim_params = SumoParams(restart_instance=True, sim_step=0.1, emission_path="./data/",render=True, sight_radius=30, pxpm=3, show_radius=True)
29.	 
30.	    if render is not None:
31.	        sim_params.render = render
32.	 
33.	    vehicles = VehicleParams()
34.	    
35.	    vehicles.add(
36.	        veh_id="rlcar",# Lincoln MKC 4552*1864*1654
37.	        length = 4.552,
38.	        acceleration_controller=(RLController, {}),
39.	        car_following_params=SumoCarFollowingParams(
40.	            speed_mode="obey_safe_speed",
41.	        ),
42.	        initial_speed=0,
43.	        num_vehicles=1)
44.	    
45.	    vehicles.add(
46.	        veh_id="humancar",# Volkswagen LAVIDA 4670*1806*1474 max:120km/h
47.	        length = 4.67,
48.	        #v0 : desirable velocity, in m/s (default: 30) in flow/flow/controllers/car_following_models.py 352
49.	        acceleration_controller=(IDMController,{'v0':32}),# 115km/h
50.	        lane_change_controller=(SimLaneChangeController, {}),
51.	        lane_change_params=SumoLaneChangeParams(
52.	            lane_change_mode="strategic",# Human cars make lane changes in accordance with SUMO to provide speed boosts
53.	        ),
54.	        num_vehicles=1)
55.	    
56.	    vehicles.add(
57.	        veh_id="humanbus_lane2",# YUTONG ZK6826BEV 8245*2500*3240 max:100km/h
58.	        length = 8.245,
59.	        acceleration_controller=(IDMController, {'v0':26.4}),# 95km/h
60.	        #lane_change_controller=(SimLaneChangeController, {}),
61.	        #lane_change_params=SumoLaneChangeParams(
62.	        #    lane_change_mode="strategic",# Human cars make lane changes in accordance with SUMO to provide speed boosts
63.	        #),
64.	        num_vehicles=1)
65.	    vehicles.add(
66.	        veh_id="humanbus_lane1",# YUTONG ZK6826BEV 8245*2500*3240 max:100km/h
67.	        length = 8.245,
68.	        acceleration_controller=(IDMController, {'v0':26.4}),# 95km/h
69.	        num_vehicles=1)
70.	    vehicles.add(
71.	        veh_id="humanbus_lane0",# YUTONG ZK6826BEV 8245*2500*3240 max:100km/h
72.	        length = 8.245,
73.	        acceleration_controller=(IDMController, {'v0':26.4}),# 95km/h
74.	        num_vehicles=1)
75.	        
76.	    vehicles.add(
77.	        veh_id="humantruck_lane2",# FOTON BJ5319XXY-AB 12000*2550*3950 max:100km/h
78.	        length = 12,
79.	        acceleration_controller=(IDMController, {'v0':25}),# 90km/h
80.	        #lane_change_controller=(SimLaneChangeController, {}),
81.	        #lane_change_params=SumoLaneChangeParams(
82.	        #    lane_change_mode="strategic",# Human cars make lane changes in accordance with SUMO to provide speed boosts
83.	        #),
84.	        num_vehicles=1)
85.	    vehicles.add(
86.	        veh_id="humantruck_lane1",# FOTON BJ5319XXY-AB 12000*2550*3950 max:100km/h
87.	        length = 12,
88.	        acceleration_controller=(IDMController, {'v0':25}),# 90km/h
89.	        num_vehicles=1)
90.	    vehicles.add(
91.	        veh_id="humantruck_lane0",# FOTON BJ5319XXY-AB 12000*2550*3950 max:100km/h
92.	        length = 12,
93.	        acceleration_controller=(IDMController, {'v0':25}),# 90km/h
94.	        num_vehicles=1)
95.	 
96.	    env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)
97.	 
98.	    inflow = InFlows()
99.	    
100.	    inflow.add(
101.	        veh_type="rlcar",
102.	        edge="highway_0",
103.	        #probability=0.025,# 0.25 probability for emitting a vehicle each second (not together with vehsPerHour or period)
104.	        vehs_per_hour=250,
105.	        departLane=3,# the index of the lane, starting with rightmost=0
106.	        departSpeed=30)
107.	    
108.	    inflow.add(
109.	        veh_type="humancar",
110.	        edge="highway_0",
111.	        #probability=0.85,# 0.25 probability for emitting a vehicle each second (not together with vehsPerHour or period)
112.	        vehs_per_hour=15000,
113.	        departLane="random",#free random allowed best first
114.	        departSpeed=30)
115.	    
116.	    inflow.add(
117.	        veh_type="humanbus_lane2",
118.	        edge="highway_0",
119.	        #probability=0.1,
120.	        vehs_per_hour=486,
121.	        departLane=2,
122.	        departSpeed=26.4)
123.	    inflow.add(
124.	        veh_type="humanbus_lane1",
125.	        edge="highway_0",
126.	        #probability=0.1,
127.	        vehs_per_hour=486,
128.	        departLane=1,
129.	        departSpeed=26.4)
130.	    inflow.add(
131.	        veh_type="humanbus_lane0",
132.	        edge="highway_0",
133.	        #probability=0.1,
134.	        vehs_per_hour=486,
135.	        departLane=0,
136.	        departSpeed=26.4)
137.	    
138.	    inflow.add(
139.	        veh_type="humantruck_lane2",
140.	        edge="highway_0",
141.	        #probability=0.05,
142.	        vehs_per_hour=486,
143.	        departLane=2,
144.	        departSpeed=25)
145.	    inflow.add(
146.	        veh_type="humantruck_lane1",
147.	        edge="highway_0",
148.	        #probability=0.05,
149.	        vehs_per_hour=486,
150.	        departLane=1,
151.	        departSpeed=25)
152.	    inflow.add(
153.	        veh_type="humantruck_lane0",
154.	        edge="highway_0",
155.	        #probability=0.05,
156.	        vehs_per_hour=486,
157.	        departLane=0,
158.	        departSpeed=25)
159.	 
160.	    initial_config = InitialConfig(spacing="uniform", shuffle=True)# initial position in road
161.	 
162.	    scenario = HighwayScenario(#3:110-120 2:90-120 3:90-120 4:60-120 [G1503 2019.5 daily car:180000 bus/truck:70000]
163.	        name="highway",
164.	        vehicles=vehicles,
165.	        net_params=NetParams(
166.	                inflows=inflow,
167.	                additional_params={
168.	                    'length': 6000,
169.	                    'lanes': 4,
170.	                    'speed_limit': 33.3,
171.	                    'num_edges': 1
172.	                }),
173.	        initial_config=initial_config)
174.	    
175.	 
176.	    env = LaneChangeAccelEnv(env_params, sim_params, scenario)
177.	 
178.	    return Experiment(env)
179.	 
180.	 
181.	if __name__ == "__main__":
182.	    # import the experiment variable
183.	    exp = highway_example()
184.	 
185.	    # run for a set number of rollouts / time steps
186.	    #exp.run(1, 1000, convert_to_csv = False)
187.	    exp.run(1, 5000, convert_to_csv = True)

`
HighwayScenario() can be seen that this is a function specially set up for the one-way four-lane highway scene. Because the Flow Project is intended to train reinforcement learning vehicles in simple scenarios (for complex scenarios, please consider games such as GTA), there is no overly complicated vehicle network.

Among them, inflow can input the previously created InFlow() object, length refers to the length of the road (unit: m, do not be too long, otherwise the data recording after running will be interrupted), lanes is the number of lanes, which can be increased or decreased, speed_limit is the maximum speed (unit: m/s) that vehicles on each lane of the entire road will not exceed, and num_edges refers to the number of ports on the road.
# Getting involved

We welcome your contributions.

# Citing

If you use this for academic research, you are highly encouraged to cite our paper:

The Scanner of Heterogeneous Traffic Flow in Smart Cities by an Updating Model of Connected and Automated Vehicles
