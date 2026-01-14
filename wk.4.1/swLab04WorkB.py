import lib601.poly as poly
import swLab04SignalDefinitions
reload(swLab04SignalDefinitions) # so changes you make in swLab04SignalDefinitions.py will be reloaded
from swLab04SignalDefinitions import *


cosine_signal = CosineSignal(omega=2, phase=0.5)
unit_sample_signal = UnitSampleSignal()
constant_signal = ConstantSignal(5)
step_signal = StepSignal()

cosine_signal.plot(start=0, end=100, newWindow='Cosine Signal')
unit_sample_signal.plot(start=0, end=10, newWindow='Unit Sample Signal')
constant_signal.plot(start=0, end=10, newWindow='Constant Signal')
step_signal.plot(start=0, end=10, newWindow='Step Signal')

summed_signal = cosine_signal + unit_sample_signal
scale_signal = 3 * constant_signal

r_signal = R(cosine_signal)
rn_signal = Rn(unit_sample_signal, 3)

print(summed_signal.sample(10))
print(scale_signal.sample(5))
print(r_signal.sample(2))
print(rn_signal.sample(4))