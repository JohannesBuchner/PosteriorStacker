import numpy as np
# velocity dispersions of dwarf galaxies by van Dokkum et al., Nature, 555, 629 https://arxiv.org/abs/1803.10237v1
np.random.seed(1)

values = np.array([15, 4, 2, 11, 1, -2, -1, -14, -39, -3])
values_lo = np.array([7, 16, 6, 3, 6, 5, 10, 6, 11, 13])
values_hi = np.array([7, 15, 8, 3, 6, 6, 10, 7, 14, 14])

n_data = len(values)

import matplotlib.pyplot as plt
plt.figure()
xlabel = 'Velocity [km/s]'
plt.xlabel(xlabel)
plt.errorbar(x=values, xerr=[values_lo, values_hi], y=range(n_data),
             marker='o', ls=' ', color='orange')
plt.ylabel("Galaxy number")
plt.xlim(-50, 50);
plt.savefig('example.png', bbox_inches='tight')
plt.close()


samples = []

for i in range(n_data):
    # draw normal random points
    u = np.random.normal(size=400)
    v = values[i] + np.where(u < 0, u * values_lo[i], u * values_hi[i])

    samples.append(v)

samples = np.array(samples)

plt.figure()
# for each galaxy, plot alittle cloud with its own colors
plt.violinplot(samples.transpose(), vert=False, showextrema=False)

plt.xlabel(xlabel)

plt.savefig('example-samples.png', bbox_inches='tight')
plt.close()

np.savetxt('posteriorsamples.txt', samples)
