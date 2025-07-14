import numpy as np
import matplotlib.pyplot as plt


# Defining the sinc signal
def wsrc(t):
    return np.sinc(SincP * t)


# a function which returns the total distance travelled by the signal from the source to the obstacle to the mic
def dist(src, pt, mic):

    d1 = np.sqrt((src[0] - pt[0]) ** 2 + (src[1] - pt[1]) ** 2)
    d2 = np.sqrt((pt[0] - mic[0]) ** 2 + (pt[1] - mic[1]) ** 2)
    return d1 + d2


# Function which returns the coordinates of mics positioned on the y axis
def mic_coordinates(Nmics, pitch):
    end = (Nmics - 1) / 2 * pitch
    y_val = np.linspace(-end, end, Nmics)
    x_val = np.zeros_like(y_val)
    mics = np.column_stack((x_val, y_val))
    return mics


# Function which calculates the delay experienced by the mic due to the difference is the travelled distances
def generate_dist_arr(src, obstacle, mics):
    distance = [dist(src, obstacle, mic) for mic in mics]
    distance_arr = np.array(distance)
    return distance_arr


# Generate time sample array with delay
def generate_time_sample(Nmics, mics, src, obstacle, C, Nsamp, dist_per_samp):
    delay_arr = (
        generate_dist_arr(src, obstacle, mics) / C
    )  # dividing by speed of sound to get the delay from the distance travelled
    Waves = []  # Creating a list to store the values of the shifted sinc signals
    end = Nsamp * dist_per_samp
    time_arr = np.linspace(0, end, Nsamp) / C
    plt.figure()
    for i in range(Nmics):
        time_samp_arr = (
            time_arr - delay_arr[i]
        )  # Shift by the delay experienced by the respective mic
        Waves.append(wsrc(time_samp_arr))
        plt.plot(wsrc(time_samp_arr) + i)
    plt.savefig("shifted_sinc.png")
    return Waves


""" 
Function to reconstruct images from arrays with sampled values.
This function calculates the delay associated with every mic,
if the obstacle was at a particular point in the grid,
then sums up the sampled value of the sinc signals at samp_idx indices
and appends it to the reconstruct_matrix,
on plotting which we obtain the heatmaps
"""


def reconstruct(mics, Nsamp, Waves, dist_per_samp):
    x_Nsamp = np.arange(0, int(Nsamp / 2), 1)
    reconstruct_matrix = np.zeros((int(Nsamp / 2), len(mics)))
    for i in x_Nsamp:
        for mic in mics:
            pt = (i * dist_per_samp, mic[1])
            dist_arr = generate_dist_arr(src, pt, mics)
            sum = 0
            for k in range(len(Waves)):
                samp_idx = int(
                    dist_arr[k] / dist_per_samp
                )  # Calculating the index at which the waves in the data has to be sampled
                if samp_idx < len(Waves[k]):
                    sum += Waves[k][samp_idx]

            reconstruct_matrix[i][int(mic[1] / pitch + len(mics) / 2)] = sum
    return (
        reconstruct_matrix.T
    )  # returning transpose because looped first over x instead of y


# Main function
if __name__ == "__main__":
    # Main system parameters
    Nmics = 64
    Nsamp = 200
    src = (0, 0)
    pitch = 0.1
    dist_per_samp = 0.1
    C = 2.0
    SincP = 10.0
    obstacle = (3, -1)
    mics = mic_coordinates(Nmics, pitch)

    # Generating and plotting heatmap for the generated data
    Waves = generate_time_sample(Nmics, mics, src, obstacle, C, Nsamp, dist_per_samp)
    reconstructed_1 = reconstruct(mics, Nsamp, Waves, dist_per_samp)

    # Set up a single figure with all the heatmaps as the subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    # Plot each array in a subplot
    axs[0, 0].imshow(Waves)
    axs[0, 0].set_title("Generated Waves")

    axs[0, 1].imshow(reconstructed_1)
    axs[0, 1].set_title("Reconstruction for Generated Waves")

    # Loading and plotting for rx2.txt data
    data2 = np.loadtxt("rx2.txt")
    reconstructed_2 = reconstruct(mics, Nsamp, data2, dist_per_samp)
    axs[1, 0].imshow(reconstructed_2)
    axs[1, 0].set_title("Reconstruction for Data2 (rx2.txt)")

    # Loading and plotting for rx3.txt data
    data3 = np.loadtxt("rx3.txt")
    reconstructed_3 = reconstruct(mics, Nsamp, data3, dist_per_samp)
    axs[1, 1].imshow(reconstructed_3)
    axs[1, 1].set_title("Reconstruction for Data3 (rx3.txt)")
    plt.tight_layout()
    plt.savefig("heatmap.png")
