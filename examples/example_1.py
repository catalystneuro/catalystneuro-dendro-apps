import os
from dendro.client import (
    submit_job,
    DendroJobDefinition,
    DendroJobRequiredResources,
    DendroJobParameter,
    DendroJobInputFile,
    DendroJobOutputFile,
)


service_name = os.getenv("DENDRO_SERVICE_NAME", "luiz-dandihub-service")


# Using this file: https://dandiarchive.org/dandiset/000350/0.240822.1759/files?location=sub-20161022-1&page=1
def main():
    parameters_dict = {
        "registration": "high",
        "diam_cell": 5.0,
        "f_volume": 2.0,
        "timepoints": 1000,
    }
    job_def = DendroJobDefinition(
        appName="voluseg",
        processorName="voluseg_processor",
        inputFiles=[
            DendroJobInputFile(
                name="input",
                fileBaseName="sub-20161022-1",
                url="https://dandiarchive.s3.amazonaws.com/blobs/057/ecb/057ecbef-e732-4e94-8d99-40ebb74d346e",
            )
        ],
        outputFiles=[
            DendroJobOutputFile(
                name="output",
                fileBaseName="cells0_clean.nwb",
            )
        ],
        parameters=[
            DendroJobParameter(name=k, value=v) for k, v in parameters_dict.items()
        ],
    )
    required_resources = DendroJobRequiredResources(
        numCpus=24,
        numGpus=0,
        memoryGb=120,
        timeSec=6 * 3600,
    )
    job = submit_job(
        service_name=service_name,
        job_definition=job_def,
        required_resources=required_resources,
        target_compute_client_ids=["*"],
        tags=["example"],
        skip_cache=True,
    )
    print(job.job_url, job.status)


if __name__ == "__main__":
    main()
