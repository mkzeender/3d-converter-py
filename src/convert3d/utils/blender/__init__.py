from pathlib import Path
from typing import TYPE_CHECKING, Any
import logging
import bpy.ops  # type: ignore


bpy.ops.wm.read_factory_settings(use_empty=True)


def convert(input_path: str, input_format: str, output_path: str, output_format: str):

    match input_format:
        case "obj":
            bpy.ops.import_scene.obj(
                filepath=input_path, axis_forward="-Z", axis_up="Y"
            )

        case "dae":
            bpy.ops.wm.collada_import(filepath=input_path)

        case "glb":
            bpy.ops.import_scene.gltf(filepath=input_path, filter_glob=".glb")

        case "fbx":
            bpy.ops.import_scene.fbx(filepath=input_path)

        case "ply":
            bpy.ops.wm.ply_import(  # type: ignore
                filepath=input_path, forward_axis="NEGATIVE_Z", up_axis="Y"
            )
        # case "ply":
        #     bpy.ops.import_mesh.ply(
        #         filepath=input_path,  # forward_axis="NEGATIVE_Z", up_axis="Y"
        #     )

        case "stl":
            bpy.ops.import_mesh.stl(filepath=input_path)
        case val:
            raise ValueError(f"Unknown file format: {val}")

    logging.info("Successful importing!")

    match output_format:
        case "obj":
            bpy.ops.wm.obj_export(  # type: ignore
                filepath=output_path, forward_axis="NEGATIVE_Z", up_axis="Y"
            )

        case "dae":
            bpy.ops.wm.collada_export(filepath=output_path)

        case "glb":
            bpy.ops.export_scene.gltf(filepath=output_path, export_format="GLB")

        case "fbx":
            bpy.ops.export_scene.fbx(
                filepath=output_path, axis_forward="-Z", axis_up="Y"
            )

        case "ply":
            # bpy.ops.export_mesh.ply(
            #     filepath=output_path, axis_forward="-Z", axis_up="Y"
            # )
            bpy.ops.wm.ply_export(  # type: ignore
                filepath=output_path, forward_axis="NEGATIVE_Z", up_axis="Y"
            )

        case "stl":
            bpy.ops.wm.stl_export(  # type: ignore
                filepath=output_path, forward_axis="NEGATIVE_Z", up_axis="Y"
            )

            # bpy.ops.export_mesh.stl(filepath=output_path)

        case val:
            raise ValueError(f"Unknown file format: '{val}'")
    logging.info("Successful exporting!")
