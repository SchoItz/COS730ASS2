import java.util.List;

public class SubmissionController {

    private UI ui;
    private Validator validator;
    private Database database;
    private ReviewerManager reviewerManager;
    private EvaluationManager evaluationManager;

    public SubmissionController(UI ui) {
        this.ui = ui;
        this.validator = new Validator();
        this.database = new Database();
        NotificationService notificationService = new NotificationService(ui);
        this.reviewerManager = new ReviewerManager(this.database);
        this.evaluationManager = new EvaluationManager(this.database, notificationService);
    }

    public String submit(String[] data) {
        MetricTracker.record("SubmissionController.submit");
        boolean valid = validator.validateFormat(data);
        if (!valid) {
            ui.returnError("Invalid submission format");
            return "invalid";
        }
        String confirmation = database.saveSubmission(data);
        List<Reviewer> filteredReviewers = reviewerManager.getAvailableReviewers();
        for (Reviewer reviewer : filteredReviewers) {
            reviewer.assignReview(data);
        }
        return evaluationManager.startEvaluation(filteredReviewers);
    }
}
