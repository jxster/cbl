Feature: Confirming homepage functionality

    Scenario: check that the homepage returns expected content
        When I go to the CBL site
        Then I should see standings on the sidebar
        And I should see recent games
