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

    public String submit(String[] data) {
        MetricTracker.record("SubmissionController.submit");

        ValidationResult result = validator.validateFormat(data);
        if (!result.isValid()) {
            if (ui != null) ui.displayError(result.getReason());
            else System.out.println("[SubmissionController] Error: " + result.getReason());
            return "invalid";
        }

        String confirmation = database.saveSubmission(data);

        List<Reviewer> assigned = reviewerManager.assignReviewers(data);

        String outcome = evaluationManager.evaluateSubmission(assigned);

        notificationService.notify(outcome);
        return outcome;
    }
}
