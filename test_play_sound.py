import sounddevice as sd
import pytest
from audio_tools import make_sine, save_audio_file, open_wave, record_audio


def test_save_sine(make_sine, save_audio_file):
    """
    ERROR:
    ALSA lib pcm.c:8306:(snd_pcm_recover) underrun occurred
    """

    frequency = 440
    fs = 44100
    duration = 7

    audio = make_sine(frequency, fs, duration)
    save_audio_file(audio, 'sine', fs)


@pytest.mark.skip
def test_play_wav(open_wave):
    """
    Play recorded sound
    ERROR:
    ALSA lib pcm.c:8306:(snd_pcm_recover) underrun occurred
    """

    fs, data = open_wave('output.wav')
    sd.play(data, fs)


def test_record_output(record_audio, save_audio_file):
    """ Record sound """

    time = 3
    fs = 44100

    audio = record_audio(fs, time)
    save_audio_file(audio, 'output', fs)
