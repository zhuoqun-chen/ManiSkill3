import os
import sys

import gymnasium as gym
import numpy as np
import torch

from mani_skill.envs.scenes.base_env import SceneManipulationEnv

from mani_skill.envs.scenes.tasks import PickSequentialTaskEnv, SequentialTaskEnv
from mani_skill.envs.scenes.tasks.planner import PickSubtask, plan_data_from_file
from mani_skill.utils.scene_builder.ai2thor import (
    ArchitecTHORSceneBuilder,
    ProcTHORSceneBuilder,
    RoboTHORSceneBuilder,
    iTHORSceneBuilder,
)
from mani_skill.utils.scene_builder.replicacad import ReplicaCADSceneBuilder
from mani_skill.utils.scene_builder.replicacad.rearrange import (
    ReplicaCADPrepareGroceriesTrainSceneBuilder,
    ReplicaCADPrepareGroceriesValSceneBuilder,
    ReplicaCADSetTableTrainSceneBuilder,
    ReplicaCADSetTableValSceneBuilder,
    ReplicaCADTidyHouseTrainSceneBuilder,
    ReplicaCADTidyHouseValSceneBuilder,
)
from mani_skill.utils.wrappers import RecordEpisode

render_mode = (
    "rgb_array"
    if ("SAPIEN_NO_DISPLAY" in os.environ and int(os.environ["SAPIEN_NO_DISPLAY"]) == 1)
    else "human"
)
print("RENDER_MODE", render_mode)

env: SceneManipulationEnv = gym.make(
    "SceneManipulation-v1",
    obs_mode="rgbd",
    render_mode=render_mode,
    control_mode="pd_joint_delta_pos",
    reward_mode="dense",
    robot_uids="fetch",
    scene_builder_cls=ReplicaCADSetTableTrainSceneBuilder,
    # num_envs=2,
    scene_idxs=int(sys.argv[-1]),
)

# print(env.unwrapped._init_raw_obs)

# print(env.observation_space.keys())

if render_mode != "human":
    env = RecordEpisode(env, output_dir=".", save_trajectory=False, info_on_video=False)

# env.step(np.zeros(env.action_space.shape))
# while True:
for _ in range(1):
    obs, info = env.reset(seed=0)
    for _ in range(10 if render_mode != "human" else int(1e8)):
        # print(
        #     env.agent.robot.get_net_contact_forces(
        #         [x.name for x in env.agent.robot.get_links()]
        #     ),
        #     env.agent.robot.pose.p,
        # )
        env.step(np.zeros(env.action_space.shape))
        env.render()
env.close()

print(env.scene_builder.movable_objects.keys())


# SCENE_IDX_TO_APPLE_PLAN = {
#     0: [PickSubtask(obj_id="objects/Apple_5_111")],
#     1: [PickSubtask(obj_id="objects/Apple_16_40")],
#     2: [PickSubtask(obj_id="objects/Apple_12_64")],
#     3: [PickSubtask(obj_id="objects/Apple_29_113")],
#     4: [PickSubtask(obj_id="objects/Apple_28_35")],
#     5: [PickSubtask(obj_id="objects/Apple_17_88")],
#     6: [PickSubtask(obj_id="objects/Apple_1_35")],
#     7: [PickSubtask(obj_id="objects/Apple_25_48")],
#     8: [PickSubtask(obj_id="objects/Apple_9_46")],
#     9: [PickSubtask(obj_id="objects/Apple_13_72")],
# }

# SCENE_IDX = 6
# env: SequentialTaskEnv = gym.make(
#     "SequentialTask-v0",
#     obs_mode="rgbd",
#     render_mode=render_mode,
#     control_mode="pd_joint_delta_pos",
#     reward_mode="dense",
#     robot_uids="fetch",
#     scene_builder_cls=ArchitecTHORSceneBuilder,
#     task_plans=[SCENE_IDX_TO_APPLE_PLAN[SCENE_IDX]],
#     scene_idxs=SCENE_IDX,
#     # num_envs=2,
# )

# print(env.unwrapped._init_raw_obs)

# # print(env.observation_space.keys())

# obs, info = env.reset(seed=0)