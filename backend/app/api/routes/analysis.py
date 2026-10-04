import time
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status

from app.core.config import settings
from app.core.logging import log_operational_event
from app.core.rate_limit import rate_limit_guard
from app.core.security import SSRFSecurityError, URLLengthExceededError, URLValidationError
from app.ingestion.image import (
    ImageSizeExceededError,
    ImageValidationError,
    UnsupportedImageTypeError,
)
from app.ingestion.text import MessageLengthExceededError, MessageValidationError
from app.schemas.analysis import MessageAnalysisRequest, URLAnalysisRequest, URLAnalysisResponse
from app.services.unified_analyzer import analyze_message_service, analyze_screenshot_service
from app.services.url_analyzer import analyze_url_service

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post(
    "/url",
    response_model=URLAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Safely fetch and analyze webpage structure and trust signals",
    description=(
        "Validates the submitted URL against strict SSRF rules, fetches HTML content "
        "within strict size/redirect caps, and extracts structured metadata, links, "
        "and factual claims without claiming verification."
    ),
    dependencies=[Depends(rate_limit_guard("url", settings.RATE_LIMIT_URL_PER_MINUTE))],
)
async def analyze_url_endpoint(payload: URLAnalysisRequest, request: Request) -> URLAnalysisResponse:
    start_time = time.time()
    try:
        result = await analyze_url_service(payload.url)
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_url_success",
            status_code=200,
            duration_ms=duration_ms,
            extra={"input_type": "URL", "target_url": payload.url},
        )
        return result
    except URLLengthExceededError as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_url_rejected",
            status_code=413,
            duration_ms=duration_ms,
            error_category="URL_LENGTH_EXCEEDED",
        )
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail={
                "error_type": "PAYLOAD_TOO_LARGE",
                "message": str(exc),
            },
        )
    except SSRFSecurityError as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_url_blocked",
            status_code=400,
            duration_ms=duration_ms,
            error_category="SSRF_SECURITY_BLOCK",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_type": "SSRF_SECURITY_BLOCK",
                "message": str(exc),
            },
        )
    except URLValidationError as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_url_invalid",
            status_code=400,
            duration_ms=duration_ms,
            error_category="URL_VALIDATION_ERROR",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_type": "URL_VALIDATION_ERROR",
                "message": str(exc),
            },
        )
    except Exception as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_url_error",
            status_code=500,
            duration_ms=duration_ms,
            error_category=type(exc).__name__,
        )
        # Prevent stack trace leakage in accordance with SECURITY.md
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_type": "INTERNAL_ANALYSIS_ERROR",
                "message": "An unexpected error occurred while analyzing the target URL.",
            },
        )


@router.post(
    "/message",
    response_model=URLAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze copied or pasted financial message/chat text",
    description=(
        "Normalizes submitted message text, extracts financial claims, regulatory references, "
        "entities, urgency cues, and feeds them into the shared evidence & risk intelligence pipeline."
    ),
    dependencies=[Depends(rate_limit_guard("message", settings.RATE_LIMIT_MESSAGE_PER_MINUTE))],
)
async def analyze_message_endpoint(payload: MessageAnalysisRequest, request: Request) -> URLAnalysisResponse:
    start_time = time.time()
    try:
        result = await analyze_message_service(payload.text)
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_message_success",
            status_code=200,
            duration_ms=duration_ms,
            payload_size_bytes=len(payload.text.encode("utf-8")),
            extra={"input_type": "MESSAGE"},
        )
        return result
    except MessageLengthExceededError as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_message_rejected",
            status_code=413,
            duration_ms=duration_ms,
            error_category="MESSAGE_LENGTH_EXCEEDED",
        )
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail={
                "error_type": "PAYLOAD_TOO_LARGE",
                "message": str(exc),
            },
        )
    except MessageValidationError as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_message_invalid",
            status_code=400,
            duration_ms=duration_ms,
            error_category="MESSAGE_VALIDATION_ERROR",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_type": "MESSAGE_VALIDATION_ERROR",
                "message": str(exc),
            },
        )
    except Exception as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_message_error",
            status_code=500,
            duration_ms=duration_ms,
            error_category=type(exc).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_type": "INTERNAL_ANALYSIS_ERROR",
                "message": "An unexpected error occurred while analyzing the submitted message.",
            },
        )


@router.post(
    "/screenshot",
    response_model=URLAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze uploaded screenshot image using local/offline OCR",
    description=(
        "Validates image format and size, extracts optical text using local offline OCR, "
        "and routes the extracted text into the structured evidence, risk assessment, "
        "Trust Chain, and Scam Journey pipeline without cloud API transmission or permanent storage."
    ),
    dependencies=[Depends(rate_limit_guard("screenshot", settings.RATE_LIMIT_SCREENSHOT_PER_MINUTE))],
)
async def analyze_screenshot_endpoint(
    request: Request,
    file: UploadFile = File(..., description="Uploaded screenshot image file (PNG, JPEG, WEBP)"),
) -> URLAnalysisResponse:
    start_time = time.time()
    try:
        # Validate that a file was supplied
        if not file.filename:
            raise ImageValidationError("No file uploaded or filename is missing.")

        file_bytes = await file.read()

        # Enforce file size limit immediately before parsing
        if len(file_bytes) > settings.MAX_IMAGE_BYTES:
            raise ImageSizeExceededError(
                f"Image payload size ({len(file_bytes)} bytes) exceeds the maximum limit of {settings.MAX_IMAGE_BYTES} bytes (10MB)."
            )

        result = await analyze_screenshot_service(
            file_bytes=file_bytes,
            filename=file.filename,
            content_type=file.content_type,
        )
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_screenshot_success",
            status_code=200,
            duration_ms=duration_ms,
            payload_size_bytes=len(file_bytes),
            extra={"input_type": "SCREENSHOT", "filename": file.filename},
        )
        return result
    except ImageSizeExceededError as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_screenshot_rejected",
            status_code=413,
            duration_ms=duration_ms,
            error_category="IMAGE_SIZE_EXCEEDED",
        )
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail={
                "error_type": "PAYLOAD_TOO_LARGE",
                "message": str(exc),
            },
        )
    except (UnsupportedImageTypeError, ImageValidationError) as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_screenshot_invalid",
            status_code=400,
            duration_ms=duration_ms,
            error_category="IMAGE_VALIDATION_ERROR",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_type": "IMAGE_VALIDATION_ERROR",
                "message": str(exc),
            },
        )

    except Exception as exc:
        duration_ms = (time.time() - start_time) * 1000
        log_operational_event(
            event_type="analyze_screenshot_error",
            status_code=500,
            duration_ms=duration_ms,
            error_category=type(exc).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_type": "INTERNAL_ANALYSIS_ERROR",
                "message": "An unexpected error occurred while processing the uploaded screenshot.",
            },
        )

