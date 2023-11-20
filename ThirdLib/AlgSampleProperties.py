from ThirdLib.AlgSignalUtil import concatenateTimeSeries, calRangeOfFrequency
import numpy as np
from numpy.fft import fft
from scipy import signal
#与C#版本的配置文件一样，文件中函数提取FrequencyAnalysisUtil.py中
class SampleProperties:
    def __init__(self, refT, refX, sampT, sampX, d, mode='none', lowLimit=0.3, upLimit=0.5, denoise=False):
        if mode not in ['linear_fit', 'phase_comp', 'none']:
            raise ValueError("The mode should be linear_fit, phase_comp")
        self.refT = refT[:]
        self.refX = refX[:]
        self.sampT = sampT[:]
        self.sampX = sampX[:]
        self.d = d
        self.mode = mode
        self.lowLimit = lowLimit
        self.upLimit = upLimit
        self.denoise = denoise
        self.__calTransFunction()

    def calRefractiveIndex(self):
        c = 3e8
        refractiveIndex = self.__phaseTransFunction * c
        refractiveIndex /= (2 * np.pi * 1e9)
        refractiveIndex /= self.f
        refractiveIndex /= self.d
        refractiveIndex += 1

        return refractiveIndex

    def calExtinction(self):

        refractiveIndex = self.calRefractiveIndex()
        refractiveIndex = np.mean(refractiveIndex[(self.f > 0.6) & (self.f < 1.6)])
        absorptionRate = 4 * refractiveIndex
        absorptionRate /= self.__ampTransFunction
        absorptionRate /= np.power(refractiveIndex + 1, 2)
        if np.min(absorptionRate) < 0:
            absorptionRate = absorptionRate - np.min(absorptionRate) + 1
        absorptionRate = np.log(absorptionRate)

        # Convert the unit to cm^-1
        absorptionRate = absorptionRate * 0.3 / (self.d * self.f)

        return absorptionRate

    def calAbsorptionRate(self):

        refractiveIndex = self.calRefractiveIndex()
        refractiveIndex = np.mean(refractiveIndex[(self.f > 0.6) & (self.f < 1.6)])
        absorptionRate = 4 * refractiveIndex
        absorptionRate /= self.__ampTransFunction
        absorptionRate /= np.power(refractiveIndex + 1, 2)
        if np.min(absorptionRate) < 0:
            absorptionRate = absorptionRate - np.min(absorptionRate) + 1
        absorptionRate = np.log(absorptionRate)

        # Convert the unit to cm^-1
        absorptionRate *= 2 / (self.d * 0.1)

        return absorptionRate

    def calAbsorptionRatio(self, absorption, d):
        absorption_ratio = np.exp(-absorption * d)
        absorption_ratio[absorption_ratio > 1] = 0
        return absorption_ratio

    def calPSD(self, sample_value):
        ff, psd = signal.welch(sample_value, fs=100, nperseg=sample_value.shape[0])
        psd = 10 * np.log10(psd)
        return ff, psd

    #####################################Private Methods#######################

    def __calPhaseAndAmplitude(self, t, refX, sampX, indices):
        refXf = fft(refX)
        sampXf = fft(sampX)

        xf = sampXf / refXf
        amplitudes = np.abs(xf)
        phase = np.angle(xf)

        return phase[indices], amplitudes[indices]

    def __calPhaseAndAmplitude1(self, t, refX, sampX):
        refXf = fft(refX)
        sampXf = fft(sampX)

        xf = sampXf / refXf
        amplitudes = np.abs(xf)
        phase = np.angle(xf)

        return phase, amplitudes

    def __calTransFunction(self):
        # The default length of the time signal
        defDuration = 1
        sampDuration = self.sampT[-1] - self.sampT[0]
        refDuration = self.refT[-1] - self.refT[0]

        # Concatenate the time series to the default duration or the longer duration
        # of the reference series and the sample series
        duration = max(defDuration, sampDuration, refDuration)
        newSampT, newSampX = concatenateTimeSeries(self.sampT, self.sampX, duration)
        self.sampX = newSampX
        _, newRefX = concatenateTimeSeries(self.refT, self.refX, duration)
        self.refX = newRefX
        f, _ = calRangeOfFrequency(newSampT, len(newSampT), True)
        f = np.array(f)

        # The frequency spectrum below 0.1 THz may contain peculiar values, therefore remove the portion below 0.1 THz
        self.f = f
        self.refraction_ratio = np.abs(np.fft.fft(self.refX)) / np.abs(np.fft.fft(self.sampX))
        self.refraction_ratio = self.refraction_ratio

        phaseTrans, self.__ampTransFunction = self.__calPhaseAndAmplitude1(newSampT, newRefX, newSampX)

        # Correct the jumps between consecutive phase shifts to be within pi.
        phaseTrans = -np.unwrap(phaseTrans)


        f1 = np.argmin(np.abs(f - 0.2))
        f2 = np.argmin(np.abs(f - 0.6))

        t = range(len(f[f1:f2])) + f1
        params = np.polyfit(t, phaseTrans[f1:f2], 1)
        phaseTrans = phaseTrans - params[1]

        if self.mode == 'phase_comp':
            indices, theorPhase = self.__calTheoreticalPhase()
            phaseOffset = np.mean(phaseTrans[indices] - theorPhase) / np.pi
            phaseOffset = np.round(phaseOffset) * np.pi
            self.__phaseTransFunction = phaseTrans - phaseOffset
        else:
            self.__phaseTransFunction = phaseTrans

    def __calculateSlope(self, phase, f):
        """ Use y = x * k to estimate k, thereby trans(x) * y = trans(x) * x * k, to assure that the fitted line goes
        through the origin."""
        phase = np.array(phase)
        f = np.array(f)
        x = np.sum(np.power(phase, 2))
        y = np.sum(np.multiply(phase, f))
        k = y / x
        return k

    def __linearFitRefractIndex(self):
        """Make linear fitting to the sample's refractive index

        Args:
            see calAbsorptionRate

        Returns:
            a float representing the corrected refractive index
        """
        # Fit the phase shift
        indicef = np.array(np.where((self.f >= self.lowLimit) & (self.f <= self.upLimit)))
        indicef = indicef.reshape(indicef.shape[1], )
        indices = indicef.tolist()

        f = self.f[indices]
        phaseTrans = self.__phaseTransFunction[indices]

        # Make linear fitting
        slope = self.__calculateSlope(phaseTrans, f)

        # The light speed
        c = 3e8
        factor = c / self.d / (2 * np.pi * 1e9)
        refractiveIndex = factor * slope + 1

        return refractiveIndex

    def __calTheoreticalPhase(self):
        """ Calculate the theoretical phase assuming no dispersion occurs in the sample
        """
        indicef = np.array(np.where((self.f >= self.lowLimit) & (self.f <= self.upLimit)))
        indicef = indicef.reshape(indicef.shape[1], )
        indices = indicef.tolist()

        f = self.f[indices]
        delay = self.__calTimeDelay()
        theorPhase = 2 * np.pi * f * delay

        return indices, theorPhase

    def __calTimeDelay(self):
        """Calculate the time delay of the primary peak of the sample signal by comparing with the reference signal."""
        refMaxIndex = np.argmax(np.array(self.refX))
        refPeakTime = self.refT[refMaxIndex]
        sampMaxIndex = np.argmax(np.array(self.sampX))
        sampPeakTime = self.sampT[sampMaxIndex]
        delay = sampPeakTime - refPeakTime

        return delay
