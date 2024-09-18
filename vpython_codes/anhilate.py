from vpython import *
import random

# Set a custom size for the canvas
scene = canvas(width=1200, height=800, center=vector(0, 0, 0), background=color.black)

# Parameters
num_particles = 150
box_size = 30
particle_radius = 0.5
initial_speed = 20

# Create the box
box_obj = box(pos=vector(0, 0, 0), size=vector(box_size, box_size, box_size), opacity=0.2)

# Initialize particles
particles = []
for _ in range(num_particles):
    charge = 1 if random.random() < 0.5 else -1  # Randomly assign charge -1 or +1
    particle_color = color.red if charge > 0 else color.blue  # Directly use color.red and color.blue
    position = vector(random.uniform(-box_size/2, box_size/2),
                      random.uniform(-box_size/2, box_size/2),
                      random.uniform(-box_size/2, box_size/2))
    velocity = vector(random.uniform(-initial_speed, initial_speed),
                      random.uniform(-initial_speed, initial_speed),
                      random.uniform(-initial_speed, initial_speed))
    particle = sphere(pos=position, radius=particle_radius, color=particle_color, make_trail=False)
    particle.charge = charge
    particle.velocity = velocity
    particles.append(particle)

# Function to check for collisions and merge particles
def check_collisions():
    global particles
    new_particles = []
    i = 0
    while i < len(particles):
        j = i + 1
        while j < len(particles):
            if mag(particles[i].pos - particles[j].pos) < (particles[i].radius + particles[j].radius):  # Use mag() for distance
                # Collided particles
                charge_sum = particles[i].charge + particles[j].charge
                new_color = color.red if charge_sum > 0 else color.blue  # Directly use color.red and color.blue
                size = abs(charge_sum) * particle_radius
                
                # Remove the old particles
                particles[i].visible = False
                particles[j].visible = False
                
                # Create a new particle with the sum of charges
                new_particle = sphere(pos=(particles[i].pos + particles[j].pos) / 2,
                                      radius=size,
                                      color=new_color,
                                      make_trail=False)
                new_particle.charge = charge_sum
                new_particle.velocity = (particles[i].velocity + particles[j].velocity) / 2
                new_particles.append(new_particle)
                
                # Remove the old particles
                particles.pop(j)
                particles.pop(i)
                # Adjust index due to removal
                i -= 1
                break
            j += 1
        i += 1

    # Add new particles to the list
    particles += new_particles

# Animation loop
dt = 0.01
while True:
    rate(60)
    
    # Move particles
    for p in particles:
        p.pos += p.velocity * dt
        
        # Bounce off walls
        if abs(p.pos.x) > box_size / 2-p.radius:
            p.velocity.x *= -1
        if abs(p.pos.y) > box_size / 2-p.radius:
            p.velocity.y *= -1
        if abs(p.pos.z) > box_size / 2-p.radius:
            p.velocity.z *= -1

    # Check for collisions
    check_collisions()
