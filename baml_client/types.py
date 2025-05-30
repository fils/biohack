###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml-py
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off
import baml_py
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing_extensions import TypeAlias
from typing import Dict, Generic, List, Literal, Optional, TypeVar, Union


T = TypeVar('T')
CheckName = TypeVar('CheckName', bound=str)

class Check(BaseModel):
    name: str
    expression: str
    status: str

class Checked(BaseModel, Generic[T,CheckName]):
    value: T
    checks: Dict[CheckName, Check]

def get_checks(checks: Dict[CheckName, Check]) -> List[Check]:
    return list(checks.values())

def all_succeeded(checks: Dict[CheckName, Check]) -> bool:
    return all(check.status == "succeeded" for check in get_checks(checks))



class NanoPred(str, Enum):
    
    HAS_DIGITAL_OBJECT_TYPE = "HAS_DIGITAL_OBJECT_TYPE"
    HAS_MEDIA_TYPE = "HAS_MEDIA_TYPE"
    HAS_ACCESS_URI = "HAS_ACCESS_URI"
    HAS_PUBLISHER = "HAS_PUBLISHER"
    HAS_PUBLICATION_DATE = "HAS_PUBLICATION_DATE"
    HAS_VERSION = "HAS_VERSION"
    USES_FIP = "USES_FIP"
    HAS_LICENSE = "HAS_LICENSE"
    HAS_LANGUAGE = "HAS_LANGUAGE"
    HAS_DOMAIN = "HAS_DOMAIN"
    HAS_TITLE = "HAS_TITLE"
    HAS_DESCRIPTION = "HAS_DESCRIPTION"
    HAS_FUNDER = "HAS_FUNDER"
    HAS_PROJECT_ID = "HAS_PROJECT_ID"
    CREATOR = "CREATOR"
    CONTRIBUTOR = "CONTRIBUTOR"
    HAS_CONTACT_POINT = "HAS_CONTACT_POINT"
    HAS_WEBSITE = "HAS_WEBSITE"
    HAS_START_DATE = "HAS_START_DATE"
    HAS_END_DATE = "HAS_END_DATE"
    IS_PART_OF = "IS_PART_OF"
    IS_IN_RESPONSE_TO = "IS_IN_RESPONSE_TO"
    HAS_PROJECT_PRE_REGISTRATION = "HAS_PROJECT_PRE_REGISTRATION"
    HAS_PROJECT_PROPOSAL = "HAS_PROJECT_PROPOSAL"
    HAS_MEMBERS = "HAS_MEMBERS"
    HAD_BUDGET = "HAD_BUDGET"
    HAS_ETHICS_CLEARANCE = "HAS_ETHICS_CLEARANCE"
    HAS_CONSORTIUM_AGREEMENT = "HAS_CONSORTIUM_AGREEMENT"
    IS_OUTPUT_OF_PROJECT = "IS_OUTPUT_OF_PROJECT"
    HAS_BEEN_REPOSED = "HAS_BEEN_REPOSED"
    HAS_REPOSITORY_PID = "HAS_REPOSITORY_PID"
    GENERATED_FROM_SAMPLE = "GENERATED_FROM_SAMPLE"
    HAS_DATASET = "HAS_DATASET"
    HAS_METHOD = "HAS_METHOD"
    HAS_IMAGE = "HAS_IMAGE"
    HAS_CODE = "HAS_CODE"
    HAS_DMP = "HAS_DMP"

class NanoPred2(str, Enum):
    
    Predict = "Predict"
    Classify = "Classify"
    Enhance = "Enhance"
    Suggest = "Suggest"
    Reveal = "Reveal"
    Support = "Support"
    AreBecoming = "AreBecoming"
    AreNotMakingAsManyConnectionsAsExpected = "AreNotMakingAsManyConnectionsAsExpected"
    ArePotentiallyBasedOn = "ArePotentiallyBasedOn"
    AreTrainedWith = "AreTrainedWith"
    CanReliablyCharacterize = "CanReliablyCharacterize"
    DemonstratedAnIncreaseInPredictionAccuracyTo = "DemonstratedAnIncreaseInPredictionAccuracyTo"
    Determines = "Determines"
    FaceChallengesWhenGeneralizedTo = "FaceChallengesWhenGeneralizedTo"
    HasPlasmaCharacteristicsSimilarTo = "HasPlasmaCharacteristicsSimilarTo"
    HasPredictionAccuracyOf = "HasPredictionAccuracyOf"
    HaveSparkedInterestIn = "HaveSparkedInterestIn"
    IllustratesShortcomingsIn = "IllustratesShortcomingsIn"
    IsDecreasing = "IsDecreasing"
    IsIdentified = "IsIdentified"
    IsUsedFor = "IsUsedFor"
    IsUsedToSimulate = "IsUsedToSimulate"
    Used = "Used"

class Assertion(BaseModel):
    Cardinal: List[str]
    Supporting: List[str]

class Idea(BaseModel):
    hypothesis: List[str]
    supportingArguments: List[str]
    researchOpportunities: List[str]
    methodology: List[str]
    results: List[str]
    conclusions: List[str]
    limitations: List[str]
    futureDirections: List[str]
    keyFindings: List[str]
    references: List[str]

class Nanograph(BaseModel):
    triples: List["Nanopub"]

class Nanopub(BaseModel):
    subject: str
    predicate: "NanoPred2"
    object: str
