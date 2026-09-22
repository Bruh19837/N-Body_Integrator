"""
=== N-Body Integrator ===

BODY CLASS

This file contains the Body class, representing a single point mass. A Body 
tracks its mass, position, and velocity, which is mutated in place by the 
integrator as the simulation "steps" forward in time.
"""
import numpy as np
 
class Body:
    """A point mass participating in an N-body gravitational simulation.
 
    Public Attributes:
    - mass: the mass of this body, in kilograms
    - pos: this body's position as a 2-element array, [x, y]
    - vel: this body's velocity as a 2-element array, [vx, vy]
 
    Representation Invariants:
    - self.mass > 0
    - self.pos.shape == (2,)
    - self.vel.shape == (2,)
    """
    mass: float
    pos: np.ndarray
    vel: np.ndarray
 
    def __init__(self, mass: float, pos: np.ndarray, vel: np.ndarray) -> None:
        """Initialize a body with mass <mass>, position <pos>, and velocity <vel>.
 
        Preconditions:
        - mass > 0
        - pos.shape == (2,)
        - vel.shape == (2,)
        """
        self.mass = mass
        self.pos = pos
        self.vel = vel
