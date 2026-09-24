"""
=== N-Body Integrator ===

MAIN CLASS 

An attempt at making a basic simulator using matplotlib to graph how multiple
bodies interact given a set of initial values including mass, position, and velcotiy.
This version uses the Leapfrog method due to it its higher accuracy in energy conservation
in higher simulation times.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import time

# Gravitational Constant
G = 6.67430 * 10**-11 

def Calculate_Net_Forces(masses_list: np.ndarray, positions_list: np.ndarray) -> np.ndarray:
	"""
	Return the net force vectors acting on each body in <bodies> due to all other bodies

	Precondition:
    - ∀ x,y ∈ <bodies> (x.pos ≠ y.pos)
	- len(masses_list) == len(positions_list) == len(velocities_list)
	"""
	# Calculate Distance Vectors and Distance Magnitudes Between All Bodies
	Vectors = positions_list[np.newaxis, :, :] - positions_list[:, np.newaxis, :]
	Vector_Magnitudes = np.linalg.norm(Vectors, axis=2)

	# Dealing With Division By Zero When Calculating Force Between A Body and Itself 
	np.fill_diagonal(Vector_Magnitudes, np.inf)

	# Calculate Force Vectors
	Force_Vectors = (G * (masses_list[:, np.newaxis] * masses_list[np.newaxis, :]) / Vector_Magnitudes**3)[:, :, np.newaxis] * Vectors

	# Return Net Force Vectors for Each Body
	return Force_Vectors.sum(axis=1)

def Energy_In_System(masses: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> float:
    """
    Return the total energy of the system of <bodies>
 
    Preconditions:
    - ∀ x,y ∈ <bodies> (x.pos ≠ y.pos)
	- len(masses_list) == len(positions_list) == len(velocities_list)
    """
    
    # Kinetic Energy Calculation
    Kinetic_Energy = sum([0.5 * mass * np.linalg.norm(velocity)**2 for mass, velocity in zip(masses, velocities)])
    
    # Potential Energy Calculation
    Potential_Energy = sum((-G * masses[i] * masses[j])/np.linalg.norm(positions[j] - positions[i]) for i in range(len(masses)) for j in range(i + 1, len(masses)))

    return (Kinetic_Energy + Potential_Energy)

def Simulate(masses: np.ndarray, positions: np.ndarray, velocities: np.ndarray, total_simulation_time: float, interval_of_time: float, energy_conservation_stat: bool = False, run_time_stat: bool = False) -> list:
	"""
    Simulate <bodies> forward in time for <total_simulation_time> steps of size
    <interval_of_time>, using Leapfrog integration, and return the
    recorded trajectory
 
    Each body in <bodies> is mutated in place over the course of the simulation.
    Its final position and velocity reflect the state at the last step
 
    Preconditions:
    - number_of_steps > 0
    - dt > 0
    - ∀ x,y ∈ <bodies> (x.pos ≠ y.pos)
	- len(masses_list) == len(positions_list) == len(velocities_list)
 
    Return value:
    - a numpy array of shape (number_of_steps, len(bodies), 2), where
      trajectory[step, k] is the position of bodies[k] after <step> steps
	"""
	Masses = masses.copy()
	Positions = positions.copy()
	Velocities = velocities.copy()

    # Start Recording Time
	if run_time_stat:
		Start_Time = time.perf_counter()

    # Record Initial Energy
	if energy_conservation_stat:
		Initial_Energy = Energy_In_System(Masses, Positions, Velocities)

	# Calculate Number of Loops
	Number_Of_Steps = math.floor(total_simulation_time/interval_of_time)

	# Initial Force Calculation to Reduce Loop Calculations
	Net_Forces = Calculate_Net_Forces(Masses, Positions)

	# Array Containing Positional Movement Data Across "Steps" in Time
	Trajectory = np.zeros((Number_Of_Steps, len(Masses), 2))

    # "Stepping" Through Intervals of Time Till Total Simulation Time is reached
	for step in range(Number_Of_Steps):

		# Kick
		Velocities += (Net_Forces / Masses[:, np.newaxis]) * (interval_of_time / 2)

		# Drift
		Positions += Velocities * interval_of_time

		# Recalculate Forces
		Net_Forces = Calculate_Net_Forces(Masses, Positions)

		# Kick
		Velocities += (Net_Forces / Masses[:, np.newaxis]) * (interval_of_time / 2)

		# Storing Time Data and Body Position Data
		Trajectory[step] = Positions

	# End Recording Time
	if run_time_stat:
		End_Time = time.perf_counter()

	# Record Final Energy
	if energy_conservation_stat:
		Final_Energy = Energy_In_System(Masses, Positions, Velocities)

	# Return Values Based on Initialization
	Results = [Trajectory]

	# Add Time Value
	if run_time_stat:
		Results.append(End_Time - Start_Time)
	# Add Energy Value
	if energy_conservation_stat:
		Results.append(math.fabs((Final_Energy - Initial_Energy) / Initial_Energy * 100))

	return Results

if __name__ == "__main__":
    # Replace With Desired Total Simulation Time
    Total_Simulation_Time: float = 0.0
    # Replace With Desired Length Of Interval
    Interval_Of_Time: float = 0.0 

    # Define Masses, Initial Positions, and Initial Velocities of Bodies
    # Insert Masses With Comma Separation
    Masses = np.array([])

    # Insert Initial Positions As Each Body Having It's Own Coordinate Pair In a List
    Positions = np.array([])

    # Insert Initial Velocity As Each Body Having It's Own Coordinate Pair In a List
    Velocities = np.array([])

    # Calculate The Trajectory Of All Bodies
    Total_Information = Simulate(Masses, Positions, Velocities, Total_Simulation_Time, Interval_Of_Time, True, True)

    # Trajectory Information
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
    for k in range(len(Masses)):
        plt.plot(Trajectory[:, k, 0], Trajectory[:, k, 1], label=f"body{k+1}")
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()