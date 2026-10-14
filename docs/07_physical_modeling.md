# Physical Modeling — Robot Arm 4R

**Phase:** 02 — Dynamic Simulation  
**Step:** 11 — Physical Properties & URDF Upgrade  
**Status:** URDF structural validation passed

---

## 1. Objective

Upgrade the robot's kinematic URDF to include
physical properties required for dynamic simulation.

The original kinematic model remains unchanged:

`models/arm_4r.urdf`

The physical model is stored separately:

`models/arm_4r_physics.urdf`

## 2. Kinematics vs Dynamics

Kinematics describes robot position and motion
without considering the forces that produce them.

Dynamics describes how forces, torques, mass,
inertia and gravity affect robot motion.

Basic rotational relationship:

$$
\tau = I\alpha
$$

Where:

- $\tau$: Torque (N·m)
- $I$: Moment of inertia (kg·m²)
- $\alpha$: Angular acceleration (rad/s²)

This equation describes a simplified fixed-axis
rotation, not the complete dynamics of a 4R robot.

## 3. Physical Properties in URDF

Each physical link contains:

### Visual

Defines the appearance of the robot.

### Collision

Defines geometry used for collision calculations.

### Inertial

Defines mass, center of mass and inertia tensor.

These elements are siblings within the `<link>` tag.

## 4. Moment of Inertia

Moment of inertia describes resistance to
angular acceleration around a specified axis.

For a uniform rectangular box:

$$
I_{xx}=\frac{m}{12}(W^2+H^2)
$$

$$
I_{yy}=\frac{m}{12}(L^2+H^2)
$$

$$
I_{zz}=\frac{m}{12}(L^2+W^2)
$$

For a uniform solid cylinder along the Z-axis:

$$
I_{xx}=I_{yy}=\frac{m}{12}(3r^2+h^2)
$$

$$
I_{zz}=\frac12mr^2
$$

All these values are calculated around
the center of mass.

## 5. Assumed Masses

| Link | Mass |
|---|---:|
| base_link | 0.20 kg |
| base_rotation | 0.15 kg |
| upper_arm | 0.10 kg |
| forearm | 0.08 kg |
| wrist | 0.05 kg |

Total modeled mass: 0.58 kg.

These masses are assumptions for simulation,
not measurements of physical hardware.

## 6. Tool Link

`tool_link` represents the end-effector reference
frame used by the FK and IK calculations.

It is connected to `wrist` by a fixed joint.

It does not add another degree of freedom.

## 7. World Frame

A new `world` link and fixed joint
`world_to_base` were added.

Purpose:
Represent a robot base anchored to the world.

Whether the simulator enforces this attachment
must be verified in Gazebo.

## 8. Validation

Command:

```bash
check_urdf models/arm_4r_physics.urdf
```

Result:

Successfully Parsed XML

Root link:

world → base_link → base_rotation
→ upper_arm → forearm → wrist → tool_link

Physical properties:

- 5 inertial blocks
- 5 collision blocks

Gazebo Classic version: 11.10.2

## 9. Current Limitations

- Masses are estimated.
- Inertia is based on simplified uniform solids.
- Servo mass distribution is not modeled separately.
- Self-collision has not been evaluated.
- Physical stability has not been tested.
- Joint actuators and controllers are not configured.

## 10. Next Step

Spawn the robot in Gazebo Classic.

Verify:
- Robot appears correctly.
- Base remains fixed.
- Gravity is active.
- No unexpected instability occurs.
