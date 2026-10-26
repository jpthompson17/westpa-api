# `westpa-api-0.9`

A simplified Python API for running weighted ensemble (WE) simulations in 
the [WESTPA](https://westpa.github.io/westpa/) framework.

> [!WARNING]
> This package is available as a pre-release to gather user feedback
> on features proposed for inclusion in a future, stable/production
> release of WESTPA. 
> The Python API and HDF5 file structure defined by ``westpa-api``
> are currently in flux and subject to change without notice between
> pre-release versions.
>
> The [`westpa`](https://github.com/westpa/westpa) base package,
> which provides the stable reference implementation of WESTPA, 
> should be used in production environments.


## Installation

```shell
git clone https://github.com/jpthompson17/westpa-api.git
cd westpa-api
python -m pip install .
```

## Usage

The example below is an adaptation of the 
[`basic_nacl_gmx`](https://github.com/westpa/westpa_tutorials/tree/main/additional_tutorials/basic_nacl_gmx)
tutorial. It requires
[GROMACS](https://www.gromacs.org/)
for running molecular dynamics and 
[MDTraj](https://www.mdtraj.org/) for computing the progress coordinate.
The current working directory (the simulation root folder) is assumed
to contain the following initial files:

- `conf.gro` &mdash; Initial configuration
- `topol.top` &mdash; Molecular topology
- `grompp.mdp` &mdash; MD options for each segment
  (`ld-seed` is dynamically overridden)


```python
import os.path
import concurrent.futures
import mdtraj as md
import westpa_api as we

def get_distance(obj):
    atom_pair = [0, 1]
    if isinstance(obj, we.State):
        t = md.load(obj.file)
        return md.compute_distances(t, [atom_pair])[0]
    elif isinstance(obj, we.Segment):
        t = md.load([obj.initial_state.file, obj.final_state.file])
        return md.compute_distances(t, [atom_pair])
    
def is_bound(segment):
    return segment.pcoord[-1, 0] < 0.26

initial_state = we.State(file=os.path.abspath('conf.gro'))
    
sim = we.Simulation(
    datafile='west.h5',
    propagator=we.GROMACSPropagator('topol.top', 'grompp.mdp'),
    pcoord_calculator=get_distance,
    bin_mapper=we.RectilinearBinMapper([[
        0.0, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36, 0.38,
        0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9, 1.0,
        1.1, 1.2, 1.3, 1.4, 1.5, float('inf')]]),
    bin_target_counts=2,
    source=we.Source(initial_state),
    sink=we.Sink(indicator=is_bound, label='bound'),
    executor=concurrent.futures.ProcessPoolExecutor(),
)

sim.initialize(initial_state)
sim.run(2)

```

## Contributing

If you encounter a bug or have a request or idea for a new feature,
please
[create an issue](https://github.com/jpthompson17/westpa-api/issues/new).
