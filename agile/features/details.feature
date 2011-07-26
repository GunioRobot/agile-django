Feature: Details
  Scenario: #1 - Add entry and stop times to a story
    Given I am logged in
    When I click on the link "Projects"
    Then I see the "Projects" page
    And I click on the link "Add project"
    Then I see the "add" project form
    When I fill the form with the next info:
      | name          | value                 |
      | name          | Project to check      |
    And I select the admin as a member
    Then I submit the form
    When I click on the link "Projects"
    Then I click on a link project
    And I see the board of stories
    And I click on the link "Add story"
    Then I see the "add" story form
    When I fill the form with the next info:
      | name          | value                 |
      | name          | Story to check      |
    And I click the menu phase
    Then I see the page for 3 seconds
    And I select the phase
    Then I submit the form
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
    
  Scenario: #2 - Intend take a time entry with another time entry already taken
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