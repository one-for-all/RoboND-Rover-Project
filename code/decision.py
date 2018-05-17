import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def path_filtering(nav_dists, nav_angles):
    # Remove the winding path ahead
    # To help with computing the drivable angle
    # Note: Not used
    # Failed to implement efficiently/correctly
    sort_indices = nav_dists.argsort()
    sorted_dists = nav_dists[sort_indices]
    sorted_angles = nav_angles[sort_indices]
    filtered_dists = []
    filtered_angles = []
    for dist, angle in zip(sorted_dists, sorted_angles):
        if dist < 10:
            filtered_dists.append(dist)
            filtered_angles.append(angle)
        else:
            for i_dist, i_angle in zip(filtered_dists, filtered_angles):
                if np.abs(i_angle-angle) < 0.01 and i_dist < dist:
                    filtered_dists.append(dist)
                    filtered_angles.append(angle)
                    break
    return np.array(filtered_dists), np.array(filtered_angles)


def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:
                if Rover.rock_angles is not None:
                    Rover.steer = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15)
                    if Rover.vel < Rover.max_vel:
                        # Set throttle value to half throttle setting
                        Rover.throttle = .5*Rover.throttle_set
                    else:  # Else coast
                        Rover.throttle = 0
                    print("rock distance: {:.3f}".format(np.mean(
                        Rover.rock_dists)))
                    if np.mean(Rover.rock_dists) < 20:
                        Rover.throttle = 0
                        Rover.brake = Rover.brake_set
                        Rover.mode = 'stop'
                    Rover.brake = 0
                else:
                    # If mode is forward, navigable terrain looks good
                    # and velocity is below max, then throttle
                    if Rover.vel < Rover.max_vel:
                        # Set throttle value to throttle setting
                        Rover.throttle = Rover.throttle_set
                    else:  # Else coast
                        Rover.throttle = 0
                    angles = Rover.nav_angles * 180/np.pi
                    mean_angle = np.mean(angles)
                    Rover.steer = np.clip(mean_angle, -15, 15) + \
                                  np.random.normal(scale=2)
                    Rover.brake = 0
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

