def normalize_threshold(connectivity_matrix, threshold = 0.5):
    """
    This function gets a connectivity matrix and normalize its values between 0 to 1. 
    After normalization, the function zero the matrix values that are lower than  the threshold

    Parameters 
    ----------
    connectivity_matrix: np.ndarray
        n X n matrix where n is the number of ROIs in  the atlas. 
        Each cell in the matrix describes the connection between each pair of ROIs.
    
    threshold: float
        A float between 0 to 1 by. Values lower than threshold are set to zero.
    
    Returns
    -------
    filtered_matrix: np.ndarray
        connecitivty matrix after thresholding and normalization
    """
    if threshold < 0 or threshold > 1:
        raise ValueError("Threshold value must be between 0-1!")

    normalized_connectivity_matrix = (connectivity_matrix - np.min(connectivity_matrix)) / (np.max(connectivity_matrix) - np.min(connectivity_matrix))
    
    filtered_matrix = normalized_connectivity_matrix
    filtered_matrix[normalized_connectivity_matrix < threshold] = 0

    return filtered_matrix
