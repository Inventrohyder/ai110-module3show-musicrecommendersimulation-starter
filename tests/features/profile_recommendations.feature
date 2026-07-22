Feature: Named profile recommendations
  VibeFinder should expose observable differences for distinct listeners.

  Scenario Outline: A named profile receives explained real-catalog results
    Given the checked-in VibeFinder catalog
    And the "<profile>" profile
    When that profile requests three recommendations
    Then exactly three recommendations are returned
    And recommendations are ordered from highest score to lowest score
    And every returned recommendation has score-derived reasons

    Examples:
      | profile           |
      | high-energy-pop   |
      | chill-lofi        |
      | deep-intense-rock |
