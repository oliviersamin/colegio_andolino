from .parent import ParentSerializer, ParentDetailSerializer
from .child import ChildSerializer, ChildDetailSerializer
from .teachers import TeacherSerializer, TeacherDetailSerializer
from .school_group import GroupSerializer, GroupDetailSerializer
from .document import DocumentSerializer, DocumentDetailSerializer
from .user import UserSerializer, UserDetailSerializer

__all__ = [
    ParentSerializer,
    ParentDetailSerializer,
    ChildSerializer,
    ChildDetailSerializer,
    TeacherSerializer,
    TeacherDetailSerializer,
    GroupSerializer,
    GroupDetailSerializer,
    DocumentSerializer,
    DocumentDetailSerializer,
    UserDetailSerializer,
    UserSerializer,
]
