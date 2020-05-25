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
        audio = note * (pow(2, 12) - 1) / np.max(np.abs(note))
        audio = audio.astype(np.int16)

        return audio

    return _make_sine


@pytest.fixture(scope='module')
def record_audio():
    """ Audio record factory """

    def _record_audio(fs, seconds, record_filename):
        """
        Records sound with desired sampling frequency and duration
        :param fs: Sampling frequency
        :param seconds: Duration
        :param record_filename: Name of the file to record data to
        :return:
        """

        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()

        full_file_name = record_filename + '.wav'
        wavfile.write(full_file_name, fs, recording)

    return _record_audio


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


@pytest.mark.skip
def test_play_sine(make_sine):
    """
    ERROR:
    ALSA lib pcm.c:8306:(snd_pcm_recover) underrun occurred
    """
    audio = make_sine(440, 44100, 3)
    sd.play(audio, 44100)


def test_record(record_audio):
    """ Record sound """

    time = 3
    fs = 41000

    record_audio(fs, time, 'output')


@pytest.mark.skip
def test_play_wav(open_wave):
    """
    Play recorded sound
    ERROR:
    ALSA lib pcm.c:8306:(snd_pcm_recover) underrun occurred
    """

    fs, data = open_wave('output.wav')
    sd.play(data, fs)
