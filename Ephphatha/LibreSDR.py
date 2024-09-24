import adi
from lief import exception
from Ephphatha.Radio import *

class LibreSDR(Transceiver):

    def __init__(self, params: TransceiverParams, uri: str):

        def set_gain(gain):
            if gain == GainType.Auto:
                return "manual"
            else:
                return "slow_attack"

        super().__init__(params)

        assert len(params.tx_channels) == 2
        assert len(params.rx_channels) == 2

        self.sdr = adi.ad9361(uri)
        self.sdr.rx_lo = self.params.rx_channels[0].center_frequency
        self.sdr.tx_lo = self.params.tx_channels[0].center_frequency
        self.sdr.rx_rf_bandwidth = self.params.rx_channels[0].bandwidth
        self.sdr.tx_rf_bandwidth = self.params.tx_channels[0].bandwidth
        self.sdr.sample_rate = self.params.sample_rate
        self.sdr.rx_buffer_size = self.params.buffer_size

        #rx channel 0
        gain_type = self.params.rx_channels[0].gain.type
        self.sdr.gain_control_mode_chan0 = set_gain(gain_type)
        if gain_type != GainType.Auto:
            self.sdr.rx_hardwaregain_chan0 = set_gain(self.params.rx_channels[0].gain.value)
        #rx channel 1
        gain_type = self.params.rx_channels[1].gain.type
        self.sdr.gain_control_mode_chan1 = set_gain(gain_type)
        if gain_type != GainType.Auto:
            self.sdr.rx_hardwaregain_chan1 = set_gain(self.params.rx_channels[1].gain.value)

        tx_gain_0 = self.params.tx_channels[0].gain.value
        tx_gain_1 = self.params.tx_channels[1].gain.value
        assert tx_gain_0 is not None and tx_gain_1 is not None
        #tx channel 0
        self.sdr.tx_hardwaregain_chan0 = tx_gain_0
        #tx channel 1
        self.sdr.tx_hardwaregain_chan1 = tx_gain_1

        self.sdr.rx_enabled_channels = [0]
        self.sdr.tx_enabled_channels = [0]

    def set_rx_channel(self, channel: int, enable: bool) -> bool:
        if enable:
            if channel not in self.sdr.rx_enabled_channels:
                self.sdr.rx_enabled_channels.append(channel)
        else:
            self.sdr.rx_enabled_channels.remove(channel)
        return True

    def set_tx_channel(self, channel: int, enable: bool) -> bool:
        if enable:
            if channel not in self.sdr.tx_enabled_channels:
                self.sdr.tx_enabled_channels.append(channel)
        else:
            self.sdr.tx_enabled_channels.remove(channel)
        return True

    def set_tx_continuous(self, enable: bool) -> bool:
        self.sdr.tx_cyclic_buffer = enable
        return True

    def transmit(self, values: list[np.ndarray]) -> bool:
        try:
            if self.sdr.tx_cyclic_buffer:
                self.sdr.tx_destroy_buffer()
            if len(self.sdr.tx_enabled_channels) == 1 and type(values) is list:
                values = values[0]
            self.sdr.tx(values)
        except exception:
            return False
        return True

    def receive(self) -> tp.Optional[list[np.ndarray]]:
        try:
            ret = self.sdr.rx()
            if type(ret) is not list:
                ret = [ret]
        except exception:
            return None
        return ret