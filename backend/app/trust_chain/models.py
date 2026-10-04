"""Data models for RakshaScan Financial Trust Chain."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TrustChainNodeType(str, Enum):
    CLAIM = "CLAIM"
    ENTITY = "ENTITY"
    REGISTRATION = "REGISTRATION"
    OFFICIAL_IDENTITY = "OFFICIAL_IDENTITY"
    WEBSITE = "WEBSITE"
    APP = "APP"
    SOCIAL_ACCOUNT = "SOCIAL_ACCOUNT"
    PAYMENT_IDENTITY = "PAYMENT_IDENTITY"


class TrustChainStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    CONTRADICTORY = "CONTRADICTORY"
    UNKNOWN = "UNKNOWN"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_OBSERVED = "NOT_OBSERVED"


class TrustChainRelationshipType(str, Enum):
    CLAIMS = "CLAIMS"
    REGISTERED_AS = "REGISTERED_AS"
    IDENTIFIED_AS = "IDENTIFIED_AS"
    OPERATES = "OPERATES"
    ASSOCIATED_WITH = "ASSOCIATED_WITH"
    LINKS_TO = "LINKS_TO"
    USES = "USES"
    RECEIVES_PAYMENT = "RECEIVES_PAYMENT"


class TrustChainNode(BaseModel):
    node_id: str
    node_type: str  # CLAIM, ENTITY, REGISTRATION, OFFICIAL_IDENTITY, WEBSITE, APP, SOCIAL_ACCOUNT, PAYMENT_IDENTITY
    label: str
    value: str
    status: str  # VERIFIED, UNVERIFIED, CONTRADICTORY, UNKNOWN, UNAVAILABLE, NOT_OBSERVED
    evidence_ids: List[str] = Field(default_factory=list)
    verification_ids: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TrustChainRelationship(BaseModel):
    relationship_id: str
    source_node_id: str
    target_node_id: str
    relationship_type: str  # CLAIMS, REGISTERED_AS, IDENTIFIED_AS, OPERATES, ASSOCIATED_WITH, LINKS_TO, USES, RECEIVES_PAYMENT
    status: str  # VERIFIED, UNVERIFIED, CONTRADICTORY, UNKNOWN, UNAVAILABLE, NOT_OBSERVED
    evidence_ids: List[str] = Field(default_factory=list)
    verification_ids: List[str] = Field(default_factory=list)
    explanation: str


class TrustChainSummary(BaseModel):
    total_nodes: int = 0
    total_relationships: int = 0
    verified_count: int = 0
    unverified_count: int = 0
    contradictory_count: int = 0
    unknown_count: int = 0
    unobserved_count: int = 0
    summary_text: str = ""


class TrustChainGraph(BaseModel):
    nodes: List[TrustChainNode] = Field(default_factory=list)
    relationships: List[TrustChainRelationship] = Field(default_factory=list)
    summary: TrustChainSummary = Field(default_factory=TrustChainSummary)
