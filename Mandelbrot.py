# Author : Youssef Aitbouddroub
# Visualization for the Mandelbrot set with focus on some interesting target positions
# 1/27/2025

from manim import *
import numpy as np
import matplotlib.cm as cm

class MandelbrotZoomSequence(MovingCameraScene):
    def construct(self):
        """
        Main construct method to create the Mandelbrot zoom sequence animation.
        """
        # Display introductory text
        intro_text_1 = Text("Mandelbrot Set Exploration", font_size=36)
        intro_text_2 = Text("Implemented by Youssef Aitbouddroub", font_size=24).next_to(intro_text_1, DOWN)
        intro_group = VGroup(intro_text_1, intro_text_2)
        self.play(Write(intro_group))
        self.wait(2)
        self.play(FadeOut(intro_group))

        # Configure initial camera position and size
        zoom_start_point = np.array([-0.373973468, 0.659770403, 0]) # first target
        self.camera.frame.move_to(zoom_start_point).set_width(0.001)
        
        # Fixed resolution for all frames
        RESOLUTION = 1024
        
        # Create initial Mandelbrot set image
        image = self.generate_mandelbrot_image(
            zoom_start_point[0] - 0.0005,
            zoom_start_point[0] + 0.0005,
            zoom_start_point[1] - 0.0005,
            zoom_start_point[1] + 0.0005,
            RESOLUTION, RESOLUTION
        )
        mandelbrot_mob = ImageMobject(image).move_to(zoom_start_point)
        self.add(mandelbrot_mob)
        
        # Add updater with fixed resolution
        mandelbrot_mob.add_updater(lambda mob: self.update_mandelbrot(mob, RESOLUTION))
        
        # First zoom out animation
        self.animate_zoom(
            start_width=0.1e-4,
            end_width=4.0,
            zoom_steps=80,
            zoom_point=zoom_start_point,
            zoom_out=True
        )

        self.wait(1)
       
        # Animate camera movement to the new zoom-in position
        second_target = np.array([-1.768778833, -0.001738995, 0])
        self.play(
            self.camera.frame.animate.move_to(second_target),
            run_time=3
        )
        
        # Second zoom in animation
        self.animate_zoom(
            start_width=3.0,
            end_width=1e-9,
            zoom_steps=20,
            zoom_point=second_target,
            zoom_out=False,
            run_time=1
        )

        self.wait(1)

    def animate_zoom(self, start_width, end_width, zoom_steps, zoom_point, zoom_out=True, run_time=0.1):
        """
        Generic zoom animation function.
        
        Parameters:
        - start_width: Initial width of the camera frame.
        - end_width: Final width of the camera frame.
        - zoom_steps: Number of steps for the zoom animation.
        - zoom_point: The point to zoom into.
        - zoom_out: Boolean indicating whether to zoom out (default is True).
        - run_time: Duration of each zoom step (default is 0.1 seconds).
        """
        self.camera.frame.set_width(start_width).move_to(zoom_point)
        zoom_factor = (end_width / start_width) ** (1/zoom_steps)
        
        for _ in range(zoom_steps):
            new_width = self.camera.frame.width * zoom_factor
            self.play(
                self.camera.frame.animate.set_width(new_width).move_to(zoom_point),
                run_time=run_time,
                rate_func=rate_functions.ease_in_out_quad
            )

    def generate_mandelbrot_image(self, x_start, x_end, y_start, y_end, width, height, max_iter=450):
        """
        Generate Mandelbrot set image array for given coordinates.
        
        Parameters:
        - x_start: Starting x-coordinate.
        - x_end: Ending x-coordinate.
        - y_start: Starting y-coordinate.
        - y_end: Ending y-coordinate.
        - width: Width of the image.
        - height: Height of the image.
        - max_iter: Maximum number of iterations for the Mandelbrot calculation.
        
        Returns:
        - A NumPy array representing the RGB image of the Mandelbrot set.
        """
        # Create complex grid
        x = np.linspace(x_start, x_end, width)
        y = np.linspace(y_start, y_end, height)
        c = x[:, None] + 1j*y[None, :] # Reshaping x into a column vector and y into row vector creating 2D array of complex numbers 
        
        # Vectorized Mandelbrot calculation
        z = np.zeros_like(c, dtype=np.complex128) # Creates an array z of the same shape as c, initialized to 0 + 0j.
        div_time = np.full(c.shape, max_iter, dtype=np.int32) # Number of iterations before the escape
        mask = np.ones_like(c, dtype=bool) # Boolean matrix that keeps track of which points should continue iterating.
        
        for i in range(max_iter):
            z[mask] = z[mask]**2 + c[mask]
            mask[np.abs(z) > 4] = False
            div_time[mask] = i

        # Normalize and format for color mapping
        div_time = div_time.T  # Transposing the matrix match coordinate systems when displaying the image.
        max_val = div_time.max() or 1
        normalized = div_time.astype(np.float32) / max_val
        
        # Generate RGB colors with explicit 3 channels
        return cm.plasma(normalized, bytes=True)[..., :3]

    def update_mandelbrot(self, mob, resolution):
        """
        Update function with fixed resolution.
        
        Parameters:
        - mob: The ImageMobject to update.
        - resolution: The resolution of the image.
        """
        frame = self.camera.frame
        center = frame.get_center()
        current_width = frame.width
        
        # Calculate view bounds with fixed aspect ratio
        aspect_ratio = 1.0  # Maintain square aspect ratio
        x_half = current_width / 2
        y_half = x_half * aspect_ratio
        
        # Generate new image with consistent resolution
        new_image = self.generate_mandelbrot_image(
            center[0] - x_half,
            center[0] + x_half,
            center[1] - y_half,
            center[1] + y_half,
            resolution, resolution
        )
        
        # Update display with consistent dimensions
        mob.become(ImageMobject(new_image)
            .move_to(center)
            .stretch_to_fit_width(current_width)
            .stretch_to_fit_height(current_width * aspect_ratio))