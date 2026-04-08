import numpy as np
import pytest

from westfall_2006 import predict_height_westfall
from westfall_2006.model import _validate_inputs


class TestReadmeExample:
    """
    Runs tests on the example in the README.

    The example is described as:
    A poplar tree (species group = 12) with DBH = 15.5 in.,
    compacted crown ratio = 40 percent, tree class = acceptable
    (TC = 2), and crown class = codominant (CC1 = 0, CC2 = 1,
    CC3 = 0).

    The species group coefficients for group 12 are:
    beta_0 = -4.2401, beta_1 = 84.2529, beta_2 = 91.5048,
    beta_3 = 78.7788, beta_4 = 0.1023, beta_5 = 0.0054,
    beta_6 = 0.0638, beta_7 = 0.1422
    """

    species_group = 12
    dbh = 15.5
    ccr = 40
    tree_class = "acceptable"
    crown_class = "codominant"

    def test_total_height(self):
        """
        Prediction of total height (top diameter = 0):
        H = (91.5048) * (1 - exp(-0.1023 * 15.5))
            ^ (0.0054*40 + 0.0638*2 + (0/15.5 + 0.01)^0.1422)
        H ~= 75.0 ft

        The paper reports approximately 75.0 ft.
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 0.0,
            )
            == 75.08210159707517
        )

    def test_bole_height(self):
        """
        Prediction of bole height (4-in. top diameter):
        H = (-4.2401*4 + 91.5048) * (1 - exp(-0.1023 * 15.5))
            ^ (0.0054*40 + 0.0638*2 + (4/15.5 + 0.01)^0.1422)
        H ~= 56.9 ft

        The paper reports approximately 56.9 ft.
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 4.0,
            )
            == 56.9740957505897
        )

    def test_sawlog_height(self):
        """
        Prediction of sawlog height (9-in. top diameter):
        H = (-4.2401*9 + 91.5048) * (1 - exp(-0.1023 * 15.5))
            ^ (0.0054*40 + 0.0638*2 + (9/15.5 + 0.01)^0.1422)
        H ~= 39.8 ft

        The paper reports approximately 39.8 ft.
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 9.0,
            )
            == 39.859721210981185
        )


class TestSoftwoodDominant:
    """
    Tests a softwood species group with dominant/preferred attributes.

    Assume a tree in species group 1 with DBH = 20.0 in.,
    compacted crown ratio = 55 percent, tree class = preferred
    (TC = 1), and crown class = dominant (CC1 = 0, CC2 = 1,
    CC3 = 0).

    The species group coefficients for group 1 are:
    beta_0 = -4.0092, beta_1 = 80.4990, beta_2 = 89.3969,
    beta_3 = 65.0335, beta_4 = 0.0969, beta_5 = 0.0124,
    beta_6 = 0.3150, beta_7 = 1.8500
    """

    species_group = 1
    dbh = 20.0
    ccr = 55
    tree_class = "preferred"
    crown_class = "dominant"

    def test_total_height(self):
        """
        Total height prediction (top diameter = 0).
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 0.0,
            )
            == 76.55781961600512
        )

    def test_bole_height(self):
        """
        Bole height prediction (4-in. top diameter).
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 4.0,
            )
            == 62.28412088723717
        )

    def test_sawlog_height(self):
        """
        Sawlog height prediction (9-in. top diameter).
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 9.0,
            )
            == 44.001753341279
        )


class TestOvertoppedRough:
    """
    Tests an overtopped rough-cull tree.

    Assume a tree in species group 8 with DBH = 12.0 in.,
    compacted crown ratio = 30 percent, tree class = rough
    (TC = 3), and crown class = overtopped (CC1 = 0, CC2 = 0,
    CC3 = 1).

    The species group coefficients for group 8 are:
    beta_0 = -3.9480, beta_1 = 74.3455, beta_2 = 80.9280,
    beta_3 = 69.3210, beta_4 = 0.0947, beta_5 = 0.0085,
    beta_6 = 0.3092, beta_7 = 2.0523
    """

    species_group = 8
    dbh = 12.0
    ccr = 30
    tree_class = "rough"
    crown_class = "overtopped"

    def test_total_height(self):
        """
        Total height prediction (top diameter = 0).
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 0.0,
            )
            == 43.85727492152837
        )

    def test_bole_height(self):
        """
        Bole height prediction (4-in. top diameter).
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 4.0,
            )
            == 32.436949584096766
        )


