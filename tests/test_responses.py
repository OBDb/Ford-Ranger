import glob
import os
import pytest
from pathlib import Path
from typing import Dict, Any

# These will be imported from the schemas repository
from schemas.python.can_frame import CANIDFormat
from schemas.python.json_formatter import format_file
from schemas.python.signals_testing import obd_testrunner_by_year

REPO_ROOT = Path(__file__).parent.parent.absolute()

TEST_CASES = [
    {
        "model_year": 2004,
        "tests": [
            # Fuel tank level
            ("7280462618519", {"RANGER_FLI": 9.803921568627452}),
            ("7280462618575", {"RANGER_FLI": 45.88235294117647}),
        ]
    },

    {
        "model_year": 2019,
        "tests": [
            # Tire pressures
            ("72E05622813021B", {"RANGER_TP_FL": 26.95}),
            ("72E05622813027F", {"RANGER_TP_FL": 31.95}),
            ("72E05622814022A", {"RANGER_TP_FR": 27.7}),
            ("72E056228140278", {"RANGER_TP_FR": 31.6}),
            ("72E05622815021B", {"RANGER_TP_RR": 26.95}),
            ("72E05622815027A", {"RANGER_TP_RR": 31.7}),
            ("72E05622816022A", {"RANGER_TP_RL": 27.7}),
            ("72E056228160296", {"RANGER_TP_RL": 33.1}),

            # Gears
            ("7E804621E1201", {"RANGER_GEAR": "1"}),
            ("7E804621E1202", {"RANGER_GEAR": "2"}),
            ("7E804621E1203", {"RANGER_GEAR": "3"}),
            ("7E804621E1204", {"RANGER_GEAR": "4"}),
            ("7E804621E1205", {"RANGER_GEAR": "5"}),
            ("7E804621E1206", {"RANGER_GEAR": "6"}),
            ("7E804621E1207", {"RANGER_GEAR": "7"}),
            ("7E804621E1208", {"RANGER_GEAR": "8"}),
            ("7E804621E1209", {"RANGER_GEAR": "9"}),
            ("7E804621E120A", {"RANGER_GEAR": "10"}),
            ("7E804621E1232", {"RANGER_GEAR": None}),  # TODO: Unknown mapping
            ("7E804621E123C", {"RANGER_GEAR": None}),  # TODO: Unknown mapping
            ("7E804621E1246", {"RANGER_GEAR": None}),  # TODO: Unknown mapping

            # Gear shift
            ("7E804621E2364", {"RANGER_GEAR_SHFT": None}),  # TODO: Unknown mapping
            ("7E804621E2367", {"RANGER_GEAR_SHFT": None}),  # TODO: Unknown mapping

            # Transmission oil temperature
            ("7E805621E1C009C", {"RANGER_TOT": 9.75}),
            ("7E805621E1C05DD", {"RANGER_TOT": 93.8125}),

            # Fuel level
            ("7E80462F42F00", {"RANGER_FLI": 0}),
            ("7E80462F42FAF", {"RANGER_FLI": 68.62745098039215}),
            ("7E80462F42FFF", {"RANGER_FLI": 100}),
        ]
    },

    {
        "model_year": 2021,
        "tests": [
            # Fuel level
            ("7E80462F42F00", {"RANGER_FLI": 0}),
            ("7E80462F42F95", {"RANGER_FLI": 58.431372549019606}),
            ("7E80462F42FFC", {"RANGER_FLI": 98.82352941176471}),
        ]
    },

    {
        "model_year": 2024,
        "tests": [
            # Tire pressures
            ("72E0562281302C9", {"RANGER_TP_FL": 35.65}),
            ("72E05622813034E", {"RANGER_TP_FL": 42.3}),
            ("72E0562281402CE", {"RANGER_TP_FR": 35.9}),
            ("72E05622814034E", {"RANGER_TP_FR": 42.3}),
            ("72E0562281502D8", {"RANGER_TP_RR": 36.4}),
            ("72E056228150358", {"RANGER_TP_RR": 42.8}),
            ("72E0562281602C9", {"RANGER_TP_RL": 35.65}),
            ("72E056228160353", {"RANGER_TP_RL": 42.55}),

            # Gears
            ("7E804621E1201", {"RANGER_GEAR": "1"}),
            ("7E804621E1202", {"RANGER_GEAR": "2"}),
            ("7E804621E1203", {"RANGER_GEAR": "3"}),
            ("7E804621E1204", {"RANGER_GEAR": "4"}),
            ("7E804621E1205", {"RANGER_GEAR": "5"}),
            ("7E804621E1206", {"RANGER_GEAR": "6"}),
            ("7E804621E1207", {"RANGER_GEAR": "7"}),
            ("7E804621E1208", {"RANGER_GEAR": "8"}),
            ("7E804621E1209", {"RANGER_GEAR": "9"}),
            ("7E804621E120A", {"RANGER_GEAR": "10"}),
            ("7E804621E1232", {"RANGER_GEAR": None}),  # TODO: Unknown mapping
            ("7E804621E123C", {"RANGER_GEAR": None}),  # TODO: Unknown mapping
            ("7E804621E1246", {"RANGER_GEAR": None}),  # TODO: Unknown mapping

            # Gear shift
            ("7E804621E2364", {"RANGER_GEAR_SHFT": None}),  # TODO: Unknown mapping
            ("7E804621E2365", {"RANGER_GEAR_SHFT": None}),  # TODO: Unknown mapping
            ("7E804621E2366", {"RANGER_GEAR_SHFT": None}),  # TODO: Unknown mapping
            ("7E804621E2367", {"RANGER_GEAR_SHFT": None}),  # TODO: Unknown mapping
            ("7E804621E2369", {"RANGER_GEAR_SHFT": None}),  # TODO: Unknown mapping

            # Transmission oil temperature
            ("7E805621E1C006B", {"RANGER_TOT": 6.6875}),
            ("7E805621E1C0601", {"RANGER_TOT": 96.0625}),

            # Fuel level
            ("7E80462F42F00", {"RANGER_FLI": 0}),
            ("7E80462F42F78", {"RANGER_FLI": 47.05882352941177}),
            ("7E80462F42FFD", {"RANGER_FLI": 99.2156862745098}),
        ]
    },
]

