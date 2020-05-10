Mobile Robot learning to navigate trough a construction environment using range sensors while collecting boreholes in a efficient way.
The main objective is similar to the TSP, however, is extended by the possibility to cluster coordinates/boreholes.
A modified version of the Proximal Policy Optimization Implementation from stable-baselines is used.

Requirements:
-tensorflow 1.14
-pygame 1.9.6

The simulation is wrapped for usage as an OpenAI gym and uses a modified version of stable-baselines.
Install by changing into the main directory for installation of gym and into the stable-baselines-master directory for stable-baselines by using: pip install -e .