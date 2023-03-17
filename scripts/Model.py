import numpy as np
import laspy
import sys
import pptk

class Model:

    def View(las_data):

        inliers = las_data[las_data[:, 8] != 7]
        inliers = inliers[:, [0,1,2]]
        noise = las_data[las_data[:, 8] == 7]
        noise = noise[:, [0,1,2]]
        n_rgb = np.full((len(noise), 3), [255, 255, 0])
        i_rgb = np.full((len(inliers), 3), [255, 0, 0])
        points = np.vstack((inliers, noise))
        rgb = np.vstack((i_rgb, n_rgb))
        v = pptk.viewer(points, rgb)
