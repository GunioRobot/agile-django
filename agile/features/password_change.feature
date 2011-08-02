Feature: Password Change
  Scenario: Change success
    Given I am logged in
    And I click on the link "Profile"
    Then I see the "Profile" page
    And I click on the link "Change password"
    Then I see the password form
    And I fill the form with the next info:
      | name          | value  |
      | old_password  | admin  |
      | new_password1 | 123qwe |
      | new_password2 | 123qwe |
    Then I submit the "change-password" form
    And I see the "Profile" page