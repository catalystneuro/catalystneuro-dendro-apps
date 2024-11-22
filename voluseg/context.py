from dendro.sdk import BaseModel, Field, InputFile, OutputFile


class VolusegContext(BaseModel):
    input: InputFile = Field(
        description="Input NWB file in .nwb or .nwb.lindi.tar format"
    )
    output: OutputFile = Field(description="Output embedding in .lindi.tar format")
    detrending: str = Field(
        default="standard",
        description="Type of detrending: 'standard', 'robust', or 'none'",
        json_schema_extra={"options": ["standard", "robust", "none"]},
    )
    registration: str = Field(
        default="medium",
        description="Quality of registration: 'high', 'medium', 'low' or 'none'",
        json_schema_extra={"options": ["high", "medium", "low", "none"]},
    )
    registration_restrict: str = Field(
        default="",
        description="Restrict registration (e.g. 1x1x1x1x1x1x0x0x0x1x1x0)",
    )
    diam_cell: float = Field(
        default=6.0,
        description="Cell diameter in microns",
    )
    ds: int = Field(
        default=2,
        description="Spatial coarse-graining in x-y dimension",
    )
    planes_pad: int = Field(
        default=0,
        description="Number of planes to pad the volume with for robust registration",
    )
    planes_packed: bool = Field(
        default=False,
        description="Packed planes in each volume (for single plane imaging with packed planes)",
    )
    parallel_clean: bool = Field(
        default=True,
        description="Parallelization of final cleaning (True is fast but memory intensive)",
    )
    parallel_volume: bool = Field(
        default=True,
        description="Parallelization of mean-volume computation (True is fast but memory intensive)",
    )
    save_volume: bool = Field(
        default=False,
        description="Save registered volumes after segmentation (True keeps a copy of the volumes)",
    )
    type_timepoints: str = Field(
        default="dff",
        description="Type of timepoints to use for cell detection: 'dff', 'periodic' or 'custom'",
        json_schema_extra={"options": ["dff", "periodic", "custom"]},
    )
    type_mask: str = Field(
        default="geomean",
        description="Type of volume averaging for mask: 'mean', 'geomean' or 'max'",
        json_schema_extra={"options": ["mean", "geomean", "max"]},
    )
    timepoints: int = Field(
        default=1000,
        description="Number ('dff', 'periodic') or vector ('custom') of timepoints for segmentation",
    )
    f_hipass: float = Field(
        default=0,
        description="Frequency (Hz) for high-pass filtering of cell timeseries",
    )
    f_volume: float = Field(
        default=2.0,
        description="Imaging frequency in Hz",
    )
    n_cells_block: int = Field(
        default=316,
        description="Number of cells in a block. Small number is fast but can lead to blocky output",
    )
    n_colors: int = Field(
        default=1,
        description="Number of brain colors (2 in two-color volumes)",
    )
    res_x: float = Field(
        default=0.40625,
        description="X resolution in microns",
    )
    res_y: float = Field(
        default=0.40625,
        description="Y resolution in microns",
    )
    res_z: float = Field(
        default=5.0,
        description="Z resolution in microns",
    )
    t_baseline: int = Field(
        default=300,
        description="Interval for baseline calculation in seconds",
    )
    t_section: float = Field(
        default=0.01,
        description="Exposure time in seconds for slice acquisition",
    )
    thr_mask: float = Field(
        default=0.5,
        description="Threshold for volume mask: 0 < thr <= 1 (probability) or thr > 1 (intensity)",
    )
    ext: str = Field(
        default=".nwb",
        description="File extension",
    )
    dim_order: str = Field(
        default="xyz",
        description="Dimensions order. Examples: 'zyx', 'xyz'",
    )
    remote: bool = Field(
        default=True,
        description="Remote file",
    )
    output_to_nwb: bool = Field(
        default=True,
        description="Save results to a new NWB file",
    )
