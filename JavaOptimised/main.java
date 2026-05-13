public class main {

    public static void main(String[] args) {
        // Wire dependencies externally — controller no longer constructs collaborators
        Database database = new Database();
        Validator validator = new Validator();
        ReviewerManager reviewerManager = new ReviewerManager(database);
        EvaluationManager evaluationManager = new EvaluationManager(database);
        NotificationService notificationService = new NotificationService();
        SubmissionController controller = new SubmissionController(
                validator, database, reviewerManager, evaluationManager, notificationService);
        UI ui = new UI(controller);
        controller.setUI(ui);  // resolve circular dependency via setter

        String[] data = {"Francois", "Scholtz", "ResearchTitle", "Content"};

        long startTime = System.nanoTime();
        ui.submitResearchOutput(data);
        long endTime = System.nanoTime();

        CallTracker.printReport("Optimised");
        System.out.println("Execution time: " + (endTime - startTime) / 1_000_000 + " ms");
    }
}
