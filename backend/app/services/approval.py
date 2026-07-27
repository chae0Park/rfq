from app.models.result import ApprovalResult


class ApprovalService:

    def approve(
        self,
        approved: bool,
        approver: str,
        comments: str | None = None,
    ) -> ApprovalResult:

        return ApprovalResult(
            approved=approved,
            approver=approver,
            comments=comments,
        )