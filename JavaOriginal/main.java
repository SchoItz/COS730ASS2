public class main {

    public static void main(String[] args) {
        long StartTime = System.nanoTime();
        String[] data = {"Francois", "Scholtz", "ResearchTitle", "Content"};
        UI ui = new UI();
        ui.submitResearchOutput(data);
        long EndTime = System.nanoTime();
        CallTracker.printReport("Original");
        System.out.println("Execution time: " + (EndTime - StartTime) / 1000000 + " ms");
    }
}
