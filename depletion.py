import math
import openmc
import openmc.deplete

fuel = openmc.Material(name="uo2")
fuel.add_element("U", 1, percent_type="ao", enrichment=4.25)
fuel.add_element("O", 2)
fuel.set_density("g/cc", 10.4)

clad = openmc.Material(name="clad")
clad.add_element("Zr", 1)
clad.set_density("g/cc", 6)

water = openmc.Material(name="water")
water.add_element("O", 1)
water.add_element("H", 2)
water.set_density("g/cc", 1.0)
water.add_s_alpha_beta("c_H_in_H2O")
materials = openmc.Materials([fuel, clad, water])

radii = [0.42, 0.45]

pin_surfaces = [openmc.ZCylinder(r=r) for r in radii]
pin_univ = openmc.model.pin(pin_surfaces, materials)


bound_box = openmc.rectangular_prism(1.24, 1.24, boundary_type="reflective")
root_cell = openmc.Cell(fill=pin_univ, region=bound_box)
geometry = openmc.Geometry([root_cell])

settings = openmc.Settings()
settings.particles = 1000
settings.inactive = 10
settings.batches = 50

fuel.volume = math.pi * radii[0] ** 2

chain = openmc.deplete.Chain.from_xml("./chain_simple.xml")

# create model object and run depletion
model = openmc.Model(geometry=geometry, settings=settings)
operator = openmc.deplete.CoupledOperator(model, "./chain_simple.xml")
power = 174
time_steps = [30]*6
integrator = openmc.deplete.PredictorIntegrator(operator, time_steps, power, timestep_units='d')
integrator.integrate()
