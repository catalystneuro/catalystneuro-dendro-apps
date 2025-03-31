import numpy as np
import json
from h5py import File
import remfile
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from pynwb import NWBHDF5IO
from pynwb import NWBFile
from pynwb.ophys import TwoPhotonSeries
from dendro.sdk import ProcessorBase, InputFile, OutputFile
from photon_flux_estimation import PhotonFluxEstimator


def _retrieve_two_photon_series_pynwb(
    nwbfile: NWBFile, two_photon_series_path: Optional[str] = None
) -> TwoPhotonSeries:
    """
    Get an TwoPhotonSeries object from an NWBFile.

    Parameters
    ----------
    nwbfile : NWBFile
        The NWBFile object from which to extract the TwoPhotonSeries.
    two_photon_series_path : str, default: None
        The name of the TwoPhotonSeries to extract. If not specified, it will return the first found TwoPhotonSeries
        if there's only one; otherwise, it raises an error.

    Returns
    -------
    TwoPhotonSeries
        The requested TwoPhotonSeries object.

    Raises
    ------
    ValueError
        If no acquisitions are found in the NWBFile or if multiple acquisitions are found but no two_photon_series_path
        is provided.
    AssertionError
        If the specified two_photon_series_path is not present in the NWBFile.
    """

    two_photon_series_dict: Dict[str, TwoPhotonSeries] = {}

    for item in nwbfile.all_children():
        if isinstance(item, TwoPhotonSeries):
            # remove data and skip first "/"
            two_photon_series_key = item.data.name.replace("/data", "")[1:]
            two_photon_series_dict[two_photon_series_key] = item

    if two_photon_series_path is not None:
        if two_photon_series_path not in two_photon_series_dict:
            raise ValueError(f"{two_photon_series_path} not found in the NWBFile. ")
        two_photon_series = two_photon_series_dict[two_photon_series_path]
    else:
        two_photon_series_list = list(two_photon_series_dict.keys())
        if len(two_photon_series_list) > 1:
            raise ValueError(
                f"More than one acquisition found! You must specify 'two_photon_series_path'. \n"
                f"Options in current file are: {[e for e in two_photon_series_list]}"
            )
        if len(two_photon_series_list) == 0:
            raise ValueError("No acquisitions found in the .nwb file.")
        two_photon_series = two_photon_series_dict[two_photon_series_list[0]]

    return two_photon_series


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

        with File(file) as file:
            with NWBHDF5IO(file=file, load_namespaces=True) as io:

                nwbfile = io.read()
                two_photon_series = _retrieve_two_photon_series_pynwb(
                    nwbfile=nwbfile, two_photon_series_path=series_path
                )
                # TODO add option to select series to process when ndx-microscopy is used

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

                    # Add mean photon flux image
                    results["photon_flux_mean_image"] = photon_flux.mean(
                        axis=0
                    ).tolist()

                    # Add coefficient of variation (CV) matrix
                    q = results["sensitivity"]
                    b = results["zero_level"]
                    m = movie.mean(axis=0)
                    v = (
                        (movie[1:, :, :].astype("float64") - movie[:-1, :, :]) ** 2 / 2
                    ).mean(axis=0)
                    imx = np.stack(((m - b) / q, v / q / q, (m - b) / q), axis=-1)
                    coefficient_of_variation_matrix = np.minimum(
                        1,
                        np.sqrt(0.01 + np.maximum(0, imx / np.quantile(imx, 0.9999)))
                        - 0.1,
                    )
                    results["coefficient_of_variation_matrix"] = (
                        coefficient_of_variation_matrix.tolist()
                    )

                    # TODO create lindi output file instead of json

                    output_fname = "output.json"
                    with open(output_fname, "w") as f:
                        json.dump(results, f, indent=2)

                    print("Uploading output...")
                    context.output.upload(output_fname)
                    print("Done uploading output")

                except Exception as e:
                    print(f"Error processing series {two_photon_series.name}: {e}\n")
