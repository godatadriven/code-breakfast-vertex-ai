# Code Breakfast - Vertex AI + Kubeflow Pipelines

In this code breakfast, we'll introduce you to the basic components of Vertex AI and show you how to run (custom) training jobs on Vertex AI using the Kubeflow Pipeline SDK.

## Exercises

### 1. Getting started with Vertex Workbench

For this code breakfast, we'll use a cloud-based JupyterLab environment for developing and running code on Vertex AI. This JupyterLab environment runs on your own personal VM in Vertex Workbench. To find your VM and open JupyterLab, follow these steps:

1. Open the Google Cloud Console (http://console.cloud.google.com) in your browser.
2. In the console, select the project `gdd-cb-vertex`.
3. Next, navigate to the Vertex Workbench section in the console (under `Vertex AI > Workbench`).
4. In the Workbench section, find the VM with your name (e.g. `vwb-<your-user-name`).
5. Open JupyterLab by clicking on the `Open JupyterLab` button next to your VM name.

This should open a new tab in your browser with JupyterLab. Look around and familiarize yourself with the environment!

### 2. Setting up this project

To set up the code for the code breakfast, open a terminal in JupyterLab (under `File > New > Terminal`) and do the following:

1. Clone this repository using: `git clone https://github.com/godatadriven/code-breakfast-vertex-ai.git`.
2. Switch to the directory we just cloned: `cd code-breakfast-vertex-ai`.
3. Set up the projects Python environment using: `make python-init`

Finally, explore our code and see if you can identify what everything does. See if you can answer the following questions:
* Check out the code in `src`. Can you find where the model is trained?
* What is the Makefile used for? What do the different commands do?
* Which tooling is used for checking code quality and formatting our code?

### 3. Training the model locally

Open the notebook `notebooks/train-local.ipynb` and run through the exercises in the notebook.

### 4. Training in Vertex Pipelines

Open the notebook `notebooks/train-vertex.ipynb` and run through the exercises in the notebook.

## Deployment

TODO.

## Roadmap

See todo: https://github.com/godatadriven/code-breakfast-vertex-ai/projects/1
