Feature: Phases
  Scenario: #1 Add Phase Correctly
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the link "Add phase"
    And I see the "add" phase form
    Then I fill the form with the next info:
      | name          | value                 |
      | name          | To check              |
      | stories_limit | 20                    |
    And I submit the "add-phase-dialog" form
    Then I see the "phases" port
    And I check existence of object with the next info:
      | name          | value                 |
      | name          | To check              |
      | stories_limit | 20                    |

  Scenario: #2 Add Phase Empty Name
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the link "Add phase"
    And I see the "add" phase form
    Then I fill the form with the next info:
      | name          | value                 |
      | name          |                       |
      | stories_limit | 20                    |
    And I submit the "add-phase-dialog" form
    Then I see the "Add" validation error "Name: This field is required."

  Scenario: 3# Add Phase Invalid Stories Limit
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the link "Add phase"
    And I see the "add" phase form
    Then I fill the form with the next info:
      | name          | value                 |
      | name          | To check              |
      | stories_limit | 20a                   |
    And I submit the "add-phase-dialog" form
    Then I see the "Add" validation error "Stories limit: Enter a whole number."

  Scenario: #4 Edit Phase Correctly
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the "Edit" button of phase number 2
    And I see the "edit" phase form
    Then I fill the "edit" form with the next info:
      | name          | value                 |
      | name          | Now Working           |
      | description   | Phases working on     |
      | stories_limit | 32                    |
    And I submit the "edit-phase-dialog" form
    Then I see the "phases" port
    Then I click on the "Edit" button of phase number 2
    And I see the "edit" phase form
    And I check that the phase has the edited info:
      | name          | value                 |
      | name          | Now Working           |
      | description   | Phases working on     |
      | stories_limit | 32                    |


  Scenario: #5 Edit Phase Empty Name
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the "Edit" button of phase number 3
    And I see the "edit" phase form
    Then I fill the "edit" form with the next info:
      | name          | value                 |
      | name          |                       |
    And I submit the "edit-phase-dialog" form
    Then I see the "Edit" validation error "Name: This field is required."

  Scenario: #6 Edit Phase Invalid Stories Limit
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the "Edit" button of phase number 4
    And I see the "edit" phase form
    Then I fill the "edit" form with the next info:
      | name          | value                 |
      | stories_limit | dos                   |
    And I submit the "edit-phase-dialog" form
    Then I see the "Edit" validation error "Stories limit: Enter a whole number."

  Scenario: #7 Delete a phase
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the "Delete" button of phase number 4
    And I see a dialog
    Then I click the "Delete" button of the dialog
    And I see that no error is reported

  Scenario: #8 Delete a phase with stories
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the "Delete" button of phase number 2
    And I see a dialog
    Then I click the "Delete" button of the dialog
    And I see an error message that says "Cannot delete this phase. This phase has Stories."

  Scenario: #9 Delete a backlog phase
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the "Delete" button of phase number 1
    And I see a dialog
    Then I click the "Delete" button of the dialog
    And I see an error message that says "Cannot delete this phase. This phase is Backlog."

  Scenario: #10 Delete a archive phase
    Given I am logged in
    Then I click on the link "Projects"
    And I see the "Projects" page
    Then I click on a project
    And I wait for the "phases" port
    Then I click on the link "Phases"
    And I see the "phases" port
    Then I click on the "Delete" button of phase number 5
    And I see a dialog
    Then I click the "Delete" button of the dialog
    And I see an error message that says "Cannot delete this phase. This phase is Archive."
