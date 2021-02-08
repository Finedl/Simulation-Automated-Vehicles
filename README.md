# Branch Name
highway_newfunc

# Master Fork From
https://github.com/flow-project/flow

# Introduction Blog(Chinese):
https://blog.csdn.net/m0_37857300/article/details/113762705

# New Functions
1. Improve install steps and correct one dependancy bug: pip should be installed first. redis>=3.3.2 is necessary for one package in environment.yml.
2. Add new parameters for VehicleParams: Enable set length, width, height and vClass for each vehicle. Settings are effective in sumo simulation. (vClass: https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html#abstract_vehicle_class. Potential parameters in future: https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html#available_vtype_attributes)
3. Add width for TraCIKernelNetwork: Enable set lane width for each edge.(Width refer to the width of one lane. Same width for all lanes in same edge temporarily. Potential to set specific width for each lane by the method showed in '4.'.)
4. Add lane_list in highway network: Enable set specific speed and disallow vehicle class for specific lane in specific edge.(disallow vehicle class shows like "A B C" separated by space. Potential parameters in future: https://sumo.dlr.de/docs/Networks/PlainXML.html#lane-specific_definitions)
5. Add example file for new function in this branch(flow/examples/exp_configs/non_rl/test0205.py).
6. All new functions are optional, not necessary.

# How to install
0. (If in China, change source: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple)
1. git clone https://github.com/BingLiHanShuang/flow.git
2. cd flow
3. git checkout highway_newfunc
4. conda env create -f environment.yml
5. pip install -r requirements.txt
6. Install sumo:
For Ubuntu 14.04:
scripts/setup_sumo_ubuntu1404.sh
For Ubuntu 16.04:
scripts/setup_sumo_ubuntu1604.sh
For Ubuntu 18.04:
scripts/setup_sumo_ubuntu1804.sh
For Mac:
scripts/setup_sumo_osx.sh
7. Test sumo:
(1) which sumo
(2) sumo --version
(3) sumo-gui
8. conda activate flow_new2
9. python setup.py develop
Reference: https://flow.readthedocs.io/en/latest/flow_setup.html

# How to run
Open Terminal, change dir to flow, git checkout to this branch and input:
1. cd flow
2. conda deactivate
3. source activate flow_new2
4. export PYTHONPATH="/home/hongyong/.conda/envs/flow_new2/lib/python3.7/site-packages:$PYTHONPATH"
5. python examples/simulate.py test0205 --gen_emission

# Changed Files
1. flow/environment.yml
2. flow/README.md
3. flow/requirements.txt
4. flow/examples/exp_configs/non_rl/test0205.py
5. flow/core/params.py
6. flow/core/kernel/network/traci.py
7. flow/networks/highway.py

# New Function Test Result
Terminal:
~/flow$ python examples/simulate.py test0205 --gen_emission

Output:
/home/hongyong/.conda/envs/flow_new2/lib/python3.7/site-packages/numpy/core/fromnumeric.py:3335: RuntimeWarning: Mean of empty slice.
  out=out, **kwargs)
/home/hongyong/.conda/envs/flow_new2/lib/python3.7/site-packages/numpy/core/_methods.py:161: RuntimeWarning: invalid value encountered in double_scalars
  ret = ret.dtype.type(ret / rcount)
Round 0, return: -0.1
./data/test0205_20210208-1735491612776949.4998093-0_emission.csv ./data
Average, std returns: -0.1, 0.0
Average, std velocities: nan, nan
Average, std outflows: 2030.4, 0.0
Total time: 220.84119844436646
steps/second: 48.04350433419724

Generated File:
~/flow/data/test0205.json
~/flow/data/test0205_20210208-1735491612776949.4998093-0_emission.csv (237.8 MB, deleted for too large)


********************************** THIS IS SPLIT LINE ****************************************
************************** THE FOLLOWING IS MASTER BRANCH README******************************

<img src="docs/img/square_logo.png" align="right" width="25%"/>

[![Build Status](https://travis-ci.com/flow-project/flow.svg?branch=master)](https://travis-ci.com/flow-project/flow)
[![Docs](https://readthedocs.org/projects/flow/badge)](http://flow.readthedocs.org/en/latest/)
[![Coverage Status](https://coveralls.io/repos/github/flow-project/flow/badge.svg?branch=master)](https://coveralls.io/github/flow-project/flow?branch=master)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/flow-project/flow/binder)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/flow-project/flow/blob/master/LICENSE.md)

# Flow

[Flow](https://flow-project.github.io/) is a computational framework for deep RL and control experiments for traffic microsimulation.

See [our website](https://flow-project.github.io/) for more information on the application of Flow to several mixed-autonomy traffic scenarios. Other [results and videos](https://sites.google.com/view/ieee-tro-flow/home) are available as well.

# More information

- [Documentation](https://flow.readthedocs.org/en/latest/)
- [Installation instructions](http://flow.readthedocs.io/en/latest/flow_setup.html)
- [Tutorials](https://github.com/flow-project/flow/tree/master/tutorials)
- [Binder Build (beta)](https://mybinder.org/v2/gh/flow-project/flow/binder)

# Technical questions

If you have a bug, please report it. Otherwise, join the [Flow Users group](https://join.slack.com/t/flow-users/shared_invite/enQtODQ0NDYxMTQyNDY2LTY1ZDVjZTljM2U0ODIxNTY5NTQ2MmUxMzYzNzc5NzU4ZTlmNGI2ZjFmNGU4YjVhNzE3NjcwZTBjNzIxYTg5ZmY) on Slack!  

# Getting involved

We welcome your contributions.

- Please report bugs and improvements by submitting [GitHub issue](https://github.com/flow-project/flow/issues).
- Submit your contributions using [pull requests](https://github.com/flow-project/flow/pulls). Please use [this template](https://github.com/flow-project/flow/blob/master/.github/PULL_REQUEST_TEMPLATE.md) for your pull requests.

# Citing Flow

If you use Flow for academic research, you are highly encouraged to cite our paper:

C. Wu, A. Kreidieh, K. Parvate, E. Vinitsky, A. Bayen, "Flow: Architecture and Benchmarking for Reinforcement Learning in Traffic Control," CoRR, vol. abs/1710.05465, 2017. [Online]. Available: https://arxiv.org/abs/1710.05465

If you use the benchmarks, you are highly encouraged to cite our paper:

Vinitsky, E., Kreidieh, A., Le Flem, L., Kheterpal, N., Jang, K., Wu, F., ... & Bayen, A. M,  Benchmarks for reinforcement learning in mixed-autonomy traffic. In Conference on Robot Learning (pp. 399-409). Available: http://proceedings.mlr.press/v87/vinitsky18a.html

# Contributors

Flow is supported by the [Mobile Sensing Lab](http://bayen.eecs.berkeley.edu/) at UC Berkeley and Amazon AWS Machine Learning research grants. The contributors are listed in [Flow Team Page](https://flow-project.github.io/team.html).
