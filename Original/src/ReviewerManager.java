import java.util.ArrayList;
import java.util.List;

public class ReviewerManager {

    private Database db;

    public ReviewerManager(Database db) {
        this.db = db;
    }

    public List<Reviewer> getAvailableReviewers() {
        MetricTracker.record("ReviewerManager.getAvailableReviewers");
        List<String> reviewerList = db.fetchReviewers();
        reviewerList = filterConflicts(reviewerList);
        reviewerList = checkWorkload(reviewerList);
        List<Reviewer> filtRev = new ArrayList<>();
        for (String name : reviewerList) {
            filtRev.add(new Reviewer(name));
        }
        return filtRev;
    }

    private List<String> filterConflicts(List<String> reviewerList) {
        MetricTracker.record("ReviewerManager.filterConflicts");
        return reviewerList;
    }

    private List<String> checkWorkload(List<String> reviewerList) {
        MetricTracker.record("ReviewerManager.checkWorkload");
        return reviewerList;
    }
}
