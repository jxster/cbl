Feature: Confirming that loading season data works

    Scenario: Adding teams to the database
        When I load team data from a JSON file
        Then I should be able to add the teams to the database
        And I should be able to see the data on the site

    Scenario: Adding players to the database
        When I load player data from a JSON file
        Then I should be able to add the players into the db
        And I should see the correct team rosters

    Scenario: Adding games to the database
        When I load game data from a JSON file
        Then I should be able to add games 
        And I should be able to add player stats
        And I should see it reflected on the pages