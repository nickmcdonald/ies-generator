
# Easy IES

[![donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8SFL6DVAVMJ8Q)

A free and open source program that you can use to create custom IES files

These files can be used in game engines like unreal and unity, or other rendering applications to greatly increase the quality of your lighting.
IES files are great, and you can find thousands of them online, but it can be very hard to find one that fits your needs. Other programs
for creating them are either overly complicated paid products, or not very usable.

![IES Comparison](https://github.com/nickmcdonald/ies-generator/blob/master/img/Compare.PNG?raw=true "Compare")

# Interface

This program allows you to create custom IES files using a simple, yet powerful user interface.

![interface](https://github.com/nickmcdonald/ies-generator/blob/master/img/gui.png?raw=true "Interface")

## Layers

Layers are used to organize your project and to select which angles of the light to modify. The layers are then mixed together in order (top to bottom) using the layers mix method.

### Full 360

This is the simplest layer, it applies the operation to all points

### Angle Range

This layer applies the operations to a given range of angles

## Operations

Operations are added to a layer, and applies an effect to the light

### Adjust Intensity

Adjusts the intensity of every point by a percentage

### Interpolate

Blends between 2 intensity values

### Simple Curve

Similar to Interpolate, but adds a middle value and blends between the 3 values

### Noise

Applies noise of a given scale and intensity

## Mix Methods

Each Layer and Operation has its own mix method the mix method is the mathematical
operation that defines how this Layer or Operation blends with the next

![Example](https://github.com/nickmcdonald/ies-generator/blob/master/img/iesgenExample.png?raw=true "Examples")

# Contribution

Contribution is welcome, feel free to make a pull request or contact me with your ideas.

If you like Easy IES and would like to support its development, the best way is by a donation.

[![donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8SFL6DVAVMJ8Q)
