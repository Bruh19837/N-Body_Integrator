"""
This is an example showing the orbital relation between the Sun and the inner planets, unaffected by other masses,
along with showing energy conservation and total time to simulate.
"""
if __name__ == '__main__':
	import numpy as np
	import matplotlib.pyplot as plt
	from Main import Simulate

	# Define Masses, Initial Positions, and Initial Velocities of Bodies
	# Insert Masses With Comma Separation
	Masses = np.array([
		1.989e30,  # Sun
		3.301e23,  # Mercury
		4.867e24,  # Venus
		5.972e24,  # Earth
		6.417e23,  # Mars
	])

	# Insert Initial Positions As Each Body Having It's Own Coordinate Pair In a List
	Positions = np.array([
		[0.,       0.],  # Sun
		[5.791e10, 0.],  # Mercury
		[1.082e11, 0.],  # Venus
		[1.496e11, 0.],  # Earth
		[2.279e11, 0.],  # Mars
	])

	# Insert Initial Velocity As Each Body Having It's Own Coordinate Pair In a List
	Velocities = np.array([
		[0., 0.],      # Sun
		[0., 4.784e4], # Mercury
		[0., 3.502e4], # Venus
		[0., 2.978e4], # Earth
		[0., 2.408e4], # Mars
	])

	# Replace With Desired Total Simulation Time
	Total_Simulation_Time: float = 59356800
	# Replace With Desired Length Of Interval
	Interval_Of_Time: float = 50

	# Result Of Simulation
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