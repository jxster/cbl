Feature: Confirming standings page works

    Scenario: confirm standings page exists and is accurate
        When I go to the CBL standings
        Then I should see standings as the main content