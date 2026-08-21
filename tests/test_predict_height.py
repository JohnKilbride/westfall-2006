"""
Tests for predict_height_westfall.

Every test is run twice: once with the species group number used in
Westfall and Laustsen (2006) and once with an equivalent FIA species code
(SPCD).  The ``species_id`` fixture supplies both modes, and ``as_species``
translates a test's species group number into the identifier that matches
the mode under test.  Because an FIA code is resolved to its species group
before any arithmetic happens, both modes must return bit-identical results.
"""

import numpy as np
import pytest

from westfall_2006 import predict_height_westfall
from westfall_2006.model import _validate_inputs


# Species group number -> a representative FIA SPCD assigned to that group in
# the README species table.  Groups 1 and 12 cover several species, so the code
# below is one member of the group; groups 3 and 8 hold a single species each.
# TestFiaSpcdEquivalence checks every code in the table, not just these four.
GROUP_TO_FIA = {
    1: 125,   # Red pine           -> Miscellaneous softwood
    3: 129,   # Eastern white pine
    8: 261,   # Eastern hemlock
    12: 746,  # Quaking aspen      -> Poplars
}


@pytest.fixture(params=["group", "fia"])
def species_id(request):
    """
    Run each test once per species identifier mode.

    Yields "group" (species group number, as in the original paper) and
    then "fia" (FIA species code).
    """
    return request.param


def as_species(groups, species_id):
    """
    Translate species group number(s) into identifiers for `species_id`.

    Returns the input unchanged for species_id="group"; for species_id="fia"
    returns the corresponding FIA species code(s), preserving whether the
    input was a scalar, a list, or a NumPy array.
    """
    if species_id == "group":
        return groups
    if isinstance(groups, np.ndarray):
        return np.array([GROUP_TO_FIA[int(g)] for g in groups])
    if isinstance(groups, (list, tuple)):
        return [GROUP_TO_FIA[int(g)] for g in groups]
    return GROUP_TO_FIA[int(groups)]


class TestReadmeExample:
    """
    Runs tests on the example in the README.

    The example is described as:
    A poplar tree (species group = 12; FIA SPCD 746, Quaking aspen)
    with DBH = 15.5 in., compacted crown ratio = 40 percent,
    tree class = acceptable (TC = 2), and crown class = codominant
    (CC1 = 0, CC2 = 1, CC3 = 0).

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

    def test_total_height(self, species_id):
        """
        Prediction of total height (top diameter = 0):
        H = (91.5048) * (1 - exp(-0.1023 * 15.5))
            ^ (0.0054*40 + 0.0638*2 + (0/15.5 + 0.01)^0.1422)
        H ~= 75.0 ft

        The paper reports approximately 75.0 ft.
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 0.0,
            )
            == 75.08210159707517
        )

    def test_bole_height(self, species_id):
        """
        Prediction of bole height (4-in. top diameter):
        H = (-4.2401*4 + 91.5048) * (1 - exp(-0.1023 * 15.5))
            ^ (0.0054*40 + 0.0638*2 + (4/15.5 + 0.01)^0.1422)
        H ~= 56.9 ft

        The paper reports approximately 56.9 ft.
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 4.0,
            )
            == 56.9740957505897
        )

    def test_sawlog_height(self, species_id):
        """
        Prediction of sawlog height (9-in. top diameter):
        H = (-4.2401*9 + 91.5048) * (1 - exp(-0.1023 * 15.5))
            ^ (0.0054*40 + 0.0638*2 + (9/15.5 + 0.01)^0.1422)
        H ~= 39.8 ft

        The paper reports approximately 39.8 ft.
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 9.0,
            )
            == 39.859721210981185
        )


class TestSoftwoodDominant:
    """
    Tests a softwood species group with dominant/preferred attributes.

    Assume a tree in species group 1 (FIA SPCD 125, Red pine) with
    DBH = 20.0 in., compacted crown ratio = 55 percent, tree class =
    preferred (TC = 1), and crown class = dominant (CC1 = 0, CC2 = 1,
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

    def test_total_height(self, species_id):
        """
        Total height prediction (top diameter = 0).
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 0.0,
            )
            == 76.55781961600512
        )

    def test_bole_height(self, species_id):
        """
        Bole height prediction (4-in. top diameter).
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 4.0,
            )
            == 62.28412088723717
        )

    def test_sawlog_height(self, species_id):
        """
        Sawlog height prediction (9-in. top diameter).
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 9.0,
            )
            == 44.001753341279
        )


