from random import randint

import pymunk
from anim import App

app = App()

b0 = app.space.static_body
body = pymunk.Body(mass=1, moment=10)
body.position = 100, 100
circle = pymunk.Circle(body, radius=20)
circle.elasticity = 0.99
joint = pymunk.constraints.PinJoint(b0, body, (200, 200))

body2 = pymunk.Body(mass=1, moment=10)
body2.position = 240, 340
circle2 = pymunk.Circle(body2, radius=20)
circle2.elasticity = 0.99
joint2 = pymunk.constraints.PinJoint(b0, body2, (240, 200))
app.space.add(body, circle, joint, body2, circle2, joint2)

app.run()
