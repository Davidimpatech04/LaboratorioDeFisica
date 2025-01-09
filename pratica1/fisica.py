import numpy as np
from scipy.odr import ODR, Model, RealData
import matplotlib.pyplot as plt

def linear_model(params, x):
    m, b = params
    return m * x + b

x = np.array([0.300, 0.600, 0.900, 1.200, 1.500, 1.510])  
y = np.array([0.9922, 1.9892, 2.9814, 3.9785, 4.9707, 5.0])  

x_err = np.array([0.015, 0.030, 0.045, 0.060, 0.075, 0.0755])
y_err = np.array([0.0049, 0.0049, 0.0049, 0.0049, 0.0049, 0.0049])


data = RealData(x, y, sx=x_err, sy=y_err)

model = Model(linear_model)
odr = ODR(data, model, beta0=[1.0, 0.0])  

output = odr.run()

m, b = output.beta  
m_err, b_err = output.sd_beta  


print(f"Coeficiente angular (m): {m:.3f} ± {m_err:.3f}")
print(f"Coeficiente linear (b): {b:.3f} ± {b_err:.3f}")

x_fit = np.linspace(min(x), max(x), 100)
y_fit = m * x_fit + b

plt.figure(figsize=(8, 6))
plt.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o', label='Dados com Erros', ecolor='red', capsize=5)
plt.plot(x_fit, y_fit, 'b-', label=f'Ajuste Linear: y = {m:.2f}x + {b:.2f}')

plt.title("Ajuste Linear com ODR", fontsize=16)
plt.xlabel("Resistência (kΩ)", fontsize=14)
plt.ylabel("Tensão (V)", fontsize=14)
plt.legend(fontsize=12)
plt.grid(alpha=0.5)
plt.show()