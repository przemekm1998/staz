import sounddevice as sd
import pytest
import numpy as np
from scipy.io import wavfile


@pytest.fixture(scope='module')
def make_sine():
    """ Sine waves factory """

    def _make_sine(frequency, fs, seconds):
        """
        Create sine wave with desired parameters
        :param frequency: Sine wave frequency
        :param fs: Sampling frequency
        :param seconds: Duration of signal
        :return:
        """

        time = np.linspace(0, seconds, seconds * fs, False)

        note = np.sin(frequency * time * 2 * np.pi)

        # Assure highest value in 16 bit range
        audio = note * (pow(2, 15) - 1) / np.max(np.abs(note))
        audio = audio.astype(np.int16)

        return audio

    return _make_sine


@pytest.fixture(scope='module')
def record_audio():
    """ Audio record factory """

    def _record_audio(fs, seconds):
        """
        Records sound with desired sampling frequency and duration
        :param fs: Sampling frequency
        :param seconds: Duration
        :return:
        """

        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        return recording

    return _record_audio


@pytest.fixture(scope='module')
def save_audio_file():
    """ Saving audio factory """

    def _save_audio(audio_data, filename, fs):
        """
        Saving audio data as wave file
        :param audio_data: Data to be saved as audio
        :param filename: Name of the wav file
        :param fs: Sampling frequency
        :return:
        """

        full_file_name = filename + '.wav'
        wavfile.write(full_file_name, fs, audio_data)

    return _save_audio


@pytest.fixture(scope='module')
def open_wave():
    """ Wave files factory to play """

    audio_files_root = './'

    def _open_file(filename):
        """
        Open given wave file
        :param filename: File to open
        :return:
        """

        filepath = audio_files_root + filename
        fs, data = wavfile.read(filepath)

        return fs, data

    return _open_file
