from __future__ import annotations

import os
from sys import stdout

import toml
from loguru import logger
from pydantic import ValidationError

from .device import Device
from .field import BaseExtraField, DefaultExtraField
from .generator import (
    AnsibleHostsGenerator,
    DNSHostsGenerator,
    DNSManagerGenerator,
    SSHHostsGenerator,
)
from .service import Service


def get_devices[T: BaseExtraField](
    devices_config: list[dict], extra_field_cls: type[T] = BaseExtraField
) -> list[Device[T]]:
    devices = []
    for device in devices_config:
        try:
            extra_field_cls.model_validate(device.get("extra", {}))
            devices.append(Device[extra_field_cls].model_validate(device))
        except ValidationError as e:
            logger.warning(f"device has invalid extra field: {e}")
            continue
    return devices


def get_services(services_config: list[dict]) -> list[Service]:
    services = []
    for service in services_config:
        services.append(Service.model_validate(service))
    return services


def generate_config(
    path: str = "~/.config/autoconfig/config.toml",
    *,
    groups: list[str] | None = None,
    gateway_group: str | None = None,
    log_level="INFO",
):
    logger.remove()
    logger.add(stdout, level=log_level)
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    with open(path) as f:
        config = toml.load(f)
    devices = get_devices(config["devices"], DefaultExtraField)
    generator = AnsibleHostsGenerator(devices)
    generator.write("~/.config/ansible/hosts")
    generator = SSHHostsGenerator(devices, domain=config.get("domain", "bone6.com"))
    generator.write("~/.ssh/config")
    generator = DNSManagerGenerator(devices, extra_groups=groups)
    # TODO: `ddns.json` is not only ddns, so we need a better name.
    generator.write("~/.config/dns-manager/ddns.json")
    if gateway_group is not None:
        generator = DNSHostsGenerator(devices, group=gateway_group)
        generator.write("/var/mosdns/hosts")
