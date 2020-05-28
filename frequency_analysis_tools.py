import pytest
import numpy as np
from scipy.signal.windows import hamming
import matplotlib.pyplot as plt


class _FrequencyAnalyzer:

    def __init__(self, signal, fs, window_length=2048):
        self.signal = signal
        self.fs = fs
        self.window_length = window_length

    @property
    def signal_length(self):
        return len(self.signal)

    def plot_spectrum(self):
        """ Plot calculated amplitude spectrum """

        frequencies = np.fft.rfftfreq(self.signal_length, 1 / self.fs)
        amplitude_spectrum = self.generate_amplitude_spectrum()
        print('mean', np.mean(20 * np.log10(amplitude_spectrum)))

        plt.figure(figsize=(15, 7))
        plt.plot(frequencies, 20 * np.log10(amplitude_spectrum))
        plt.xlabel('częstotliwość [Hz]')
        plt.ylabel('amplituda widma')
        plt.title('Widmo sygnału sinusoidalnego 440 kHz')
        plt.show()

    def generate_amplitude_spectrum(self):
        """ Return the amplitude spectrum of signal """

        self._multiply_signal_by_window()
        complex_spectrum = np.fft.rfft(self.signal)
        amplitude_spectrum = np.abs(complex_spectrum) / (self.signal_length / 2)

        return amplitude_spectrum

    def _multiply_signal_by_window(self):
        """ Multiply signal by window """

        hamming_window = hamming(2048)
        self.signal = self.signal * hamming_window


@pytest.fixture(scope='module')
def spectrum_analysis_plot():
    """ Plot amplitude spectrum of given signal """

    def _freq_analysis(signal, fs, window_length=2048):
        """
        Plot amplitude spectrum
        :param signal: Signal to calculate spectrum of
        :param fs: Sampling frequency
        :param window_length: Length of the time window
        :return:
        """

        frequency_analyzer = _FrequencyAnalyzer(signal, fs, window_length)
        frequency_analyzer.plot_spectrum()

    return _freq_analysis
