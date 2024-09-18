from vpython import *
import imageio
import numpy as np

# Parameters
crank_radius = 2
connecting_rod_length = 6
piston_height = 2
piston_width = 3
cylinder_height = 10
rotation_speed = 2  # radians per second

# Create objects
ground = box(pos=vector(0, -5, 0), size=vector(20, 0.5, 10), color=color.green)
crankshaft = cylinder(pos=vector(0, 0, 0), axis=vector(0, crank_radius, 0), radius=0.3, color=color.blue)
rod = cylinder(pos=crankshaft.axis, axis=vector(connecting_rod_length, 0, 0), radius=0.15, color=color.red)
piston = box(pos=rod.pos + rod.axis, size=vector(piston_width, piston_height, 3), color=color.orange)

# Add the cylinder for piston to move in
cylinder_wall = cylinder(pos=vector(0, 0, -1.5), axis=vector(0, cylinder_height, 0), radius=crank_radius * 2, color=color.gray(0.5), opacity=0.3)

# Piston rod joint (white sphere) to show connection between rod and piston
piston_joint = sphere(pos=piston.pos - vector(0, piston_height / 2, 0), radius=0.3, color=color.white)

# List to store frames for GIF
frames = []

# Animation loop for one full rotation (2*pi radians)
theta = 0
dt = 0.01
total_rotation = 0

while total_rotation < 2 * pi:
    rate(100)
    theta += rotation_speed * dt
    total_rotation += rotation_speed * dt

    # Update the crank position
    crankshaft.axis = vector(crank_radius * cos(theta), crank_radius * sin(theta), 0)

    # Calculate the position of the connecting rod
    x_rod = crank_radius * cos(theta)
    y_rod = crank_radius * sin(theta)

    rod.pos = vector(x_rod, y_rod, 0)

    try:
        # Calculate piston position using basic geometry
        piston_y = y_rod + sqrt(connecting_rod_length**2 - x_rod**2)

        # Move the piston in the cylinder
        piston.pos = vector(0, piston_y + piston_height / 2, 0)
        
        # Update the connecting rod's axis so it correctly points to the piston joint
        rod.axis = piston_joint.pos - rod.pos

        # Update piston joint position
        piston_joint.pos = piston.pos - vector(0, piston_height / 2, 0)
        
        # Capture frame and convert to numpy array
        scene.capture('temp_frame.png')
        frame = imageio.imread('temp_frame.png')
        frames.append(frame)
        
    except ValueError:
        print("Math domain error: Check parameters like connecting rod length and crank radius.")
        break

# Save the frames as a GIF in memory
imageio.mimsave('crank_slider.gif', frames, fps=24)
