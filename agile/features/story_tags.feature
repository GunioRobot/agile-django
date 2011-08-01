Feature: Story Tags Actions
  Scenario: #1 Add a new tag
    Given I opened a story
    And I add a new tag with the name "tag test"
    Then I see the tag named "tag test"

  Scenario: #2 Edit a tag
    Given I opened a story
    Then I double click on the name of the tag "design"
    And I see a text box with the text "design"
    Then I replace it with "tag1"
    And I click elsewhere
    Then I see the tag named "tag1"

  Scenario: #3 Delete a tag
    Given I opened a story
    Then I click the close button of the tag named "design"
    And I do not see the tag named "design"