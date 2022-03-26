from matplotlib import pyplot as plt


def show_sample(sample):
    """
    Usage:

    train_batch, _ = next(train_datagenerator.as_numpy_iterator())
    show_sample(train_batch[0])
    """

    fig, axes = plt.subplots()
    plt.imshow(sample.astype(int))
    plt.show()

    return fig, axes
