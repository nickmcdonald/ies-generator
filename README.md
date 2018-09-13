
# Easy IES

[![donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8SFL6DVAVMJ8Q)

A free and open source program that generates custom IES files

These files can be used in game engines like unreal and unity, or other rendering applications to greatly increase the quality of your lighting.
IES files are great, and you can find thousands of them online, but it can be very hard to find one that fits your needs. Other programs
for creating them are either overly complicated paid products, or not very usable.

![IES Comparison](https://github.com/nickmcdonald/ies-generator/blob/master/img/Compare.PNG?raw=true "Compare")

# Interface

This program allows you to create custom IES files using a simple, yet powerful user interface.

![interface](https://github.com/nickmcdonald/ies-generator/blob/master/img/gui.png?raw=true "Interface")

You can add a variety of modifiers and operations that are applied in order to alter the lights intensity at each point. Currently, only symmetrical
lights are supported, but I have plans to add modifiers that are asymmetrical so that you could create effects such as elliptical or rectangular spotlight
or simulate elliptical or rectangular lamp shades.

## Modifiers

You can think of modifiers like a "layer" in photoshop. Modifiers define the points in the IES grid that are to be affected, and operations are added
to the modifier to alter the intensity of those points on the grid. The modifiers are then mixed together in order (top to bottom) using the modifiers mix method.

### Full 360

This is the simplest modifier, it applies the operation to all points

### Angle Range

This modifier applies the operations to a given range of angles

## Operations

Operations are added to a modifier, and applies an effect every IES point specified by the modifier

### Adjust Intensity

Adjusts the intensity of every point by a percentage

### Interpolate

Interpolates between 2 intensity values using linear or smooth interpolation.

### Simple Curve

Similar to Interpolate, but adds a middle value and interpolates between the 3 values.

### Noise

Applies noise of a given scale and intensity

## Mix Methods

Each Modifier and Operation has its own mix method (default is Multiply) the mix method is a mathematical
operation that defines how this Modifier or Operation is applied.

![Example](https://github.com/nickmcdonald/ies-generator/blob/master/img/iesgenExample.png?raw=true "Examples")

# Contribution

Contribution is welcome, feel free to make a pull request or contact me with your ideas.

If you like Easy IES and would like to support its development, the best way is by a donation. I don't have a lot of time to dedicate
to this project because my financial situation is less than ideal. Even a small donation would be greatly appreciated. But rent is expensive.

[![donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8SFL6DVAVMJ8Q)
