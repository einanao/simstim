# Simstim



## Setup
1. Install the [Arduino Desktop IDE](https://www.arduino.cc/en/Guide)
2. Go to the [Cthulhu GitHub repo](https://github.com/SapienLLCdev/Cthulhu) and [download ZIP](https://github.com/SapienLLCdev/Cthulhu/archive/refs/heads/master.zip)
3. Open the Arduino IDE, go to `Sketch > Include Library > Add .ZIP Library`, and select the `.zip` file downloaded in the previous step
4. Setup [Anaconda](https://www.anaconda.com/products/distribution) environment with `conda env create -f environment.yml`
5. Set the default `port` value in `simstim/cthulhu.py`. If you don't know the port, make sure the Arduino is connected to your computer and run `ls -lha /dev/tty*` (it will probably look like `/dev/tty.usbmodem`).

## Usage
1. In the Arduino IDE, open `File > Examples > Cthulhu-master > SerialInput` and run the program
2. Activate Anaconda environment with `conda activate simstim`
3. Run `python study.py`
4. Click on circle to toggle prediction. If you think the electrode is on, toggle it black. Otherwise, leave it gray.
5. When you're ready to submit your prediction, hit Enter. The difference between your prediction and the true pattern will be revealed.
  - Gray: predicted off, actually off
  - Green: predicted on, actually on
  - Blue: predicted off, actually on
  - Red: predicted on, actually off
6. Once you are done looking at the results, hit the right arrow key. The display will be reset, and the electrodes will be reset to a new pattern.
7. When you want to end the experiment, click the `X` button at the top of the experiment window