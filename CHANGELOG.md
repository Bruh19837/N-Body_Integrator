## [2.0.0] - 2026-09-22

### Added
- Initial N-body Gravitational Simulation
- Integration Method Involves Leapfrog Integration Method
- Direct Pairwise Force Calculation Between All Bodies
- Outputs Graph Plotting Trajectory Of Bodies At The End Of Simulation Time

### Known limitations
- Global Error Is O(t^2) With Per Step Error Being O(t^3)
- Fails Handling Collisions
- Time Complexity Of Calculations is O(n²)