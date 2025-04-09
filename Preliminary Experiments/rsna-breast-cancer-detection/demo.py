#%% packages
import torch
import numpy as np

#%% tensor
x = torch.tensor(1.5)
print(x)

# %%
y = x**2
print(y)
# %%
z = torch.tensor(3.0, requires_grad=True)
print(z)
print(z.requires_grad)
# %%
print(y.requires_grad)
# %%
y = z ** 2
print(y.requires_grad)
# %%
def func(x):
    return (x-3)*(x-6)*(x-4)

x_r = np.linspace(0, 10, 101)
y_r = [func(i) for i in x_r]
# %%
import seaborn as sns

sns.lineplot(x = x_r, y = y_r)
# %%
y = func(z)
y.backward()
print(z.grad)
# %%
