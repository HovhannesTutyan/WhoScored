from django.test import SimpleTestCase

from apps.math_utils.blended_poisson import calculate_blended_lambdas
from apps.math_utils.monte_carlo import run_poisson_simulation
from apps.math_utils.normalization import min_max_normalize, percentile_rank, reverse_normalize, z_score_normalize
from apps.math_utils.poisson import outcome_probabilities, poisson_probability, score_matrix
from apps.math_utils.xg_poisson import calculate_xg_lambdas


class MathUtilsTests(SimpleTestCase):
    def test_min_max_normalize(self):
        self.assertAlmostEqual(min_max_normalize(5, [0, 5, 10]), 0.5)
        self.assertAlmostEqual(reverse_normalize(2, [1, 2, 3]), 0.5)

    def test_z_score_and_percentile(self):
        self.assertAlmostEqual(round(z_score_normalize(3, [1, 2, 3, 4, 5]), 5), 0.0)
        self.assertAlmostEqual(percentile_rank(3, [1, 2, 3, 4, 5]), 0.6)

    def test_poisson_probability_and_matrix(self):
        self.assertAlmostEqual(round(poisson_probability(1.5, 2), 6), 0.251021)
        matrix = score_matrix(1.2, 1.0)
        self.assertAlmostEqual(sum(sum(row) for row in matrix), 1.0, places=4)
        outcomes = outcome_probabilities(matrix)
        self.assertAlmostEqual(sum(outcomes.values()), 1.0, places=4)

    def test_xg_and_blended_lambdas(self):
        xg_lambda_a, xg_lambda_b = calculate_xg_lambdas(1.8, 0.9, 1.4, 1.1, 1.5)
        self.assertAlmostEqual(xg_lambda_a, 1.32)
        self.assertAlmostEqual(xg_lambda_b, 0.84)
        blended_a, blended_b = calculate_blended_lambdas(1.4, 1.0, xg_lambda_a, xg_lambda_b)
        self.assertIsNotNone(blended_a)
        self.assertIsNotNone(blended_b)

    def test_monte_carlo_simulation(self):
        result = run_poisson_simulation(1.4, 1.1, 1000)
        self.assertIn("outcomes", result)
        self.assertIn("scorelines", result)
        self.assertIn("over_under", result)
        self.assertIn("btts", result)
        self.assertAlmostEqual(sum(result["outcomes"].values()), 1.0, places=1)
