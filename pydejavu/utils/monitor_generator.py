import json


class MonitorGenerator:
    """Utility class for handling files operations."""

    PYTHON_SCRIPT_TEMPLATE = """
import logging
from pydejavu.core.monitor import Monitor, event, parser

# Read the specification
specification = \"\"\"{specification}\"\"\"

# Initialize the monitor with the provided specification and arguments
monitor = Monitor(
    i_spec=specification,
    i_bits={bits},
    i_statistics={stats},
    i_logging_level=logging.INFO if {stats} else logging.WARNING
)

# Dynamically defined event handlers for the operational phase
{event_handlers}

  
# Process events using the monitor  
for chunk in monitor.read_bulk_events_as_dict("{events}", chunk_size=10000):
    results = monitor.verify(chunk)
    monitor.logger.debug(f"Processed chunk of {{len(chunk)}} events")

monitor.end()
"""

    @staticmethod
    def generate_python_script(qtl_path, pqtl_path, trace_path, bits, stats):
        # Read QTL specification from file
        with open(qtl_path, 'r') as qtl_file:
            specification = qtl_file.read()

        # Read operational event handlers from file
        event_handlers = ""
        if pqtl_path is not None:
            with open(pqtl_path, 'r') as pqtl_file:
                event_handlers = pqtl_file.read()

        # Format the template with the actual values
        script_content = MonitorGenerator.PYTHON_SCRIPT_TEMPLATE.format(
            specification=specification,
            bits=bits,
            stats=stats,
            event_handlers=event_handlers,
            events=trace_path
        )

        # Write the generated script to a .py file
        generated_script_path = 'generated_script.py'
        with open(generated_script_path, 'w') as generated_script:
            generated_script.write(script_content)

        print(f"Generated script written to {generated_script_path}")

        return generated_script_path
