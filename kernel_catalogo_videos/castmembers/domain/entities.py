"""
Define uma entidade
"""
# pylint: disable=duplicate-code


# Python
from typing import Any, Dict, Optional
from datetime import datetime
from dataclasses import field, dataclass

# Apps
from kernel_catalogo_videos.core.utils import KIND_ACTOR, ACTIVE_STATUS, now
from kernel_catalogo_videos.core.domain.entities import Entity


@dataclass(kw_only=True, frozen=True, slots=True)
class CastMember(Entity):
    """
    Representa os dados da entidade cast member
    """

    name: str
    kind: int = KIND_ACTOR
    status: Optional[int] = ACTIVE_STATUS
    is_deleted: bool = False
    created_at: Optional[datetime] = field(default_factory=now)

    def __post_init__(self):
        pass

    def update(self, data: Dict[str, Any]):
        """
        Atualiza os dados internos da entidade
        """
        for field_name, value in data.items():
            self._set(field_name, value)

        pass
