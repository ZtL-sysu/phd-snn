# Stress-test notes (round 001)

The strict validator checks exact H2 headings, the six canonical outline entries, required terms,
trailing-colon placeholders, empty table rows and TBD/TODO strings. The build script asserts these
before invoking the skill validator, so a formatting failure is caught before any experiment starts.
`validate_guidance.py` validates structure only; it does not prove scientific validity, novelty or
truthfulness. P5, P5A, P9 and P12 remain evidence gates.
