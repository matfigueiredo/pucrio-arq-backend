from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models.auth import VerificationCode
from app.schemas.auth import EmailRequest, CodeVerification, TokenResponse
from app.services.auth import generate_verification_code, create_jwt_token
from app.services.email import send_verification_code

router = APIRouter()


@router.post("/request-code", status_code=200)
async def request_code(
    request: EmailRequest, db: Session = Depends(get_db)
) -> dict:
    code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    verification_code = VerificationCode(
        email=request.email,
        code=code,
        expires_at=expires_at,
        used=False,
    )

    db.add(verification_code)
    db.commit()

    send_verification_code(request.email, code)

    return {"message": "Verification code sent", "email": request.email}


@router.post("/verify-code", response_model=TokenResponse)
async def verify_code(
    request: CodeVerification, db: Session = Depends(get_db)
) -> TokenResponse:
    verification_code = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.email == request.email,
            VerificationCode.code == request.code,
            VerificationCode.used == False,
            VerificationCode.expires_at > datetime.utcnow(),
        )
        .first()
    )

    if not verification_code:
        raise HTTPException(
            status_code=400, detail="Invalid or expired verification code"
        )

    verification_code.used = True
    db.commit()

    token = create_jwt_token(request.email)

    return TokenResponse(token=token)


@router.post("/verify-token", status_code=200)
async def verify_token(
    token: str,
) -> dict:
    from app.services.auth import verify_jwt_token

    email = verify_jwt_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"valid": True, "email": email}