@pytest.mark.parametrize(
    "test_group",
    TEST_CASES,
    ids=lambda test_case: f"MY{test_case['model_year']}"
)
def test_signals(test_group: Dict[str, Any]):
    """Test signal decoding against known responses."""
    # Run each test case in the group
    for response_hex, expected_values in test_group["tests"]:
        try:
            obd_testrunner_by_year(
                test_group['model_year'],
                response_hex,
                expected_values,
                can_id_format=CANIDFormat.ELEVEN_BIT
            )
        except Exception as e:
            pytest.fail(
                f"Failed on response {response_hex} "
                f"(Model Year: {test_group['model_year']}: {e}"
            )

def get_json_files():
    """Get all JSON files from the signalsets/v3 directory."""
    signalsets_path = os.path.join(REPO_ROOT, 'signalsets', 'v3')
    json_files = glob.glob(os.path.join(signalsets_path, '*.json'))
    # Convert full paths to relative filenames
    return [os.path.basename(f) for f in json_files]

@pytest.mark.parametrize("test_file",
    get_json_files(),
    ids=lambda x: x.split('.')[0].replace('-', '_')  # Create readable test IDs
)
def test_formatting(test_file):
    """Test signal set formatting for all vehicle models in signalsets/v3/."""
    signalset_path = os.path.join(REPO_ROOT, 'signalsets', 'v3', test_file)

    formatted = format_file(signalset_path)

    with open(signalset_path) as f:
        assert f.read() == formatted

if __name__ == '__main__':
    pytest.main([__file__])
