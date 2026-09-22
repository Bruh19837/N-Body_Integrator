"""
This is an example showing the orbital relation between the Sun and the inner planets, unaffected by other masses,
along with showing energy conservation and total time to simulate.
"""
if __name__ == '__main__':
	import numpy as np
	import matplotlib.pyplot as plt
	from Body import Body
	from Main import Simulate

	Bodies = [
			Body(1.989e30, np.array([0., 0.]),       np.array([0.00, 0.00])),   # Sun
			Body(3.301e23, np.array([5.791e10, 0.]), np.array([0., 4.784e4])),  # Mercury
			Body(4.867e24, np.array([1.082e11, 0.]),  np.array([0., 3.502e4])), # Venus
			Body(5.972e24, np.array([1.496e11, 0.]),  np.array([0., 2.978e4])), # Earth
			Body(6.417e23, np.array([2.279e11, 0.]),  np.array([0., 2.408e4])), # Mars
			# Adding The Gas Giants Makes The Graph So Large That The Inner Planets Become Hidden 
			]

	# Replace With Desired Total Simulation Time
	Total_Simulation_Time: float = 59356800
	# Replace With Desired Length Of Interval
	Interval_Of_Time: float = 50

	# Result Of Simulation
	Total_Information = Simulate(Bodies, Total_Simulation_Time, Interval_Of_Time, True, True)

	# Trajectory Information
	Trajectory = Total_Information[0]

	# Run Time Information
	if len(Total_Information) > 2:
		Calculation_Time = Total_Information[2]
		print(f"Calculation Time: {Calculation_Time} seconds")

	# Energy Conservation Information
	if len(Total_Information) > 1:
		Energy_Conservation_Delta = Total_Information[1]
		print(f"Energy Conservation Delta: {Energy_Conservation_Delta} %")

	# Plot All Bodies
	plt.figure()
	for k in range(len(Bodies)):
		plt.plot(Trajectory[:, k, 0], Trajectory[:, k, 1], label=f"body{k+1}")
	plt.legend()
	plt.xlabel("x")
	plt.ylabel("y")
	plt.show()