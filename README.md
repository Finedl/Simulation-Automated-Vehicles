
# Simulation-Automated-Vehicles
we presented the updating Connected and Automated Vehicles (CAVs) model as the scanner of heterogeneous traffic flow, which uses various sensors to detect the characteristics of traffic flow in several traffic scenes on the roads. The model contains the hardware platform, software algorithm of CAV, and the analysis of traffic flow detection and simulation by Flow Project, where the driving of vehicles is mainly controlled by Reinforcement Learning (RL). Finally, the effectiveness of the proposed model and the corresponding swarm intelligence strategy is evaluated through simulation experiments. The results showed that the traffic flow scanning, tracking, and data recording performed continuously by CAVs are effective. The increase in the penetration rate of CAVs in the overall traffic flow has a significant effect on vehicle detection and identification. In addition, the vehicle occlusion rate is independent of the CAV lane position in all cases. The complete street scanner is a new technology that realizes the perception of the human settlement environment with the help of the Internet of Vehicles based on 5G communications and sensors. Although there are some shortcomings in the experiment, it still provides an experimental reference for the development of smart vehicles.

![image](https://user-images.githubusercontent.com/67223039/162754304-7778f415-21e5-42fb-b89e-7c1229ca7bcd.png)

# Getting involved

We welcome your contributions.

# Citing

If you use this for academic research, you are highly encouraged to cite our paper:

Dongliang Chen, Hongyong Huang,Yuchao Zheng, Piotr Gawkowski, Haibin Lv, and Zhihan Lv, " Traffic Flow of Connected and Automated Vehicles in Smart Cities: Human-Centric," The 7th IEEE International Conference on Internet of People  (2021). 

A paper that is being submitted but not published：

Dongliang Chen, Hongyong Huang,Yuchao Zheng, Piotr Gawkowski, Haibin Lv, and Zhihan Lv, " The Scanner of Heterogeneous Traffic Flow in Smart Cities by an Updating Model of Connected and Automated Vehicles." 

# How to use？

Only in the Ubuntu

1. Install anaconda2 (refer to anaconda official website https://www.anaconda.com/), then create a dedicated operating environment in the flow directory and install dependencies
`
conda env create -f environment.yml
`
`
source activate flow
`
2. Install Project and SUMO:
`
pip install -e .
`
3. Check if SUMO is installed successfully:
`which sumo`

`sumo --version`

`sumo-gui`

4. Check if the project is installed successfully:
`source activate flow`

`python examples/sumo/sugiyama.py`

# Qusetion
There is a high probability that this step is unsuccessful, or it is unsuccessful after restarting, there will be a problem that the flow cannot be activated, or an error will be reported due to the Python version. The default python version of my system is Python2 under /usr/bin .7, but the Flow Project relies on python3.5 in the anaconda directory, and casually changing the system environment variables can easily break many framework dependencies. The solution is to run the following three sentences before running the script of Flow Project for the first time every time you boot up (the UBUNTU in the third line is changed to your home directory name):
`
export PATH=/usr/local/anaconda2/bin:$PATH`
`
source activate flow`
`
export PYTHONPATH="/home/UBUNTU/.conda/envs/flow/lib/python3.5/site-packages:$PYTHONPATH"
`
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

(1) highway.py:
`
"""Example of an open multi-lane network with human-driven vehicles."""
 
from flow.controllers import IDMController, SimLaneChangeController, ContinuousRouter, RLController
from flow.core.experiment import Experiment
from flow.core.params import SumoParams, EnvParams, \
    NetParams, InitialConfig, InFlows, SumoLaneChangeParams, SumoCarFollowingParams
from flow.core.params import VehicleParams
from flow.envs.loop.lane_changing import LaneChangeAccelEnv, \
    ADDITIONAL_ENV_PARAMS
from flow.scenarios.highway import HighwayScenario, ADDITIONAL_NET_PARAMS
#from flow.core.params import SimParams
def highway_example(render=None):
    """
    Perform a simulation of vehicles on a highway.
    Parameters
    ----------
    render : bool, optional
        specifies whether to use the gui during execution
    Returns
    -------
    exp: flow.core.experiment.Experiment
        A non-rl experiment demonstrating the performance of human-driven
        vehicles on a figure eight.
    """
    sim_params = SumoParams(restart_instance=True, sim_step=0.1, emission_path="./data/",render=True, sight_radius=30, pxpm=3, show_radius=True)
 
    if render is not None:
        sim_params.render = render
 
    vehicles = VehicleParams()
    
    vehicles.add(
        veh_id="rlcar",# Lincoln MKC 4552*1864*1654
        length = 4.552,
        acceleration_controller=(RLController, {}),
        car_following_params=SumoCarFollowingParams(
            speed_mode="obey_safe_speed",
        ),
        initial_speed=0,
        num_vehicles=1)
    
    vehicles.add(
        veh_id="humancar",# Volkswagen LAVIDA 4670*1806*1474 max:120km/h
        length = 4.67,
        #v0 : desirable velocity, in m/s (default: 30) in flow/flow/controllers/car_following_models.py 352
        acceleration_controller=(IDMController,{'v0':32}),# 115km/h
        lane_change_controller=(SimLaneChangeController, {}),
        lane_change_params=SumoLaneChangeParams(
            lane_change_mode="strategic",# Human cars make lane changes in accordance with SUMO to provide speed boosts
        ),
        num_vehicles=1)
    
    vehicles.add(
        veh_id="humanbus_lane2",# YUTONG ZK6826BEV 8245*2500*3240 max:100km/h
        length = 8.245,
        acceleration_controller=(IDMController, {'v0':26.4}),# 95km/h
        #lane_change_controller=(SimLaneChangeController, {}),
        #lane_change_params=SumoLaneChangeParams(
        #    lane_change_mode="strategic",# Human cars make lane changes in accordance with SUMO to provide speed boosts
        #),
        num_vehicles=1)
    vehicles.add(
        veh_id="humanbus_lane1",# YUTONG ZK6826BEV 8245*2500*3240 max:100km/h
        length = 8.245,
        acceleration_controller=(IDMController, {'v0':26.4}),# 95km/h
        num_vehicles=1)
    vehicles.add(
        veh_id="humanbus_lane0",# YUTONG ZK6826BEV 8245*2500*3240 max:100km/h
        length = 8.245,
        acceleration_controller=(IDMController, {'v0':26.4}),# 95km/h
        num_vehicles=1)
        
    vehicles.add(
        veh_id="humantruck_lane2",# FOTON BJ5319XXY-AB 12000*2550*3950 max:100km/h
        length = 12,
        acceleration_controller=(IDMController, {'v0':25}),# 90km/h
        #lane_change_controller=(SimLaneChangeController, {}),
        #lane_change_params=SumoLaneChangeParams(
        #    lane_change_mode="strategic",# Human cars make lane changes in accordance with SUMO to provide speed boosts
        #),
        num_vehicles=1)
    vehicles.add(
        veh_id="humantruck_lane1",# FOTON BJ5319XXY-AB 12000*2550*3950 max:100km/h
        length = 12,
        acceleration_controller=(IDMController, {'v0':25}),# 90km/h
        num_vehicles=1)
    vehicles.add(
        veh_id="humantruck_lane0",# FOTON BJ5319XXY-AB 12000*2550*3950 max:100km/h
        length = 12,
        acceleration_controller=(IDMController, {'v0':25}),# 90km/h
        num_vehicles=1)
 
    env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)
 
    inflow = InFlows()
    
    inflow.add(
        veh_type="rlcar",
        edge="highway_0",
        #probability=0.025,# 0.25 probability for emitting a vehicle each second (not together with vehsPerHour or period)
        vehs_per_hour=250,
        departLane=3,# the index of the lane, starting with rightmost=0
        departSpeed=30)
    
    inflow.add(
        veh_type="humancar",
        edge="highway_0",
        #probability=0.85,# 0.25 probability for emitting a vehicle each second (not together with vehsPerHour or period)
        vehs_per_hour=15000,
        departLane="random",#free random allowed best first
        departSpeed=30)
    
    inflow.add(
        veh_type="humanbus_lane2",
        edge="highway_0",
        #probability=0.1,
        vehs_per_hour=486,
        departLane=2,
        departSpeed=26.4)
    inflow.add(
        veh_type="humanbus_lane1",
        edge="highway_0",
        #probability=0.1,
        vehs_per_hour=486,
        departLane=1,
        departSpeed=26.4)
    inflow.add(
        veh_type="humanbus_lane0",
        edge="highway_0",
        #probability=0.1,
        vehs_per_hour=486,
        departLane=0,
        departSpeed=26.4)
    
    inflow.add(
        veh_type="humantruck_lane2",
        edge="highway_0",
        #probability=0.05,
        vehs_per_hour=486,
        departLane=2,
        departSpeed=25)
    inflow.add(
        veh_type="humantruck_lane1",
        edge="highway_0",
        #probability=0.05,
        vehs_per_hour=486,
        departLane=1,
        departSpeed=25)
    inflow.add(
        veh_type="humantruck_lane0",
        edge="highway_0",
        #probability=0.05,
        vehs_per_hour=486,
        departLane=0,
        departSpeed=25)
 
    initial_config = InitialConfig(spacing="uniform", shuffle=True)# initial position in road
 
    scenario = HighwayScenario(#3:110-120 2:90-120 3:90-120 4:60-120 [G1503 2019.5 daily car:180000 bus/truck:70000]
        name="highway",
        vehicles=vehicles,
        net_params=NetParams(
                inflows=inflow,
                additional_params={
                    'length': 6000,
                    'lanes': 4,
                    'speed_limit': 33.3,
                    'num_edges': 1
                }),
        initial_config=initial_config)
    
 
    env = LaneChangeAccelEnv(env_params, sim_params, scenario)
 
    return Experiment(env)
 
 
if __name__ == "__main__":
    # import the experiment variable
    exp = highway_example()
 
    # run for a set number of rollouts / time steps
    #exp.run(1, 1000, convert_to_csv = False)
    exp.run(1, 5000, convert_to_csv = True) 
`

The function of restart_instance here is to avoid the previously unclosed SUMO window. After setting to True, each time the script is run, the window will be closed and reopened after clicking the play button of the simulation interface. sim_step is the interval time for recording coordinates, here is 0.1s to record the current coordinates of all vehicles on the road; emission_path determines the save location of the coordinate file, after the operation ends naturally (there will be a longer recording time after the vehicle runs) A csv and an xml file will be found in the flow/data/ directory.
The subsequent parameters are the parameters that take effect for the network simulation function, and a "detection range circle" will be displayed around each vehicle in the network simulation. It is not involved in this simulation, and the above parameters can be maintained.

（2）Add an existing vehicle：

`vehicles = VehicleParams()
    
    vehicles.add(
        veh_id="rlcar",# Lincoln MKC 4552*1864*1654
        length = 4.552,
        acceleration_controller=(RLController, {}),
        car_following_params=SumoCarFollowingParams(
            speed_mode="obey_safe_speed",
        ),
        initial_speed=0,
        num_vehicles=1)
    
    vehicles.add(
        veh_id="humancar",# Volkswagen LAVIDA 4670*1806*1474 max:120km/h
        length = 4.67,
        #v0 : desirable velocity, in m/s (default: 30) in flow/flow/controllers/car_following_models.py 352
        acceleration_controller=(IDMController,{'v0':32}),# 115km/h
        lane_change_controller=(SimLaneChangeController, {}),
        lane_change_params=SumoLaneChangeParams(
            lane_change_mode="strategic",# Human cars make lane changes in accordance with SUMO to provide speed boosts
        ),
        num_vehicles=1)
`

The function of this section is to add vehicles on the existing road at the beginning of the simulation, and the length of this type of vehicle set here will also act in the subsequent added Project. Vehicles will be evenly distributed on the road at equal intervals to avoid a situation where there are no cars on the road at the beginning of the simulation (to allow the traffic to mix well).

vehicles is the created object. The parameter veh_id in add represents the type of vehicle, which needs to be the same as the type name of the corresponding vehicle when the Project is created later. The type name in the final generated coordinate file is also a key variable for search traversal.

length is the length of the vehicle in m.

acceleration_controller is the acceleration control logic of this kind of vehicle. You can choose acceleration control logic such as RL and IDM, and set variables such as initial vehicle speed (unit: m/s) in the form of a dictionary in each acceleration control logic function (for details, please refer to flow VehicleParams source code in params.py in the /flow/core directory).

 car_following_params sets the following logic for this type of vehicle. The speed_mode includes "right_of_way" (default), "obey_safe_speed", "no_collide", "aggressive", and "all_checks". For details, see flow/flow/core VehicleParams source code in params.py in the directory.

lane_change_controller sets the lane-changing logic of this vehicle. The specific lane-changing parameters are set in lane_change_params. Lane_change_mode also includes options such as "no_lat_collide" (default), "strategic", and "aggressive". For details, see params.py .

initial_speed sets the initial speed of these existing vehicles on the road, regardless of the departure speed of the subsequent traffic added in the Project. num_vehicles is to add the number of existing vehicles, because my simulation does not depend on the initial vehicle, so I set a random 1.

Because the project has not yet set the upper and lower limits of the speed of each lane, and can only set the maximum speed of the four lanes at the same time, I choose to establish different types of traffic flows with different initial speeds and expected speeds on each lane. In c will be reflected.

（3）Add input stream:
`    
inflow = InFlows()
inflow.add(
        veh_type="rlcar",
        edge="highway_0",
        #probability=0.025,# 0.25 probability for emitting a vehicle each second (not together with vehsPerHour or period)
        vehs_per_hour=250,
        departLane=3,# the index of the lane, starting with rightmost=0
        departSpeed=30)
`
The simulation model cannot have only the vehicles on the road without input, so the Inflow() function is prepared for establishing the input traffic flow on the road.

Inflow is the created object. The veh_type in the add function corresponds to the traffic flow created by VehicleParams() above, and the vehicle type created above must be used.

The edge is the road end that selects the vehicle input, _0 is generally the left side, and the other side is naturally _1.

Regarding the traffic flow of the input traffic flow, there are two ways to set the traffic flow: probability and vehs_per_hour. Probabilty is a probability-based traffic generation method, which represents the probability of generating traffic per second. The maximum is 1, and it can only be 1. Therefore, this generation method has a generation limit problem. In order to solve this kind of less free Flow Project also uses TraCI to give the parameter of vehs_per_hour, which is the number of input vehicles per hour.

departLane is to select the initial lane of this kind of traffic flow, and it has options of "free", "random", "allowed", "best" and "first" (see http://sumo.dlr.de/wiki for details). /Definition_of_Vehicles,_Vehicle_Types,_and_Routes), but here you can also choose the number of lanes, such as four lanes is 0 to 3 from left to right, so that the car will continue to spawn in this lane.

departSpeed ​​is the departure speed of this kind of traffic, in m/s.

（4）Setting up the road scene:
`
initial_config = InitialConfig(spacing="uniform", shuffle=True)# initial position in road
 
    scenario = HighwayScenario(#3:110-120 2:90-120 3:90-120 4:60-120 [G1503 2019.5 daily car:180000 bus/truck:70000]
        name="highway",
        vehicles=vehicles,
        net_params=NetParams(
                inflows=inflow,
                additional_params={
                    'length': 6000,
                    'lanes': 4,
                    'speed_limit': 33.3,
                    'num_edges': 1
                }),
        initial_config=initial_config)
    
 
    env = LaneChangeAccelEnv(env_params, sim_params, scenario)
`

HighwayScenario() can be seen that this is a function specially set up for the one-way four-lane highway scene. Because the Flow Project is intended to train reinforcement learning vehicles in simple scenarios (for complex scenarios, please consider games such as GTA), there is no overly complicated vehicle network.

Among them, inflow can input the previously created InFlow() object, length refers to the length of the road (unit: m, do not be too long, otherwise the data recording after running will be interrupted), lanes is the number of lanes, which can be increased or decreased, speed_limit is the maximum speed (unit: m/s) that vehicles on each lane of the entire road will not exceed, and num_edges refers to the number of ports on the road.

（5）Finally：start simulation:

`exp.run(1, 5000, convert_to_csv = True)`
This sentence in the main function represents the start of the simulation, where 1 refers to the number of simulations (not the start time of the simulation!!), 5000 refers to the number of seconds of the simulation (if it is too long, the data record will be interrupted), convert_to_csv refers to Whether to automatically convert the xml file generated by the simulation to a csv file. If the simulation network must be large, do not choose automatic conversion, it will collapse and occupy a lot of memory.

