# matplotlib_utils.py
import matplotlib.pyplot as plt
from pathlib import Path


# %%
def create_subplots_matplotlib(n_plots, n_cols=2, figsize=(30, 5)):
    """
    Creates a figure with subplots in a grid layout.

    Parameters:
    - n_plots (int): The number of subplots to create.
    - n_cols (int, optional): The number of columns in the subplot grid. Default is 2.
    - figsize (tuple, optional): The size of the figure in inches (width, height). Default is (15, 5).

    Returns:
    - fig (matplotlib.figure.Figure): The created matplotlib figure object.
    - axes (list of matplotlib.axes.Axes): A flattened list of axes objects (subplots).

    Raises:
    - ValueError: If the number of plots (`n_plots`) is less than 1 or if `n_cols` is less than 1.
    """
    # Validate inputs
    if n_plots < 1:
        raise ValueError("The number of plots (n_plots) must be at least 1.")

    if n_cols < 1:
        raise ValueError("The number of columns (n_cols) must be at least 1.")

    # Determine the number of rows required to fit the plots
    n_rows = (n_plots + n_cols - 1) // n_cols

    # Create the figure and axes
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array for easy iteration
    axes = axes.flatten() if n_plots > 1 else [axes]

    return fig, axes


# %%
def customize_plot(
    ax,
    title="",
    xlabel="",
    ylabel="",
    legend_title=None,
    legend_loc="upper left",
    bbox_to_anchor=(1.05, 1),
    grid_axis="both",
    grid_style="--",
    grid_alpha=0.7,
    tight_layout=True,
):
    """
    Customize a matplotlib plot with common settings.

    Args:
        ax (matplotlib.axes.Axes): The axis object to customize.
        title (str): The title of the plot.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        legend_title (str): The title for the legend.
        legend_loc (str, optional): Location of the legend. Default is "upper left".
        bbox_to_anchor (tuple, optional): Bounding box anchor for the legend. Default is (1.05, 1).
        grid_axis (str, optional): The axis to apply grid to. Default is "both".
        grid_style (str, optional): The linestyle for the grid. Default is "--".
        grid_alpha (float, optional): The transparency of the grid. Default is 0.7.
        tight_layout (bool, optional): Whether to adjust the layout to fit. Default is True.

    Returns:
        matplotlib.axes.Axes: The customized axis.
    """
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    legend = ax.legend(
        title=legend_title, loc=legend_loc, bbox_to_anchor=bbox_to_anchor
    )
    if legend:
        legend.set_title(legend_title)

    ax.grid(axis=grid_axis, linestyle=grid_style, alpha=grid_alpha)

    if tight_layout:
        plt.tight_layout()

    return ax


# %%
def save_fig_matplotlib(fig, file_path: str) -> None:
    """
    Save a Matplotlib or Seaborn plot to a file in the specified format and directory.

    This function saves a plot to a file with the format specified in the file_path extension
    and ensures that the output directory exists. It supports both Matplotlib and Seaborn figures.

    Parameters:
    - fig (plt.Figure): The plot object to be saved. Can be a Matplotlib or Seaborn figure.
    - file_path (str): The path where the plot will be saved, including the file name and extension.

    Raises:
    - ValueError: If the file format (extracted from file_path) is not supported.
    - TypeError: If the provided figure is neither a Matplotlib nor a Seaborn figure.

    Returns:
    None
    """

    # List of supported formats
    supported_formats = ["png", "jpg", "svg", "pdf"]

    # Extract the format from the file path
    file_extension = Path(file_path).suffix.lstrip(".")

    # Ensure the provided format is valid
    if file_extension not in supported_formats:
        raise ValueError(
            f"Unsupported format '{file_extension}'. Supported formats are: {', '.join(supported_formats)}."
        )

    # Ensure the directory exists
    dir_path = Path(file_path).parent
    dir_path.mkdir(parents=True, exist_ok=True)

    # Check if the figure is a Matplotlib or Seaborn figure
    if isinstance(fig, plt.Figure):
        # Save the Matplotlib or Seaborn figure as an image file (PNG, JPG, SVG, PDF)
        fig.savefig(file_path, format=file_extension)
    else:
        raise TypeError(
            "The 'fig' parameter must be a Matplotlib 'plt.Figure' or a Seaborn 'sns.Figure' object."
        )


# %%
if __name__ == "__main__":
    current_working_directory = Path.cwd()
    output_file_path = current_working_directory / "plots"
