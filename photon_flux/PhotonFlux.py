from dendro.sdk import ProcessorBase
from dendro.sdk import BaseModel, Field, InputFile, OutputFile
from photon_flux_estimation import PhotonFluxEstimator
import json
import h5py
import remfile
import pynwb

class PhotonFluxContext(BaseModel):
    input: InputFile = Field(description='Input NWB file in .nwb or .nwb.lindi.tar format')
    output: OutputFile = Field(description='Output data in .json format')

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
        with h5py.File(f) as file:
            with pynwb.NWBHDF5IO(file=file, load_namespaces=True) as io:
                # TODO how we distinguish this in the old implementation (before OnePhotonSerires) and the new implementation (ndx-microscopy)? 
                # Get all two-photon series objects
                collection = (
                    _ for _ in io.read().objects.values() 
                    if isinstance(_, pynwb.ophys.TwoPhotonSeries)
                )

                for count, two_photon_series in enumerate(collection):
                    # TODO select subset of frame to estimate sensitivity --> input parameter
                    # TODO option to cut edges --> input parameter
                    movie = two_photon_series.data[:, :, :]

                    # TODO add function to determine if transpose or not the data
                    movie = movie.transpose(0, 2, 1)
                    
                    try:
                        # Create estimator and compute sensitivity
                        estimator = PhotonFluxEstimator(movie)
                        results = estimator.compute_sensitivity()  

                        # Compute photon flux movie
                        photon_flux = estimator.compute_photon_flux()

                        output_fname = 'output.json'
                        with open(output_fname, 'w') as f:
                            f.write(json.dumps(results))

                        print('Uploading output...')
                        context.output.upload(output_fname)
                        print('Done uploading output')

                    except Exception as e:
                        print(f'Error processing series {count}: {e}\n')

