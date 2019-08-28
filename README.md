C4D-animSampler
---------------

This script is to sample cinema 4d  animation to a lower framerate. The aim  is to emulate scenes where objects are animated to different frame rate.     I developed it for a short film where I wanted to reproduce the impression of traditional clay motion,

This script is to sample cinema 4d  animation to a lower framerate. The aim  is to emulate scenes where objects are animated to different frame rate.

I developed it for a short film where I wanted to reproduce the impression of traditional clay motion, usually animated at 12 fps, while maintaining camera movement to a smoother 24 fps.

you need to define :
- max fps : the maximum framerate an object will be animated to.
- object local fps: the frame rate of the object you want to animate.
- object local fps needs to be a multiple of max fps.
- The scene framerate shall be equal to max fps. 

to use the script :

- temporally modify the scene fps to object local fps.
- craft the animation of your object.
- change the frame rate of the scene back to max fps.
- Select the object
- Run the script, it will sample the animation of the selected object and all of its children object.

timeline of an object before sampling : 
![Alt text](etc/original.png?raw=true "timeline_orignal")

and after sampling : 
![Alt text](etc/sampled.png?raw=true "timeline_sampled")