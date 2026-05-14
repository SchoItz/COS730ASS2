import java.util.ArrayList;
import java.util.List;

public class ReviewerManager {

    private final Database database;

    public ReviewerManager(Database database) {
        this.database = database;
    }

    public List<Reviewer> assignReviewers(String[] data) {
        MetricTracker.record("ReviewerManager.assignReviewers");
        List<String> rawList = database.fetchReviewers();
        List<String> eligible = filterReviewers(rawList);
        List<Reviewer> assigned = new ArrayList<>();
        for (String name : eligible) {
            Reviewer r = new Reviewer(name);
            r.assignReview(data);
            assigned.add(r);
        }
        return assigned;
    }

    private List<String> filterReviewers(List<String> reviewerList) {
        MetricTracker.record("ReviewerManager.filterReviewers");
        return reviewerList;
    }
}
