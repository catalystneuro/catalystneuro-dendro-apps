from dendro.sdk import ProcessorBase, BaseModel, Field, InputFile, OutputFile


class VolusegContext(BaseModel):
    input: InputFile = Field(description='Input NWB file in .nwb or .nwb.lindi.tar format')
    output: OutputFile = Field(description='Output embedding in .lindi.tar format')
    # units_path: str = Field(description='Path to the units table in the NWB file', default='units')
    # max_iterations: int = Field(description='Maximum number of iterations', default=1000)
    # batch_size: int = Field(description='Batch size', default=1000)
    # bin_size_msec: float = Field(description='Bin size in milliseconds', default=20)
    # output_dimensions: int = Field(description='Output dimensions', default=10)


class VolusegProcessor(ProcessorBase):
    name = 'voluseg_processor'
    description = 'Run Voluseg for volumetric segmentation.'
    label = 'voluseg_processor'
    image = 'catalystneuro/dendro-voluseg:0.1.0'
    executable = '/app/main.py'
    attributes = {}

    @staticmethod
    def run(
        context: VolusegContext
    ):
        pass