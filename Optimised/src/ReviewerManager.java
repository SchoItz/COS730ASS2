import java.util.ArrayList;
import java.util.List;

public class ReviewerManager {

    private final Database db;

    public ReviewerManager(Database db) {
        this.db = db;
    }

    public List<Reviewer> assignReviewers(String[] data) {
        MetricTracker.record("ReviewerManager.assignReviewers");
        List<String> list = db.fetchReviewers();
        List<String> filteredList = filterReviewers(list);
        List<Reviewer> reviewerList = new ArrayList<>();
        for (String name : filteredList) {
            Reviewer r = new Reviewer(name);
            r.assignReview(data);
            reviewerList.add(r);
        }
        return reviewerList;
    }

    private List<String> filterReviewers(List<String> reviewerList) {
        MetricTracker.record("ReviewerManager.filterReviewers");
        return reviewerList;
    }
}
