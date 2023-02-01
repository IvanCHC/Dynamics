from dataclasses import dataclass, field
from typing import Literal


COORDINATE_SYSTEM = Literal["cartesian_1D", "cartesian_2D", "cartesian_3D",
                            "polar", "cylindrical", "spherical"]


class Simulation:

    def __init__(self, coordinate_system: COORDINATE_SYSTEM,
                 model, solver) -> None:
        self.coodinate_system: str = coordinate_system
        self.model = model
        self.solver = solver

        self._validated: bool = False

    def run(self) -> None:
        pass

    def _validate_simulation(self) -> None:
        pass


@dataclass(frozen=True, slots=True)
class SimulationParameters:
    time_step: float = field(default_factory=float)
    time_start: float = field(default_factory=float)
    time_end: float = field(default_factory=float)
    n_iter: int = field(init=False, default_factory=int)

    def __post_init__(self) -> None:
        object.__setattr__(self, 'n_iter', 
            int((self.time_end - self.time_start) / self.time_step))



from typing import List, Tuple

from sympy.physics.vector import dynamicsymbols

MOTION_TYPE = Literal["translational", "rotational"]
# SOLUTION_COLUMS: List[str] = ["displacement", "velocity", "acceleration", "time"]

class MotionData:

    def __init__(self, variable_name: str, motion_type: MOTION_TYPE,
                 displacement_initial: float = 0.0, 
                 velocity_initial: float = 0.0,
                 accelration_initial: float = 0.0,
                 time_initial: float = 0.0) -> None:
        self.variable_name = variable_name
        self.motion_type = motion_type

        self.symbolic_displacement = dynamicsymbols(variable_name)
        self.symbolic_velocity = dynamicsymbols(variable_name, 1)
        self.symbolic_acceleration = dynamicsymbols(variable_name, 2)

        self.displacement: List[float] = [displacement_initial]
        self.velocity: List[float] = [velocity_initial]
        self.acceration: List[float] = [accelration_initial]
        self.time: List[float] = [time_initial]

        self.initial_conditions: Tuple[float] = (
            displacement_initial, velocity_initial, accelration_initial, time_initial
        )

    def reset(self) -> None:
        self.displacement, self.velocity, self.acceration, self.time = \
            ([value] for value in self.initial_conditions)

    def append(self, displacement: float, velocity: float,
               acceleration: float, time: float) -> None:
        self.displacement.append(displacement)
        self.velocity.append(velocity)
        self.acceration.append(acceleration)
        self.time.append(time)



from abc import ABC

COMPONENT_TYPE = Literal["support", "body", "connection"]

class Component(ABC):
    component_type: COMPONENT_TYPE

    def __init__(self, name: str) -> None:
        self.name = name

class Support(Component):
    component_type: COMPONENT_TYPE = "support"

class Body(Component):
    component_type: COMPONENT_TYPE = "body"

class Connection(Component):
    component_type: COMPONENT_TYPE = "connection"

class FixPoint(Support):
    def __init__(self, name: str) -> None:
        super().__init__(name)

class PointMass(Body):
    def __init__(self, name: str, mass: float, drag_coefficient: float) -> None:
        super().__init__(name)
        self.mass = mass
        self.drag_coefficient = drag_coefficient

class RigidRod(Connection):
    def __init__(self, name: str, length: float) -> None:
        super().__init__(name)
        self.length = length

class Spring(Connection):
    def __init__(self, name: str, natural_length: float, damping_coefficient: float) -> None:
        super().__init__(name)
        self.natural_length = natural_length
        self.damping_coefficient = damping_coefficient



from dataclasses import dataclass

@dataclass
class Asset:
    name: str
    variable_name: str
    asset_type: 'Component'
    motion: List['MotionData']
    connections: List['Component']



from typing import Any, Optional

from scipy.constants import g 

def construct_kinectic_energy(mass: float, velocity: Optional[Any] = None) -> Any:
    if velocity is None:
        return 0
    else:
        return 0.5 * mass * velocity ** 2

def construct_gravitational_potential_energy(mass: float, displacement: Optional[Any] = None,
                                             gravity_acceleration: float = g) -> Any:
    if displacement is None:
        return 0
    else:
        return mass * displacement * gravity_acceleration

def construct_elastic_potential_energy(stiffness: float, displacement: Optional[Any] = None) -> Any:
    if displacement is None:
        return 0
    else:
        return 0.5 * stiffness * displacement ** 2

def construct_dissipated_energy(coefficient: float, velocity: Optional[Any] = None) -> Any:
    if velocity is None:
        return 0
    else:
        return 0.5 * coefficient * velocity ** 2