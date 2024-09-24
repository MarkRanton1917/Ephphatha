import sys
import numpy as np
import matplotlib.pyplot as plt
from Ephphatha.LibreSDR import LibreSDR
from Ephphatha.Radio import *


def main(argv):

    buffer_size = 2048
    sample_rate = int(4096e3)
    rx_channel_params = ChannelParams(
        int(434e6),
        Gain("slow_attack", None),
        sample_rate
    )

    tx_channel_params = ChannelParams(
        int(434e6),
        Gain("manual", 0.0),
        sample_rate
    )

    assert len(argv) == 2
    sdr = LibreSDR(
        TransceiverParams(
            rx_channels=[rx_channel_params] * 2,
            tx_channels=[tx_channel_params] * 2,
            sample_rate=sample_rate,
            buffer_size=buffer_size
        ),
        argv[1]
    )

    fs = int(sample_rate)
    N = 1024
    fc = int(1000000 / (fs / N)) * (fs / N)
    ts = 1 / float(fs)
    t = np.arange(0, N * ts, ts)
    i = np.cos(2 * np.pi * t * fc) * 2 ** 14
    q = np.sin(2 * np.pi * t * fc) * 2 ** 14
    iq = i + 1j * q
    sdr.set_tx_continuous(True)
    sdr.transmit(iq)

    sdr.set_rx_channel(1, True)
    x = np.linspace(0, buffer_size, buffer_size)
    data = np.abs(sdr.receive())
    plt.plot(x, data[0])
    plt.plot(x, data[-1])
    plt.show()


if __name__ == '__main__':
    main(sys.argv)
