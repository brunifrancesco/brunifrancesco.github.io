from IPython.display import Audio
from wave import open as open_wave
from math import pi

import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt


def create_wave_samples(duration:int=2, framerate=3000, frequency:int=400, amplitude:int=1, phase:float=0, periodic_function=np.cos) -> Tuple[np.ndarray, np.ndarray]:
    """Create the digital representation of analogue wave
    
    duration: Wave duration (default=2)
    framerate: Wave framerate (equals to sampling rate) (default=3000)
    frequency: Signal frequency (default=400)
    amplitude: Signal amplitude (default=1)
    phase: Signal offset in radians duration (default=2)
    periodic_function: Waveform (default=np.cos)
    """
    n = round(duration * framerate)
    ts = np.arange(n) / framerate
    ts = np.asarray(ts)
    phases =  pi * 2 * frequency * ts + phase
    return amplitude * periodic_function(phases), ts

def create_audio(ys: np.ndarray, framerate:int = 3000, autoplay: bool=False) -> Audio:
  """Create the Audio object ready for being listened

  ys: samples
  framerate: wave framerate (default=3000)
  autoplay: reproduce it automatically
  """
  return Audio(data=ys, rate=framerate)

def plot(x:np.ndarray, y: np.ndarray, title="", xlabel="", ylabel=""):
    """Plot subset of provided wave given its time samples and values
    x: x values
    y: y values
    title: chart title
    xlabel: x axis label
    ylabel: y axis label
    
    """
    plt.plot(x, y, '-')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def normalize(ys: np.ndarray, amp: float) -> np.ndarray:
  """Normalize samples by amplitude
  ys: samples
  amp: amplitude
  """
  high, low = abs(max(ys)), abs(min(ys))
  return amp * ys / max(high, low)

def get_wave_samples(filename: str) -> Tuple[np.ndarray, np.ndarray, int]:
  """Open a wav file and get the samples, time units and framerate
  filename: the file to be read
  """

  with open_wave(filename, "r") as fp:
    nchannels = fp.getnchannels()
    nframes = fp.getnframes()
    framerate = fp.getframerate()
    z_str = fp.readframes(nframes)
    ys = np.fromstring(z_str, dtype=np.int16)

  # if it's in stereo, just pull out the first channel
  if nchannels == 2:
      ys = ys[::2]

  ts = np.arange(len(ys)) / framerate
  ys = normalize(ys, amp=1.0)

  return ys, ts, framerate

def low_pass(hs, fs, cutoff, factor=0.01) -> np.ndarray:
    """Attenuate frequencies above the cutoff.
    cutoff: frequency in Hz
    factor: what to multiply the magnitude by
    """

    hs[abs(fs) > cutoff] *= factor
    return hs
    
def high_pass(hs, fs, cutoff, factor=0.01) -> np.ndarray:
    """Attenuate frequencies below the cutoff.
    cutoff: frequency in Hz
    factor: what to multiply the magnitude by
    """

    hs[abs(fs) < cutoff] *= 0.01
    return hs