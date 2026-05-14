import java.util.List;

public class SubmissionController {

    private UI ui;
    private Validator val;
    private Database db;
    private ReviewerManager revMan;
    private EvaluationManager evalMman;

    public SubmissionController(UI ui) {
        this.ui = ui;
        this.val = new Validator();
        this.db = new Database();
        NotificationService msg = new NotificationService(ui);
        this.revMan = new ReviewerManager(this.db);
        this.evalMman = new EvaluationManager(this.db, msg);
    }

    public String submit(String[] data) {
        MetricTracker.record("SubmissionController.submit");
        boolean valid = val.validateFormat(data);
        if (!valid) {
            ui.returnError("Invalid submission format");
            return "invalid";
        }
        String confirmation = db.saveSubmission(data);
        List<Reviewer> filtRev = revMan.getAvailableReviewers();
        for (Reviewer reviewer : filtRev) {
            reviewer.assignReview(data);
        }
        return evalMman.startEvaluation(filtRev);
    }
}