class TestOvertoppedRough:
    """
    Tests an overtopped rough-cull tree.

    Assume a tree in species group 8 (FIA SPCD 261, Eastern hemlock) with
    DBH = 12.0 in., compacted crown ratio = 30 percent, tree class = rough
    (TC = 3), and crown class = overtopped (CC1 = 0, CC2 = 0, CC3 = 1).

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

    def test_total_height(self, species_id):
        """
        Total height prediction (top diameter = 0).
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 0.0,
            )
            == 43.85727492152837
        )

    def test_bole_height(self, species_id):
        """
        Bole height prediction (4-in. top diameter).
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 4.0,
            )
            == 32.436949584096766
        )


class TestDeadTree:
    """
    Tests a dead tree.

    Assume a dead tree in species group 3 (FIA SPCD 129, Eastern white pine)
    with DBH = 18.0 in., compacted crown ratio = 25 percent, tree class =
    dead (TC = 3), and crown class = dead (CC1 = 1, CC2 = 0, CC3 = 0).

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

    def test_total_height(self, species_id):
        """
        Total height prediction (top diameter = 0).
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 0.0,
            )
            == 68.84553875174208
        )

    def test_bole_height(self, species_id):
        """
        Bole height prediction (4-in. top diameter).
        """
        assert (
            predict_height_westfall(
                as_species(self.species_group, species_id), species_id,
                self.dbh, self.ccr, self.tree_class, self.crown_class, 4.0,
            )
            == 54.501248362832285
        )


class TestVectorized:
    """
    Test full vectorization: all six parameters may be arrays.

    Uses the same four trees from the scalar test classes, each with
    a different species group, tree class, and crown class:

    Tree 1 (TestReadmeExample):
        species_group=12 (SPCD 746), DBH=15.5, CCR=40,
        tree_class="acceptable", crown_class="codominant"
    Tree 2 (TestSoftwoodDominant):
        species_group=1  (SPCD 125), DBH=20.0, CCR=55,
        tree_class="preferred",   crown_class="dominant"
    Tree 3 (TestOvertoppedRough):
        species_group=8  (SPCD 261), DBH=12.0, CCR=30,
        tree_class="rough",       crown_class="overtopped"
    Tree 4 (TestDeadTree):
        species_group=3  (SPCD 129), DBH=18.0, CCR=25,
        tree_class="dead",        crown_class="dead"
    """

    species_group = np.array([12, 1, 8, 3])
    dbh = np.array([15.5, 20.0, 12.0, 18.0])
    ccr = np.array([40.0, 55.0, 30.0, 25.0])
    tree_class = np.array(["acceptable", "preferred", "rough", "dead"])
    crown_class = np.array(["codominant", "dominant", "overtopped", "dead"])

    def test_total_height(self, species_id):
        """Vectorized total height matches individual scalar calls."""
        result = predict_height_westfall(
            as_species(self.species_group, species_id), species_id,
            self.dbh, self.ccr, self.tree_class, self.crown_class, 0.0,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == pytest.approx(75.08210159707517, rel=1e-12)   # TestReadmeExample
        assert result[1] == pytest.approx(76.55781961600512, rel=1e-12)   # TestSoftwoodDominant
        assert result[2] == pytest.approx(43.85727492152837, rel=1e-12)   # TestOvertoppedRough
        assert result[3] == pytest.approx(68.84553875174208, rel=1e-12)   # TestDeadTree

    def test_bole_height(self, species_id):
        """Vectorized bole height (4-in. top diameter) matches scalar calls."""
        result = predict_height_westfall(
            as_species(self.species_group, species_id), species_id,
            self.dbh, self.ccr, self.tree_class, self.crown_class, 4.0,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == pytest.approx(56.9740957505897, rel=1e-12)    # TestReadmeExample
        assert result[1] == pytest.approx(62.28412088723717, rel=1e-12)   # TestSoftwoodDominant
        assert result[2] == pytest.approx(32.436949584096766, rel=1e-12)  # TestOvertoppedRough
        assert result[3] == pytest.approx(54.501248362832285, rel=1e-12)  # TestDeadTree

    def test_vectorized_top_diameter(self, species_id):
        """Vectorized with varying top diameters."""
        top_diam = np.array([0.0, 4.0, 9.0, 0.0])
        result = predict_height_westfall(
            as_species(self.species_group, species_id), species_id,
            self.dbh, self.ccr, self.tree_class, self.crown_class, top_diam,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == pytest.approx(75.08210159707517, rel=1e-12)    # tree 1 total height
        assert result[1] == pytest.approx(62.28412088723717, rel=1e-12)    # tree 2 bole height
        assert result[2] == pytest.approx(17.149335239781124, rel=1e-12)   # tree 3 sawlog height (group 8 9-in)
        assert result[3] == pytest.approx(68.84553875174208, rel=1e-12)    # tree 4 total height

    def test_list_input(self, species_id):
        """List inputs for all parameters produce the same results as arrays."""
        result = predict_height_westfall(
            as_species([12, 1, 8, 3], species_id),
            species_id,
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


class TestFiaSpcdEquivalence:
    """
    Tests that species_id="fia" produces identical results to species_id="group".

    Every FIA species code listed for a group in the README must resolve to
    that group, so a prediction made from any of its codes has to match the
    prediction made from the group number exactly.
    """

    @pytest.mark.parametrize(
        "group, fia_spcd",
        [
            (1, 6212), (1, 91), (1, 105), (1, 125), (1, 126), (1, 128), (1, 130),
            (2, 71),
            (3, 129),
            (4, 94),
            (5, 95),
            (6, 97),
            (7, 12),
            (8, 261),
            (9, 241),
            (10, 318),
            (11, 541), (11, 543), (11, 544),
            (12, 741), (12, 742), (12, 743), (12, 744), (12, 746),
            (13, 407), (13, 762), (13, 806), (13, 833), (13, 837), (13, 951),
            (14, 371),
            (15, 375),
            (16, 310), (16, 315), (16, 317), (16, 319), (16, 320), (16, 331),
            (16, 356), (16, 372), (16, 379), (16, 391), (16, 601), (16, 641),
            (16, 660), (16, 701), (16, 761), (16, 763), (16, 802), (16, 804),
            (16, 920), (16, 922), (16, 927), (16, 935), (16, 970), (16, 972),
            (17, 316),
            (18, 531),
        ],
    )
    def test_every_fia_spcd_matches_its_group(self, group, fia_spcd):
        """Each FIA code in the README table matches its species group."""
        expected = predict_height_westfall(
            group, "group", 15.5, 40, "acceptable", "codominant", 4.0
        )
        result = predict_height_westfall(
            fia_spcd, "fia", 15.5, 40, "acceptable", "codominant", 4.0
        )
        assert result == expected

    def test_array_fia_spcd_matches_species_group(self):
        """An array of FIA codes matches the equivalent species group array."""
        expected = predict_height_westfall(
            [12, 1, 8, 3],
            "group",
            [15.5, 20.0, 12.0, 18.0],
            [40.0, 55.0, 30.0, 25.0],
            ["acceptable", "preferred", "rough", "dead"],
            ["codominant", "dominant", "overtopped", "dead"],
            0.0,
        )
        result = predict_height_westfall(
            [746, 125, 261, 129],
            "fia",
            [15.5, 20.0, 12.0, 18.0],
            [40.0, 55.0, 30.0, 25.0],
            ["acceptable", "preferred", "rough", "dead"],
            ["codominant", "dominant", "overtopped", "dead"],
            0.0,
        )
        np.testing.assert_array_equal(result, expected)

    def test_invalid_species_id_raises(self):
        """A species_id other than 'group' or 'fia' raises ValueError."""
        with pytest.raises(ValueError, match="Invalid species_id"):
            predict_height_westfall(12, "groups", 15.5, 40, "acceptable", "codominant")

    def test_unknown_fia_spcd_raises(self):
        """An unrecognised FIA species code raises ValueError."""
        with pytest.raises(ValueError, match="Unknown FIA species code"):
            predict_height_westfall(
                99999, "fia", 15.5, 40, "acceptable", "codominant"
            )

    def test_unknown_fia_spcd_in_array_raises(self):
        """An unrecognised FIA species code inside an array raises ValueError."""
        with pytest.raises(ValueError, match="Unknown FIA species code"):
            predict_height_westfall(
                [746, 99999], "fia", [15.5, 15.5], [40, 40],
                ["acceptable", "acceptable"], ["codominant", "codominant"],
            )

    def test_species_group_number_rejected_as_fia_spcd(self):
        """A species group number is not accepted as an FIA species code."""
        with pytest.raises(ValueError, match="Unknown FIA species code"):
            predict_height_westfall(1, "fia", 15.5, 40, "acceptable", "codominant")


class TestValidateInputs:
    """
    Tests for _validate_inputs and the validation wired into
    predict_height_westfall.

    The range checks are exercised through both species identifier modes, so
    a valid species never masks an invalid dbh, crown ratio, top diameter,
    tree class, or crown class.
    """

    # Shared valid baseline values (species group 12 / FIA SPCD 746).
    _sg = 12
    _dbh = 15.5
    _ccr = 40.0
    _top = 0.0

    def test_invalid_species_raises(self, species_id):
        """
        An unusable species identifier raises for either mode: a group
        number outside 1-18, or an FIA code that is not in the lookup table.
        """
        bad_species, message = (
            (0, "Invalid species_group")
            if species_id == "group"
            else (99999, "Unknown FIA species code")
        )
        with pytest.raises(ValueError, match=message):
            predict_height_westfall(
                bad_species, species_id, self._dbh, self._ccr,
                "acceptable", "codominant",
            )

    def test_invalid_species_array_raises(self, species_id):
        """The same check applies element-wise to array input."""
        bad_species, message = (
            ([12, 99], "Invalid species_group")
            if species_id == "group"
            else ([746, 99999], "Unknown FIA species code")
        )
        with pytest.raises(ValueError, match=message):
            predict_height_westfall(
                bad_species, species_id, [15.5, 15.5], [40, 40],
                ["acceptable", "acceptable"], ["codominant", "codominant"],
            )

    def test_invalid_species_group_19(self):
        """Species group 19 is one past the last valid group."""
        with pytest.raises(ValueError, match="Invalid species_group"):
            predict_height_westfall(
                19, "group", self._dbh, self._ccr, "acceptable", "codominant"
            )

    def test_dbh_zero_raises(self, species_id):
        with pytest.raises(ValueError, match="dbh_in must be positive"):
            predict_height_westfall(
                as_species(self._sg, species_id), species_id, 0.0, self._ccr,
                "acceptable", "codominant",
            )

    def test_dbh_negative_raises(self, species_id):
        with pytest.raises(ValueError, match="dbh_in must be positive"):
            predict_height_westfall(
                as_species(self._sg, species_id), species_id, -1.0, self._ccr,
                "acceptable", "codominant",
            )

    def test_ccr_below_range_raises(self, species_id):
        with pytest.raises(ValueError, match="ccr_pct must be in"):
            predict_height_westfall(
                as_species(self._sg, species_id), species_id, self._dbh, -1.0,
                "acceptable", "codominant",
            )

    def test_ccr_above_range_raises(self, species_id):
        with pytest.raises(ValueError, match="ccr_pct must be in"):
            predict_height_westfall(
                as_species(self._sg, species_id), species_id, self._dbh, 101.0,
                "acceptable", "codominant",
            )

    def test_top_diam_negative_raises(self, species_id):
        with pytest.raises(ValueError, match="top_diam_in must be non-negative"):
            predict_height_westfall(
                as_species(self._sg, species_id), species_id, self._dbh, self._ccr,
                "acceptable", "codominant", -1.0,
            )

    def test_invalid_tree_class_raises(self, species_id):
        with pytest.raises(ValueError, match="Invalid tree_class"):
            predict_height_westfall(
                as_species(self._sg, species_id), species_id, self._dbh, self._ccr,
                "invalid", "codominant",
            )

    def test_invalid_crown_class_raises(self, species_id):
        with pytest.raises(ValueError, match="Invalid crown_class"):
            predict_height_westfall(
                as_species(self._sg, species_id), species_id, self._dbh, self._ccr,
                "acceptable", "invalid",
            )

    def test_validate_inputs_directly_valid(self):
        """
        _validate_inputs does not raise for valid inputs.

        This helper runs after an FIA code has already been resolved, so it
        only ever sees species group numbers.
        """
        _validate_inputs(12, 15.5, 40.0, 0.0)

    def test_validate_inputs_directly_array(self):
        """_validate_inputs does not raise for valid array inputs."""
        _validate_inputs([1, 12, 8], [10.0, 15.5, 12.0], [30.0, 40.0, 55.0], [0.0, 4.0, 9.0])
