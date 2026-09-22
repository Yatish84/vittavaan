"""FastAPI dependency for identities verified by the separate auth-core service."""

from typing import Annotated, cast

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from vittavaan.domain.identity import VerifiedIdentity
from vittavaan.infrastructure.auth_core import (
    AuthCoreVerifier,
    AuthTokenRejectedError,
    AuthVerifierUnavailableError,
)

bearer_scheme = HTTPBearer(auto_error=False)


async def require_verified_identity(
    request: Request,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ],
) -> VerifiedIdentity:
    """Return verified identity facts; never infer household authorization."""

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    verifier = cast(AuthCoreVerifier, request.app.state.auth_core_verifier)
    try:
        return await verifier.verify(credentials.credentials)
    except AuthTokenRejectedError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from exc
    except AuthVerifierUnavailableError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE) from exc
