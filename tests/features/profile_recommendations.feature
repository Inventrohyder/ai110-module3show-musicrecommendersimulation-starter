Feature: Named profile CLI recommendations
  VibeFinder should expose observable, user-facing recommendations for distinct listeners.

  Scenario Outline: A named profile receives explained CLI results
    When I run the VibeFinder CLI for the "<profile>" profile
    Then the CLI exits successfully
    And the output identifies the "<profile>" profile
    And the first table recommendation is "<top_song>"
    And the table shows the "<reason_fragment>" contribution

    Examples:
      | profile           | top_song     | reason_fragment       |
      | high-energy-pop   | Sunrise City | genre match: +18.0/18 |
      | chill-lofi        | Library Rain | genre match: +18.0/18 |
      | deep-intense-rock | Everlong     | genre match: +18.0/18 |
