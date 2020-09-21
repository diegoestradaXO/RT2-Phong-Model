from lib import *
from sphere import Sphere, Material
from math import pi, tan

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
BG = color(107,156,245)


class Raytracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.background_color = BG
    self.scene = []
    self.clear()

  def clear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)


  def point(self, x, y, c = None):
    try:
      self.pixels[y][x] = c or self.current_color
    except:
      pass

  def cast_ray(self, orig, direction):
    material = self.scene_intersect(orig, direction)

    if material is None:
      return self.background_color
    else:
      return material.diffuse

  def scene_intersect(self, orig, direction):
    zbuffer = float('inf')

    material = None
    for obj in self.scene:
      intersect = obj.ray_intersect(orig, direction)
      if intersect is not None:
        if intersect.distance < zbuffer:  # infront of the zbuffer
          zbuffer = intersect.distance
          material = obj.material

    return material

  def render(self):
    fov = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * self.width/self.height
        j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
        direction = norm(V3(i, j, -1))
        self.pixels[y][x] = self.cast_ray(V3(0,0,0), direction)

#size
width = 400
height = 600

#materials
snowball = Material(diffuse=color(255,255,255)) #white
button = Material(diffuse=color(0,0,0)) #black
mouth= Material(diffuse=(color(128,128,128))) #grey i think
carrot = Material(diffuse=(color(255,166,0))) #orange


r = Raytracer(width,height)

#body
r.scene.append( Sphere(V3(0, -1.9, -10), 2.2, snowball) )
r.scene.append( Sphere(V3(0, 0.8,  -10), 1.6, snowball) )
r.scene.append( Sphere(V3(0, 3.3, -10), 1.1, snowball) )

#body buttons
r.scene.append( Sphere(V3(0, 1.0, -6), 0.2, button) )
r.scene.append( Sphere(V3(0, 0, -6), 0.3, button) )
r.scene.append( Sphere(V3(0, -1.4, -6), 0.5, button) )

#eyes
r.scene.append( Sphere(V3(0.40, 3.1, -8), 0.12, button) )
r.scene.append( Sphere(V3(-0.40, 3.1, -8), 0.12, button) )

#nose
r.scene.append( Sphere(V3(0, 2.83, -8), 0.24, carrot) )

#mouth
r.scene.append( Sphere(V3(0.43, 2.4, -8), 0.1, mouth) )
r.scene.append( Sphere(V3(0.15, 2.2, -8), 0.1, mouth) )
r.scene.append( Sphere(V3(-0.15, 2.2, -8), 0.1, mouth) )
r.scene.append( Sphere(V3(-0.43, 2.4, -8), 0.1, mouth) )

r.render()
r.write("out.bmp")