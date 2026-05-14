public class NotificationService {

    public void notify(String outcome) {
        CallTracker.record("NotificationService.notify");
        switch (outcome) {
            case "accepted":
                System.out.println("[NotificationService] notifyAcceptance");
                System.out.println("[Researcher] Your submission has been accepted.");
                break;
            case "rejected":
                System.out.println("[NotificationService] notifyRejection");
                System.out.println("[Researcher] Your submission has been rejected.");
                break;
            default:
                System.out.println("[NotificationService] notifyRevision");
                System.out.println("[Researcher] Your submission requires revision.");
                break;
        }
    }
}
