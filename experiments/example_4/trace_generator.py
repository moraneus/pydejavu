import csv
import random


def generate_events(num_events):
    events = []
    for _ in range(num_events):
        # Randomly choose an event type 'p' or 'q'
        event_type = random.choice(['p', 'q'])
        # Generate a random integer argument between 1 and 100
        argument = random.randint(1, 10000)
        # Append the event and its argument as a tuple
        events.append((event_type, argument))
    return events


def write_events_to_csv(events):
    # Extract the number of events for naming the file
    num_events = len(events)
    # Define the file name
    filename = f'log{num_events}.csv'

    # Open the CSV file in write mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write each event (type, argument) to a row in the CSV file
        for event in events:
            writer.writerow(event)

        # Write the last line as "#end#"
        writer.writerow(["#end#"])

    print(f"Events written to {filename}")


def main():
    # Ask user for the number of events to generate
    num_events = int(input("Enter the number of events to generate: "))

    # Generate the events
    events = generate_events(num_events)

    # Write the events to a CSV file
    write_events_to_csv(events)


if __name__ == "__main__":
    main()