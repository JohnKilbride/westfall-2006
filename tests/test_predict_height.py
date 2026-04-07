import numpy as np
import pytest

from westfall_2006 import predict_height_westfall


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
    Test vectorization by passing arrays to predict_height_westfall.

    Uses the same trees from the scalar test classes, all
    evaluated with species group 12 and codominant/acceptable
    attributes to allow vectorized calling:
    - DBH = [15.5, 20.0, 12.0, 18.0]
    - CCR = [40, 55, 30, 25]
    """

    species_group = 12
    dbh = np.array([15.5, 20.0, 12.0, 18.0])
    ccr = np.array([40.0, 55.0, 30.0, 25.0])
    tree_class = "acceptable"
    crown_class = "codominant"

    def test_total_height(self):
        """Vectorized total height matches individual scalar calls."""
        result = predict_height_westfall(
            self.species_group, self.dbh, self.ccr,
            self.tree_class, self.crown_class, 0.0,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == 75.08210159707517
        assert result[1] == 80.29636086963121
        assert result[2] == 69.12084600442284
        assert result[3] == 79.944568707806

    def test_bole_height(self):
        """Vectorized bole height (4-in. top diameter)."""
        result = predict_height_westfall(
            self.species_group, self.dbh, self.ccr,
            self.tree_class, self.crown_class, 4.0,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        assert result[0] == 56.9740957505897
        assert result[1] == 62.91430096299435
        assert result[2] == 50.05713847064891
        assert result[3] == 61.9136944145404

    def test_vectorized_top_diameter(self):
        """Vectorized with varying top diameters."""
        top_diam = np.array([0.0, 4.0, 9.0, 0.0])
        result = predict_height_westfall(
            self.species_group, self.dbh, self.ccr,
            self.tree_class, self.crown_class, top_diam,
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4

        # First tree: total height
        assert result[0] == 75.08210159707517
        # Second tree: bole height
        assert result[1] == 62.91430096299435
        # Fourth tree: total height
        assert result[3] == 79.944568707806

    def test_list_input(self):
        """List inputs produce the same results as numpy arrays."""
        result = predict_height_westfall(
            self.species_group,
            [15.5, 20.0, 12.0, 18.0],
            [40.0, 55.0, 30.0, 25.0],
            self.tree_class,
            self.crown_class,
            [0.0, 0.0, 0.0, 0.0],
        )

        assert isinstance(result, np.ndarray)
        assert len(result) == 4
        assert result[0] == 75.08210159707517
        assert result[1] == 80.29636086963121


class TestSpeciesGroupByName:
    """Test passing species group as a string name."""

    def test_string_name_poplars(self):
        """Species group name 'Poplars' should resolve to group 12."""
        result = predict_height_westfall(
            "Poplars", 15.5, 40, "acceptable", "codominant", 0.0,
        )
        expected = predict_height_westfall(
            12, 15.5, 40, "acceptable", "codominant", 0.0,
        )
        assert result == expected

    def test_string_name_case_insensitive(self):
        """Species group names should be case-insensitive."""
        result = predict_height_westfall(
            "poplars", 15.5, 40, "acceptable", "codominant", 0.0,
        )
        expected = predict_height_westfall(
            12, 15.5, 40, "acceptable", "codominant", 0.0,
        )
        assert result == expected

    def test_string_name_with_whitespace(self):
        """Species group names should be whitespace-tolerant."""
        result = predict_height_westfall(
            "  Poplars  ", 15.5, 40, "acceptable", "codominant", 0.0,
        )
        expected = predict_height_westfall(
            12, 15.5, 40, "acceptable", "codominant", 0.0,
        )
        assert result == expected

    def test_string_name_eastern_white_pine(self):
        """Multi-word species group name should work."""
        result = predict_height_westfall(
            "Eastern white pine", 18.0, 25, "dead", "dead", 0.0,
        )
        expected = predict_height_westfall(
            3, 18.0, 25, "dead", "dead", 0.0,
        )
        assert result == expected

    def test_invalid_string_name(self):
        """Invalid species group name should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown species group name"):
            predict_height_westfall(
                "InvalidTree", 15.5, 40, "acceptable", "codominant",
            )

    def test_string_list_same_group(self):
        """List of species group names resolving to the same group."""
        # "Poplars" appears only once, so use a list with duplicates
        result = predict_height_westfall(
            ["Poplars", "Poplars"], 15.5, 40, "acceptable", "codominant", 0.0,
        )
        expected = predict_height_westfall(
            12, 15.5, 40, "acceptable", "codominant", 0.0,
        )
        assert result == expected

    def test_string_list_different_groups(self):
        """List of names resolving to different groups should raise."""
        with pytest.raises(ValueError, match="same group"):
            predict_height_westfall(
                ["Poplars", "Ash"], 15.5, 40, "acceptable", "codominant",
            )


