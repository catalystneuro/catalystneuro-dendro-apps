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
        import os
        import lindi
        import voluseg

        # set and save parameters
        parameters0 = voluseg.parameter_dictionary()
        parameters0["dir_ants"] = "/ants-2.5.3/bin/"
        parameters0["dir_input"] = "/voluseg/data/"
        parameters0["dir_output"] = "/tmp/voluseg_output"

        # user-defined parameters
        parameters0["detrending"] = context.detrending
        parameters0["registration"] = context.registration
        parameters0["registration_restrict"] = context.registration_restrict
        parameters0["diam_cell"] = context.diam_cell
        parameters0["ds"] = context.ds
        parameters0["planes_pad"] = context.planes_pad
        parameters0["planes_packed"] = context.planes_packed
        parameters0["parallel_clean"] = context.parallel_clean
        parameters0["parallel_volume"] = context.parallel_volume
        parameters0["save_volume"] = context.save_volume
        parameters0["type_timepoints"] = context.type_timepoints
        parameters0["type_mask"] = context.type_mask
        parameters0["timepoints"] = context.timepoints
        parameters0["f_hipass"] = context.f_hipass
        parameters0["f_volume"] = context.f_volume
        parameters0["n_cells_block"] = context.n_cells_block
        parameters0["n_colors"] = context.n_colors
        parameters0["res_x"] = context.res_x
        parameters0["res_y"] = context.res_y
        parameters0["res_z"] = context.res_z
        parameters0["t_baseline"] = context.t_baseline
        parameters0["t_section"] = context.t_section
        parameters0["thr_mask"] = context.thr_mask

        voluseg.step0_process_parameters(parameters0)
        filename_parameters = str(
            os.path.join(parameters0["dir_output"], "parameters.json")
        )
        parameters = voluseg.load_parameters(filename_parameters)
        print("Parameters:\n", parameters)

        print("Process volumes...")
        voluseg.step1_process_volumes(parameters)

        print("Align volumes...")
        voluseg.step2_align_volumes(parameters)

        print("Mask volumes...")
        voluseg.step3_mask_volumes(parameters)

        print("Detect cells...")
        voluseg.step4_detect_cells(parameters)

        print("Clean cells...")
        voluseg.step5_clean_cells(parameters)