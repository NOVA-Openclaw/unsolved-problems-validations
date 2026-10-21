import numpy as np
import scipy.integrate as integrate

def verify_scaling(L):
    epsilon = np.exp(-L)
    
    # 1. Analytical check for L^2 norm of unnormalized profile on annulus [epsilon, 1]
    # Int_{epsilon}^{1} r * (cos(theta) / (2*pi*r))^2 d_theta d_r
    # = (1 / (4 * pi^2)) * Int_{0}^{2*pi} cos^2(theta) d_theta * Int_{epsilon}^{1} 1/r d_r
    # = (1 / (4 * pi^2)) * pi * ln(1/epsilon) = (1 / (4*pi)) * L
    analytical_L2_sq = L / (4 * np.pi)
    
    # Numerical integration check for L^2 norm
    # f_L2(r, theta) = r * (cos(theta) / (2*pi*r))^2 = cos^2(theta) / (4 * pi^2 * r)
    f_L2 = lambda theta, r: np.cos(theta)**2 / (4 * np.pi**2 * r)
    numerical_L2_sq, _ = integrate.dblquad(f_L2, epsilon, 1, lambda r: 0, lambda r: 2*np.pi)
    
    # 2. Analytical check for L^1 norm of unnormalized profile
    # Int_{epsilon}^{1} r * |cos(theta) / (2*pi*r)| d_theta d_r
    # = (1 / (2*pi)) * Int_{0}^{2*pi} |cos(theta)| d_theta * Int_{epsilon}^{1} 1 d_r
    # = (1 / (2*pi)) * 4 * (1 - epsilon) = (2 / pi) * (1 - epsilon)
    analytical_L1 = (2.0 / np.pi) * (1.0 - epsilon)
    
    # Numerical integration check for L^1 norm
    f_L1 = lambda theta, r: np.abs(np.cos(theta)) / (2 * np.pi)
    numerical_L1, _ = integrate.dblquad(f_L1, epsilon, 1, lambda r: 0, lambda r: 2*np.pi)
    
    # 3. Normalized Profile calculations (psi_L)
    # A_epsilon = sqrt(numerical_L2_sq)
    A_epsilon = np.sqrt(numerical_L2_sq)
    
    # Normalized L^1 norm
    normalized_L1 = numerical_L1 / A_epsilon
    analytical_normalized_L1 = ((2.0 / np.pi) * (1.0 - epsilon)) / np.sqrt(L / (4 * np.pi))
    
    # 4. Gradient check (H^1 seminorm) of unnormalized profile h_epsilon
    # h_epsilon = (cos(theta)/(2*pi*r), -sin(theta)/(2*pi*r)) in some coordinate, but let's look at grad h_epsilon.
    # In Cartesian coordinates, h_epsilon = (x / (2*pi*(x^2+y^2)), y / (2*pi*(x^2+y^2)))? No, dipole.
    # Dipole is h_epsilon = ( (x^2 - y^2) / (2*pi*(x^2+y^2)^2), 2xy / (2*pi*(x^2+y^2)^2) )
    # Let's check |h_epsilon|^2 = 1 / (4 * pi^2 * (x^2+y^2)) = 1 / (4 * pi^2 * r^2). Yes, |h_epsilon| = 1/(2*pi*r).
    # The gradient magnitude |grad h_epsilon|^2 = 1 / (4 * pi^2 * r^4).
    # Let's verify the L^2 norm of the gradient of the unnormalized profile over [epsilon, 1]:
    # Int_{epsilon}^{1} r * (1 / (4 * pi^2 * r^4)) d_theta d_r = (2*pi / (4*pi^2)) * Int_{epsilon}^{1} r^{-3} d_r
    # = (1 / (2*pi)) * [-1/(2*r^2)]_{epsilon}^{1} = (1 / (4*pi)) * (1/epsilon^2 - 1)
    # Thus, gradient L^2 norm of normalized profile psi_L is:
    # ||grad psi_L||_L2^2 = (1 / A_epsilon^2) * ||grad h_epsilon||_L2^2
    # = (1 / (L / (4*pi))) * (1 / (4*pi)) * (1/epsilon^2 - 1) = (1/L) * (1/epsilon^2 - 1) = (e^(2L) - 1) / L
    # Therefore, ||grad psi_L||_L2 = sqrt( (e^(2L) - 1) / L )
    analytical_grad_L2 = np.sqrt((np.exp(2*L) - 1.0) / L)
    
    return {
        "L": L,
        "epsilon": epsilon,
        "L2_sq_analytical": analytical_L2_sq,
        "L2_sq_numerical": numerical_L2_sq,
        "L1_analytical": analytical_L1,
        "L1_numerical": numerical_L1,
        "psi_L_L1_analytical": analytical_normalized_L1,
        "psi_L_L1_numerical": normalized_L1,
        "psi_L_grad_L2_analytical": analytical_grad_L2
    }

print(f"{'L':<4} | {'epsilon':<10} | {'L2_sq Num':<10} | {'L2_sq Anal':<10} | {'psi_L L1 Num':<12} | {'psi_L L1 Anal':<12} | {'psi_L grad L2':<15}")
print("-" * 90)
for L in [2, 4, 6, 8, 10]:
    res = verify_scaling(L)
    print(f"{res['L']:<4} | {res['epsilon']:<10.6f} | {res['L2_sq_numerical']:<10.6f} | {res['L2_sq_analytical']:<10.6f} | {res['psi_L_L1_numerical']:<12.6f} | {res['psi_L_L1_analytical']:<12.6f} | {res['psi_L_grad_L2_analytical']:<15.2f}")
