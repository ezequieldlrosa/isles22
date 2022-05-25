__author__      = "Ezequiel de la Rosa"

import numpy as np
import warnings
import cc3d


def compute_dice(im1, im2, empty_value=1.0):
    """
    Computes the Dice coefficient, a measure of set similarity.
    Parameters
    ----------
    im1 : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    im2 : array-like, bool
        Any other array of identical size as im1. If not boolean, it will be converted.
    empty_value : scalar, float.

    Returns
    -------
    dice : float
        Dice coefficient as a float on range [0,1].
        Maximum similarity = 1
        No similarity = 0
        If both images are empty (sum equal to zero) = empty_value

    Notes
    -----
    The order of inputs for `dice` is irrelevant. The result will be
    identical if `im1` and `im2` are switched.

    This function has been adapted from the Verse Challenge repository:
    https://github.com/anjany/verse/blob/main/utils/eval_utilities.py
    """

    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    im_sum = im1.sum() + im2.sum()
    if im_sum == 0:
        return empty_value

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)

    return 2. * intersection.sum() / im_sum


def compute_absolute_volume_difference(im1, im2, voxel_size):
    """
    Computes the absolute volume difference between two masks.

    Parameters
    ----------
    im1 : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    im2 : array-like, bool
        Any other array of identical size as 'ground_truth'. If not boolean, it will be converted.
    voxel_size : scalar, float (ml)
        If not float, it will be converted.

    Returns
    -------
    abs_vol_diff : float, measured in ml.
        Absolute volume difference as a float.
        Maximum similarity = 0
        No similarity = inf


    Notes
    -----
    The order of inputs is irrelevant. The result will be identical if `im1` and `im2` are switched.
    """

    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)
    voxel_size = voxel_size.astype(np.float)

    if im1.shape != im2.shape:
        warnings.warn("Shape mismatch: ground_truth and prediction have difference shapes."
                      " The absolute volume difference is computed with mismatching shape masks")

    ground_truth_volume = np.sum(im1)*voxel_size
    prediction_volume = np.sum(im2)*voxel_size
    abs_vol_diff = np.abs(ground_truth_volume-prediction_volume) 
    
    return abs_vol_diff


def compute_absolute_lesion_difference(ground_truth, prediction):
    """
    Computes the absolute lesion difference between two masks. The number of lesions are counted for
    each volume, and their absolute difference is computed.

    Parameters
    ----------
    ground_truth : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    prediction : array-like, bool
        Any other array of identical size as 'ground_truth'. If not boolean, it will be converted.

    Returns
    -------
    abs_les_diff : int
        Absolute lesion difference as integer.
        Maximum similarity = 0
        No similarity = inf


    Notes
    -----
    """
    ground_truth = np.asarray(ground_truth).astype(np.bool)
    prediction = np.asarray(prediction).astype(np.bool)

    ground_truth_numb_lesion = compute_number_of_clusters(ground_truth)
    prediction_numb_lesion = compute_number_of_clusters(prediction)
    abs_les_diff = abs(ground_truth_numb_lesion-prediction_numb_lesion)
    
    return abs_les_diff


def compute_number_of_clusters(im, connectivity=26):
    """
    Computes the number of 3D clusters (connected-components) in the image.

    Parameters
    ----------
    im : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    connectivity : scalar, int

    Returns
    -------
    num_clusters : scalar, int
    """

    labeled_im = cc3d.connected_components(im, connectivity=connectivity)
    num_clusters = labeled_im.max().astype('int16')

    return num_clusters


def compute_lesion_f1_score(ground_truth, prediction, empty_value=1.0, connectivity=26):
    """
    Computes the lesion-wise F1-score between two masks.

    Parameters
    ----------
    ground_truth : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    prediction : array-like, bool
        Any other array of identical size as 'ground_truth'. If not boolean, it will be converted.
    empty_value : scalar, float.
    connectivity : scalar, int.

    Returns
    -------
    f1_score : float
        Lesion-wise F1-score as float.
        Max score = 1
        Min score = 0
        If both images are empty (tp + fp + fn =0) = empty_value

    Notes
    -----
    This function computes lesion-wise score by defining true positive lesions (tp), false positive lesions (fp) and
    false negative lesions (fn) using 3D connected-component-analysis.

    tp: 3D connected-component from the ground-truth image that overlaps at least on one voxel with the prediction image.
    fp: 3D connected-component from the prediction image that has no voxel overlapping with the ground-truth image.
    fn: 3d connected-component from the ground-truth image that has no voxel overlapping with the prediction image.
    """
    ground_truth = np.asarray(ground_truth).astype(np.bool)
    prediction = np.asarray(prediction).astype(np.bool)
    tp = 0
    fp = 0
    fn = 0

    # Check if ground-truth connected-components are detected or missed (tp and fn respectively).
    intersection = np.logical_and(ground_truth, prediction)
    labeled_ground_truth = cc3d.connected_components(ground_truth, connectivity=connectivity)

    # Iterate over ground_truth clusters to find tp and fn.
    # tp and fn are only computed if the ground-truth is not empty.
    if labeled_ground_truth.max() > 0:
        for cluster_label in range(1, labeled_ground_truth.max()+1):
            binary_cluster_image = labeled_ground_truth == cluster_label
            if np.logical_and(binary_cluster_image, intersection).any():
                tp += 1
            else:
                fn += 1

    # iterate over prediction clusters to find fp.
    # fp are only computed if the prediction image is not empty.
    labeled_prediction = cc3d.connected_components(prediction, connectivity=connectivity)
    if labeled_prediction.max() > 0:
        for cluster_label in range(1, labeled_prediction.max()+1):
            binary_cluster_image = labeled_prediction == cluster_label
            if not np.logical_and(binary_cluster_image, ground_truth).any():
                fp += 1

    # Define case when both images are empty.
    if tp+fp+fn == 0:
        if compute_number_of_clusters(ground_truth) == 0:
            f1_score = empty_value
    else:
        f1_score = tp/(tp + (fp+fn)/2)

    return f1_score


