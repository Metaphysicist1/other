# script running: python -m pip install ... etc

#///////////////////////////////////////////////////
'''
Code below provides essential preprocessing work in Speech recognition tasks.


#FOR IMPROVEMENT
code should be flexible for stereo/mono audios, we should check that firsty and
after that follow workflow.
'''
#///////////////////////////////////////////////////




from scipy.io import wavfile
from pydub import  AudioSegment
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

#put your filename below
filename = "maybe-next-time.wav"


# 1. FIRST PART WAV/MP3 TO VEC
#NOTE WAV_TO_VEC returns VEC/MTRX of data
def WAV_TO_VEC(filename):

    try:
        #NOTE check if audio is wav, handle with scipy
        if filename.endswith(".wav"):
            sr_wav, data_wav = wavfile.read(filename)
            D = dict()
            D["data"],D["sr"]=np.array(data_wav,dtype=float),sr_wav

            return D

        #NOTE pydub work with other audio formats
        else:
            audio = AudioSegment.from_file(filename)
            audio_data = np.array(audio.get_array_of_samples(),dtype=float)
            D = dict()
            D["data"],D["sr"]=audio_data,audio.frame_rate

            return D

    except FileNotFoundError:
        print("File not found. FileNotFoundError occured.")




# 2. SECOND PART WORD DETECTION

#NOTE get vec
WAV_TO_VEC(filename)

#NOTE DETECTING FUNCTION gets two parameter first is audio data, second flag
# for performing audio protting

print(VEC)
def DETECT_WORDS(VEC, plot=False):
    #NOTE computing energy of starting points in data segments
    oenv = librosa.onset.onset_strength(y=VEC["data"],sr=VEC["sr"])
    #NOTE time detector
    times = librosa.times_like(oenv)
    onset_raw = librosa.onset.onset_detect(onset_envelope=oenv,
                                            backtrack=False)
    #NOTE finding local minimums in data
    FFT_VEC = np.abs(librosa.stft(y=VEC["data"]))
    rms = librosa.feature.rms(S=FFT_VEC)

    onset_bt_rms = librosa.onset.onset_backtrack(onset_raw,rms[0])

    if plot:



        plt.plot(times, oenv, label='Onset strength')
        #ax.vlines(librosa.frames_to_time(onset_raw), 0, oenv.max(), label='Raw onsets')
        plt.vlines(librosa.frames_to_time(onset_bt_rms), 0, oenv.max(), label='Backtracked', color='r')
        plt.legend()

        plt.show()
    return onset_bt_rms
    #NOTE







def LINEAR_SPEC():
    #NOTE data -> transformed data
    STFT = librosa.stft(VEC["data"])
    #NOTE transformed data -> dB values for spectogram
    db_STFT = librosa.amplitude_to_db(np.abs(STFT), ref=np.max)

    fig, ax = plt.subplots()
    img = librosa.display.specshow(db_STFT,x_axis="time",y_axis="linear",ax=ax)
    fig.colorbar(img, ax=ax, format="%+2.f dB")

    plt.show()

def LOG_SPEC():
    #NOTE data -> transformed data
    STFT = librosa.stft(VEC["data"])
    #NOTE transformed data -> dB values for spectogram
    db_STFT = librosa.amplitude_to_db(np.abs(STFT), ref=np.max)

    fig, ax = plt.subplots()
    img = librosa.display.specshow(db_STFT,x_axis="time",y_axis="log",ax=ax)
    fig.colorbar(img, ax=ax, format="%+2.f dB")

    plt.show()

#LOG_SPEC()