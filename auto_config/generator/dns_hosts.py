from __future__ import annotations

from collections.abc import Sequence

from ..device import Device
from ..field import DefaultExtraField
from .base import GeneratorBase


class DNSHostsGenerator(GeneratorBase):
    def __init__(
        self,
        devices: Sequence[Device[DefaultExtraField]],
        group: str,
        domain: str = "bone6.com",
    ):
        super().__init__()
        self.devices = devices
        self.group = group
        self.domain = domain

    def generate(self):
        hosts = []
        for device in self.devices:
            if device.group != self.group:
                continue

            if device.extra.dns is None:
                continue

            if device.extra.dns.private is None:
                continue

            hosts.append(f"{device.extra.dns.private} {device.get_domain()}.{self.domain}")

        self._generated_code = "\n".join(hosts)
