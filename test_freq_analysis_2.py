import pytest
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from pprint import pprint
from audio_tools import make_sine, save_audio_file, open_wave, record_audio


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

    filename = 'auda_wav.wav'
    fs, audio = open_wave(filename)

    yield audio


def test_freq_analysis(recorded_sine, generated_sine):
    fs = 44100

    widmo_amp = np.abs(np.fft.rfft(recorded_sine[:2048])) / 1024
    f = np.fft.rfftfreq(2048, 1 / fs)
    plt.figure(figsize=(15, 7))
    plt.plot(f, 20 * np.log10(widmo_amp))
    plt.xlabel('częstotliwość [Hz]')
    plt.ylabel('amplituda widma')
    plt.title('Widmo sygnału sinusoidalnego 440 kHz')
    plt.show()


def test_spectrogram(recorded_sine, generated_sine):
    fs = 44100
    f, t, sxx = sig.spectrogram(recorded_sine, fs=fs, window=np.hamming(
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
#
#
# def test_perdiodogram(generated_sine):
#     fper, pxx = sig.periodogram(generated_sine[0:2048], 44100, 'hamming', 2048,
#                                 scaling='density')
#     plt.semilogy(fper, pxx)
#     plt.xlim(0, 10000)
#     plt.xlabel('częstotliwość [Hz]')
#     plt.ylabel('widmowa gęstość mocy')
#     plt.title('Periodogram')
#     plt.show()
