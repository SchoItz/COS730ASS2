import java.util.List;

public class SubmissionController {

    private UI ui;
    private final Validator validator;
    private final Database database;
    private final ReviewerManager reviewerManager;
    private final EvaluationManager evaluationManager;
    private final NotificationService notificationService;

    public SubmissionController(Validator validator, Database database,
                                ReviewerManager reviewerManager,
                                EvaluationManager evaluationManager,
                                NotificationService notificationService) {
        this.ui = null;
        this.validator = validator;
        this.database = database;
        this.reviewerManager = reviewerManager;
        this.evaluationManager = evaluationManager;
        this.notificationService = notificationService;
    }

    public void setUI(UI ui) {
        this.ui = ui;
    }

    public void submit(String[] data) {
        CallTracker.record("SubmissionController.submit");

        ValidationResult result = validator.validateFormat(data);
        if (!result.isValid()) {
            if (ui != null) ui.displayError(result.getReason());
            else System.out.println("[SubmissionController] Error: " + result.getReason());
            return;
        }

        String confirmation = database.saveSubmission(data);
        System.out.println("[SubmissionController] confirmation: " + confirmation);

        // ReviewerManager owns the assignment loop — controller just delegates
        List<Reviewer> assigned = reviewerManager.assignReviewers(data);

        // EvaluationManager returns the outcome — controller routes notification
        String outcome = evaluationManager.evaluateSubmission(assigned);

        notificationService.notify(outcome);
    }
}
