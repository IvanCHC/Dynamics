from dynamics.new.core import *

support_1 = Support('support_1')
spring_1 = Spring('spring_1', 10, 0)
mass_1 = PointMass('mass_1', 1, 0)

components = [support_1, spring_1, mass_1]
components = {c.name: c for c in components}

connections = {
    'spring_1': ['support_1', 'mass_1']
}

motions = {
    mass_1: [
        MotionData 
    ]
}

assets = {
    mass_1: {
        'name': mass_1.name,
        'variable_name': 'x',
        'motions': [
            {
                'subject': mass_1,
                'connection': spring_1,
                'object': support_1,
                'motion': 'translational'
            }
        ]
    }
}

print(assets)

energys = {
    mass_1: {
        'kinectic_energy': construct_kinectic_energy(mass_1.mass, )
    }
}