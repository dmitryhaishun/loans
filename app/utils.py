import enum


class LoanProductType(enum.StrEnum):
    STUDENT_LOAN = "Student loan"
    AUTO_LOAN = "Auto loan"
    MORTGAGE_LOAN = "Mortgage loan"


class LoanStage(enum.Enum):
    LOAN_VERIFICATION = "Loan Verification"
    LOAN_PROCESSING = "Loan Processing"
    UNDERWRITING = "Underwriting"
    CLOSURE = "Closure"
    NONE = None


class LoanCurrency(enum.StrEnum):
    USD = "USD"
    EUR = "EUR"


class LoanType(enum.StrEnum):
    LOANS = "loans"
    LOAN_APPLICATIONS = "applications"


class LoanStatus(enum.StrEnum):
    ACTIVE = "Active"
    PAID_OFF = "Paid off"
    DEBT = "Debt"
    APPROVED = "Approved"
    IN_REVIEW = "In review"
    IN_PROGRESS = "In progress"
    DRAFT = "Draft"


class AvailableCurrencies(enum.StrEnum):
    USD = "USD"
    EUR = "EUR"


loan_statuses = [
    LoanStatus.ACTIVE,
    LoanStatus.DEBT,
    LoanStatus.PAID_OFF,
]

loan_application_statuses = [
    LoanStatus.APPROVED,
    LoanStatus.IN_REVIEW,
    LoanStatus.IN_PROGRESS,
    LoanStatus.DRAFT,
]
