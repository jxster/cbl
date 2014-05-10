Feature: Confirming basic functionality for players

    Scenario: check that the homepage returns expected content
        When I go to the CBL site
        Then I should see standings
        And I should see recent-games