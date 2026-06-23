"""Custom exceptions for clear error handling."""


class StudyRAGError(Exception):
    """Base exception for the application."""


class DocumentLoadError(StudyRAGError):
    """Raised when a document cannot be loaded or parsed."""

    def __init__(self, path: str, reason: str = "") -> None:
        self.path = path
        self.reason = reason
        msg = f"Failed to load document: {path}"
        if reason:
            msg += f" — {reason}"
        super().__init__(msg)


class IndexNotFoundError(StudyRAGError):
    """Raised when a FAISS index does not exist for a subject."""

    def __init__(self, subject: str) -> None:
        self.subject = subject
        super().__init__(f"No index found for subject: {subject}")


class APIError(StudyRAGError):
    """Raised when the DeepSeek API call fails."""

    def __init__(self, message: str = "API request failed") -> None:
        super().__init__(message)


class SubjectNotFoundError(StudyRAGError):
    """Raised when a subject folder does not exist in data/."""

    def __init__(self, subject: str) -> None:
        self.subject = subject
        super().__init__(f"Subject not found: {subject}")


class SessionNotFoundError(StudyRAGError):
    """Raised when a chat session does not exist."""

    def __init__(self, session_id: str, subject: str = "") -> None:
        self.session_id = session_id
        self.subject = subject
        msg = f"Session not found: {session_id}"
        if subject:
            msg += f" in subject: {subject}"
        super().__init__(msg)
