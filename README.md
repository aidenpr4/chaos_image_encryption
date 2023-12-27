# ChaosCrypt 

This project combines Chaos-based image encryption (ChaosCrypt) and data analysis tools to visualize the behavior of the logistic map and the Lorenz system.

## ChaosCrypt (lorenzfin.py)

ChaosCrypt is an image encryption implementation based on chaotic systems. It utilizes the Lorenz system for encryption and decryption. The encryption process involves applying chaotic dynamics to the image pixels, creating a unique encrypted image. The decryption process uses the inverse of the chaotic dynamics to recover the original image.

### Usage

1. Run `lorenzfin.py`.
2. Select an image for encryption.
3. Enter encryption keys (Key 1, Key 2, Key 3).
4. Click the "Encrypt" button.
5. Optionally, decrypt the encrypted image using the "Decrypt" button and the same keys.

## Histogram Comparison (histogram.py)

The `histogram.py` script compares the histograms and adjacent pixel correlations between an original and a decrypted image. It provides insights into the impact of encryption on the statistical distribution of pixel values.

### Usage

1. Run `histogram.py`.
2. Select an original image and a decrypted image.
3. Click the "Analyze Images" button to generate histograms and correlation plots.

## Chaos Visualization (docplot.py)

`docplot.py` generates a bifurcation diagram for the logistic map and visualizes the Lorenz attractor using a 3D plot. It demonstrates the chaotic behavior of these systems.

### Usage

1. Run `docplot.py`.
2. Observe the bifurcation diagram of the logistic map.
3. Enjoy the animated visualization of the Lorenz attractor.

## Requirements

- Python 3.x
- Required Python packages (install using `pip install package_name`):
  - NumPy
  - Matplotlib
  - SciPy
  - PyQt5
  - PIL (Pillow)
You can install these dependencies using the following command:

#bash
pip install numpy scipy matplotlib pillow pyqt5
or pip install -r requirements.txt

## Note

- The project is designed for educational purposes, and the encryption method is a simple demonstration. Do not use it for sensitive data.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Folder Structure

/
|-- lorenzfin.py  #it will create 2 folders for encrypted_images and decrypted_images

|-- encrypted_images/

|   |-- encrypted_timestamp.npy

|   |-- encrypted_timestamp.png

|-- decrypted_images/

|   |-- decrypted_timestamp.jpg

|-- noimg.png



Usage

    Run the script using the following command:

     #bash
     python lorenzfin.py

    The GUI window will appear, allowing you to perform image encryption and decryption.

    Select an image by clicking the "Select" button.

    Enter the required encryption keys when prompted.

    Click the "Encrypt" button to encrypt the selected image.

    Click the "Decrypt" button to decrypt an encrypted image.


Important Notes

    Ensure you have Python and the required dependencies installed.

    Encryption and decryption keys must be provided during the process.

    Encrypted and decrypted images will be saved in separate folders.

Feel free to explore, experiment, and modify the code for your learning and development.

Happy coding!
ChaosCrypt is a Python script that demonstrates a simple image encryption and decryption technique based on chaos theory. It uses the Lorenz system to generate chaotic behavior, which is then applied to encrypt and decrypt image data.


