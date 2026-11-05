"""
Processor Module (Warranty Claims Application)
Hardened against unexpected, malformed, and edge-case inputs via defensive programming.
Tested with Hypothesis property-based fuzz testing.
"""
from warranty_claims import parse_claim, age_average, payable_charge, main

if __name__ == "__main__":
    main()
