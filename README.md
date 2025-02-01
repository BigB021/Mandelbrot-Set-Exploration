# Mandelbrot-Set-Exploration
Visualization for the Mandelbrot set with focus on some interesting target positions

## Overview
`mandelbrot.py` is a Python script that generates and visualizes the Mandelbrot set. The Mandelbrot set is a set of complex numbers that produces a fractal when plotted. This script allows you to explore the intricate and beautiful patterns of the Mandelbrot set by generating high-resolution images.

## Installation
To run `mandelbrot.py`, you need to have Python installed on your system.

You will also need the following Python libraries:
- `numpy`
- `matplotlib`
- `manim`

You can install these libraries using pip:
```sh
pip install numpy matplotlib manim
```

## Usage
To generate and visualize the Mandelbrot set, run the following command:

```sh
manim -pqh Mandelbrot.py MandelbrotZoomSequence --disable_caching
```
-m for medium quality, -l for low and -h for high resolution.

### Parameters
The script includes several parameters that you can adjust to change the visualization:
- `width` and `height`: Dimensions of the output image.
- `max_iter`: Maximum number of iterations to determine if a point is in the Mandelbrot set.
- `x_min`, `x_max`, `y_min`, `y_max`: The range of the complex plane to visualize.

## Output
The script will generate video animation zooming out from "starfish region" and zoom into "Julia Island"

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- The Mandelbrot set was first defined and studied by the mathematician Benoît B. Mandelbrot.
- This script uses the `numpy` library for numerical computations and the `matplotlib` library for plotting the fractal, and `manim` for animation and image generation.

Feel free to contribute to this project by submitting issues or pull requests.
