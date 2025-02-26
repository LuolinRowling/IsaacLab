# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""This script demonstrates how to create a simple stage in Isaac Sim.

.. code-block:: bash

    # Usage
    ./isaaclab.sh -p scripts/tutorials/00_sim/create_empty.py

"""

"""Launch Isaac Sim Simulator first."""

# ./isaaclab.sh -p scripts/tutorials/00_sim/create_empty_with_usd_camera.py --enable_cameras

import argparse

from isaaclab.app import AppLauncher

# create argparser
parser = argparse.ArgumentParser(description="Tutorial on creating an empty stage.")
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()
# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import isaaclab.sim as sim_utils
from isaaclab.sim import SimulationCfg, SimulationContext
import omni.usd
from pxr import UsdGeom
from isaaclab.sensors.camera import Camera, CameraCfg

def main():
    """Main function."""

    # Initialize the simulation context
    sim_cfg = SimulationCfg(dt=0.01)
    sim = SimulationContext(sim_cfg)
    # Set main camera
    # sim.set_camera_view([2.5, 2.5, 2.5], [0.0, 0.0, 0.0])

    cfg = sim_utils.UsdFileCfg(usd_path="/home/liluo/repo/IsaacLab/assets/cameraCfgTest.usd")
    cfg.func("/World/cam", cfg)

    # stage = omni.usd.get_context().get_stage()
    # Convert all encapsulated prims to Camera
    
    # # Get camera prim
    cam_prim_path = "/World/cam/Realsense/RSD455/Camera_OmniVision_OV9782_Color"
    # cam_prim = stage.GetPrimAtPath(cam_prim_path)
    # # Check if prim is a camera
    # if not cam_prim.IsA(UsdGeom.Camera):
        # raise RuntimeError(f"Prim at path '{cam_prim_path}' is not a Camera.")
    # # Add to list
    # sensor_prim = UsdGeom.Camera(cam_prim)


    camera_cfg = CameraCfg(
        prim_path=cam_prim_path,
        update_period=0,
        height=480,
        width=640,
        # data_types=[
        #     "rgb",
        #     "distance_to_image_plane",
        #     "normals",
        #     "semantic_segmentation",
        #     "instance_segmentation_fast",
        #     "instance_id_segmentation_fast",
        # ],
        # colorize_semantic_segmentation=True,
        # colorize_instance_id_segmentation=True,
        # colorize_instance_segmentation=True,
        spawn=None
    )

    camera = Camera(cfg=camera_cfg)

    # # Play the simulator
    sim.reset()
    # Now we are ready!
    print("[INFO]: Setup complete...")

    # TODO: Load usd, and link the camera prim path to the paramter 'camera'
    # load usd
    
    # Simulate physics
    # input()
    while simulation_app.is_running():
        # perform step
        sim.step()
        camera.update(dt=sim.get_physics_dt())
        # print(camera)
        # camera.update(dt=sim.get_physics_dt())

        # # Print camera info
        print(camera)
        if "rgb" in camera.data.output.keys():
            print("Received shape of rgb image        : ", camera.data.output["rgb"].shape)
            # save image
            # import cv2
            # cv2.imwrite("rgb.png", camera.data.output["rgb"][0].cpu().numpy())
        # if "distance_to_image_plane" in camera.data.output.keys():
        #     print("Received shape of depth image      : ", camera.data.output["distance_to_image_plane"].shape)
        # if "normals" in camera.data.output.keys():
        #     print("Received shape of normals          : ", camera.data.output["normals"].shape)
        # if "semantic_segmentation" in camera.data.output.keys():
        #     print("Received shape of semantic segm.   : ", camera.data.output["semantic_segmentation"].shape)
        # if "instance_segmentation_fast" in camera.data.output.keys():
        #     print("Received shape of instance segm.   : ", camera.data.output["instance_segmentation_fast"].shape)
        # if "instance_id_segmentation_fast" in camera.data.output.keys():
        #     print("Received shape of instance id segm.: ", camera.data.output["instance_id_segmentation_fast"].shape)
        # print("-------------------------------")


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
