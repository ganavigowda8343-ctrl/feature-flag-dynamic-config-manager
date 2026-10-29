import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# --- Tests for out_of_warranty_charge (Code / Line Coverage Focus) ---

def test_unknown_plan_raises_error():
    """Verify ValueError is raised for an unsupported plan."""
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("platinum", 10, "defect", False)


def test_negative_age_raises_error():
    """Verify ValueError is raised for negative age."""
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_registered_non_premium_within_warranty():
    """Test registered user with basic plan receives 6-month extension and within warranty."""
    # basic: 12 + 6 = 18. age 15 <= 18 -> excess <= 0 -> 0 charge
    assert out_of_warranty_charge("basic", 15, "defect", True) == 0


def test_excess_greater_than_12_accidental():
    """Test excess > 12 months with accidental damage surcharge."""
    # standard: 24, unregistered -> covered = 24.
    # age = 40 -> excess = 16.
    # rate = 200 + 50 + 25 = 275. charge = 16 * 275 = 4400.
    assert out_of_warranty_charge("standard", 40, "accidental", False) == 4400


def test_excess_within_12_non_accidental():
    """Test excess <= 12 months with defect (non-accidental) rate."""
    # basic: 12, unregistered -> covered = 12.
    # age = 20 -> excess = 8.
    # rate = 100. charge = 8 * 100 = 800.
    assert out_of_warranty_charge("basic", 20, "defect", False) == 800


# --- Tests for claim_allowed (Code / Line Coverage Focus) ---

def test_claim_allowed_recall_eligible():
    """Test recall claim allowed when claims filed is within recall limit (<= 5)."""
    assert claim_allowed(10, 3, True) is True


def test_claim_rejected_too_recent():
    """Test regular claim rejected when filed within 30 days of last claim."""
    assert claim_allowed(15, 1, False) is False


def test_claim_allowed_regular():
    """Test regular claim allowed after 30 days with <= 2 claims."""
    assert claim_allowed(45, 2, False) is True


# --- Tests for sla_status (Code / Line Coverage Focus) ---

def test_sla_hardware_priority_on_track():
    """Test hardware priority ticket (cutoff = 72 hrs) is on track."""
    assert sla_status(75, is_hardware=True, is_priority=True) == "on_track"


def test_sla_software_at_risk():
    """Test software non-priority ticket (cutoff = 24 hrs) is at risk (12-23 hrs left)."""
    assert sla_status(18, is_hardware=False, is_priority=False) == "at_risk"


def test_sla_software_critical():
    """Test software ticket with less than cutoff - 12 hrs left is critical."""
    assert sla_status(5, is_hardware=False, is_priority=False) == "critical"
