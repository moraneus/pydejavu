import pytest
from pydejavu.core.monitor import Monitor
import tempfile
import csv
import random
import time


class TestEndToEndScenarios:
    @pytest.fixture
    def sample_log_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
            writer = csv.writer(temp_file)
            writer.writerows([
                ['p', 3], ['q', 5], ['p', 7], ['q', 2], ['p', 1],
                ['r', 3, 5], ['r', 7, 2], ['r', 1, 2], ['w', -1, -2]
            ])
        return temp_file.name

    @pytest.fixture
    def complex_log_file(self):
        events = []
        for _ in range(1000):
            event_type = random.choice(['p', 'q', 'r'])
            if event_type in ['p', 'q']:
                events.append([event_type, random.randint(1, 100)])
            else:
                events.append([event_type, random.randint(1, 100), random.randint(1, 100)])

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
            writer = csv.writer(temp_file)
            writer.writerows(events)
        return temp_file.name, events

    @pytest.fixture
    def dejavu_instance(self):
        specification = """
        prop example1 : forall x . forall y . ((p(x, "true") | @@q(y)) -> P r(x, y))
        prop example2 : forall x . exists y . (p(x, "true") -> P r(x, y))
        """
        dejavu = Monitor(i_spec=specification, i_bits=20, i_statistics=True)
        dejavu.init_monitor()

        @dejavu.operational("p")
        def handle_p(arg_x: int):
            x_lt_y = arg_x < dejavu.get_shared("y", 0)
            dejavu.set_shared("last_seen_q", False)
            return "p", arg_x, x_lt_y

        @dejavu.operational("q")
        def handle_q(arg_y: int):
            dejavu.set_shared("y", arg_y)
            dejavu.set_shared("last_seen_q", True)
            return "q", arg_y

        @dejavu.operational("r")
        def handle_r(arg_x: int, arg_y: int):
            return ["r", arg_x, arg_y]

        @dejavu.operational("w")
        def handle_r(arg_x: int, arg_y: int):
            dejavu.set_shared("x", arg_x)
            dejavu.set_shared("y", arg_y)

        return dejavu

    def test_basic_event_bulk_as_dict_processing(self, dejavu_instance, sample_log_file):
        expected_results = [
            {"Original Event": "p,3", "Modified Event": "p,3,false", "Eval result": "example1=true,example2=true"},
            {"Original Event": "q,5", "Modified Event": "q,5", "Eval result": "example1=true,example2=true"},
            {"Original Event": "p,7", "Modified Event": "p,7,false", "Eval result": "example1=true,example2=true"},
            {"Original Event": "q,2", "Modified Event": "q,2", "Eval result": "example1=true,example2=true"},
            {"Original Event": "p,1", "Modified Event": "p,1,true", "Eval result": "example1=false,example2=false"},
            {"Original Event": "r,3,5", "Modified Event": "r,3,5", "Eval result": "example1=false,example2=true"},
            {"Original Event": "r,7,2", "Modified Event": "r,7,2", "Eval result": "example1=true,example2=true"},
            {"Original Event": "r,1,2", "Modified Event": "r,1,2", "Eval result": "example1=true,example2=true"},
            {"Original Event": "w,-1,-2", "Modified Event": "skip", "Eval result": None}
        ]

        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_dict(sample_log_file, chunk_size=3):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))

        assert len(actual_results) == len(expected_results), "Number of processed events doesn't match expected"

        for expected, actual in zip(expected_results, actual_results):
            assert expected == actual, f"Mismatch in results: expected {expected}, got {actual}"

    def test_basic_event_bulk_as_string_processing(self, dejavu_instance, sample_log_file):
        expected_results = [
            {"Original Event": "p,3", "Modified Event": "p,3,false", "Eval result": "example1=true,example2=true"},
            {"Original Event": "q,5", "Modified Event": "q,5", "Eval result": "example1=true,example2=true"},
            {"Original Event": "p,7", "Modified Event": "p,7,false", "Eval result": "example1=true,example2=true"},
            {"Original Event": "q,2", "Modified Event": "q,2", "Eval result": "example1=true,example2=true"},
            {"Original Event": "p,1", "Modified Event": "p,1,true", "Eval result": "example1=false,example2=false"},
            {"Original Event": "r,3,5", "Modified Event": "r,3,5", "Eval result": "example1=false,example2=true"},
            {"Original Event": "r,7,2", "Modified Event": "r,7,2", "Eval result": "example1=true,example2=true"},
            {"Original Event": "r,1,2", "Modified Event": "r,1,2", "Eval result": "example1=true,example2=true"},
            {"Original Event": "w,-1,-2", "Modified Event": "skip", "Eval result": None}
        ]

        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_string(sample_log_file, chunk_size=3):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))

        assert len(actual_results) == len(expected_results), "Number of processed events doesn't match expected"

        for expected, actual in zip(expected_results, actual_results):
            assert expected == actual, f"Mismatch in results: expected {expected}, got {actual}"

    def test_p_event_modification_bulk_events_as_dict(self, dejavu_instance, sample_log_file):
        expected_p_events = [
            {"Original Event": "p,3", "Modified Event": "p,3,false"},
            {"Original Event": "p,7", "Modified Event": "p,7,false"},
            {"Original Event": "p,1", "Modified Event": "p,1,true"}
        ]

        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_dict(sample_log_file, chunk_size=3):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))

        actual_p_events = [
            {"Original Event": r["Original Event"], "Modified Event": r["Modified Event"]}
            for r in actual_results if r["Original Event"].startswith("p")
        ]

        assert len(actual_p_events) == len(expected_p_events), "Number of 'p' events doesn't match expected"

        for expected, actual in zip(expected_p_events, actual_p_events):
            assert expected == actual, f"Mismatch in 'p' event results: expected {expected}, got {actual}"

    def test_p_event_modification_bulk_events_as_string(self, dejavu_instance, sample_log_file):
        expected_p_events = [
            {"Original Event": "p,3", "Modified Event": "p,3,false"},
            {"Original Event": "p,7", "Modified Event": "p,7,false"},
            {"Original Event": "p,1", "Modified Event": "p,1,true"}
        ]

        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_string(sample_log_file, chunk_size=3):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))

        actual_p_events = [
            {"Original Event": r["Original Event"], "Modified Event": r["Modified Event"]}
            for r in actual_results if r["Original Event"].startswith("p")
        ]

        assert len(actual_p_events) == len(expected_p_events), "Number of 'p' events doesn't match expected"

        for expected, actual in zip(expected_p_events, actual_p_events):
            assert expected == actual, f"Mismatch in 'p' event results: expected {expected}, got {actual}"

    def test_shared_variable_updates_bulk_events_as_dict(self, dejavu_instance, sample_log_file):
        expected_final_y = -2
        expected_final_last_seen_q = False

        for chunk in dejavu_instance.read_bulk_events_as_dict(sample_log_file, chunk_size=3):
            dejavu_instance.verify.process_events(chunk)

        assert dejavu_instance.get_shared(
            "y") == expected_final_y, \
            f"Final 'y' value mismatch: expected {expected_final_y}, " \
            f"got {dejavu_instance.get_shared('y')}"

        assert dejavu_instance.get_shared(
            "last_seen_q") == expected_final_last_seen_q, \
            f"Final 'last_seen_q' value mismatch: expected {expected_final_last_seen_q}, " \
            f"got {dejavu_instance.get_shared('last_seen_q')}"

    def test_shared_variable_updates_bulk_events_as_string(self, dejavu_instance, sample_log_file):
        expected_final_y = -2
        expected_final_last_seen_q = False

        for chunk in dejavu_instance.read_bulk_events_as_string(sample_log_file, chunk_size=3):
            dejavu_instance.verify.process_events(chunk)

        assert dejavu_instance.get_shared(
            "y") == expected_final_y, \
            f"Final 'y' value mismatch: expected {expected_final_y}, " \
            f"got {dejavu_instance.get_shared('y')}"

        assert dejavu_instance.get_shared(
            "last_seen_q") == expected_final_last_seen_q, \
            f"Final 'last_seen_q' value mismatch: expected {expected_final_last_seen_q}, " \
            f"got {dejavu_instance.get_shared('last_seen_q')}"

    def test_property_evaluations_bulk_events_as_dict(self, dejavu_instance, complex_log_file):
        log_file, events = complex_log_file

        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_dict(log_file, chunk_size=50):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))

        assert len(actual_results) == len(
            events), f"Number of processed events ({len(actual_results)}) doesn't match expected ({len(events)})"

        for actual, event in zip(actual_results, events):
            assert actual["Original Event"] == ",".join(map(str, event)), \
                f"Original event mismatch: expected {','.join(map(str, event))}, got {actual['Original Event']}"
            assert "example1=" in actual[
                "Eval result"], f"'example1' not in eval result for event: {actual['Original Event']}"
            assert "example2=" in actual[
                "Eval result"], f"'example2' not in eval result for event: {actual['Original Event']}"

        assert dejavu_instance.last_eval("example1") in [True, False], "Invalid final evaluation for 'example1'"
        assert dejavu_instance.last_eval("example2") in [True, False], "Invalid final evaluation for 'example2'"

    def test_property_evaluations_bulk_events_as_string(self, dejavu_instance, complex_log_file):
        log_file, events = complex_log_file

        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_string(log_file, chunk_size=50):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))

        assert len(actual_results) == len(
            events), f"Number of processed events ({len(actual_results)}) doesn't match expected ({len(events)})"

        for actual, event in zip(actual_results, events):
            assert actual["Original Event"] == ",".join(map(str, event)), \
                f"Original event mismatch: expected {','.join(map(str, event))}, got {actual['Original Event']}"
            assert "example1=" in actual[
                "Eval result"], f"'example1' not in eval result for event: {actual['Original Event']}"
            assert "example2=" in actual[
                "Eval result"], f"'example2' not in eval result for event: {actual['Original Event']}"

        assert dejavu_instance.last_eval("example1") in [True, False], "Invalid final evaluation for 'example1'"
        assert dejavu_instance.last_eval("example2") in [True, False], "Invalid final evaluation for 'example2'"

    def test_error_handling(self, dejavu_instance):
        # Test with invalid event
        invalid_event = {"name": "invalid_event", "args": [1, 2, 3]}
        expected_result = {
            "Original Event": "invalid_event,1,2,3",
            "Modified Event": "invalid_event,1,2,3",
            "Eval result": "example1=true,example2=true"
        }

        actual_result = dejavu_instance.verify.process_event(invalid_event)
        assert actual_result == expected_result, \
            f"Unexpected result for invalid event: expected {expected_result}, got {actual_result}"

        # Test with missing arguments
        missing_args_event = {"name": "p", "args": []}

        with pytest.raises(ValueError):
            dejavu_instance.verify.process_event(missing_args_event)

        # Test with incorrect argument type
        incorrect_type_event = {"name": "p", "args": ["not_an_integer"]}

        with pytest.raises(TypeError):
            dejavu_instance.verify.process_event(incorrect_type_event)

    def test_complex_scenario_event_bulk_as_dict(self, dejavu_instance, complex_log_file):
        log_file, events = complex_log_file

        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_dict(log_file, chunk_size=100):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))

        assert len(actual_results) == len(
            events), f"Number of processed events ({len(actual_results)}) doesn't match expected ({len(events)})"

        p_count = sum(1 for e in events if e[0] == 'p')
        q_count = sum(1 for e in events if e[0] == 'q')
        r_count = sum(1 for e in events if e[0] == 'r')

        actual_p_count = sum(1 for r in actual_results if r["Original Event"].startswith("p"))
        actual_q_count = sum(1 for r in actual_results if r["Original Event"].startswith("q"))
        actual_r_count = sum(1 for r in actual_results if r["Original Event"].startswith("r"))

        assert actual_p_count == p_count, f"Mismatch in 'p' event count: expected {p_count}, got {actual_p_count}"
        assert actual_q_count == q_count, f"Mismatch in 'q' event count: expected {q_count}, got {actual_q_count}"
        assert actual_r_count == r_count, f"Mismatch in 'r' event count: expected {r_count}, got {actual_r_count}"

        example1_violations = sum(1 for r in actual_results if "example1=false" in r["Eval result"])
        example2_satisfactions = sum(1 for r in actual_results if "example2=true" in r["Eval result"])

        print(f"Example1 violations: {example1_violations}")
        print(f"Example2 satisfactions: {example2_satisfactions}")

    def test_complex_scenario_event_bulk_as_string(self, dejavu_instance, complex_log_file):
        log_file, events = complex_log_file

        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_string(log_file, chunk_size=100):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))

        assert len(actual_results) == len(
            events), f"Number of processed events ({len(actual_results)}) doesn't match expected ({len(events)})"

        p_count = sum(1 for e in events if e[0] == 'p')
        q_count = sum(1 for e in events if e[0] == 'q')
        r_count = sum(1 for e in events if e[0] == 'r')

        actual_p_count = sum(1 for r in actual_results if r["Original Event"].startswith("p"))
        actual_q_count = sum(1 for r in actual_results if r["Original Event"].startswith("q"))
        actual_r_count = sum(1 for r in actual_results if r["Original Event"].startswith("r"))

        assert actual_p_count == p_count, f"Mismatch in 'p' event count: expected {p_count}, got {actual_p_count}"
        assert actual_q_count == q_count, f"Mismatch in 'q' event count: expected {q_count}, got {actual_q_count}"
        assert actual_r_count == r_count, f"Mismatch in 'r' event count: expected {r_count}, got {actual_r_count}"

        example1_violations = sum(1 for r in actual_results if "example1=false" in r["Eval result"])
        example2_satisfactions = sum(1 for r in actual_results if "example2=true" in r["Eval result"])

        print(f"Example1 violations: {example1_violations}")
        print(f"Example2 satisfactions: {example2_satisfactions}")

    def test_performance_bulk_event_as_dict(self, dejavu_instance, complex_log_file):
        log_file, events = complex_log_file

        start_time = time.time()
        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_dict(log_file, chunk_size=200):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))
        end_time = time.time()

        assert len(actual_results) == len(
            events), f"Number of processed events ({len(actual_results)}) doesn't match expected ({len(events)})"

        processing_time = end_time - start_time
        events_per_second = len(events) / processing_time

        print(f"Processed {len(events)} events in {processing_time:.2f} seconds")
        print(f"Performance: {events_per_second:.2f} events/second")

    def test_performance_bulk_event_as_string(self, dejavu_instance, complex_log_file):
        log_file, events = complex_log_file

        start_time = time.time()
        actual_results = []
        for chunk in dejavu_instance.read_bulk_events_as_string(log_file, chunk_size=200):
            actual_results.extend(dejavu_instance.verify.process_events(chunk))
        end_time = time.time()

        assert len(actual_results) == len(
            events), f"Number of processed events ({len(actual_results)}) doesn't match expected ({len(events)})"

        processing_time = end_time - start_time
        events_per_second = len(events) / processing_time

        print(f"Processed {len(events)} events in {processing_time:.2f} seconds")
        print(f"Performance: {events_per_second:.2f} events/second")

