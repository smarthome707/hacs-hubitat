from asyncio import Future
from typing import Any, Awaitable, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity

from tests.async_mock import Mock, call, patch


@patch("custom_components.hubitat.switch.create_and_add_entities")
@patch("custom_components.hubitat.switch.create_and_add_event_emitters")
async def test_setup_entry(create_emitters, create_entities) -> None:
    def _create_entities(*args: Any) -> Awaitable[List[Any]]:
        future: Future[List[Any]] = Future()
        future.set_result([])
        return future

    create_entities.side_effect = _create_entities

    create_emitters.return_value = Future()
    create_emitters.return_value.set_result(None)

    from custom_components.hubitat.switch import (
        async_setup_entry,
        HubitatSwitch,
        HubitatPowerMeterSwitch,
    )

    mock_hass = Mock(spec=["async_register"])
    mock_config_entry = Mock(spec=ConfigEntry)

    def add_entities(entities: List[Entity]) -> None:
        pass

    mock_add_entities = Mock(spec=add_entities)

    await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert create_entities.call_count == 3, "expected 3 calls to create entities"

    call1 = call(
        mock_hass, mock_config_entry, mock_add_entities, "switch", HubitatSwitch
    )
    call2 = call(
        mock_hass,
        mock_config_entry,
        mock_add_entities,
        "switch",
        HubitatPowerMeterSwitch,
    )
    call3 = call(
        mock_hass,
        mock_config_entry,
        mock_add_entities,
        "switch",
        HubitatPowerMeterSwitch,
    )
    assert create_entities.has_calls([call1, call2, call3])

    assert create_emitters.call_count == 1, "expected 1 call to create emitters"
