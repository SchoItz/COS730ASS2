public class NotificationService {

    public void notify(String outcome) {
        MetricTracker.record("NotificationService.notify");
        switch (outcome) {
            case "accepted":
                System.out.println("Your submission has been accepted.");
                break;
            case "rejected":
                System.out.println("Your submission has been rejected.");
                break;
            default:
                System.out.println("Your submission requires revision.");
                break;
        }
    }
}
