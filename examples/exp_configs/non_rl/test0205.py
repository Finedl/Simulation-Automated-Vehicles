"""Example of an open multi-lane network with human-driven vehicles."""

import traci
from flow.core.kernel.vehicle import KernelVehicle
from flow.core.kernel.vehicle import TraCIVehicle
from flow.core.kernel import Kernel
from flow.core.params import SimParams

from flow.controllers import IDMController, SimLaneChangeController, RLController
from flow.core.params import SumoParams, EnvParams, NetParams, InitialConfig, SumoLaneChangeParams, SumoCarFollowingParams
from flow.core.params import VehicleParams, InFlows
from flow.envs.ring.lane_change_accel import ADDITIONAL_ENV_PARAMS
from flow.networks.highway import HighwayNetwork, ADDITIONAL_NET_PARAMS
from flow.envs import LaneChangeAccelEnv

vehicles = VehicleParams()

vehicles.add(
    veh_id="Rlcar",# Lincoln MKC 4552*1864*1654 THIS IS TYPE NAME
    length = 4.552,
    width = 1.864,
    height = 1.654,
    vClass = "passenger",
    #color = "1,0,0",
    acceleration_controller=(IDMController, {}), # RLController
    lane_change_params=SumoLaneChangeParams(
        lane_change_mode="only_speed_gain_safe"
    ),
    num_vehicles=0)

vehicles.add(
    veh_id="Gashumancar",# Volkswagen LAVIDA 4670*1806*1474 max:120km/h
    length = 4.67,
    width = 1.806,
    height = 1.474,
    vClass = "passenger",
    #v0 : desirable velocity, in m/s (default: 30) in flow/flow/controllers/car_following_models.py 352
    acceleration_controller=(IDMController,{'v0':30.556}),# desirable velocity 110km/h
    car_following_params=SumoCarFollowingParams(
        speed_mode="obey_safe_speed", # default
        max_speed=33.333,
        accel=2.153,
        decel=4.5, 
        sigma=0.5, # The driver imperfection (0 denotes perfect driving)
        tau=1.0, # This parameter is intended to model a drivers desired time headway (in seconds). https://sumo.dlr.de/docs/Car-Following-Models.html#tau
        min_gap=2.5, # Minimum Gap when standing (m)
        speed_factor=1.0, # The vehicles expected multiplicator for lane speed limits
        speed_dev=0.1, # The deviation of the speedFactor
        impatience=0.5, # The impatience of a driver is value between 0 and 1 that grows whenever the driver has to stop unintentionally (i.e. due to a jam or waiting at an intersection).
        car_follow_model="IDM"
    ),
    lane_change_params=SumoLaneChangeParams(
        lane_change_mode="only_speed_gain_safe",# sumo_default, only_speed_gain_safe, only_strategic_safe, only_cooperative_safe
        model="LC2013" # Lane-changing model for sublane-simulation [https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html] [https://sumo.dlr.de/docs/Simulation/SublaneModel.html]
    ),
    num_vehicles=0)

vehicles.add(
    veh_id="Elehumancar",# Tesla Model3(CN) 4694*1850*1443 max:120km/h
    length = 4.694,
    width = 1.850,
    height = 1.443,
    vClass = "passenger",
    color = "1,1,1",
    acceleration_controller=(IDMController,{'v0':30.556}),# desirable velocity 110km/h
    car_following_params=SumoCarFollowingParams(
        speed_mode="obey_safe_speed", # default
        max_speed=33.333,
        accel=4.960,
        decel=4.5, 
        sigma=0.5, 
        tau=1.0, 
        min_gap=2.5,
        speed_factor=1.0, 
        speed_dev=0.1, 
        impatience=0.5, 
        car_follow_model="IDM"
    ),
    lane_change_params=SumoLaneChangeParams(
        lane_change_mode="only_speed_gain_safe",# sumo_default, only_speed_gain_safe, only_strategic_safe, only_cooperative_safe
        model="LC2013" # Lane-changing model for sublane-simulation [https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html] [https://sumo.dlr.de/docs/Simulation/SublaneModel.html]
    ),
    num_vehicles=0)

vehicles.add(
    veh_id="Bushuman",# YUTONG T7 7148*2075*2770 max:120km/h
    length = 7.148,
    width = 2.075,
    height = 2.770,
    vClass = "bus",
    color = "1,1,0",
    acceleration_controller=(IDMController, {'v0':27.778}),# 100km/h
    car_following_params=SumoCarFollowingParams(
        speed_mode="obey_safe_speed", # default
        max_speed=33.333,
        accel=1.543,
        decel=3, 
        sigma=0.4, # Careful than car
        tau=1.5, # Careful than car
        min_gap=3, # Careful than car
        speed_factor=1.0, 
        speed_dev=0.1, 
        impatience=0.5, 
        car_follow_model="IDM"
    ),
    lane_change_params=SumoLaneChangeParams(
        lane_change_mode="only_speed_gain_safe",# sumo_default, only_speed_gain_safe, only_strategic_safe, only_cooperative_safe
        model="LC2013" # Lane-changing model for sublane-simulation [https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html] [https://sumo.dlr.de/docs/Simulation/SublaneModel.html]
    ),
    num_vehicles=0)

