from __future__ import annotations

from collections.abc import Sequence

from ..service import Service
from .base import GeneratorBase


class CaddyFileGenerator(GeneratorBase):
    def __init__(self, services: Sequence[Service], domain: str = "bone6.com"):
        super().__init__()
        self.services = services
        self.domain = domain

    def generate(self):
        for service in self.services:
            self.add_block(f"{service.get_domain()}.{self.domain} {{", "}", indentation=4)
            self.add_line(f"reverse_proxy {service.target}")
            self.add_line("tls {")
            self.add_line("    dns dnspod {$DNSPOD_ID},{$DNSPOD_TOKEN}")
            self.add_line("}")
        super().generate()
