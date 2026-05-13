public class Validator {

    public boolean validateFormat(String[] data) {
        CallTracker.record("Validator.validateFormat");
        boolean isValid = data != null && data.length > 0;
        System.out.println("[Validator] validateFormat -> " + (isValid ? "valid" : "invalid"));
        return isValid;
    }
}
