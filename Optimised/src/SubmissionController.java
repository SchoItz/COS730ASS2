import java.util.List;

public class SubmissionController {

    private UI ui;
    private final Validator val;
    private final Database db;
    private final ReviewerManager revMan;
    private final EvaluationManager evalMan;
    private final NotificationService notify;

    public SubmissionController(Validator val, Database db,
                                ReviewerManager revMan,
                                EvaluationManager evalMan,
                                NotificationService notify) {
        this.ui = null;
        this.val = val;
        this.db = db;
        this.revMan = revMan;
        this.evalMan = evalMan;
        this.notify = notify;
    }

    public void setUI(UI ui) {
        this.ui = ui;
    }

    public String submit(String[] data) {
        MetricTracker.record("SubmissionController.submit");

        ValidationResult result = val.validateFormat(data);
        if (!result.isValid()) {
            if (ui != null) ui.displayError(result.getReason());
            else System.out.println("[SubmissionController] Error: " + result.getReason());
            return "invalid";
        }

        String confrim = db.saveSubmission(data);

        List<Reviewer> assign = revMan.assignReviewers(data);

        String outcome = evalMan.evaluateSubmission(assign);

        notify.notify(outcome);
        return outcome;
    }
}
