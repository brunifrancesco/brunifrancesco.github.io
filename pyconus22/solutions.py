from utils import *

################################################### PART 1 ##########################################################

class Wave:
  def __init__(self, ys, ts, framerate):
    self.ys = ys
    self.ts = ts
    self.framerate = framerate  

  def play(self):
    return create_audio(self.ys, self.framerate, autoplay=True)
    
  def plot(self, slice_from=0, slice_to=100):
    return plot(self.ts, self.ys, slice_from=slice_from, slice_to=slice_to)

class Signal:
    def __init__(self, freq=400, amp=1.0, offset=0, function=np.sin):
        self.freq = freq
        self.amp = amp
        self.offset = offset
        self.function=function

    def print_period(self):
      print("Period (s): %f" %(1.0/self.freq))

    
    def create_wave(self, duration=2, start=0, framerate=3000):
        ys, ts = create_wave_samples(duration, framerate, self.freq, self.amp, self.function)
        print(len(ts))
        return Wave(ys, ts, framerate=framerate)

################################################### PART 2 ##########################################################

class SinWaveform:
  """Sin waveform container
  """
  periodic_function = np.sin

class SinFunctionBasedSignal(Signal):
  """Sin based signal with composition
  """
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.function = SinWaveform()
  
  def create_wave(self, duration=2, start=0, framerate=3000):
        ys, ts = create_wave_samples(periodic_function=self.function.periodic_function)
        print(len(ts))
        return Wave(ys, ts, framerate=framerate)

class ScaleBy2:
  """Mixin to scale the samples by 2
  """
  def scale(self):
    """Scale samples
    """
    self.ys = self.ys * 2
    return self

class AugmentedWave(Wave, ScaleBy2):
  """Complete class based on Wave and ScaleByMixin signal
  """
  pass

class AugmentedSignal(SinFunctionBasedSignal):
  """Augmented version of signal
  """
  def create_wave(self, duration=2, start=0, framerate=3000):
    """create the AugmentedWave instance
    """
    ys, ts = create_wave_samples(periodic_function=self.function.periodic_function)
    return AugmentedWave(ys, ts, framerate=framerate)

class DictSerializerMixin:
  """Dictionary serializer mixin
  """
  def serialize(self, amp, freq, phase):
    """Serialize amplitude, frequency and phase in a dict
    """
    return dict(amp=amp, freq=freq, phase=phase)

class SignalWithSer(SinFunctionBasedSignal, DictSerializerMixin):
  """Serializator
  """
  def serialize(self):
    return super().serialize(self.amp, self.freq, self.phase)

###################### Part 3 ######################################

class AmDemodulator(AMModulator, LowpassFilter):
  """Amplitude demodulator with low pass filtering

  cutoff: frequency cutoff
  """
  def __init__(self, cutoff=10000):
    self.cutoff = cutoff

  def demodulate(self, modulated_wave, carrier_wave):
    """Demodulate modulated wave

    modulated_wave: the modulated wave
    carrier_wave: the carrier wave
    """
    dm = super().demodulate(modulated_wave, carrier_wave)
    spectrum = dm.make_spectrum()
    spectrum.hs = self.filter(spectrum.hs, spectrum.fs, self.cutoff)
    return spectrum.make_wave()

###################### Part 4 ######################################

class IteratorCreator:
  """Abstract base class for returning an iterator based on condition
  """
  @abstractmethod
  def create_iterator(self, condition: str) -> Iterator:
    """Create an iterator based on the condition param
    condition: a string indicating which type of iterator should be returned
    """
    raise NotImplementedError("You need to implement this method before calling it")

class ReverseIterator(Iterator):
  """Reverse iterator: iterate the iterable in the reverse order
  _position: private variable to track the state of the iteration
  """
  _position = -1

  def __next__(self):
    """Get next element.
    it raises an StopIteration error that stops the loop when the iterable has been whole looped
    """
    try:
      value = self._collection[self._position]
      self._position -= 1
      return value
    except IndexError:
          raise StopIteration()
      

class WaveSampleCollection(IteratorCreator, Iterable):
  """The collection class enriched with the Iterator
  _collection: the collection for which the iterator will loop for
  """
  def __init__(self, collection: np.ndarray) -> None:
        self._collection = collection
  
  def __iter__(self):
    """Default iterator
    """
    return self.create_iterator()
  
  def create_iterator(self, condition: str = 'sequential'):
    """Factory method for returning the iterator based on the condition
    """
    if condition == 'sequential':
      return ReverseIterator(self._collection)
    return SequentialIterator(self._collection)