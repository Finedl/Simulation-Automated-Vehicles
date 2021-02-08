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
    veh_id="rlcar",# Lincoln MKC 4552*1864*1654 THIS IS TYPE NAME
    length = 4.552,
    width = 1.864,
    height = 1.654,
    vClass = "passenger",
    #color = "1,0,0",
    acceleration_controller=(RLController, {}),
    car_following_params=SumoCarFollowingParams(
        speed_mode="obey_safe_speed",
        max_speed=33.333,
        accel=2.6, #Wait changed
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
        lane_change_mode="only_speed_gain_safe",# no_lc_safe, Disable all SUMO lane changing but still handle safety checks (collision avoidance and safety-gap enforcement) in the simulation.
        model="SL2015",
        lc_sublane=2.0,
    ),
    num_vehicles=0)

vehicles.add(
    veh_id="humancar",# Volkswagen LAVIDA 4670*1806*1474 max:120km/h
    length = 4.67,
    width = 1.806,
    height = 1.474,
    vClass = "passenger",
    #v0 : desirable velocity, in m/s (default: 30) in flow/flow/controllers/car_following_models.py 352
    acceleration_controller=(IDMController,{'v0':32}),# desirable velocity 115km/h
    car_following_params=SumoCarFollowingParams(
        speed_mode="obey_safe_speed", # default
        max_speed=33.333,
        accel=2.6, #Wait changed
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
        model="SL2015", # Lane-changing model for sublane-simulation [https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html] [https://sumo.dlr.de/docs/Simulation/SublaneModel.html]
        lc_sublane=2.0, # The eagerness for using the configured lateral alignment within the lane. Higher values result in increased willingness to sacrifice speed for alignment. default: 1.0, range [0-inf]
    ),
    num_vehicles=0)

vehicles.add(
    veh_id="humanbus",# YUTONG ZK6826BEV 8245*2500*3240 max:100km/h
    length = 8.245,
    width = 2.500,
    height = 3.240,
    vClass = "bus",
    color = "1,1,0",
    acceleration_controller=(IDMController, {'v0':26.4}),# 95km/h
    car_following_params=SumoCarFollowingParams(
        speed_mode="obey_safe_speed", # default
        max_speed=27.778,
        accel=2.6, #Wait changed
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
        lane_change_mode="only_speed_gain_safe",
        model="SL2015",
        lc_sublane=2.0,
    ),
    num_vehicles=0)

vehicles.add(
    veh_id="humantruck",# FOTON BJ5319XXY-AB 12000*2550*3950 max:100km/h
    length = 12,
    width = 2.550,
    height = 3.950,
    vClass = "truck",
    color = "0,1,0",
    acceleration_controller=(IDMController, {'v0':25}),# 90km/h
    car_following_params=SumoCarFollowingParams(
        speed_mode="obey_safe_speed", # default
        max_speed=27.778,
        accel=2.6, #Wait changed
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
        lane_change_mode="only_speed_gain_safe",
        model="SL2015",
        lc_sublane=2.0,
    ),
    num_vehicles=0)

env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

inflow = InFlows()
inflow.add(
    veh_type="rlcar",
    edge="highway_0",
    #probability=0.025,# 0.25 probability for emitting a vehicle each second (not together with vehsPerHour or period)
    vehs_per_hour=120,#250
    depart_lane=3,# the index of the lane, starting with rightmost=0
    depart_speed=30)
    
inflow.add(
    veh_type="humancar",
    edge="highway_0",
    #probability=0.85,# 0.25 probability for emitting a vehicle each second (not together with vehsPerHour or period)
    vehs_per_hour=2500,#15000
    depart_lane="random",#free random allowed best first
    depart_speed=30)
    
inflow.add(
    veh_type="humanbus",
    edge="highway_0",
    #probability=0.1,
    vehs_per_hour=486,#486
    depart_lane="random",
    depart_speed=26.4)
    
inflow.add(
    veh_type="humantruck",
    edge="highway_0",
    #probability=0.05,
    vehs_per_hour=486,#486
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
        lateral_resolution=3.75,
        sight_radius=120, # sets the radius of observation for RL vehicles (meter)
        pxpm=3, # specifies rendering resolution (pixel / meter)
        show_radius=True # specifies whether to render the radius of RL observation
        #save_render=True # specifies whether to save rendering data to disk
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
