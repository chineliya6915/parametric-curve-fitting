# Parametric Curve Parameter Estimation

## 1. Problem Statement

The objective of this assignment is to estimate the unknown parameters
θ, M, and X from a given parametric equation of a curve.

The provided dataset `xy_data.csv` contains points that lie on the
unknown curve.

The estimated parameters should satisfy the given parameter constraints
and produce a curve that closely matches the provided data points.

---

## 2. Given Parametric Equation

The curve is defined by:

```text
x = t cos(θ) - exp(M|t|) sin(0.3t) sin(θ) + X

y = 42 + t sin(θ) + exp(M|t|) sin(0.3t) cos(θ)
```

Since the given range of `t` is:

```text
6 < t < 60
```

we have `|t| = t`.

Therefore, the equations can be written as:

```text
x = t cos(θ) - exp(Mt) sin(0.3t) sin(θ) + X

y = 42 + t sin(θ) + exp(Mt) sin(0.3t) cos(θ)
```

---

## 3. Parameter Constraints

The assignment provides the following parameter ranges:

- `0° < θ < 50°`
- `-0.05 < M < 0.05`
- `0 < X < 100`
- `6 < t < 60`

---

## 4. Dataset

The input dataset is:

```text
data/xy_data.csv
```

The dataset contains 1500 observed `(x, y)` coordinate pairs.

The values of `t` corresponding to the observed points are not directly
provided and therefore need to be recovered during parameter estimation.

---

## 5. Mathematical Approach

The curve can be viewed as a rotated combination of two components.

For a candidate value of `θ`, the parameter `t` can be recovered by
projecting the coordinates onto the direction defined by `θ`:

```text
t = (x - X) cos(θ) + (y - 42) sin(θ)
```

The perpendicular component is:

```text
b = -(x - X) sin(θ) + (y - 42) cos(θ)
```

From the original parametric equation:

```text
b = exp(Mt) sin(0.3t)
```

Therefore, for each candidate set of parameters `(θ, M, X)`, the
difference between the observed perpendicular component and the
mathematical model can be calculated.

The residual is:

```text
error = b - exp(Mt) sin(0.3t)
```

The objective function minimizes the mean squared residual:

```text
Loss = (1/N) Σ error²
```

where `N` is the number of observed data points.

---

## 6. Optimization Method

Differential Evolution was used to search for the optimal values of
`θ`, `M`, and `X`.

The optimization was performed within the parameter ranges specified
in the assignment.

The optimization process evaluates different parameter combinations
and selects the combination producing the minimum objective-function
value.

This approach is useful because the equation contains nonlinear
components such as exponential and trigonometric functions.

---

## 7. Implementation

The implementation was developed in Python using:

- NumPy
- Pandas
- SciPy
- Matplotlib

The main implementation is available in:

```text
src/solve.py
```

---

## 8. Estimated Parameters

The optimization produced the following values:

| Parameter | Estimated Value |
|-----------|----------------:|
| θ         | 29.99997293°    |
| M         | 0.0299999969    |
| X         | 54.9999982128   |

These values are effectively:

```text
θ = 30°
M = 0.03
X = 55
```

---

## 9. Optimization Result

The final objective-function loss was:

```text
1.215331957292e-11
```

The very small loss indicates that the estimated parameters provide a
very close fit to the supplied data.

---

## 10. Final Parametric Curve

Using the clean parameter values:

```text
θ = 30°
M = 0.03
X = 55
```

the resulting curve is:

```text
x = t cos(30°) - exp(0.03t) sin(0.3t) sin(30°) + 55

y = 42 + t sin(30°) + exp(0.03t) sin(0.3t) cos(30°)
```

for:

```text
6 < t < 60
```

---

## 11. Visualization

The generated visualization compares:

- The observed points from `xy_data.csv`
- The fitted parametric curve

The result is saved as:

```text
results/curve_fit.png
```

The observed points and fitted curve closely overlap, demonstrating
the quality of the estimated parameters.

---

## 12. Project Structure

```text
parametric_curve_fitting/
│
├── data/
│   └── xy_data.csv
│
├── results/
│   └── curve_fit.png
│
├── src/
│   └── solve.py
│
├── README.md
│
└── requirements.txt
```

---

## 13. L1 Distance Validation

The fitted curve is further evaluated using the L1 distance between
uniformly sampled observed and predicted curve points.

The observed data points are first assigned a parameter `t` using the
estimated parameters. The points are then sorted according to `t` and
interpolated onto a uniform grid of 1500 points.

The predicted curve is generated using the same uniformly sampled
values of `t`.

The L1 distance is calculated as:

```text
L1 = Σ (|x_observed - x_predicted| + |y_observed - y_predicted|)
```

The obtained validation results are:

| Metric | Value |
|--------|------:|
| L1 Distance | 3.504977686290e-01 |
| Mean L1 Distance | 2.336651790860e-04 |

The small mean L1 distance indicates that the fitted curve closely
matches the observed data.

---

## 14. How to Run

### Install Dependencies

Open a terminal in the project root directory and run:

```bash
pip install -r requirements.txt
```

### Run the Program

Navigate to the `src` directory:

```bash
cd src
```

Then run:

```bash
python solve.py
```

The program will:

1. Load the dataset from `data/xy_data.csv`.
2. Optimize the parameters `θ`, `M`, and `X`.
3. Display the optimized parameter values.
4. Calculate the optimization loss.
5. Generate the fitted parametric curve.
6. Calculate the L1 validation distance.
7. Save the fitted curve visualization to `results/curve_fit.png`.

---

## 15. Expected Output

The optimization should produce parameter values close to:

```text
Optimization completed!
--------------------------------
Theta = 29.99997293 degrees
M     = 0.0299999969
X     = 54.9999982128
Loss  = 1.215331957292e-11
```

The validation should produce values close to:

```text
Validation
--------------------------------
L1 distance       = 3.504977686290e-01
Mean L1 distance  = 2.336651790860e-04
```

Small differences may occur depending on the environment or numerical
optimization behavior.

---

## 16. Conclusion

The unknown parameters of the given parametric curve were successfully
estimated using Differential Evolution.

The estimated parameters are approximately:

```text
θ = 30°
M = 0.03
X = 55
```

The extremely small optimization loss and low mean L1 distance indicate
that the fitted curve closely matches the observed dataset.

The complete implementation, dataset, validation result, and generated
visualization are included in this repository.
