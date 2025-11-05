🌟 MZI Array Generator (Clements Decomposition)

📝 Overview

This project provides a user-friendly Graphical User Interface (GUI) application built with Python and Tkinter for the automated layout generation of a Mach-Zehnder Interferometer (MZI) mesh. The generated mesh architecture is based on the Clements Decomposition method, allowing the creation of complex N x N mode optical switches.

The application allows photonic designers to easily customize key geometrical parameters and export the simplified GDS-II file directly.

✨ Key Features

Automated Layout Generation: Automatically constructs the complex MZI mesh structure using the Nazca PDK framework.

Clements Decomposition: Supports N x N mode mesh generation (where N is derived from the user-defined Modes parameter).

User-Friendly GUI: All critical parameters are adjustable via a simple Tkinter interface, eliminating the need to edit source code for each run.

Parameter Customization: Control parameters such as mode count, MZI arm spacing, directional coupler (DC) gaps, waveguide width, and taper lengths.

GDS Export: Exports the final design as a GDS-II file, ready for mask fabrication or advanced layout tools.

Grating Coupler Support: Includes logic to integrate a placeholder gc (Grating Coupler) Cell from an external merged_output.gds file when enabled.

🚀 Getting Started

Prerequisites

You need Python 3.8+ and the following libraries:

pip install nazca-design
# Pillow is optional but recommended for loading the application icon
pip install Pillow


Installation and Run

Clone or download the project files.

Place your pre-designed Grating Coupler GDS file (if used) in the same directory, named merged_output.gds.

Run the main Python script:

python MZI_Generator_GUI.py


⚙️ Usage Guide

Launch the GUI: Run the command above to open the "MZI Array Generator" window.

Set Parameters: Adjust the required parameters in the "Global Parameters" frame:

Modes: Must be an even positive integer (e.g., 4, 6, 8). This determines the size of the mesh.

MZI_y_begin, MZI_X_distance, dc_gap, etc.: Define the physical dimensions of the MZI and directional coupler components.

shallow_DC: Set to 1 to use shallow-etched directional couplers/waveguides.

gc_output: Set to 1 to use the pre-loaded gc Cell for the outputs.

Generate: Click the "Generate MZI GDS" button.

Export: The application will generate the GDS file named [Modes]_modes_MZI.gds in the script directory.

🖼️ Visualization

The generated GDS file is a standard industry format. We highly recommend using KLayout for viewing and inspecting the resulting MZI mesh layout.

📅 Project Information

First Version Completed: 2025-11-05

Author: Ze-Sheng Xu   

Contact: zesheng@kth.se
