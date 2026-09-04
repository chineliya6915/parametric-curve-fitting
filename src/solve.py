import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution


# --------------------------------------------------
# 1. Load the dataset
# --------------------------------------------------

df = pd.read_csv("../data/xy_data.csv")

x = df["x"].values
y = df["y"].values

print(f"Loaded {len(df)} data points.")


# --------------------------------------------------
# 2. Define the objective function
# --------------------------------------------------

def objective(params):

    theta, M, X = params

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # Recover t from the observed x and y coordinates
    t = (
        (x - X) * cos_theta
        + (y - 42) * sin_theta
    )

    # Perpendicular component
    b = (
        -(x - X) * sin_theta
        + (y - 42) * cos_theta
    )

    # Model prediction
    predicted_b = (
        np.exp(M * t)
        * np.sin(0.3 * t)
    )

    # Penalize solutions outside the required t range
    if np.any(t <= 6) or np.any(t >= 60):
        return 1e6

    # Residual
    error = b - predicted_b

    return np.mean(error ** 2)


# --------------------------------------------------
# 3. Parameter ranges
# --------------------------------------------------

bounds = [
    (np.deg2rad(0.0001), np.deg2rad(49.9999)),  # theta
    (-0.049999, 0.049999),                       # M
    (0.0001, 99.9999)                            # X
]


# --------------------------------------------------
# 4. Find the best parameters
# --------------------------------------------------

print("Starting optimization...")

result = differential_evolution(
    objective,
    bounds,
    seed=42,
    tol=1e-10,
    polish=True
)


# --------------------------------------------------
# 5. Extract the solution
# --------------------------------------------------

theta, M, X = result.x

theta_degrees = np.rad2deg(theta)


print("\nOptimization completed!")
print("--------------------------------")
print(f"Theta = {theta_degrees:.8f} degrees")
print(f"M     = {M:.10f}")
print(f"X     = {X:.10f}")
print(f"Loss  = {result.fun:.12e}")


# --------------------------------------------------
# 6. Generate the fitted curve
# --------------------------------------------------

t_curve = np.linspace(6.0001, 59.9999, 2000)

x_curve = (
    t_curve * np.cos(theta)
    - np.exp(M * t_curve)
    * np.sin(0.3 * t_curve)
    * np.sin(theta)
    + X
)

y_curve = (
    42
    + t_curve * np.sin(theta)
    + np.exp(M * t_curve)
    * np.sin(0.3 * t_curve)
    * np.cos(theta)
)


# --------------------------------------------------
# 7. Plot the original points and fitted curve
# --------------------------------------------------

plt.figure(figsize=(10, 7))

plt.scatter(
    x,
    y,
    s=10,
    label="Observed data"
)

plt.plot(
    x_curve,
    y_curve,
    linewidth=2,
    label="Fitted parametric curve"
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Parametric Curve Fitting")

plt.legend()
plt.grid(True)

plt.savefig(
    "../results/curve_fit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# --------------------------------------------------
# 8. L1 distance validation
# --------------------------------------------------

# Recover t values corresponding to the observed points
t_observed = (
    (x - X) * np.cos(theta)
    + (y - 42) * np.sin(theta)
)

# Sort observed points according to t
sort_idx = np.argsort(t_observed)

t_sorted = t_observed[sort_idx]
x_sorted = x[sort_idx]
y_sorted = y[sort_idx]

# Uniformly sample t over the valid range
t_uniform = np.linspace(
    6.0001,
    59.9999,
    1500
)

# Interpolate observed data onto the uniform t grid
x_observed_uniform = np.interp(
    t_uniform,
    t_sorted,
    x_sorted
)

y_observed_uniform = np.interp(
    t_uniform,
    t_sorted,
    y_sorted
)

# Generate predicted points on the same uniform t grid
x_predicted_uniform = (
    t_uniform * np.cos(theta)
    - np.exp(M * t_uniform)
    * np.sin(0.3 * t_uniform)
    * np.sin(theta)
    + X
)

y_predicted_uniform = (
    42
    + t_uniform * np.sin(theta)
    + np.exp(M * t_uniform)
    * np.sin(0.3 * t_uniform)
    * np.cos(theta)
)

# Calculate L1 distance
l1_distance = np.sum(
    np.abs(x_observed_uniform - x_predicted_uniform)
    + np.abs(y_observed_uniform - y_predicted_uniform)
)

mean_l1_distance = l1_distance / len(t_uniform)

print("\nValidation")
print("--------------------------------")
print(f"L1 distance       = {l1_distance:.12e}")
print(f"Mean L1 distance  = {mean_l1_distance:.12e}")


# --------------------------------------------------
# 9. Plot the original points and fitted curve
# --------------------------------------------------

plt.figure(figsize=(10, 7))

plt.scatter(
    x,
    y,
    s=10,
    label="Observed data"
)

plt.plot(
    x_curve,
    y_curve,
    linewidth=2,
    label="Fitted parametric curve"
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Parametric Curve Fitting")

plt.legend()
plt.grid(True)

plt.savefig(
    "../results/curve_fit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()