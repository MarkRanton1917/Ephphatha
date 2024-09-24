import abc
import numpy as np
import typing as tp


class Gain:
    def __init__(
            self,
            gain_type: str,
            value: tp.Union[float, None] = None
    ):
        self.type = gain_type
        self.value = value


class ChannelParams:
    def __init__(
            self,
            center_frequency: int = int(100e6),
            gain: Gain = Gain("auto", None),
            bandwidth: int = int(100e3)
    ):
        self.center_frequency = center_frequency
        self.gain = gain
        self.bandwidth = bandwidth


class TransceiverParams:
    def __init__(
            self,
            rx_channels: list[ChannelParams],
            tx_channels: list[ChannelParams],
            sample_rate: int = int(1e6),
            buffer_size: int = 1024
    ):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.rx_channels = rx_channels
        self.tx_channels = tx_channels


class Transceiver(abc.ABC):

    def __init__(self, params: TransceiverParams):
        self.params = params

    @abc.abstractmethod
    def set_rx_channel(self, channel: int, enable: bool) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def set_tx_channel(self, channel: int, enable: bool) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def set_tx_continuous(self, enable: bool) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def transmit(self, values: list[np.ndarray]) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def receive(self) -> tp.Optional[list[np.ndarray]]:
        raise NotImplementedError

