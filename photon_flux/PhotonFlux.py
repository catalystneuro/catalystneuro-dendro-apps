from dendro.sdk import ProcessorBase
from dendro.sdk import BaseModel, Field, InputFile, OutputFile
from photon_flux_estimation import PhotonFluxEstimator
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
    subset_frames: list = Field(
        description="Indices of frames to use for sensitivity estimation"
    )
    crop_edges: list = Field(
        description="Number of pixels to crop from each edge of the frames: [top, bottom, left, right]"
    )


class PhotonFluxProcessor(ProcessorBase):
    name = "photon_flux_processor"
    description = "Run Photon Flux Estimation for two photon imaging data."
    label = "photon_flux_processor"
    image = "ghcr.io/catalystneuro/dendro-photon_flux_estimator:latest"
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
                        results = estimator.compute_sensitivity()

                        # Compute photon flux movie
                        photon_flux = estimator.compute_photon_flux()

                        output_fname = "output.json"
                        with open(output_fname, "w") as f:
                            f.write(json.dumps(results))

                        print("Uploading output...")
                        context.output.upload(output_fname)
                        print("Done uploading output")

                    except Exception as e:
                        print(f"Error processing series {count}: {e}\n")
