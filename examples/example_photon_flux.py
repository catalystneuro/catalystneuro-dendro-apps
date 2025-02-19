import os
from dandi.dandiapi import DandiAPIClient

from dendro.client import (
    submit_job,
    DendroJobDefinition,
    DendroJobRequiredResources,
    DendroJobParameter,
    DendroJobInputFile,
    DendroJobOutputFile,
)


service_name = "photon_flux"


# Using this file: https://dandiarchive.org/dandiset/000402/0.230307.2132/files?location=sub-17797&page=1
def main():
    url = "https://dandiarchive.s3.amazonaws.com/blobs/a65/6b4/a656b41f-99f7-49e0-a13e-1b283b97a002"

    parameters_dict = {
        "series_path": "acquisition/TwoPhotonSeries1",
        "subset_frames": list(range(500)),
        "crop_edges": [4, 4, 4, 4],
    }
    job_def = DendroJobDefinition(
        appName="photon_flux",
        processorName="photon_flux_processor",
        inputFiles=[
            DendroJobInputFile(
                name="input",
                fileBaseName="sub-17797_ses-4-scan-10_behavior+image+ophys.nwb",
                url=url,
            )
        ],
        outputFiles=[
            DendroJobOutputFile(
                name="output",
                fileBaseName="photon_flux.json",
            )
        ],
        parameters=[
            DendroJobParameter(name=k, value=v) for k, v in parameters_dict.items()
        ],
    )
    required_resources = DendroJobRequiredResources(
        numCpus=2,
        numGpus=0,
        memoryGb=4,
        timeSec=3600,
    )
    job = submit_job(
        service_name=service_name,
        job_definition=job_def,
        required_resources=required_resources,
        target_compute_client_ids=["IcUxwh0z6edS"],
        tags=["example"],
        skip_cache=True,
    )
    print(job.job_url, job.status)


if __name__ == "__main__":
    main()
