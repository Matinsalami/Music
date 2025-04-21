import ffmpeg
from scipy.signal import butter, lfilter
import scipy.io.wavfile as wav
import numpy as np
_AUDIO_FILE_ = "audio.wav"

def fileSaver(fileObj):
    fileObj.save(fileObj.filename)
    return 

def upscaler(tw, th, filename):
    stream = ffmpeg.input(filename)
    stream = stream.filter("scale", w=tw, h=th) 
    stream = stream.output(f'processedFile.{filename.split(".")[1]}')
    stream.run()
    return 



def makePhoneLike(filterOrder, sideGain, filename):
    global _AUDIO_FILE_
    vid = ffmpeg.input(filename).video
    au = ffmpeg.input(filename).audio
    info = ffmpeg.probe(filename, cmd="ffprobe") # metadata of the file! 
    noChannels = info["streams"][1]["channels"] # extract number of channels from original file
    audioStream = au.output(_AUDIO_FILE_, ac=(noChannels if sideGain else 1)).overwrite_output().run()

    sample_rate, samples_original = wav.read(_AUDIO_FILE_)
    num, denom = butter(filterOrder,  [800, 12000] , "bandpass", fs=sample_rate)
    ot = lfilter(num, denom, samples_original)
    data2 = np.asarray(ot, dtype=np.int16) 
    wav.write(_AUDIO_FILE_, sample_rate, data2)

    auInpF = ffmpeg.input(_AUDIO_FILE_)

    ffmpeg.output(vid, auInpF, f"./static/{_AUDIO_FILE_}").overwrite_output().run()

    # ot = ffmpeg.output(prob, au, "video.mp4")
    return 
