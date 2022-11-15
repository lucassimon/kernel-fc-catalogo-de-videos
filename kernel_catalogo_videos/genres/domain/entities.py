"""
Define uma entidade
"""
# Python
from typing import Optional
from datetime import datetime
from dataclasses import field, dataclass

# Third

# Apps
from kernel_catalogo_videos.core.utils import ACTIVE_STATUS, now, uuidv4


@dataclass()
class Genre:
    """
    Representa os dados da entidade genero
    """

    title: str
    slug: str
    status: Optional[int] = ACTIVE_STATUS
    is_deleted: bool = False
    code: Optional[str] = field(default_factory=uuidv4)
    created_at: Optional[datetime] = field(default_factory=now)