class TestDeadTree:
    """
    Tests a dead tree.

    Assume a dead tree in species group 3 with DBH = 18.0 in.,
    compacted crown ratio = 25 percent, tree class = dead
    (TC = 3), and crown class = dead (CC1 = 1, CC2 = 0,
    CC3 = 0).

    The species group coefficients for group 3 are:
    beta_0 = -4.9167, beta_1 = 97.4497, beta_2 = 102.9998,
    beta_3 = 89.3026, beta_4 = 0.0762, beta_5 = 0.0126,
    beta_6 = 0.2908, beta_7 = 2.4458
    """

    species_group = 3
    dbh = 18.0
    ccr = 25
    tree_class = "dead"
    crown_class = "dead"

    def test_total_height(self):
        """
        Total height prediction (top diameter = 0).
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 0.0,
            )
            == 68.84553875174208
        )

    def test_bole_height(self):
        """
        Bole height prediction (4-in. top diameter).
        """
        assert (
            predict_height_westfall(
                self.species_group, self.dbh, self.ccr,
                self.tree_class, self.crown_class, 4.0,
            )
            == 54.501248362832285
        )


class TestVectorized:
    """
    Test full vectorization: all six parameters may be arrays.

    Uses the same four trees from the scalar test classes, each with
    a different species group, tree class, and crown class:

    Tree 1 (TestReadmeExample):
        species_group=12, DBH=15.5, CCR=40,
        tree_class="acceptable", crown_class="codominant"
    Tree 2 (TestSoftwoodDominant):
        species_group=1,  DBH=20.0, CCR=55,
        tree_class="preferred",   crown_class="dominant"
    Tree 3 (TestOvertoppedRough):
        species_group=8,  DBH=12.0, CCR=30,
        tree_class="rough",       crown_class="overtopped"
    Tree 4 (TestDeadTree):
        species_group=3,  DBH=18.0, CCR=25,
        tree_class="dead",        crown_class="dead"
    """

    species_group = np.array([12, 1, 8, 3])
    dbh = np.array([15.5, 20.0, 12.0, 18.0])
    ccr = np.array([40.0, 55.0, 30.0, 25.0])
    tree_class = np.array(["acceptable", "preferred", "rough", "dead"])
    crown_class = np.array(["codominant", "dominant", "overtopped", "dead"])

    def test_total_height(self):
        """Vectorized total height matches individual scalar calls."""
        result = predict_height_westfall(
            self.species_group, self.dbh, self.ccr,
            self.tree_class, self.crown_class, 0.0,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == pytest.approx(75.08210159707517, rel=1e-12)   # TestReadmeExample
        assert result[1] == pytest.approx(76.55781961600512, rel=1e-12)   # TestSoftwoodDominant
        assert result[2] == pytest.approx(43.85727492152837, rel=1e-12)   # TestOvertoppedRough
        assert result[3] == pytest.approx(68.84553875174208, rel=1e-12)   # TestDeadTree

    def test_bole_height(self):
        """Vectorized bole height (4-in. top diameter) matches scalar calls."""
        result = predict_height_westfall(
            self.species_group, self.dbh, self.ccr,
            self.tree_class, self.crown_class, 4.0,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == pytest.approx(56.9740957505897, rel=1e-12)    # TestReadmeExample
        assert result[1] == pytest.approx(62.28412088723717, rel=1e-12)   # TestSoftwoodDominant
        assert result[2] == pytest.approx(32.436949584096766, rel=1e-12)  # TestOvertoppedRough
        assert result[3] == pytest.approx(54.501248362832285, rel=1e-12)  # TestDeadTree

    def test_vectorized_top_diameter(self):
        """Vectorized with varying top diameters."""
        top_diam = np.array([0.0, 4.0, 9.0, 0.0])
        result = predict_height_westfall(
            self.species_group, self.dbh, self.ccr,
            self.tree_class, self.crown_class, top_diam,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == pytest.approx(75.08210159707517, rel=1e-12)    # tree 1 total height
        assert result[1] == pytest.approx(62.28412088723717, rel=1e-12)    # tree 2 bole height
        assert result[2] == pytest.approx(17.149335239781124, rel=1e-12)   # tree 3 sawlog height (group 8 9-in)
        assert result[3] == pytest.approx(68.84553875174208, rel=1e-12)    # tree 4 total height

    def test_list_input(self):
        """List inputs for all parameters produce the same results as arrays."""
        result = predict_height_westfall(
            [12, 1, 8, 3],
            [15.5, 20.0, 12.0, 18.0],
            [40.0, 55.0, 30.0, 25.0],
            ["acceptable", "preferred", "rough", "dead"],
            ["codominant", "dominant", "overtopped", "dead"],
            [0.0, 0.0, 0.0, 0.0],
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == pytest.approx(75.08210159707517, rel=1e-12)
        assert result[1] == pytest.approx(76.55781961600512, rel=1e-12)
        assert result[2] == pytest.approx(43.85727492152837, rel=1e-12)
        assert result[3] == pytest.approx(68.84553875174208, rel=1e-12)


class TestFiaSpcd:
    """
    Tests that fia_spcd produces identical results to species_group.

    FIA species codes used:
      746  Quaking aspen   → group 12  (TestReadmeExample)
      129  Eastern white pine → group 3   (TestDeadTree)
      125  Red pine        → group 1   (TestSoftwoodDominant)
      261  Eastern hemlock → group 8   (TestOvertoppedRough)
    """

    def test_scalar_fia_spcd_matches_species_group(self):
        """fia_spcd=746 (Quaking aspen → group 12) gives the same result."""
        expected = predict_height_westfall(12, 15.5, 40, "acceptable", "codominant")
        result = predict_height_westfall(
            None, 15.5, 40, "acceptable", "codominant", fia_spcd=746
        )
        assert result == expected

    def test_scalar_fia_spcd_bole_height(self):
        """fia_spcd scalar with non-zero top diameter matches species_group."""
        expected = predict_height_westfall(3, 18.0, 25, "dead", "dead", 4.0)
        result = predict_height_westfall(
            None, 18.0, 25, "dead", "dead", 4.0, fia_spcd=129
        )
        assert result == expected

    def test_array_fia_spcd_matches_species_group(self):
        """Array of fia_spcd values produces the same result as species_group array."""
        expected = predict_height_westfall(
            [12, 1, 8, 3],
            [15.5, 20.0, 12.0, 18.0],
            [40.0, 55.0, 30.0, 25.0],
            ["acceptable", "preferred", "rough", "dead"],
            ["codominant", "dominant", "overtopped", "dead"],
            0.0,
        )
        result = predict_height_westfall(
            None,
            [15.5, 20.0, 12.0, 18.0],
            [40.0, 55.0, 30.0, 25.0],
            ["acceptable", "preferred", "rough", "dead"],
            ["codominant", "dominant", "overtopped", "dead"],
            0.0,
            fia_spcd=[746, 125, 261, 129],
        )
        np.testing.assert_array_equal(result, expected)

    def test_neither_raises(self):
        """Omitting both species_group and fia_spcd raises ValueError."""
        with pytest.raises(ValueError, match="Either species_group or fia_spcd"):
            predict_height_westfall(None, 15.5, 40, "acceptable", "codominant")

    def test_both_raises(self):
        """Providing both species_group and fia_spcd raises ValueError."""
        with pytest.raises(ValueError, match="not both"):
            predict_height_westfall(
                12, 15.5, 40, "acceptable", "codominant", fia_spcd=746
            )

    def test_unknown_fia_spcd_raises(self):
        """An unrecognised FIA species code raises ValueError."""
        with pytest.raises(ValueError, match="Unknown FIA species code"):
            predict_height_westfall(
                None, 15.5, 40, "acceptable", "codominant", fia_spcd=99999
            )


class TestValidateInputs:
    """Tests for _validate_inputs and the validation wired into predict_height_westfall."""

    # Shared valid baseline values
    _sg = 12
    _dbh = 15.5
    _ccr = 40.0
    _top = 0.0

    def test_invalid_species_group_scalar(self):
        with pytest.raises(ValueError, match="Invalid species_group"):
            predict_height_westfall(0, self._dbh, self._ccr, "acceptable", "codominant")

    def test_invalid_species_group_19(self):
        with pytest.raises(ValueError, match="Invalid species_group"):
            predict_height_westfall(19, self._dbh, self._ccr, "acceptable", "codominant")

    def test_invalid_species_group_array(self):
        with pytest.raises(ValueError, match="Invalid species_group"):
            predict_height_westfall(
                [12, 99], [15.5, 15.5], [40, 40],
                ["acceptable", "acceptable"], ["codominant", "codominant"],
            )

    def test_dbh_zero_raises(self):
        with pytest.raises(ValueError, match="dbh_in must be positive"):
            predict_height_westfall(self._sg, 0.0, self._ccr, "acceptable", "codominant")

    def test_dbh_negative_raises(self):
        with pytest.raises(ValueError, match="dbh_in must be positive"):
            predict_height_westfall(self._sg, -1.0, self._ccr, "acceptable", "codominant")

    def test_ccr_below_range_raises(self):
        with pytest.raises(ValueError, match="ccr_pct must be in"):
            predict_height_westfall(self._sg, self._dbh, -1.0, "acceptable", "codominant")

    def test_ccr_above_range_raises(self):
        with pytest.raises(ValueError, match="ccr_pct must be in"):
            predict_height_westfall(self._sg, self._dbh, 101.0, "acceptable", "codominant")

    def test_top_diam_negative_raises(self):
        with pytest.raises(ValueError, match="top_diam_in must be non-negative"):
            predict_height_westfall(
                self._sg, self._dbh, self._ccr, "acceptable", "codominant", -1.0
            )

    def test_invalid_tree_class_raises(self):
        with pytest.raises(ValueError, match="Invalid tree_class"):
            predict_height_westfall(self._sg, self._dbh, self._ccr, "invalid", "codominant")

    def test_invalid_crown_class_raises(self):
        with pytest.raises(ValueError, match="Invalid crown_class"):
            predict_height_westfall(self._sg, self._dbh, self._ccr, "acceptable", "invalid")

    def test_validate_inputs_directly_valid(self):
        """_validate_inputs does not raise for valid inputs."""
        _validate_inputs(12, 15.5, 40.0, 0.0)

    def test_validate_inputs_directly_array(self):
        """_validate_inputs does not raise for valid array inputs."""
        _validate_inputs([1, 12, 8], [10.0, 15.5, 12.0], [30.0, 40.0, 55.0], [0.0, 4.0, 9.0])
