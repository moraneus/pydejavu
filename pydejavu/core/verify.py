import inspect

from typing import Any, Dict, List, Optional, Callable, get_type_hints, Union, Tuple
from functools import lru_cache

from pydejavu.core.event_operational_mapper import EventOperationalMapper
from pydejavu.utils.logger import Logger


class Verify:
    """Class to handle event verification and shared state management for a monitoring system.

    This class uses an event mapper to process and verify events, manage shared variables,
    and interact with an underlying monitor to evaluate events.
    """

    def __init__(
            self,
            i_dejavu_monitor: Any,
            i_bits: int = 20,
            i_mode: Optional[str] = None,
            i_statistics: bool = True,
            i_logger: Logger = None
    ):
        """
        Initializes the Verify instance with the provided monitor and configuration.

        Args:
            i_dejavu_monitor (Any): The dejavu monitoring system instance to interact with.
            i_bits (int, optional): The number of bits for configuration. Defaults to 20.
            i_mode (Optional[str], optional): The mode of operation. Defaults to None.
            i_statistics (bool, optional): Flag to enable or disable statistics. Defaults to True.
            i_logger (Logger, optional): A custom logger instance. Defaults to None.
        """

        self.__m_logger = Logger(i_name=__name__) if i_logger is None else i_logger
        self.__m_dejavu_monitor = i_dejavu_monitor
        self.__monitor_setup(i_bits, i_mode, i_statistics)
        self.event_mapper = EventOperationalMapper()
        self.__m_handler_info_cache: Dict[Callable, Dict[str, Any]] = {}

        # Mapping for custom event processor handlers
        self.__m_custom_event_processor_handlers: Dict[str, Callable[[Any], Tuple[str, List[Any], str]]] = {}

    def __call__(self, input_data: Union[Dict[str, Any], str, List[Dict[str, Any]], List[str]]) -> \
            Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Process either a single event or multiple events based on the input type.

        Args:
            input_data (Union[Dict[str, Any], str, List[Dict[str, Any]], List[str]]):
                Either a single event (as a dict or string) or a list of events.

        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]]]: The result(s) of processing the event(s).

        Raises:
            ValueError: If the input_data is not in the expected format.
        """
        if isinstance(input_data, (dict, str)):
            return self.process_event(input_data)
        elif isinstance(input_data, list):
            return self.process_events(input_data)
        else:
            raise ValueError("Input must be either a single event (dict or string) or a list of events.")

    def event(self, event_name: str) -> Callable:
        """
        Maps an event name to a callable using the event mapper.

        Args:
            event_name (str): The name of the event.

        Returns:
            Callable: The function mapped to the event name.
        """
        return self.event_mapper.event(event_name)

    def get_shared(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value of a shared variable.

        Args:
            key (str): The key of the shared variable.
            default (Any, optional): The default value if the key is not found. Defaults to None.

        Returns:
            Any: The value of the shared variable.
        """
        return self.event_mapper.get_shared(key, default)

    def set_shared(self, key: str, value: Any) -> None:
        """
        Sets the value of a shared variable.

        Args:
            key (str): The key of the shared variable.
            value (Any): The value to set.
        """
        self.event_mapper.set_shared(key, value)

    def process_event(self, event: Union[Dict[str, Any], str]) -> Dict[str, Any]:
        """
        Processes a single event and evaluates it using the monitor.

        Args:
            event (Union[Dict[str, Any], str]): The event data, which can be either a dictionary
            containing 'name' and 'args', or a string formatted as 'event_name,arg1,arg2,...'.

        Returns:
            Dict[str, Any]: The result of processing and evaluating the event.
        """

        # Determine event name
        event_name = None
        if isinstance(event, dict):
            event_name = event.get('name')

        # Check if a custom parser is registered for this event name
        if event_name in self.event_mapper.parser_map:
            self.__m_logger.debug(f"Using custom parser for event '{event_name}'")
            parser = self.__get_parser(event_name)
            event_data = parser(event)
        else:
            # Default parsing logic
            event_data = self._parse_event(event)

        event_name, event_args, origin_eval_input = event_data
        handler = self.__get_handler(event_name)

        if handler is None:
            modified_eval_input = origin_eval_input
        else:
            handler_info = self.__get_handler_info(handler)
            required_params = self.__m_handler_info_cache[handler]["num_of_params"]

            if len(event_args) != required_params:
                raise ValueError(
                    f"Event '{event_name}' expects {required_params} argument(s), "
                    f"but {len(event_args)} were given."
                )
            try:
                modified_eval_input = self.__process_mapped_event(handler, handler_info, event_args)
                if modified_eval_input is None:
                    return {
                        "Original Event": origin_eval_input,
                        "Modified Event": "skip",
                        "Eval result": None
                    }

            except TypeError as e:
                raise TypeError(f"Error processing event {event_name}: {str(e)}")
            except Exception as e:
                self.__m_logger.error(f"Error processing event {event_name}: {str(e)}")
                modified_eval_input = origin_eval_input

        try:
            eval_result = self.__m_dejavu_monitor.eval(modified_eval_input)
            self.__update_last_eval(eval_result)
        except Exception as e:
            self.__m_logger.error(f"Error in eval for event {event_name}: {str(e)}")
            eval_result = "Error in eval"

        return {
            "Original Event": origin_eval_input,
            "Modified Event": modified_eval_input,
            "Eval result": eval_result
        }

    def _parse_event(self, event: Union[Dict[str, Any], str]) -> Tuple[str, List[Any], str]:
        """
        Parses the input event into event name, arguments, and original eval input.

        Args:
            event (Union[Dict[str, Any], str]): The event data to parse.

        Returns:
            tuple[str, List[Any], str]: A tuple containing the event name, list of arguments,
                and the original eval input string.
        """
        if isinstance(event, str):
            event_parts = event.split(',')
            event_name = event_parts[0]
            event_args = event_parts[1:] if len(event_parts) > 1 else []
            origin_eval_input = event
        else:
            event_name = event.get('name', '')
            event_args = event.get('args', [])
            origin_eval_input = f"{event_name},{','.join(map(self.__format_arg, event_args))}"

        return event_name, event_args, origin_eval_input

    def process_events(self, events: Union[List[Dict[str, Any]], List[str]]) -> List[Dict[str, Any]]:
        """
        Processes a list of events and evaluates each one.

        Args:
            events (Union[List[Dict[str, Any]], List[str]]): A list of event data.

        Returns:
            List[Dict[str, Any]]: A list of results from processing and evaluating each event.
        """
        return [self.process_event(event) for event in events]

    def end_eval(self):
        """
        Notify the DejaVu that user need to ends its verification.
        This makes the result file to be closed correctly.
        It also called to get stat to summarize all events statistics.
        """
        self.__m_dejavu_monitor.end_eval()

    def get_stat(self):
        """
        Get evaluation stat.
        The printed stat summarize all events until the moment it called.
        """
        self.__m_dejavu_monitor.get_stat()

    def __monitor_setup(
            self,
            i_bits: int = 20,
            i_mode: Optional[str] = "debug",
            i_statistics: bool = True,
    ) -> None:
        """
        Sets up the monitor with the given configuration.

        Args:
            i_bits (int, optional): The number of bits for configuration. Defaults to 20.
            i_mode (Optional[str], optional): The mode of operation. Defaults to "debug".
            i_statistics (bool, optional): Flag to enable or disable statistics. Defaults to True.
        """
        self.__m_dejavu_monitor.config(str(i_bits), str(i_mode), str(i_statistics), "output/resultFile")

    def format_args(self, args: Union[Dict, List, Any]) -> str:
        """
        Formats arguments into a string representation.

        Args:
            args (Union[Dict, List, Any]): The arguments to format.

        Returns:
            str: The formatted arguments as a string.
        """
        if isinstance(args, dict):
            return ",".join(f"{k}={self.__format_arg(v)}" for k, v in args.items())
        elif isinstance(args, list):
            return ",".join(map(self.__format_arg, args))
        return str(args)

    @lru_cache(maxsize=128)
    def __format_arg(self, arg: Any) -> str:
        """
        Format an argument for string representation.

        This method converts boolean values to lowercase strings and
        all other types to their string representation.

        Args:
            arg (Any): The argument to be formatted.

        Returns:
            str: The formatted string representation of the argument.

        Examples:
            self.__format_arg(True)
            'true'
            self.__format_arg(42)
            '42'
            self.__format_arg("hello")
            'hello'
        """
        if isinstance(arg, bool):
            return str(arg).lower()
        return str(arg)

    def __cast_args(
            self,
            args: Union[Dict, List, Any],
            type_hints: Dict[str, type],
            param_names: List[str]) -> Union[Dict, List, Any]:
        """
        Casts arguments to their respective types based on provided type hints and parameter names.
        Args:
            args (Union[Dict, List, Any]): The arguments to cast.
            type_hints (Dict[str, type]): A dictionary of type hints.
            param_names (List[str]): List of parameter names from the handler function.
        Returns:
            Union[Dict, List, Any]: The casted arguments.
        """
        if isinstance(args, list):
            return [self.cast_value(arg, type_hints.get(param_names[i], Any)) if i < len(param_names) else arg
                    for i, arg in enumerate(args)]
        elif isinstance(args, dict):
            return {k: self.cast_value(v, type_hints.get(k, Any)) for k, v in args.items()}
        else:
            return self.cast_value(args, next(iter(type_hints.values()), Any))

    def cast_value(self, value: Any, target_type: type) -> Any:
        """
        Casts a value to a target type.

        Args:
            value (Any): The value to cast.
            target_type (type): The target type to cast the value to.

        Returns:
            Any: The casted value.
        """
        if target_type == Any:
            return value
        try:
            if target_type == bool:
                return str(value).lower() in ('true', 't', 'yes', 'y', '1')
            return target_type(value)
        except (ValueError, TypeError) as e:
            raise TypeError(f"Failed to cast the string '{value}' into {target_type} ({str(e)})")

    def __process_mapped_event(
            self, handler: Callable, handler_info: Dict[str, Any], event_args: List[Any]) -> Optional[str]:
        """
        Processes an event using its mapped handler.
        Args:
            handler (Callable): The handler function for the event.
            handler_info (Dict[str, Any]): Handler info details.
            event_args (List[Any]): The arguments for the event.
        Returns:
            str: The formatted result from processing the event.
        """
        type_hints = handler_info['type_hints']
        param_names = handler_info['param_names']
        casted_args = self.__cast_args(event_args, type_hints, param_names)

        if isinstance(casted_args, list):
            result = handler(*casted_args)
        elif isinstance(casted_args, dict):
            result = handler(**casted_args)
        else:
            result = handler(casted_args)

        # Check if the result is None or an empty tuple
        if result is None or not result:
            return None
        return self.__format_result(result)

    def __format_result(self, result: List[Any]) -> str:
        """
        Formats the result of an event core.

        Args:
            result (List[Any]): The result to format.

        Returns:
            str: The formatted result as a string.
        """
        formatted_result = []
        for item in result:
            if isinstance(item, bool):
                formatted_result.append(str(item).lower())
            elif isinstance(item, float):
                formatted_result.append(str(int(item)))
            else:
                formatted_result.append(str(item))
        return ','.join(formatted_result)

    @lru_cache(maxsize=128)
    def __get_handler(self, event_name: str) -> Callable:
        """
        Retrieves or caches handler callable.

        Args:
            event_name (str): The event name which correspond to a callable.

        Returns:
            Callable: The handler function.
        """
        return self.event_mapper.event_map.get(event_name)

    @lru_cache(maxsize=128)
    def __get_parser(self, event_name: str) -> Callable:
        """
        Retrieves or caches parser callable.

        Args:
            event_name (str): The event name which correspond to a callable.

        Returns:
            Callable: The parser function.
        """
        return self.event_mapper.parser_map.get(event_name)

    @lru_cache(maxsize=128)
    def __get_handler_info(self, handler: Callable) -> Dict[str, Any]:
        """
        Retrieves or caches handler information (type hints and parameter names).

        Args:
            handler (Callable): The handler function.

        Returns:
            Dict[str, Any]: A dictionary containing 'type_hints' and 'param_names'.
        """
        if handler not in self.__m_handler_info_cache:
            sig = inspect.signature(handler)
            required_params = sum(1 for param in sig.parameters.values()
                                  if param.default == param.empty and param.kind != param.VAR_POSITIONAL)
            self.__m_handler_info_cache[handler] = {
                'type_hints': self._get_type_hints(handler),
                'param_names': list(sig.parameters.keys()),
                'num_of_params': required_params
            }
        return self.__m_handler_info_cache[handler]

    @lru_cache(maxsize=128)
    def _get_type_hints(self, func: Callable) -> Dict[str, type]:
        """
        Retrieves type hints for a given function, using caching for efficiency.

        Args:
            func (Callable): The function to retrieve type hints for.

        Returns:
            Dict[str, type]: A dictionary of type hints.
        """
        return get_type_hints(func)

    def __update_last_eval(self, last_eval_result: str) -> None:
        """
        Updates the shared variables with the latest evaluation results.

        This method parses the evaluation results string, extracts the property names and their verdicts,
        and updates the shared variables with the verdict for each property.

        Args:
            last_eval_result (str): A string containing the evaluation results in the
            format 'property1=verdict1,property2=verdict2,...'.
        """
        for spec in last_eval_result.split(','):
            try:
                name, verdict = spec.split('=')
                self.set_shared(f"#last_eval_{name}#", verdict == "true")
            except ValueError:
                self.__m_logger.error(f"Failed to parse the evaluation result: '{spec}'. "
                                      "Expected format is 'name=verdict'.")
                raise ValueError(f"Invalid format in evaluation result: '{spec}'")
