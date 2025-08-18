## File Structure

```
auto_car/
├── perception/        # Contains scripts that handle data collecting and processing
├── ├── sensors/
├── ├── ├── camera_node.py
├── ├── ├── encoder_node.py
├── ├── localization/
├── ├── ├── localizer.py
├── ├── ├── encoder_odometry.py
├── ├── mapping/
├── ├── ├── map_handler.py
├── ├── object_detection/
├── ├── ├── object_detection.py
├── planning/          # Handles path planning and traffic rules appliances
├── ├── route_generation.py
├── ├── obstacle_avoidance.py
├── ├── traffic_rules.py
├── ├── decision_maker.py
├── control/           # Handles controlling messages
├── ├── manual_control.py
├── ├── speed_controller.py
├── ├── steering_controller.py
├── ├── trajectory_follower.py
├── ├── vehicle_dynamics.py
├── firmware/          # Where all Arduino scripts reside
├── setup.sh           # Bash script to set up the environment and install dependencies
├── README.md          # Project documentation and usage instructions
```

## Getting Started

To set up the project environment and install all necessary dependencies, run the following command from the `auto_car` directory:

```bash
bash setup.sh
```

This will install required packages and prepare your workspace.

## Usage

- Run main.py for starting the whole system
- You will be asked to choose from auto mode or manual mode
- In manual mode, a separate screen will be created to show the camera feeds, and the terminal wiill be cleared for car control
    - On the terminal end, type w, a, s, d, x, c for full car control
    - On the camera end, type g to snap frames. The images will be stored for later use such as YOLO training
    - Both ends can accept key q for program termination