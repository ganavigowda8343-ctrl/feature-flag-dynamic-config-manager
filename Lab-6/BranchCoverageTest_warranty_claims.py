import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# ============================================================================
# 1. Tests for out_of_warranty_charge (100% Branch Coverage & Edge Cases)
# ============================================================================

def test_out_of_warranty_unknown_plan():
    """Branch: plan not in COVERED_MONTHS -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("ultra", 12, "defect", False)


def test_out_of_warranty_negative_age():
    """Branch: age_months < 0 -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -5, "defect", False)


def test_out_of_warranty_registered_basic_within_coverage():
    """
    Branch: is_registered=True and plan != 'premium' -> True (covered += 6).
    Branch: excess <= 0 -> True (returns 0).
    Basic covered = 12 + 6 = 18. Age = 18 -> excess = 0.
    """
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0


def test_out_of_warranty_registered_premium_does_not_extend():
    """
    Branch: is_registered=True but plan == 'premium' -> False (covered stays 36).
    Branch: excess <= 12 -> False branch of 'if excess > 12'.
    Branch: claim_type == 'accidental' -> True (rate = 200).
    Premium covered = 36. Age = 40 -> excess = 4. Rate = 200.
    """
    assert out_of_warranty_charge("premium", 40, "accidental", True) == 4 * 200


def test_out_of_warranty_unregistered_defect_excess_over_12():
    """
    Branch: is_registered=False -> False (no extension).
    Branch: claim_type == 'defect' (not accidental) -> rate = 100.
    Branch: excess > 12 -> True (rate += 50 -> 150).
    Branch: inside excess > 12, claim_type == 'accidental' -> False (branch 21->23).
    Standard covered = 24. Age = 40 -> excess = 16. Rate = 150. Total = 2400.
    """
    assert out_of_warranty_charge("standard", 40, "defect", False) == 16 * 150


def test_out_of_warranty_unregistered_accidental_excess_over_12():
    """
    Branch: claim_type == 'accidental' -> rate = 200.
    Branch: excess > 12 -> True (rate += 50 -> 250).
    Branch: inside excess > 12, claim_type == 'accidental' -> True (rate += 25 -> 275).
    Standard covered = 24. Age = 40 -> excess = 16. Rate = 275. Total = 4400.
    """
    assert out_of_warranty_charge("standard", 40, "accidental", False) == 16 * 275


def test_out_of_warranty_unregistered_defect_excess_under_12():
    """
    Branch: excess > 12 -> False (excess == 10).
    Branch: claim_type != 'accidental' -> rate = 100.
    Basic covered = 12. Age = 22 -> excess = 10. Rate = 100. Total = 1000.
    """
    assert out_of_warranty_charge("basic", 22, "defect", False) == 10 * 100


def test_out_of_warranty_exact_excess_12_boundary():
    """
    Boundary test: excess == 12 (excess > 12 evaluates to False).
    Basic covered = 12. Age = 24 -> excess = 12. Rate = 200 (accidental).
    Total = 12 * 200 = 2400.
    """
    assert out_of_warranty_charge("basic", 24, "accidental", False) == 12 * 200


# ============================================================================
# 2. Tests for claim_allowed (100% Branch Coverage & Boundary Value Analysis)
# ============================================================================

def test_claim_allowed_recall_within_limit():
    """Branch: is_recall=True and claims_filed <= 5 -> True (Boundary: 5)."""
    assert claim_allowed(0, 5, True) is True


def test_claim_allowed_recall_exceeds_limit():
    """Branch: is_recall=True and claims_filed > 5 -> False (Boundary: 6)."""
    assert claim_allowed(0, 6, True) is False


def test_claim_allowed_days_less_than_30():
    """Branch: is_recall=False, days_since_last_claim < 30 -> True (Boundary: 29)."""
    assert claim_allowed(29, 0, False) is False


def test_claim_allowed_regular_boundary_days_within_claims():
    """
    Branch: is_recall=False, days_since_last_claim < 30 -> False (Boundary: 30).
    Branch: claims_filed <= 2 -> True (Boundary: 2).
    """
    assert claim_allowed(30, 2, False) is True


def test_claim_allowed_regular_exceeds_claims():
    """
    Branch: is_recall=False, days >= 30, claims_filed <= 2 -> False (Boundary: 3).
    """
    assert claim_allowed(45, 3, False) is False


# ============================================================================
# 3. Tests for sla_status (100% Branch Coverage & All Cutoff Partitions)
# ============================================================================

def test_sla_hardware_priority_on_track():
    """
    Branch: is_hardware=True (cutoff=48), is_priority=True (cutoff=72).
    Branch: hours_left >= cutoff (72 >= 72) -> 'on_track'.
    """
    assert sla_status(72, is_hardware=True, is_priority=True) == "on_track"


def test_sla_hardware_priority_at_risk():
    """
    Branch: hours_left < cutoff (65 < 72) and hours_left >= cutoff - 12 (65 >= 60).
    Returns 'at_risk'.
    """
    assert sla_status(65, is_hardware=True, is_priority=True) == "at_risk"


def test_sla_hardware_priority_critical():
    """
    Branch: hours_left < cutoff - 12 (50 < 60). Returns 'critical'.
    """
    assert sla_status(50, is_hardware=True, is_priority=True) == "critical"


def test_sla_hardware_non_priority_on_track():
    """
    Branch: is_hardware=True (cutoff=48), is_priority=False (cutoff=48).
    Branch: hours_left >= 48 (50 >= 48) -> 'on_track'.
    """
    assert sla_status(50, is_hardware=True, is_priority=False) == "on_track"


def test_sla_hardware_non_priority_at_risk():
    """
    Cutoff = 48, cutoff - 12 = 36. hours_left = 36 (exact boundary) -> 'at_risk'.
    """
    assert sla_status(36, is_hardware=True, is_priority=False) == "at_risk"


def test_sla_hardware_non_priority_critical():
    """
    Cutoff = 48, cutoff - 12 = 36. hours_left = 35 -> 'critical'.
    """
    assert sla_status(35, is_hardware=True, is_priority=False) == "critical"


def test_sla_software_priority_on_track():
    """
    Branch: is_hardware=False (cutoff=24), is_priority=True (cutoff=48).
    Branch: hours_left >= 48 (48 >= 48) -> 'on_track'.
    """
    assert sla_status(48, is_hardware=False, is_priority=True) == "on_track"


def test_sla_software_priority_at_risk():
    """
    Cutoff = 48, cutoff - 12 = 36. hours_left = 40 -> 'at_risk'.
    """
    assert sla_status(40, is_hardware=False, is_priority=True) == "at_risk"


def test_sla_software_priority_critical():
    """
    Cutoff = 48, cutoff - 12 = 36. hours_left = 20 -> 'critical'.
    """
    assert sla_status(20, is_hardware=False, is_priority=True) == "critical"


def test_sla_software_non_priority_on_track():
    """
    Branch: is_hardware=False (cutoff=24), is_priority=False (cutoff=24).
    Branch: hours_left >= 24 (25 >= 24) -> 'on_track'.
    """
    assert sla_status(25, is_hardware=False, is_priority=False) == "on_track"


def test_sla_software_non_priority_at_risk():
    """
    Cutoff = 24, cutoff - 12 = 12. hours_left = 12 (exact boundary) -> 'at_risk'.
    """
    assert sla_status(12, is_hardware=False, is_priority=False) == "at_risk"


def test_sla_software_non_priority_critical():
    """
    Cutoff = 24, cutoff - 12 = 12. hours_left = 11 -> 'critical'.
    """
    assert sla_status(11, is_hardware=False, is_priority=False) == "critical"
