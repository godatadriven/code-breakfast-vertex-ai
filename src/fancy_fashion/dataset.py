from pathlib import Path

from PIL import Image
from tensorflow.keras.datasets import fashion_mnist

LABEL_MAPPING = {
    0: "tshirttop",
    1: "trouser",
    2: "pullover",
    3: "dress",
    4: "coat",
    5: "sandal",
    6: "shirt",
    7: "sneaker",
    8: "bag",
    9: "ankle_boot",
}

REVERSE_MAPPING = {v: k for k, v in LABEL_MAPPING.items()}


def generate_dataset(n_train=500, n_test=100, n_actual=50, output_dir=Path("./data")):
    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

    # Confuse others by using test as train images.
    train_labels = ["shirt", "sneaker", "bag"]
    test_labels = ["shirt", "sneaker", "bag"]
    actual_labels = ["shirt", "sneaker", "bag", "dress"]

    for label in train_labels:
        save_train_test_images(
            output_dir / "train", x_train, y_train, label, n_train, train_or_test="train"
        )

    for label in test_labels:
        save_train_test_images(
            output_dir / "test", x_test, y_test, label, n_test, train_or_test="test"
        )

    n_per_actual_label = len(actual_labels) // n_actual

    save_actuals(
        output_dir / "actuals", x_test, y_test, labels=actual_labels, n_per_label=10
    )

def save_images(save_dir: Path, images: list, prefix: str = ""):
    save_dir.mkdir(exist_ok=True, parents=True)
    for ii in range(len(images)):
        image = Image.fromarray(images[ii, :, :].squeeze())
        image.save(save_dir / f"{prefix}{ii}.jpg")


def save_train_test_images(
    target_dir: Path, x, y, label: str, n_train: int, train_or_test
):
    is_label = y == REVERSE_MAPPING[label]
    images = x[is_label]
    label_dir = target_dir / train_or_test / label
    save_images(label_dir, images[-n_train:], prefix=label)


def save_actual_images(target_dir: Path, x, y, label: str, n_train: int, prefix: str):
    is_label = y == REVERSE_MAPPING[label]
    images = x[is_label]
    label_dir = target_dir / "actual"
    save_images(label_dir, images[-n_train:], prefix=prefix)


def save_actuals(target_dir: Path, x, y, labels, n_per_label: int):
    target_dir.mkdir(exist_ok=True, parents=True)

    i = 0
    for label in labels:
        is_label = y == REVERSE_MAPPING[label]
        images = x[is_label]
        label_dir = target_dir / "actual"
        images = images[-n_per_label:]
        for image in images:
            image = Image.fromarray(image[:, :].squeeze())
            image.save(target_dir / f"{i}.jpg")
            i += 1
