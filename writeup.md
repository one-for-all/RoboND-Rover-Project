## Project: Search and Sample Return
---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[rock_image]: ./calibration_images/example_rock1.jpg
[color_classificiation]: ./misc/color_classification.png

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.

You're reading it!

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

* In [Rover_Project_Test_Notebook.ipynb](./code/Rover_Project_Test_Notebook.ipynb), the implementation for rock and obstacle color selection in written in `color_thresh()`.    
* The range of rgb values for rock is hardcoded, (by inspection of color values of rocks in sample images). The rocks are where rgb values fall in this range.    
* The obstacles are where neither covered by ground nor rocks.

Original image:    
![original rock image][rock_image]

Identification:    
![object identification by color][color_classificiation]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
The camera image is processed in the following way:
1. The image is mapped from camera perspective to top-down perspective.
2. Ground, obstacles, and rocks are identified using color thresholding.
3. The coordinates are transformed from image coordinates to rover coordinates and then to world coordinates.
4. For worldmap, blue channel value is increased for each identification of ground, red for obstacle, and green for rock.
5. A mosaic image is created, consisting of original camera image, top-down view, worldmap overlayed with ground truth, and text indicating when rocks have been identified.

A example video output can be found at [output/test_mapping.mp4](./output/test_mapping.mp4).
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.
**Perception:**    
* The image processing in `perception_step()` is the same as explained above for `process_image()`, except that worldmap is updated only when `roll` and `pitch` values of the rover are < 1 to reduce incorrect updates due to distorted perspective transform.
* The ground coordinates is also transformed into polar coordinates in rover perspective for later decision making.

**Decision:**    
* The robot moves when there is enough space as suggested by the number of ground pixels perceived, and stops and turns when not enough space ahead.
* When a rock is located, the rover will move in the direction of the rock at a lower throttle, and stop when near it, in order to pick it up.
* Otherwise, the rover moves in the average angle of all ground pixels, with some gaussian noise added to help it get unstuck in some infinite loops, and to add some randomness to its path.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**For results reproduction:**
* Screen resolution: 1024 x 640  
* Graphic Quality: Good
* Frames per second: ~20

**Results:**
* The rover should be able to map 40% of the environment with 60% fidelity most of the time, sometimes much better with 60% of environment and 80% fidelity.
* When the rover has identified a rock, it would move in the rock's direction, and stop near it. However, sometimes the rover fails to pick the rock up.

**Pipeline:**    
In an infinite loop, the rover keeps doing the perception and decision step with techniques described above.

**Potential Improvements:**
* Tried to implement wall following in `decision_step()`. However, the naive way of using left most angle failed to give correct behavior, and I couldn't think of a feasible way of doing this. A potential improvement is to find some way to implement wall following, so that the rover might be able to map the environment more comprehensively.
* Another improvement is to keep track of the areas the rover has mapped and avoid spending time on these areas.
* The rover sometimes would get stuck by the obstacles on the road.

A example video of operation can be found at [autonomous_video/video.mp4](./autonomous_video/video.mp4)


