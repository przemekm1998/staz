import pytest
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

from audio_tools import make_sine, save_audio_file, open_wave, record_audio
from scipy.fftpack import fft
from scipy.signal.windows import hamming


@pytest.fixture(scope='module')
def generated_sine(make_sine):
    """ Generate sine wave for further tests """

    frequency = 440
    fs = 44100
    duration = 3

    audio = make_sine(frequency, fs, duration)
    yield audio


@pytest.fixture(scope='module')
def recorded_sine(open_wave):
    """ Load recorded sine wave """

    filename = 'audacity.wav'
    fs, audio = open_wave(filename)

    yield audio


@pytest.fixture(scope='module')
def spectrum_plotter():
    """ Spectrum plotter factory """

    def _plot_spectrum(fs, num_samples, signal):
        """
        Plot time signal and frequency spectrum
        :param fs: Sampling rate of signal
        :param num_samples: Number of samples to analyze
        :param signal: Input signal
        :return:
        """

        fig, (ax, ax2) = plt.subplots(2, figsize=(15, 8))
        ax.plot(signal[:num_samples + 1], '-')

        sliced_signal = signal[:num_samples]
        hamming_window = hamming(num_samples)
        windowed_signal = sliced_signal * hamming_window
        complex_spectrum = fft(windowed_signal)
        magnitude_spectrum = np.abs(complex_spectrum[:(num_samples // 2)])
        ax2.plot(magnitude_spectrum)

        # frequency_range = np.linspace(0, fs, num_samples)
        # ax2.plot(frequency_range, magnitude_spectrum, '-', lw=2)
        # ax2.set_xlim(0, fs / 2)

        plt.show()

    return _plot_spectrum


@pytest.fixture(scope='module')
def correlation_plotter():
    """ Autocorrelation function plotter factory """

    def _plot_autocor(num_samples, signal):
        """
        Plot time signal and frequency spectrum
        :param num_samples: Number of samples to analyze
        :param signal: Input signal
        :return:
        """

        signal_samples = signal[:num_samples+1]
        fig, (ax, ax2) = plt.subplots(2, figsize=(15, 8))
        ax.plot(signal_samples, '-')

        autocorr = sig.correlate(signal_samples, signal_samples)
        autocorr = autocorr[len(autocorr) // 2:]
        autocorr = autocorr / autocorr[0]

        ax2.plot(autocorr, '-', lw=2)

        plt.show()

    return _plot_autocor


def test_plot_generated_sine_spectrum(generated_sine, spectrum_plotter):
    """ Plot generated sine spectrum """

    fs = 44100
    samples = 2048

    spectrum_plotter(fs, samples, generated_sine)


def test_plot_recorded_sine_spectrum(recorded_sine, spectrum_plotter):
    """ Plot generated sine spectrum """

    fs = 44100
    samples = 2048

    spectrum_plotter(fs, samples, recorded_sine)


def test_plot_generated_sine_autocorr(generated_sine, correlation_plotter):

    samples = 500
    correlation_plotter(samples, generated_sine)