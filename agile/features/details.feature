Feature: Details
  Scenario: Add entry and stop times to a story
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a link project
    And I see the board of stories
    Then I display the hidden phases
    Then I click on a story
    And I see the story page 
    Then I click on the time entry
    And I click the start button
    Then I see a new row at the table
    Then I see the page for 3 seconds
    And I click the stop button
    Then I see the page for 3 seconds
    I see the right stop and duration time
    
  Scenario: Intend take a time entry with another time entry already taken
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a link project
    And I see the board of stories
    Then I display the hidden phases
    Then I click on a story
    And I see the story page 
    Then I click on the time entry
    And I click the start button
    Then I see the page for 3 seconds
    And I click the start button
    Then I see the message of incorrect