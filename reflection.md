# Optional Project Reflection

This voluntary learning record supplements the required README and Model Card; it is not presented as a separate Project 3 rubric requirement.

## AI influence and ownership

I used Codex desktop (GPT-5) to help turn the assignment into a small, testable content-based recommender. It helped identify a shared functional/OOP scoring path, propose behavior-oriented test cases, and structure the three named profiles. I made the final project decisions: use a classroom simulation rather than pretend to have streaming data, keep all descriptors visibly manual, preserve the ten starter entries while adding ten verified recordings, and require explanations for every result.

## What I verified myself

I checked that the catalog loads, that the three profiles produce different catalog leaders, and that the CLI can run all profiles from a subprocess. I compared the README's captured outputs with the command rather than treating generated prose as evidence. I also used a controlled experiment on _Happy_: removing the energy contribution changed its score, which confirmed that the score reflects a documented feature rather than a generic label.

## What I learned

The three profiles made the recommender's trade-offs concrete. High-energy-pop selects _Sunrise City_, chill-lofi selects _Library Rain_, and deep-intense-rock selects _Everlong_, but a clear explanation is not proof that the ranking is right for a listener. For example, genre and numeric similarity can compensate for a mood mismatch. That is useful for learning how ranking works, but it also shows why a small manually annotated catalog cannot stand in for real user research or interaction data.

## Process improvement

The main process lesson is that documentation is part of the feature, not a later cleanup task. For every feature layer I keep its code, real-data checks, captured output, Model Card evidence, and changelog evidence together. If a lower layer needs correction, I amend that layer and restack rather than adding an unrelated final polish commit. This makes both the technical behavior and the AI-assisted decision trail reviewable.