class TestFiaSpcd:
    """Test passing FIA species codes."""

    def test_single_fia_code(self):
        """FIA code 746 (Quaking aspen) should resolve to group 12."""
        result = predict_height_westfall(
            dbh_in=15.5, ccr_pct=40, tree_class="acceptable",
            crown_class="codominant", top_diam_in=0.0, fia_spcd=746,
        )
        expected = predict_height_westfall(
            12, 15.5, 40, "acceptable", "codominant", 0.0,
        )
        assert result == expected

    def test_single_fia_code_beech(self):
        """FIA code 531 (American beech) should resolve to group 18."""
        result = predict_height_westfall(
            dbh_in=15.5, ccr_pct=40, tree_class="acceptable",
            crown_class="codominant", top_diam_in=0.0, fia_spcd=531,
        )
        expected = predict_height_westfall(
            18, 15.5, 40, "acceptable", "codominant", 0.0,
        )
        assert result == expected

    def test_fia_code_list_same_group(self):
        """List of FIA codes in the same group should work."""
        # 741 (Balsam poplar), 743 (Bigtooth aspen), 746 (Quaking aspen)
        # all belong to group 12
        result = predict_height_westfall(
            dbh_in=15.5, ccr_pct=40, tree_class="acceptable",
            crown_class="codominant", top_diam_in=0.0,
            fia_spcd=[741, 743, 746],
        )
        expected = predict_height_westfall(
            12, 15.5, 40, "acceptable", "codominant", 0.0,
        )
        assert result == expected

    def test_fia_code_list_different_groups(self):
        """List of FIA codes from different groups should raise."""
        # 746 = group 12, 531 = group 18
        with pytest.raises(ValueError, match="same species group"):
            predict_height_westfall(
                dbh_in=15.5, ccr_pct=40, tree_class="acceptable",
                crown_class="codominant", fia_spcd=[746, 531],
            )

    def test_invalid_fia_code(self):
        """Invalid FIA code should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown FIA species code"):
            predict_height_westfall(
                dbh_in=15.5, ccr_pct=40, tree_class="acceptable",
                crown_class="codominant", fia_spcd=9999,
            )

    def test_both_species_group_and_fia_raises(self):
        """Providing both species_group and fia_spcd should raise."""
        with pytest.raises(ValueError, match="not both"):
            predict_height_westfall(
                species_group=12, dbh_in=15.5, ccr_pct=40,
                tree_class="acceptable", crown_class="codominant",
                fia_spcd=746,
            )

    def test_neither_species_group_nor_fia_raises(self):
        """Providing neither species_group nor fia_spcd should raise."""
        with pytest.raises(ValueError, match="Must provide"):
            predict_height_westfall(
                dbh_in=15.5, ccr_pct=40,
                tree_class="acceptable", crown_class="codominant",
            )

    def test_fia_code_vectorized(self):
        """FIA code should work with vectorized inputs."""
        dbh = np.array([15.5, 20.0, 12.0, 18.0])
        ccr = np.array([40.0, 55.0, 30.0, 25.0])
        result = predict_height_westfall(
            dbh_in=dbh, ccr_pct=ccr, tree_class="acceptable",
            crown_class="codominant", top_diam_in=0.0, fia_spcd=746,
        )
        expected = predict_height_westfall(
            12, dbh, ccr, "acceptable", "codominant", 0.0,
        )
        np.testing.assert_array_equal(result, expected)
