# ScaraRobot
This project delves into the design and development of a teleoperation system for
a modified SCARA robot utilizing an intelligence-augmented virtual environment
for effective control. Phase I of the project involved designing and fabricating the
mechanical hardware, which featured an offset between its first and second joints,
distinguishing it from traditional SCARA robots. Phase II, covered in this thesis,
focused on deploying a self-determining intelligent control system to maneuver the
SCARA robot on a planar surface for picking and placing ICs.
The CAD model was designed in SolidWorks and environment simulation was performed in Coppeliasim where trajectory planning/programming was performed in
order to test the mathematical model for the control system design parameters.
Further, with the help of image processing in Python, the feedback loop sensors
were utilized for manipulation of objects on a planar surface. The Master-Slave
control system architecture has been developed, deployed and tested with the
fabricated structure of the SCARA robot where Modbus communication protocol is employed between master and slaves in order to control respective joints
synchronous to the pre-defined trajectory. The planar coordinates determined by
image processing to pick and place the object in the CoppeliaSim virtual environment were used to analyze the path and calculate the joint angles which were
then sent to the master controller via serial port for slave operations, effectively
imitating the trajectory simulated in the virtual environment.





https://github.com/user-attachments/assets/46454cf5-2870-4927-8826-12d7bb9ca14a





https://github.com/user-attachments/assets/3130911c-cec2-433c-891a-9895e9ff93b3




https://github.com/user-attachments/assets/8289dabe-d102-4994-baae-1a3d20c455d6

