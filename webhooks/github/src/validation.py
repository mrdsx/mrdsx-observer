import hashlib
import hmac

from fastapi import HTTPException, status


def verify_signature(
    secret_token: str,
    payload: bytes,
    input_signature: str,
) -> None:
    """
    Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.
    """

    if len(input_signature.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="x-hub-signature-256 header is missing!",
        )

    hash_object = hmac.new(
        key=secret_token.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, input_signature):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request signatures didn't match!",
        )
