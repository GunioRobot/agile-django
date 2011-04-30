Feature: Authentication
  Scenario: Simple login
    Given I am in the login page
    And I fill the form with the next info:
      | name     | value |
      | username | admin |
      | password | admin |
    Then I submit the form
    And I see the logged in home page
    
  Scenario: Logging out
    Given I am logged in
    Then I click on the link "Logout"
    And I see the logged out home page