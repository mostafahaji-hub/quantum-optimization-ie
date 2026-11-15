# Chapter 6, code listing 9 (in order of appearance)
import numpy as np
# one step from P(1) = 0.5 toward a best bit equal to 1
theta = np.pi/4
print('Q-bit rotation by 9 deg :', round(np.sin(theta + np.radians(9))**2, 3))
alpha = 0.3
print('PBIL with alpha = 0.3   :', round((1 - alpha) * 0.5 + alpha * 1, 3))
# many small steps toward 1
p_q, p_e, th = [], [], theta
p = 0.5
for step in range(10):
    th = min(th + np.radians(4), np.pi/2); p_q.append(np.sin(th)**2)
    p = (1 - 0.1) * p + 0.1 * 1;           p_e.append(p)
print('10 rotations of 4 deg   :', np.round(p_q, 2))
print('10 PBIL steps, alpha 0.1:', np.round(p_e, 2))