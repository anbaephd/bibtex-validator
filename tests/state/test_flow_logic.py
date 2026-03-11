# from dataclasses import dataclass

import pytest

from src import Component, ComponentSchemaMeta, ComponentType
from src.state.core import State

# @dataclass
# class RedisClientMock:
#     cache: dict[str, dict] = None

#     def __post_init__(self):
#         if self.cache is None:
#             self.cache = {}

#     def set_meta(self, key: str, value: dict) -> None:
#         self.cache[key] = value

#     def get_meta(self, key: str) -> dict | None:
#         return self.cache.get(key)


@pytest.fixture
def idle_comp():
    return Component(
        metadata=ComponentSchemaMeta(
            id="1",
            name="test",
            component_type=ComponentType.ML_COMPONENT,
        ),
    )


@pytest.fixture
def active_comp(idle_comp):
    idle_comp.active()
    return idle_comp


@pytest.fixture
def blocked_comp(idle_comp):
    idle_comp.blocked()
    return idle_comp


# def test_state_init_to_idle(idle_comp):

#     assert idle_comp.state.name == State.IDLE

#     idle_comp.delete()


# def test_state_init_to_blocked(idle_comp):

#     idle_comp.blocked()
#     assert idle_comp.state.name == State.BLOCKED


# def test_state_idle_to_blocked(idle_comp):
#     idle_comp.blocked()

#     assert idle_comp.state.name == State.BLOCKED


# def test_state_idle_to_active(idle_comp):
#     idle_comp.active()

#     assert idle_comp.state.name == State.ACTIVE


# def test_state_active_to_idle(active_comp):
#     active_comp.idle()

#     assert active_comp.state.name == State.IDLE


# def test_state_active_to_blocked(active_comp):
#     active_comp.blocked()

#     assert active_comp.state.name == State.BLOCKED


# # def test_state_init_to_active(idle_comp):
# #     with pytest.raises(AttributeError) as excinfo:
# #         idle_comp.active()
# #     assert "active" == excinfo.value.name


# def test_state_idle_to_init(idle_comp):
#     with pytest.raises(AttributeError) as excinfo:
#         idle_comp.init()
#     assert "init" == excinfo.value.name


# def test_state_active_to_init(active_comp):
#     with pytest.raises(AttributeError) as excinfo:
#         active_comp.init()
#     assert "init" == excinfo.value.name


# def test_state_blocked_to_init(blocked_comp):
#     with pytest.raises(AttributeError) as excinfo:
#         blocked_comp.init()
#     assert "init" == excinfo.value.name


# def test_state_blocked_to_idle(blocked_comp):
#     with pytest.raises(AttributeError) as excinfo:
#         blocked_comp.idle()
#     assert "idle" == excinfo.value.name


# def test_state_blocked_to_active(blocked_comp):
#     with pytest.raises(AttributeError) as excinfo:
#         blocked_comp.active()
#     assert "active" == excinfo.value.name
