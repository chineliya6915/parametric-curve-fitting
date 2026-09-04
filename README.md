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

x = t cos(θ) - exp(M|t|) sin(0.3t) sin(θ) + X

y = 42 + t sin(θ) + exp(M|t|) sin(0.3t) cos(θ)

Since the given range of t is:

6 < t < 60

we have |t| = t.

Therefore, the equations can be written as:

x = t cos(θ) - exp(Mt) sin(0.3t) sin(θ) + X

y = 42 + t sin(θ) + exp(Mt) sin(0.3t) cos(θ)

---

## 3. Parameter Constraints

The assignment provides the following ranges:

- 0° < θ < 50°
- -0.05 < M < 0.05
- 0 < X < 100
- 6 < t < 60

---

## 4. Dataset

The input dataset is:

`data/xy_data.csv`

The dataset contains 1500 observed (x, y) coordinate pairs.

The values of t corresponding to the observed points are not directly
provided and therefore need to be recovered during parameter estimation.

---

## 5. Mathematical Approach

The curve can be viewed as a rotated combination of two components.

For a candidate value of θ, the parameter t can be recovered by
projecting the coordinates onto the direction defined by θ:

t = (x - X) cos(θ) + (y - 42) sin(θ)

The perpendicular component is:

b = -(x - X) sin(θ) + (y - 42) cos(θ)

From the original parametric equation:

b = exp(Mt) sin(0.3t)

Therefore, for each candidate set of parameters (θ, M, X), the
difference between the observed perpendicular component and the
mathematical model can be calculated.

The residual is:

error = b - exp(Mt) sin(0.3t)

The objective function minimizes the mean squared residual:

Loss = (1/N) Σ error²

where N is the number of observed data points.

---

## 6. Optimization Method

Differential Evolution was used to search for the optimal values of
θ, M, and X.

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

`src/solve.py`

---

## 8. Estimated Parameters

The optimization produced:

| Parameter | Estimated Value |
|-----------|-----------------|
| θ | 29.99997293° |
| M | 0.0299999969 |
| X | 54.9999982128 |

These values are effectively:

θ = 30°

M = 0.03

X = 55

---

## 9. Optimization Result

The final objective-function loss was:

1.215331957292 × 10⁻¹¹

The very small loss indicates that the estimated parameters provide a
very close fit to the supplied data.

---

## 10. Final Parametric Curve

Using the clean parameter values:

θ = 30°

M = 0.03

X = 55

the resulting curve is:

x = t cos(30°) - exp(0.03t) sin(0.3t) sin(30°) + 55

y = 42 + t sin(30°) + exp(0.03t) sin(0.3t) cos(30°)

for:

6 < t < 60

---

## 11. Visualization

The generated visualization compares:

- The observed points from `xy_data.csv`
- The fitted parametric curve

The result is saved as:

`results/curve_fit.png`

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
└── requirements.txt

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

L1 = Σ (|x_observed - x_predicted| + |y_observed - y_predicted|)

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