# Rubik's Cube Solver

A desktop application that helps users solve a Rubik's Cube by scanning or manually inputting its colors and providing step-by-step solutions. Users can scan the cube's colors, adjust them manually, and receive solution steps. The application supports both a graphical interface and camera-based color detection.

## Features
- **Camera-based color detection**: Scan the cube's faces using a camera.
- **Manual color adjustment**: Adjust the cube state manually through the interface.
- **Solution calculation**: Calculate solution steps based on the entered cube state.
- **User-friendly interface**: Provides a graphical interface using `tkinter`.

## Requirements
This project requires Python 3.11.0 or higher.
The following libraries are required to run the project:

```
kociemba
numpy
opencv-python
tkinter
```

## Installation

1. Download or clone the project files:
   ```bash
   git clone https://github.com/username/rubiks-cube-solver.git
   cd rubiks-cube-solver
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:
   ```bash
   python main.py
   ```

## Usage

### 1. Scanning with Camera
- Click the "Scan Cube" button to open the camera.
- Scan each face of the cube and click the "Capture" button.
- Once all faces are scanned, click the "Finish" button.

### 2. Manual Color Adjustment
- Select a color from the palette in the top-left corner.
- Click on the squares on the cube to assign colors.

### 3. Calculating the Solution
- After adjusting the cube colors, click the "Solve" button.
- The solution steps will be displayed on the screen.

## File Structure
- **main.py**: The main file for the application and graphical interface.
- **cube_solver.py**: Executes the Rubik's Cube solving algorithm.
- **color_detection.py**: Detects cube colors using the camera.
- **requirements.txt**: Lists the project dependencies.

## Contributing
To contribute, please submit a pull request or open an issue.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
