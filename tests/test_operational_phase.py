import pytest
from unittest.mock import Mock, patch
from pydejavu.core.monitor import Monitor, event, parser
from pydejavu.core.verify import Verify


class TestOperationalPhase:
    @pytest.fixture
    def mock_monitor(self):
        monitor = Mock()
        monitor.eval.return_value = "a=true,b=false,c=true"
        return monitor

    @pytest.fixture
    def mock_verify(self, mock_monitor):
        verify = Verify(mock_monitor)
        return verify

    @pytest.fixture
    def monitor(self, mock_verify):
        specification = """
        prop a: some property a
        prop b: some property b
        prop c: some property c
        """

        monitor = Monitor(i_spec=None)
        monitor._Monitor__m_verify = mock_verify
        return monitor

    def test_parser_registration(self, monitor):
        @parser("custom_event")
        def custom_event_parser(event):
            event_name = event.get('name', '')
            event_args = event.get('args', [])
            origin_eval_input = f"{event_name},{','.join(map(str, event_args))}"
            return event_name, event_args, origin_eval_input

        assert "custom_event" in monitor.verify.event_mapper.parser_map

    def test_process_event_with_custom_parser(self, monitor):
        @parser("custom_event")
        def custom_event_parser(event):
            event_name = event.get('name', '')
            event_args = event.get('args', [])
            origin_eval_input = f"{event_name}_2,{','.join(map(str, event_args))}"
            return event_name, event_args, origin_eval_input

        e = {"name": "custom_event", "args": [1, 2, 3]}
        result = monitor.verify.process_event(e)

        assert result["Original Event"] == "custom_event_2,1,2,3"
        assert result["Modified Event"] == "custom_event_2,1,2,3"
        assert result["Eval result"] == "a=true,b=false,c=true"

    def test_fallback_to_default_parsing(self, monitor):
        e = {"name": "no_parser_event", "args": [1, 2, 3]}
        result = monitor.verify.process_event(e)

        assert result["Original Event"] == "no_parser_event,1,2,3"
        assert result["Modified Event"] == "no_parser_event,1,2,3"
        assert result["Eval result"] == "a=true,b=false,c=true"

    def test_custom_parser_with_handler_affecting_output(self, monitor):
        @parser("affecting_event")
        def custom_affecting_parser(event):
            event_name = "affecting_event_2"
            event_args = [arg * 2 for arg in event.get('args', [])]  # Custom modification
            origin_eval_input = f"{event_name},{','.join(map(str, event_args))}"
            return event_name, event_args, origin_eval_input

        @event("affecting_event_2")
        def handle_p(arg_x: int, arg_y: int, arg_z: int):
            return ["affecting_event_3", arg_x * 2, arg_y * 2, arg_z * 2]

        e = {"name": "affecting_event", "args": [1, 2, 3]}
        result = monitor.verify.process_event(e)

        assert result["Original Event"] == "affecting_event_2,2,4,6"
        assert result["Modified Event"] == "affecting_event_3,4,8,12"
        assert result["Eval result"] == "a=true,b=false,c=true"

    def test_custom_parser_error_handling(self, monitor):
        @parser("error_event")
        def custom_error_parser(event):
            raise ValueError("Custom parsing error")

        e = {"name": "error_event", "args": [1, 2, 3]}
        with pytest.raises(ValueError, match="Custom parsing error"):
            monitor.verify.process_event(e)

    def test_operational_decorator_registration(self, monitor):
        @event("p")
        def handle_p(arg_x: int):
            return ["p", arg_x]

        @event("q")
        def handle_q(arg_y: int):
            return ["q", arg_y]

        @event("r")
        def handle_r(arg_z: int):
            return ["r", arg_z * arg_z]

        assert "p" in monitor.verify.event_mapper.event_map
        assert "q" in monitor.verify.event_mapper.event_map
        assert "r" in monitor.verify.event_mapper.event_map

    def test_direct_handler_execution(self, monitor):
        @event("p")
        def handle_p(arg_x: int):
            return ["p", arg_x, arg_x < 5]

        wrapped_handler = monitor.verify.event_mapper.event_map["p"]

        assert wrapped_handler(3) == ["p", 3, True]
        assert wrapped_handler(7) == ["p", 7, False]
        assert wrapped_handler(5) == ["p", 5, False]

    def test_process_event_with_handler(self, monitor):
        @event("p")
        def handle_p(arg_x: int):
            return ["p", arg_x, arg_x < 5]

        e = {"name": "p", "args": [3]}
        result = monitor.verify.process_event(e)

        assert result["Original Event"] == "p,3"
        assert result["Modified Event"] == "p,3,true"
        assert result["Eval result"] == "a=true,b=false,c=true"

    def test_process_event_without_handler(self, monitor):
        e = {"name": "no_handler", "args": [1, 2, 3]}
        result = monitor.verify.process_event(e)

        assert result["Original Event"] == "no_handler,1,2,3"
        assert result["Modified Event"] == "no_handler,1,2,3"
        assert result["Eval result"] == "a=true,b=false,c=true"

    def test_process_single_event(self, monitor):
        @event("q")
        def handle_q(arg_y: int):
            return ["q", arg_y]

        event_q = {"name": "q", "args": [5]}
        result_q = monitor.verify.process_event(event_q)

        assert result_q["Original Event"] == "q,5"
        assert result_q["Modified Event"] == "q,5"
        assert result_q["Eval result"] == "a=true,b=false,c=true"

    def test_process_multiple_events(self, monitor):
        @event("p")
        def handle_p(arg_x: int):
            return ["p", arg_x, arg_x < 5]

        @event("q")
        def handle_q(arg_y: int):
            return ["q", arg_y]

        events = [
            {"name": "p", "args": [3]},
            {"name": "q", "args": [5]},
            {"name": "p", "args": [7]},
        ]

        results = monitor.verify.process_events(events)

        assert len(results) == 3
        assert results[0]["Original Event"] == "p,3"
        assert results[0]["Modified Event"] == "p,3,true"
        assert results[1]["Original Event"] == "q,5"
        assert results[1]["Modified Event"] == "q,5"
        assert results[2]["Original Event"] == "p,7"
        assert results[2]["Modified Event"] == "p,7,false"
        assert all(result["Eval result"] == "a=true,b=false,c=true" for result in results)

    def test_last_eval_results(self, monitor):
        @event("p")
        def handle_p(arg_x: int):
            return ["p", arg_x]

        e = {"name": "p", "args": [3]}
        monitor.verify.process_event(e)

        assert monitor.last_eval("a") == True
        assert monitor.last_eval("b") == False
        assert monitor.last_eval("c") == True

    def test_last_eval_undefined_property(self, monitor):
        with pytest.raises(SystemExit):
            monitor.last_eval("undefined_property")

    def test_shared_variable_operations(self, monitor):
        monitor.set_shared("test_key", "test_value")
        assert monitor.get_shared("test_key") == "test_value"
        assert monitor.get_shared("non_existent_key", "default") == "default"

        monitor.set_shared("test_key", "updated_value")
        assert monitor.get_shared("test_key") == "updated_value"

    def test_complex_event_chain(self, monitor):
        @event("start")
        def handle_start(value: int):
            monitor.set_shared("counter", value)
            return ["start", value]

        @event("increment")
        def handle_increment():
            counter = monitor.get_shared("counter", 0)
            monitor.set_shared("counter", counter + 1)
            return ["increment", counter + 1]

        @event("check")
        def handle_check(threshold: int):
            counter = monitor.get_shared("counter", 0)
            return ["check", counter, counter > threshold]

        events = [
            {"name": "start", "args": [5]},
            {"name": "increment", "args": []},
            {"name": "increment", "args": []},
            {"name": "check", "args": [6]},
        ]

        results = monitor.verify.process_events(events)

        assert results[0]["Modified Event"] == "start,5"
        assert results[1]["Modified Event"] == "increment,6"
        assert results[2]["Modified Event"] == "increment,7"
        assert results[3]["Modified Event"] == "check,7,true"

    def test_error_handling_in_handler(self, monitor):
        @event("divide")
        def handle_divide(a: int, b: int):
            return ["divide", a, b, a / b]

        event_ok = {"name": "divide", "args": [10, 2]}
        result_ok = monitor.verify.process_event(event_ok)
        assert result_ok["Modified Event"] == "divide,10,2,5"

        event_error = {"name": "divide", "args": [10, 0]}
        result_error = monitor.verify.process_event(event_error)
        assert result_error["Original Event"] == "divide,10,0"
        assert result_error["Modified Event"] == "divide,10,0"  # Should not contain the division result

    def test_multiple_property_evaluation(self, monitor):
        # Modify the mock monitor's return value
        monitor._Monitor__m_verify._Verify__m_dejavu_monitor.eval.return_value = "a=true,b=false,c=true,d=false,e=true"

        @event("complex_event")
        def handle_complex_event(x: int, y: int):
            return ["complex_event", x, y, x > y, x + y > 10]

        e = {"name": "complex_event", "args": [7, 4]}
        result = monitor.verify.process_event(e)

        assert result["Modified Event"] == "complex_event,7,4,true,true"
        assert result["Eval result"] == "a=true,b=false,c=true,d=false,e=true"

        assert monitor.last_eval("a") == True
        assert monitor.last_eval("b") == False
        assert monitor.last_eval("c") == True
        assert monitor.last_eval("d") == False
        assert monitor.last_eval("e") == True

        # These will raise SystemExit as they're not in the original spec names
        with pytest.raises(SystemExit):
            monitor.last_eval("f")
        with pytest.raises(SystemExit):
            monitor.last_eval("g")

    def test_event_with_shared_variable_dependency(self, monitor):
        @event("set_threshold")
        def handle_set_threshold(value: int):
            monitor.set_shared("threshold", value)
            return ["set_threshold", value]

        @event("check_value")
        def handle_check_value(value: int):
            threshold = monitor.get_shared("threshold", 0)
            return ["check_value", value, threshold, value > threshold]

        events = [
            {"name": "set_threshold", "args": [50]},
            {"name": "check_value", "args": [30]},
            {"name": "check_value", "args": [70]},
            {"name": "set_threshold", "args": [60]},
            {"name": "check_value", "args": [65]},
        ]

        results = monitor.verify.process_events(events)

        assert results[0]["Modified Event"] == "set_threshold,50"
        assert results[1]["Modified Event"] == "check_value,30,50,false"
        assert results[2]["Modified Event"] == "check_value,70,50,true"
        assert results[3]["Modified Event"] == "set_threshold,60"
        assert results[4]["Modified Event"] == "check_value,65,60,true"

    def test_nested_event_processing(self, monitor):
        @event("outer")
        def handle_outer(x: int):
            inner_event = {"name": "inner", "args": [x * 2]}
            inner_result = monitor.verify.process_event(inner_event)
            return ["outer", x, inner_result["Modified Event"]]

        @event("inner")
        def handle_inner(y: int):
            return ["inner", y, y > 10]

        e = {"name": "outer", "args": [5]}
        result = monitor.verify.process_event(e)

        assert result["Original Event"] == "outer,5"
        assert result["Modified Event"] == "outer,5,inner,10,false"
        assert result["Eval result"] == "a=true,b=false,c=true"

    def test_set_individual_properties(self, monitor):
        @event("set_a")
        def handle_set_a(value: bool):
            return ["set_a", value]

        @event("set_b")
        def handle_set_b(value: bool):
            return ["set_b", value]

        mock_monitor = monitor._Monitor__m_verify._Verify__m_dejavu_monitor
        mock_monitor.eval.side_effect = [
            "a=true,b=false,c=false",
            "a=true,b=true,c=false"
        ]

        events = [
            {"name": "set_a", "args": [True]},
            {"name": "set_b", "args": ["true"]}
        ]

        results = monitor.verify.process_events(events)

        assert results[0]["Modified Event"] == "set_a,true"
        assert results[0]["Eval result"] == "a=true,b=false,c=false"

        assert results[1]["Modified Event"] == "set_b,true"
        assert results[1]["Eval result"] == "a=true,b=true,c=false"

        assert monitor.last_eval("a") == True
        assert monitor.last_eval("b") == True
        assert monitor.last_eval("c") == False

    def test_complex_check_using_last_eval(self, monitor):
        # Simulate the initialization that occurs in linkage_monitor
        mock_monitor = monitor._Monitor__m_verify._Verify__m_dejavu_monitor
        mock_monitor.eval.return_value = "a=false,b=false,c=false"
        monitor.verify.process_event({"name": "#init#", "args": []})

        @event("complex_check")
        def handle_complex_check():
            a_value = monitor.last_eval("a")
            b_value = monitor.last_eval("b")
            c_value = monitor.last_eval("c")

            result = (a_value and b_value) or (not c_value)
            return ["complex_check", a_value, b_value, c_value, result]

        # Now set up the mock for the actual test
        mock_monitor.eval.return_value = "a=true,b=true,c=false"

        e = {"name": "complex_check", "args": []}
        result = monitor.verify.process_event(e)

        # This is for the first time where lase eval are initialize to False
        assert result["Modified Event"] == "complex_check,false,false,false,true"
        assert result["Eval result"] == "a=true,b=true,c=false"

        e = {"name": "complex_check", "args": []}
        result = monitor.verify.process_event(e)

        # This is for the second time where lase eval are initialize to a=true,b=true,c=false
        assert result["Modified Event"] == "complex_check,true,true,false,true"

        # Verify that last_eval values have been updated
        assert monitor.last_eval("a") == True
        assert monitor.last_eval("b") == True
        assert monitor.last_eval("c") == False

    def test_complex_check_with_changing_last_eval(self, monitor):
        # Simulate the initialization that occurs in linkage_monitor
        mock_monitor = monitor._Monitor__m_verify._Verify__m_dejavu_monitor
        mock_monitor.eval.return_value = "a=false,b=false,c=false"
        monitor.verify.process_event({"name": "#init#", "args": []})

        @event("complex_check")
        def handle_complex_check():
            a_value = monitor.last_eval("a")
            b_value = monitor.last_eval("b")
            c_value = monitor.last_eval("c")

            result = (a_value and b_value) or (not c_value)
            return ["complex_check", a_value, b_value, c_value, result]

        mock_monitor = monitor._Monitor__m_verify._Verify__m_dejavu_monitor

        # First check - where all last evals are initiate to False
        mock_monitor.eval.return_value = "a=true,b=true,c=false"
        event1 = {"name": "complex_check", "args": []}
        result1 = monitor.verify.process_event(event1)
        assert result1["Modified Event"] == "complex_check,false,false,false,true"

        # Second check - where all last evals are set to a=true,b=true,c=false
        mock_monitor.eval.return_value = "a=false,b=true,c=true"
        event2 = {"name": "complex_check", "args": []}
        result2 = monitor.verify.process_event(event2)
        assert result2["Modified Event"] == "complex_check,true,true,false,true"

        # Third check - where all last evals are set to a=false,b=true,c=true
        event3 = {"name": "complex_check", "args": []}
        result3 = monitor.verify.process_event(event3)
        assert result3["Modified Event"] == "complex_check,false,true,true,false"

    def test_last_eval_with_undefined_property(self, monitor):
        @event("check_undefined")
        def handle_check_undefined():
            try:
                monitor.last_eval("undefined_property")
            except SystemExit:
                return ["check_undefined", "error"]
            return ["check_undefined", "no_error"]

        mock_monitor = monitor._Monitor__m_verify._Verify__m_dejavu_monitor
        mock_monitor.eval.return_value = "a=true,b=false,c=false"

        e = {"name": "check_undefined", "args": []}
        result = monitor.verify.process_event(e)

        assert result["Modified Event"] == "check_undefined,error"
        assert result["Eval result"] == "a=true,b=false,c=false"
