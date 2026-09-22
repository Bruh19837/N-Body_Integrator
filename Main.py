"""
=== N-Body Integrator ===

MAIN CLASS 

An attempt at making a basic simulator using matplotlib to graph how multiple
bodies interact given a set of initial values including mass, position, and velcotiy.
This version uses a Semi-Implicit Eulers' Integration method due to it its
sympletic property. Aka mostly energy conversing over time.
"""

import math
import time
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from Body import Body

# Gravitational Constant
G = 6.67430 * 10**-11 

def Force_Of_Gravity(mass1: float, mass2: float, vector_magnitude: float) -> float:
    """
    Return the magnitude of the gravitational force between two masses
    <mass1> and <mass2> separated by a distance <vector_magnitude>
 
    Preconditions:
    - mass1 > 0 and mass2 > 0
    - vector_magnitude > 0
    """
    
    return (G * mass1 * mass2 / vector_magnitude **2)

def Energy_In_System(bodies: list[Body]) -> float:
    """
    Return the total energy of the system of <bodies>
 
    Preconditions:
    - ∀ x,y ∈ <bodies> (x.pos ≠ y.pos)
    """
    
    # Kinetic Energy Calculation
    Kinetic_Energy = sum([0.5 * body.mass * np.linalg.norm(body.vel)**2 for body in bodies])
    
    # Potential Energy Calculation
    Potential_Energy = 0
    for i, j in combinations(range(len(bodies)), 2):
        Vector = bodies[j].pos - bodies[i].pos
        Vector_Magnitude = np.linalg.norm(Vector)
        Potential_Energy += -G * bodies[i].mass * bodies[j].mass / Vector_Magnitude

    return (Kinetic_Energy + Potential_Energy)

def Simulate(bodies: list[Body], total_simulation_time: float, interval_of_time: float, energy_conservation_stat: bool = False, run_time_stat: bool = False) -> list:
    """
    Simulate <bodies> forward in time for <total_simulation_time> using time-steps of size
    <interval_of_time>, using Semi-Implicit Euler integration, and return the
    recorded trajectory
 
    Each body in <bodies> is mutated in place over the course of the simulation.
    Its final position and velocity reflect the state at the last step
 
    Preconditions:
    - number_of_steps > 0
    - dt > 0
    - ∀ x,y ∈ <bodies> (x.pos ≠ y.pos)
 
    Return value:
    - a numpy array of shape (number_of_steps, len(bodies), 2), where
      trajectory[step, k] is the position of bodies[k] after <step> steps
    """

    # Start Recording Time
    if run_time_stat:
        Start_Time = time.perf_counter()

    # Record Initial Energy
    if energy_conservation_stat:
        Initial_Energy = Energy_In_System(bodies)

    # Array Containing Positional Movement Data Across "Steps" in Time
    Trajectory = np.zeros((math.floor(total_simulation_time/interval_of_time), len(bodies), 2))

    # "Stepping" Through Intervals of Time Till Total Simulation Time is reached
    for step in range(math.floor(total_simulation_time/interval_of_time)):
        # Array to Store Force Data Between Bodies
        Forces = [np.zeros(2) for _ in bodies]

        # Calculating Distance Between Bodies and Force Between Bodies
        for i, j in combinations(range(len(bodies)), 2):

            # Distance Calculation
            Vector = bodies[j].pos - bodies[i].pos
            Vector_Magnitude = np.linalg.norm(Vector)

            # Force Calculation
            Force_Magnitude = Force_Of_Gravity(bodies[i].mass, bodies[j].mass, Vector_Magnitude)
            Force_Vector = Force_Magnitude * (Vector / Vector_Magnitude)

            # Storing Force Calculation
            Forces[i] += Force_Vector
            Forces[j] -= Force_Vector

        # Updating Body Velocity and Position
        for body, force in zip(bodies, Forces):
            body.vel += (force / body.mass) * interval_of_time
            body.pos += body.vel * interval_of_time

        # Storing Time Data and Body Position Data
        for k, body in enumerate(bodies):
            Trajectory[step, k] = body.pos

    # End Recording Time
    if energy_conservation_stat:
        Final_Energy = Energy_In_System(bodies)

    # Record Final Energy
    if run_time_stat:
        End_Time = time.perf_counter()

    # Return Values Based on Initialization
    Results = [Trajectory]

    # Add Time Value
    if run_time_stat:
        Results.append(End_Time - Start_Time)
    # Add Energy Value
    if energy_conservation_stat:
        Results.append(math.fabs((Final_Energy - Initial_Energy) / Initial_Energy * 100))

    return Results

if __name__ == "main":
    # Add Desired Simulation Bodies
    Bodies: list[Body] = []
            
    # Replace With Desired Total Simulation Time
    Total_Simulation_Time: float = 1000
    # Replace With Desired Length Of Interval
    Interval_Of_Time: float = 1.0 

    # Calculate The Trajectory Of All Bodies
    Total_Information = Simulate(Bodies, Total_Simulation_Time, Interval_Of_Time)

    Trajectory = Total_Information[0]

	# Run Time Information
    if len(Total_Information) > 1:
        Calculation_Time = Total_Information[1]
        print(f"Calculation Time: {Calculation_Time} seconds")

	# Energy Conservation Information
    if len(Total_Information) > 2:
        Energy_Conservation_Delta = Total_Information[2]
        print(f"Energy Conservation Delta: {Energy_Conservation_Delta} %")

    # Plot All Bodies
    plt.figure()
    for k in range(len(Bodies)):
        plt.plot(Trajectory[:, k, 0], Trajectory[:, k, 1], label=f"body{k+1}")
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
