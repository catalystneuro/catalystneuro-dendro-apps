from dendro.sdk import ProcessorBase, InputFile, OutputFile
from pydantic import BaseModel, Field
from typing import List
from photon_flux_estimation import PhotonFluxEstimator
import numpy as np
import json
import h5py
import remfile
import pynwb


class PhotonFluxContext(BaseModel):
    input: InputFile = Field(
        description="Input NWB file in .nwb or .nwb.lindi.tar format"
    )
    output: OutputFile = Field(description="Output data in .json format")
    series_path: str = Field(description="Path to the multiphoton series to process")
    subset_frames: List[int] = Field(
        description="Indices of frames to use for sensitivity estimation"
    )
    crop_edges: List[int] = Field(
        description="Number of pixels to crop from each edge of the frames: [top, bottom, left, right]"
    )


class PhotonFluxProcessor(ProcessorBase):
    name = "photon_flux_processor"
    description = "Run Photon Flux Estimation for two photon imaging data."
    label = "photon_flux_processor"
    image = "ghcr.io/catalystneuro/dendro-photon_flux:latest"
    executable = "/app/main.py"
    attributes = {}

    @staticmethod
    def run(context: PhotonFluxContext):

        input = context.input
        url = input.get_url()
        assert url
        file = remfile.File(url)
        series_path = context.series_path
        subset_frames = context.subset_frames
        crop_edges = context.crop_edges

        with h5py.File(file) as file:
            with pynwb.NWBHDF5IO(file=file, load_namespaces=True) as io:
                # TODO add option to select series to process when ndx-microscopy is used
                # Get all two-photon series objects
                collection = (
                    _
                    for _ in io.read().objects.values()
                    if isinstance(_, pynwb.ophys.TwoPhotonSeries)
                )

                for count, two_photon_series in enumerate(collection):
                    if subset_frames is None:
                        subset_frames = list(range(two_photon_series.data.shape[0]))
                    if crop_edges is None:
                        crop_edges = [None, None, None, None]
                    movie = two_photon_series.data[
                        subset_frames,
                        crop_edges[2] : -1 * crop_edges[3],
                        crop_edges[0] : -1 * crop_edges[1],
                    ]

                    # TODO add function to determine if the data needs to be transposed
                    movie = movie.transpose(0, 2, 1)

                    try:
                        # Create estimator and compute sensitivity
                        estimator = PhotonFluxEstimator(movie)
                        estimation_results = estimator.compute_sensitivity()

                        # Convert model to class name and numpy values to Python native types in place
                        if "model" in estimation_results:
                            estimation_results["model"] = estimation_results[
                                "model"
                            ].__class__.__name__
                        for key, value in estimation_results.items():
                            if isinstance(value, np.ndarray):
                                estimation_results[key] = value.tolist()
                            elif isinstance(value, (np.floating, np.integer)):
                                estimation_results[key] = float(value)
                        results = estimation_results

                        # Compute photon flux movie
                        photon_flux = estimator.compute_photon_flux()

                        # Add photon flux statistics
                        results["photon_flux_stats"] = {
                            "mean": float(photon_flux.mean()),
                            "min": float(photon_flux.min()),
                            "max": float(photon_flux.max()),
                        }

                        output_fname = "output.json"
                        with open(output_fname, "w") as f:
                            json.dump(results, f, indent=2)

                        print("Uploading output...")
                        context.output.upload(output_fname)
                        print("Done uploading output")

                    except Exception as e:
                        print(f"Error processing series {count}: {e}\n")
