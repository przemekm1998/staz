import pytest
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from pprint import pprint

from scipy.signal.windows import hamming

from audio_tools import make_sine, save_audio_file, open_wave, record_audio
from frequency_analysis_tools import spectrum_analysis_plot


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

    filename = 'output_sine.wav'
    fs, audio = open_wave(filename)

    yield audio


def test_generated_sine_spectrum(recorded_sine, spectrum_analysis_plot):
    """ Check the generated sine amplitude spectrum """

    sine_to_analyze = recorded_sine[2048:4096]
    fs = 44100
    spectrum_analysis_plot(sine_to_analyze, fs)


def test_damaged_generated_sine_spectrum(recorded_sine, spectrum_analysis_plot):
    sine_to_analyze = recorded_sine[2048:4096]
    sine_to_analyze = sine_to_analyze * 1
    sine_to_analyze[1024:1124] = 0
    fs = 44100
    spectrum_analysis_plot(sine_to_analyze, fs)


@pytest.mark.skip
def test_recorded_sine_spectrum(recorded_sine, spectrum_analysis_plot):
    """ Check the recorded sine amplitude spectrum """

    sine_to_analyze = recorded_sine[:2048]
    sine_to_analyze = sine_to_analyze * 1
    sine_to_analyze[1024:1124] = 0
    fs = 44100

    spectrum_analysis_plot(sine_to_analyze, fs)


@pytest.mark.skip
def test_spectrogram(recorded_sine, generated_sine):
    fs = 44100
    sine_to_analyze = generated_sine[:4096]
    sine_to_analyze[2048:2100] = 0
    f, t, sxx = sig.spectrogram(sine_to_analyze, fs=fs, window=np.hamming(
        2048),
                                nperseg=2048,
                                noverlap=1536,
                                scaling='spectrum', mode='magnitude')
    plt.figure(figsize=(15, 7))
    plt.pcolormesh(t, f, 20 * np.log10(sxx))
    plt.xlabel('czas [s]')
    plt.ylabel('częstotliwość [Hz]')
    plt.title('Spektrogram sygnału')
    plt.ylim(0, 12000)
    plt.colorbar()
    plt.show()


@pytest.mark.skip
def test_density_generated(recorded_sine):
    print('\nRECORDED_SINE')
    sine = recorded_sine[2048:4096]
    mean_y = np.mean(sine)
    std_y = np.std(sine)
    var_y = std_y ** 2.0

    complex_spectrum = np.fft.rfft(sine)
    amplitude_spectrum = np.abs(complex_spectrum) / 1024
    ps = amplitude_spectrum ** 2
    print('suma widma mocy e-06', sum(ps) * pow(10, -6))
    plt.plot(10 * np.log10(ps))
    plt.show()

    print('mean', mean_y)
    print('std', std_y)
    print('var', var_y)

@pytest.mark.skip
def test_perdiodogram(generated_sine):
    sine_to_analyze = generated_sine[:2048]

    fper, pxx = sig.periodogram(sine_to_analyze, 44100, 'hamming', 2048,
                                scaling='density')
    plt.semilogy(fper, pxx)
    plt.xlim(0, 10000)
    plt.xlabel('częstotliwość [Hz]')
    plt.ylabel('widmowa gęstość mocy')
    plt.title('Periodogram')
    plt.show()
