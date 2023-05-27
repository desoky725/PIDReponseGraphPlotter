import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.gridspec import GridSpec

# Setpoint and simulate PID response
setpoint = 1
simulationLoops = 100

def update_graph(val):
    # Get the updated values from the sliders
    kp = slider_kp.val
    ki = slider_ki.val
    kd = slider_kd.val
    

    time, output = pid_controller(setpoint, kp, ki, kd)
    
    # Update the graph with new data
    line.set_xdata(time)
    line.set_ydata(output)
    ax.relim()
    ax.autoscale_view()
    plt.draw()

def pid_controller(setpoint, kp, ki, kd):
    # PID controller parameters
    last_error = 0
    integral = 0
    
    # Simulation parameters
    time = []
    output = []
    current_output = 0  # Initial output
    
    # Simulation loop
    for t in range(0, simulationLoops):  # Simulate 100 time steps
        error = setpoint - current_output
        
        # Proportional term
        proportional = kp * error
        
        # Integral term
        integral += ki * error
        
        # Derivative term
        derivative = kd * (error - last_error)
        
        # PID output
        pid_output = proportional + integral + derivative
        
        # Update current output
        current_output += pid_output
        
        # Store time and output values
        time.append(t)
        output.append(current_output)
        
        # Update last error
        last_error = error
    
    return time, output

def close_graph(event):
    if event.key == 'escape':
        plt.close()

# Create a figure and grid layout
fig = plt.figure(num='PID Response Graph', figsize=(8, 6))  # Set the title of the GUI window and figure size
fig.canvas.mpl_connect('key_press_event', close_graph)  # Connect the key press event handler

grid = GridSpec(5, 1, height_ratios=[10, 1, 1, 1, 1])

# Create an axis for the graph
ax = fig.add_subplot(grid[0])   
line, = ax.plot([], [])
ax.set_xlabel('Time')
ax.set_ylabel('Output')
ax.set_title('PID Step Response')
ax.grid(True)

# Set y-axis to start from zero
ax.set_ylim([0, 1])

# Create sliders for kp, ki, and kd
axslider_kp = fig.add_subplot(grid[2])
axslider_ki = fig.add_subplot(grid[3])
axslider_kd = fig.add_subplot(grid[4])
slider_kp = Slider(axslider_kp, 'kp:', 0.0, 1.0, valinit=0.5)
slider_ki = Slider(axslider_ki, 'ki:', 0.0, 1.0, valinit=0.2)
slider_kd = Slider(axslider_kd, 'kd:', 0.0, 1.0, valinit=0.1)

# Add event handlers to the sliders
slider_kp.on_changed(update_graph)
slider_ki.on_changed(update_graph)
slider_kd.on_changed(update_graph)

# Setpoint and simulate initial PID response
setpoint = 1
kp = slider_kp.val
ki = slider_ki.val
kd = slider_kd.val
time, output = pid_controller(setpoint, kp, ki, kd)
line.set_xdata(time)
line.set_ydata(output)

plt.tight_layout()
plt.subplots_adjust(hspace=0.0, right=0.925) # Add spacing between subplots

# Set y-axis to start from zero
ax.set_ylim([0, setpoint*1.5])
# Set x-axis to start from 0 to number of simulation loops
ax.set_xlim([0, simulationLoops])

plt.show()
