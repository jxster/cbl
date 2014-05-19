Feature: Confirming basic functionality for players

    Scenario: check that the homepage returns expected content
        When I go to the CBL site
        Then I should see standings
        And I should see recent-games

    Scenario: confirm standings page exists and is accurate
        When I go to the CBL standings
        Then I should see standings
        And I should see the correct order