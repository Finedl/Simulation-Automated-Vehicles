"""Multi-agent I-210 example.

Trains a non-constant number of agents, all sharing the same policy, on the
highway with ramps network.
"""
import os

from ray.tune.registry import register_env

from flow.controllers import RLController
from flow.controllers.car_following_models import IDMController
import flow.config as config
from flow.core.params import EnvParams
from flow.core.params import NetParams
from flow.core.params import InitialConfig
from flow.core.params import InFlows
from flow.core.params import VehicleParams
from flow.core.params import SumoParams
from flow.core.params import SumoLaneChangeParams
from flow.networks.i210_subnetwork import I210SubNetwork, EDGES_DISTRIBUTION
from flow.envs.multiagent.i210 import I210QMIXMultiEnv, ADDITIONAL_ENV_PARAMS
from flow.utils.registry import make_create_env

# SET UP PARAMETERS FOR THE SIMULATION

# number of steps per rollout
HORIZON = 2000

# percentage of autonomous vehicles compared to human vehicles on highway
PENETRATION_RATE = 10

# SET UP PARAMETERS FOR THE ENVIRONMENT
additional_env_params = ADDITIONAL_ENV_PARAMS.copy()
additional_env_params.update({
    'max_accel': 2.6,
    'max_decel': 4.5,
    # configure the observation space. Look at the I210MultiEnv class for more info.
    'lead_obs': True,
    # whether to add in a reward for the speed of nearby vehicles
    "local_reward": True,
    "num_actions": 5,
    "max_num_agents_qmix": 200
})

# CREATE VEHICLE TYPES AND INFLOWS
# no vehicles in the network
vehicles = VehicleParams()
vehicles.add(
    "human",
    num_vehicles=0,
    lane_change_params=SumoLaneChangeParams(lane_change_mode="strategic"),
    acceleration_controller=(IDMController, {"a": .3, "b": 2.0, "noise": 0.6}),
)
vehicles.add(
    "av",
    acceleration_controller=(RLController, {}),
    num_vehicles=0,
)

inflow = InFlows()
# main highway
pen_rate = PENETRATION_RATE / 100
assert pen_rate < 1.0, "your penetration rate is over 100%"
assert pen_rate > 0.0, "your penetration rate should be above zero"
inflow.add(
    veh_type="human",
    edge="119257914",
    vehs_per_hour=int(10800 * (1 - pen_rate)),
    # probability=1.0,
    departLane="random",
    departSpeed=20)
# # on ramp
# inflow.add(
#     veh_type="human",
#     edge="27414345",
#     vehs_per_hour=321 * pen_rate,
#     departLane="random",
#     departSpeed=20)
# inflow.add(
#     veh_type="human",
#     edge="27414342#0",
#     vehs_per_hour=421 * pen_rate,
#     departLane="random",
#     departSpeed=20)

# Now add the AVs
# main highway
inflow.add(
    veh_type="av",
    edge="119257914",
    vehs_per_hour=int(10800 * pen_rate),
    # probability=1.0,
    departLane="random",
    departSpeed=20)
# # on ramp
# inflow.add(
#     veh_type="av",
#     edge="27414345",
#     vehs_per_hour=int(321 * pen_rate),
#     departLane="random",
#     departSpeed=20)
# inflow.add(
#     veh_type="av",
#     edge="27414342#0",
#     vehs_per_hour=int(421 * pen_rate),
#     departLane="random",
#     departSpeed=20)

NET_TEMPLATE = os.path.join(
    config.PROJECT_PATH,
    "examples/exp_configs/templates/sumo/test2.net.xml")

flow_params = dict(
    # name of the experiment
    exp_tag='I_210_subnetwork',

    # name of the flow environment the experiment is running on
    env_name=I210QMIXMultiEnv,

    # name of the network class the experiment is running on
    network=I210SubNetwork,

    # simulator that is used by the experiment
    simulator='traci',

    # simulation-related parameters
    sim=SumoParams(
        sim_step=0.5,
        render=False,
        color_by_speed=False,
        restart_instance=True,
        use_ballistic=True
    ),

    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=HORIZON,
        sims_per_step=1,
        warmup_steps=0,
        additional_params=additional_env_params,
    ),

    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=NetParams(
        inflows=inflow,
        template=NET_TEMPLATE
    ),

    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,

    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=InitialConfig(
        edges_distribution=EDGES_DISTRIBUTION,
    ),
)

# SET UP RLLIB MULTI-AGENT FEATURES

create_env, env_name = make_create_env(params=flow_params, version=0)

# register as rllib env
register_env(env_name, create_env)

# multiagent configuration
test_env = create_env()
obs_space = test_env.observation_space
act_space = test_env.action_space

# POLICY_GRAPHS = {'av': (None, obs_space, act_space, {})}

# POLICIES_TO_TRAIN = ['av']


# def policy_mapping_fn(_):
#     """Map a policy in RLlib."""
#     return 'av'