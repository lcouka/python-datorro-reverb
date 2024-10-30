# Python Dattorro Reverb
A Python implementation of the **Dattorro reverb algorithm**, designed to create realistic, lush audio reverberation effects. This implementation follows the original algorithm closely, delivering high-quality sound for audio processing and sound design.

For more information, please visit my [personal website](https://www.louiscouka.com/code/datorro-reverb-implementation/).  
Original paper: [Dattorro’s Reverb Paper](https://ccrma.stanford.edu/~dattorro/EffectDesignPart1.pdf).

## Overview of the Dattorro Reverb Algorithm

The **Dattorro Reverb** is a classic digital reverb technique that utilizes a feedback delay network (IIR) with various filtering and diffusion stages to create a deep, immersive reverb. Here is a breakdown of the signal flow:

1. **Pre-Delay**  
   Adds a brief delay before the reverb effect begins, creating a sense of distance.
   
2. **Input Filter**  
   A low-pass filter shapes the incoming signal, removing higher frequencies before diffusion.

3. **Input Diffusor**  
   Composed of four all-pass filters, the diffusor increases the signal's spatial complexity.
   
4. **Reverberation Tank** (Split into two main parts):  
   - **Cross Feedback**: Each half of the tank feeds into the other, increasing the reverb density.
   - **Decay Diffusors**: Includes both modulated and standard all-pass filters to add further diffusion to the reverb tail.
   - **Damping**: A low-pass filter progressively removes high frequencies from the reverb tail, simulating natural absorption.

5. **Output Stage**  
   Multiple delay taps create a lush, smooth reverb tail, providing a natural sense of space.

## Sound Examples 

Listen to the results of the Dattorro reverb applied to a drone sound from UVI Cinematic Shades, with a long decay setting of 0.9:

[Download Audio Examples (ZIP)](https://github.com/user-attachments/files/17571268/Audio.Examples.zip)

## Known Limitations

**Mono Summing**:  
A notable limitation is that the left and right input channels are summed into mono before processing, which means the reverb is not "true stereo." Some spatial detail is lost due to the early summing of channels, making it less effective for stereo imaging.

## Final Thoughts

Despite the mono summing limitation, the Dattorro Reverb produces exceptional sound quality. This implementation also serves as a robust foundation for expanding into a true stereo reverb by modifying the feedback network.