vehicles.add(
    veh_id="Truckhuman",# SINOTRUK HOWO-A7-8*4 11600*2550*3400 max:100km/h
    length = 11.600,
    width = 2.550,
    height = 3.400,
    vClass = "truck",
    color = "0,1,0",
    acceleration_controller=(IDMController, {'v0':25}),# 90km/h
    car_following_params=SumoCarFollowingParams(
        speed_mode="obey_safe_speed", # default
        max_speed=27.778,
        accel=1.0, 
        decel=2.5, 
        sigma=0.3, # Careful than bus
        tau=2.0, # Careful than bus
        min_gap=3.5, # Careful than bus
        speed_factor=1.0, 
        speed_dev=0.1, 
        impatience=0.5, 
        car_follow_model="IDM"
    ),
    lane_change_params=SumoLaneChangeParams(
        lane_change_mode="only_speed_gain_safe",# sumo_default, only_speed_gain_safe, only_strategic_safe, only_cooperative_safe
        model="LC2013" # Lane-changing model for sublane-simulation [https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html] [https://sumo.dlr.de/docs/Simulation/SublaneModel.html]
    ),
    num_vehicles=0)

env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

inflow = InFlows() #1.5:0.5:1:1  0.5:1.5:1:1  0.5:0.5:1:2  0.5:0.5:2:1// 3498.5*(0 0.25 0.5 0.75) 3498.5*()~(1.5:0.5:1:1)
inflow.add(
    veh_type="Rlcar",
    edge="highway_0",
    vehs_per_hour=875,#120 875
    depart_lane="random",# the index of the lane, starting with rightmost=0
    depart_speed=30)
    
inflow.add(
    veh_type="Gashumancar",
    edge="highway_0",
    vehs_per_hour=984,#1312
    depart_lane="random",#free random allowed best first
    depart_speed=30)

inflow.add(
    veh_type="Elehumancar",
    edge="highway_0",
    vehs_per_hour=328,#437 317 1192 1312 328
    depart_lane="random",#free random allowed best first
    depart_speed=30)
    
inflow.add(
    veh_type="Bushuman",
    edge="highway_0",
    vehs_per_hour=437,#6997/2/4/1.5
    depart_lane="random",
    depart_speed=26.4)
    
inflow.add(
    veh_type="Truckhuman",
    edge="highway_0",
    vehs_per_hour=328,#6997/2/4/2
    depart_lane="random",
    depart_speed=25)

flow_params = dict(
    # name of the experiment
    exp_tag='test0205',

    # name of the flow environment the experiment is running on
    env_name=LaneChangeAccelEnv,

    # name of the network class the experiment is running on
    network=HighwayNetwork,

    # simulator that is used by the experiment
    simulator='traci',

    # sumo-related parameters (see flow.core.params.SumoParams)
    #sim=SumoParams(
        #render=True,
        #lateral_resolution=1.0,
    #),
    sim=SumoParams(
        restart_instance=True, 
        sim_step=0.1, # seconds per simulation step, default
        emission_path="./data/",
        render=True, # delegate rendering to sumo-gui for back-compatibility(Color)
        #lateral_resolution=3.75,
        sight_radius=120, # sets the radius of observation for RL vehicles (meter)
        pxpm=3, # specifies rendering resolution (pixel / meter)
        show_radius=True, # specifies whether to render the radius of RL observation
        save_render=True # specifies whether to save rendering data to disk
    ),

    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=5000, # number of steps per rollouts
        additional_params=ADDITIONAL_ENV_PARAMS.copy(),
    ),

    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=NetParams(
        inflows=inflow,
        #additional_params=ADDITIONAL_NET_PARAMS.copy(),
        additional_params={
            'length': 6000,
            'width': 3.75,
            'lanes': 4,# highway_0_0(right) highway_0_3(left)
            'speed_limit': 33.333,
            'num_edges': 1,
            # 'lane_list': {}, # must available
            'lane_list': {'0': # edge index
                [
                    {
                        'index': '0', # 0(right)  n-1(left)
                        'speed': '27.778'
                    },
                    {
                        'index': '1', 
                        'speed': '27.778'
                    },
                    {
                        'index': '2', 
                        'speed': '33.333',
                        'disallow': "truck"
                    },
                    {
                        'index': '3', 
                        'speed': '33.333', 
                        'disallow': "bus truck"
                    }
                ]
            }, #In the order of edges index
            "use_ghost_edge": False,
            "ghost_speed_limit": 25,
            "boundary_cell_length": 500
        },
    ),

    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,

    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=InitialConfig(
        spacing="uniform",
        shuffle=True,
    ),
)
