# Exact implementation of the Datorro figure of eight implemented in Python, according to the original Paper
# Author : Louis Couka
# Website : https://www.louiscouka.com/code/datorro-reverb-implementation/
# License : MIT

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import sounddevice as sd
#import soundfile as sf

# Input
fs = 44100
x = signal.unit_impulse(fs*2)
x = np.array([x, x]).T
#x, fs = sf.read("/Users/louiscouka/Desktop/dry.flac")

# Parameters
decay = 0.5
decay_diffusion1 = 0.7
decay_diffusion2 = 0.5
input_diffusion1 = 0.75
input_diffusion2 = 0.625
bandwidth = 0.9995
damping = 0.0005
wet = 0.4
dry = 1

# Helper that convert the sample unit of the paper according to the original fs employed = 29761
def c(numSamples):
    original_fs = 29761
    return int(np.round(numSamples*fs/original_fs))

### Init
y = np.sum(x, axis = 1) / 2 # Sum L R as in the paper
pad = 10000 # Should be more than max tap index value
y = np.append(np.zeros(pad), y, axis = 0)

### Diffuser
def allpass_comb(x, d, i, diffusion):
    y = np.zeros(len(x))
    while i < len(x):
        s = min(d, len(x) - i) # Chunk the process so we can vectorize and it's fast
        y[i:][:s] = diffusion*(x[i:][:s] - y[i-d:][:s]) + x[i-d:][:s]
        i += s
    return y
y = allpass_comb(y, c(142), pad, input_diffusion1)
y = allpass_comb(y, c(107), pad, input_diffusion1)
y = allpass_comb(y, c(379), pad, input_diffusion2)
y = allpass_comb(y, c(277), pad, input_diffusion2)

### Tank
dl = np.zeros((8, len(y))) # All delaylines
dlt = [c(672), c(4453), c(1800), c(3720), c(908), c(4217), c(2656), c(3163)] # Tap time used for each delayline
i = pad
while i < len(x):
    s = min(min(dlt), len(y) - i) # Chunk the process so we can vectorize and it's fast
    for j in range(0, 8, 4):
        dl[j+0, i:][:s] = y[i:][:s] + decay * dl[j-1, i-dlt[j-1]:][:s] + decay_diffusion1 * dl[j+0, i-dlt[j+0]:][:s]
        dl[j+1, i:][:s] =                     dl[j+0, i-dlt[j+0]:][:s] - decay_diffusion1 * dl[j+0, i:][:s]
        for k in range(i-s, i):
            dl[j+1, k] = damping*dl[j+1, k-1] + (1-damping)*dl[j+1, k]
        dl[j+2, i:][:s] =             decay * dl[j+1, i-dlt[j+1]:][:s] - decay_diffusion2 * dl[j+2, i-dlt[j+2]:][:s]
        dl[j+3, i:][:s] =                     dl[j+2, i-dlt[j+2]:][:s] + decay_diffusion2 * dl[j+2, i:][:s]
    i += s

### Build the output
yL  = np.copy(dl[5, pad-dlt[5]+c(266):][:len(x)]) # node48_54
yL += dl[5, pad-dlt[5]+c(2974):][:len(x)] # node48_54
yL -= dl[6, pad-dlt[6]+c(1913):][:len(x)] # node55_59
yL += dl[7, pad-dlt[7]+c(1996):][:len(x)] # node59_63
yL -= dl[1, pad-dlt[1]+c(1990):][:len(x)] # node24_30
yL -= dl[2, pad-dlt[2]+c(187):][:len(x)] # node31_33
yL -= dl[3, pad-dlt[3]+c(1066):][:len(x)] # node33_39

yR  = np.copy(dl[1, pad-dlt[1]+c(353 ):][:len(x)]) # node24_30
yR += dl[1, pad-dlt[1]+c(3627):][:len(x)] # node24_30
yR -= dl[2, pad-dlt[2]+c(1228):][:len(x)] # node31_33
yR += dl[3, pad-dlt[3]+c(2673):][:len(x)] # node33_39
yR -= dl[5, pad-dlt[5]+c(2111):][:len(x)] # node48_54
yR -= dl[6, pad-dlt[6]+c(335):][:len(x)] # node55_59
yR -= dl[7, pad-dlt[7]+c(121):][:len(x)] # node59_63

y = np.array([yL, yR]).T
y *= 0.6 # Final mul

sd.play(dry*x + wet*y, fs)
#sf.write("/Users/louiscouka/Desktop/wet.flac", dry*x + wet*y, fs)
