import java.util.ArrayList;
import java.util.List;

public class ReviewerManager {

    private Database database;

    public ReviewerManager(Database database) {
        this.database = database;
    }

    public List<Reviewer> getAvailableReviewers() {
        MetricTracker.record("ReviewerManager.getAvailableReviewers");
        List<String> reviewerList = database.fetchReviewers();
        reviewerList = filterConflicts(reviewerList);
        reviewerList = checkWorkload(reviewerList);
        List<Reviewer> filteredReviewers = new ArrayList<>();
        for (String name : reviewerList) {
            filteredReviewers.add(new Reviewer(name));
        }
        return filteredReviewers;
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
