import os
import sys
import unittest
from unittest import mock

# Ensure the BusStopAlert project root is importable
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.utils.haversine import haversine
import app.components.bus_stop_search as bus_stop_search
import app.hooks.use_alert as use_alert


class TestHaversine(unittest.TestCase):
    def test_same_point_distance_zero(self):
        coord = (32.0853, 34.7818)  # Tel Aviv approx
        self.assertAlmostEqual(haversine(coord, coord), 0.0, places=6)

    def test_known_distance_within_tolerance(self):
        # Approx distance Tel Aviv to Jerusalem ~ 54-67 km depending on coordinates
        tel_aviv = (32.0853, 34.7818)
        jerusalem = (31.7683, 35.2137)
        dist = haversine(tel_aviv, jerusalem)
        self.assertTrue(50 <= dist <= 70, f"Distance {dist} not in expected range")


class TestBusStopSearch(unittest.TestCase):
    @mock.patch("app.components.bus_stop_search.geolocator")
    def test_search_station_returns_coords_for_valid_name(self, mock_geo):
        mock_location = mock.Mock(latitude=31.778, longitude=35.235)
        mock_geo.geocode.return_value = mock_location

        coords = bus_stop_search.search_station("Jerusalem Central Bus Station")

        self.assertEqual(coords, (31.778, 35.235))
        mock_geo.geocode.assert_called_once()

    @mock.patch("app.components.bus_stop_search.geolocator")
    def test_search_station_returns_none_when_not_found(self, mock_geo):
        mock_geo.geocode.return_value = None

        coords = bus_stop_search.search_station("Some Nonexistent Place 12345")

        self.assertIsNone(coords)
        mock_geo.geocode.assert_called_once()

    @mock.patch("app.components.bus_stop_search.st")
    @mock.patch("app.components.bus_stop_search.search_station")
    def test_bus_stop_search_ui_success_flow(self, mock_search, mock_st):
        mock_st.text_input.return_value = "Jerusalem"
        mock_search.return_value = (31.778, 35.235)

        result = bus_stop_search.bus_stop_search_ui()

        self.assertEqual(result, (31.778, 35.235))
        mock_st.success.assert_called_once()
        mock_st.warning.assert_not_called()

    @mock.patch("app.components.bus_stop_search.st")
    @mock.patch("app.components.bus_stop_search.search_station")
    def test_bus_stop_search_ui_not_found(self, mock_search, mock_st):
        mock_st.text_input.return_value = "Unknown Station"
        mock_search.return_value = None

        result = bus_stop_search.bus_stop_search_ui()

        self.assertIsNone(result)
        mock_st.warning.assert_called_once()
        mock_st.success.assert_not_called()

    @mock.patch("app.components.bus_stop_search.st")
    def test_bus_stop_search_ui_empty_query(self, mock_st):
        mock_st.text_input.return_value = ""  # user not typing anything

        result = bus_stop_search.bus_stop_search_ui()

        self.assertIsNone(result)
        mock_st.success.assert_not_called()
        mock_st.warning.assert_not_called()


class TestUseAlert(unittest.TestCase):
    @mock.patch("app.hooks.use_alert.st")
    def test_check_alert_triggers_and_returns_true_when_button_clicked(self, mock_st):
        mock_st.button.return_value = True

        res = use_alert.check_alert(2)

        self.assertTrue(res)
        mock_st.warning.assert_called_once()
        mock_st.button.assert_called_once()

    @mock.patch("app.hooks.use_alert.st")
    def test_check_alert_triggers_but_returns_false_when_button_not_clicked(self, mock_st):
        mock_st.button.return_value = False

        res = use_alert.check_alert(1.5)

        self.assertFalse(res)
        mock_st.warning.assert_called_once()
        mock_st.button.assert_called_once()

    @mock.patch("app.hooks.use_alert.st")
    def test_check_alert_does_not_trigger_when_over_threshold(self, mock_st):
        res = use_alert.check_alert(3)

        self.assertFalse(res)
        mock_st.warning.assert_not_called()
        mock_st.button.assert_not_called()


class TestMainAPI(unittest.TestCase):
    def setUp(self):
        # Import here to avoid interfering with other tests' imports
        from main_api import app, latest_coords
        self.app = app
        self.client = app.test_client()
        # reset shared state before each test
        latest_coords["lat"] = None
        latest_coords["lon"] = None

    def test_latest_location_404_when_no_coords(self):
        res = self.client.get("/location/latest")
        self.assertEqual(res.status_code, 404)
        self.assertIn("error", res.get_json())

    def test_post_location_then_get_latest_success(self):
        post_res = self.client.post("/location", json={"lat": 31.5, "lon": 35.1})
        self.assertEqual(post_res.status_code, 200)
        self.assertEqual(post_res.get_json().get("status"), "ok")

        get_res = self.client.get("/location/latest")
        self.assertEqual(get_res.status_code, 200)
        data = get_res.get_json()
        self.assertEqual(data["lat"], 31.5)
        self.assertEqual(data["lon"], 35.1)


class TestHaversineMore(unittest.TestCase):
    def test_haversine_symmetry(self):
        a = (32.0853, 34.7818)
        b = (31.7683, 35.2137)
        self.assertAlmostEqual(haversine(a, b), haversine(b, a), places=6)

    def test_haversine_antipodal_distance_range(self):
        # Approx antipodal points: (0,0) and (0,180)
        a = (0.0, 0.0)
        b = (0.0, 180.0)
        d = haversine(a, b)
        # Max great-circle distance ~ pi * R ≈ 20037 km; allow a small tolerance
        self.assertTrue(20000 <= d <= 20050, f"Unexpected antipodal distance: {d}")


class TestBusStopSearchContract(unittest.TestCase):
    @mock.patch("app.components.bus_stop_search.geolocator")
    def test_search_station_uses_timeout_and_returns_floats(self, mock_geo):
        mock_location = mock.Mock(latitude=31.0, longitude=35.0)
        mock_geo.geocode.return_value = mock_location

        coords = bus_stop_search.search_station("Some Station")

        self.assertEqual(coords, (31.0, 35.0))
        # Ensure timeout parameter is passed as defined in the implementation
        mock_geo.geocode.assert_called_once_with("Some Station", timeout=10)
        self.assertIsInstance(coords[0], float)
        self.assertIsInstance(coords[1], float)


class TestUseAlertBoundary(unittest.TestCase):
    @mock.patch("app.hooks.use_alert.st")
    def test_negative_time_triggers_warning_and_button(self, mock_st):
        mock_st.button.return_value = True

        res = use_alert.check_alert(-5)

        self.assertTrue(res)
        mock_st.warning.assert_called_once()
        mock_st.button.assert_called_once()


if __name__ == "__main__":
    unittest.main()
